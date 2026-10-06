#!/usr/bin/env python3
"""
Lint spójności vaulta — wersja szablonu (wyprowadzona z lintu v1.6 systemu-poprzednika).

13 reguł pilnujących PAR, które w praktyce poprzednika rozjeżdżały się najczęściej
(„zmiana jednej strony pary" — 13 udokumentowanych wystąpień):
  R1  depends_on_artifacts skilla ↔ zasięg odczytu persony z used_by
  R2  used_by artefaktu ↔ kolumna Odczyt w access_map (symetria)
  R3  version we frontmatterze musi być dodatnie
  R4  version ≥ najwyższa wersja w „Historia zmian" (artefakty, access_map)
  R5  liczniki logu routera (entry_count / last_entry) i kolizje ID
  R6  sieroty w wiki/ (zero linków przychodzących)
  R7  martwe linki [[...]] (propozycje w locie w inbox/ = cel rozwiązywalny; zaleganie >14 dni = osobne znalezisko)
  R8  linki [[nazwa_skilla]] wymagają aliasu w SKILL.md
  R9  ścieżki zapisu: access_map ↔ .claude/settings.json (część dot. runtime'u zewnętrznego pomijana, gdy brak --runtime-path)
  R10 warstwa deny w .claude/settings.json ↔ konstytucyjne zakazy access_map
  R11 cluster_access persony ↔ kolumna „Klastry (wiki/)" — obustronnie
  R12 read_scope persony ↔ kolumna „Odczyt (poza wiki/)" — obustronnie
  R13 wymagany_odczyt skilla ↔ zasięg persony z used_by

CZYSTO ODCZYTOWY: nigdy nie zapisuje ani nie modyfikuje żadnego pliku. Bez sieci, bez LLM,
bez zależności spoza biblioteki standardowej (własny mały parser frontmattera: skalary,
listy blokowe „- x", listy płaskie „[a, b]").

Użycie (z katalogu vaulta):
    python3 narzedzia/lint.py --vault . [--json] [--show-baselined] [--baseline PLIK]
Kody wyjścia: 0 = zero aktywnych znalezisk (cisza = czysto), 1 = są znaleziska.
Baseline (narzedzia/baseline.json): świadomie zaakceptowane znaleziska z powodem i datą —
przeglądaj kwartalnie (--show-baselined), nie dopisuj „żeby było zielone".
"""

from __future__ import annotations

import argparse
import json
import re
import time
import sys
import unicodedata
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# Finding
# ---------------------------------------------------------------------------


@dataclass
class Finding:
    rule: str  # np. "R1"
    title: str  # krótki opis reguły (nagłówek w raporcie)
    file: str  # ścieżka względem vaulta (lub runtime), string zawsze
    message: str  # opis konkretnego znaleziska
    line: int | None = None


@dataclass
class RuleResult:
    rule: str
    title: str
    findings: list[Finding] = field(default_factory=list)
    skipped: str | None = None  # powód pominięcia reguły w całości (np. brak runtime.py)


# ---------------------------------------------------------------------------
# Katalogi wykluczone z każdego chodzenia po drzewie (immutable / nie-wiedza / narzędzia)
# ---------------------------------------------------------------------------

WYKLUCZONE_TOP = {"raw", ".obsidian", ".git", "sandbox", "narzedzia", "_to_delete"}
WYKLUCZONE_PREFIX = ("system/templates/",)


def chodz_md(root: Path, wykluczone_top: set[str] = WYKLUCZONE_TOP):
    """Generator ścieżek .md pod root, z pominięciem katalogów w WYKLUCZONE_TOP
    (dopasowanych po pierwszym segmencie ścieżki względnej) i system/templates/."""
    for p in sorted(root.rglob("*.md")):
        rel = p.relative_to(root).as_posix()
        top = rel.split("/", 1)[0]
        if top in wykluczone_top:
            continue
        if any(rel.startswith(pref) for pref in WYKLUCZONE_PREFIX):
            continue
        yield p, rel


def czytaj(path: Path) -> str | None:
    """Bezpieczny odczyt pliku tekstowego. None = nie do odczytania (nie rzuca)."""
    try:
        return path.read_text(encoding="utf-8")
    except Exception:  # noqa: BLE001 — celowo szerokie: wymaganie 5, skrypt nigdy nie ma wywrócić się wyjątkiem
        return None


# ---------------------------------------------------------------------------
# Parser frontmattera — mały, świadomie ograniczony podzbiór YAML
# ---------------------------------------------------------------------------


def rozdziel_frontmatter(text: str) -> tuple[str | None, str]:
    """Zwraca (tekst_frontmattera, treść_po_frontmatterze). Jeśli plik nie ma
    poprawnego bloku frontmattera (--- ... ---), zwraca (None, cały_tekst)."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, text
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None, text
    fm = "\n".join(lines[1:end])
    body = "\n".join(lines[end + 1 :])
    return fm, body


def _odetnij_komentarz(s: str) -> str:
    s = s.strip()
    if s.startswith('"'):
        m = re.match(r'^"((?:[^"\\]|\\.)*)"', s)
        if m:
            return m.group(1)
    if s.startswith("'"):
        m = re.match(r"^'([^']*)'", s)
        if m:
            return m.group(1)
    idx = s.find(" #")
    if idx != -1:
        s = s[:idx]
    return s.strip()


def parsuj_frontmatter(fm_text: str) -> dict:
    """Bardzo mały parser YAML dopasowany do konwencji tego vaulta:
    - skalar:            klucz: wartość   (z opcjonalnym cudzysłowem i komentarzem #...)
    - lista blokowa:      klucz:\n  - a\n  - b
    - lista płaska:        klucz: [a, b]  lub  klucz: ["a", "b"]
    - pusta lista:         klucz: []
    Brak wsparcia dla zagnieżdżonych map — w tym vaultcie nie występują we frontmatterze
    reguł objętych lintem."""
    data: dict = {}
    lines = fm_text.split("\n")
    n = len(lines)
    i = 0
    klucz_re = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$")
    while i < n:
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        # tylko klucze bez wcięcia (top-level) — reguły objęte lintem tego potrzebują
        if line[:1].isspace():
            i += 1
            continue
        m = klucz_re.match(line)
        if not m:
            i += 1
            continue
        klucz, reszta = m.group(1), m.group(2).strip()
        if reszta == "" or reszta.startswith("#"):
            items = []
            j = i + 1
            while j < n:
                l2 = lines[j]
                if not l2.strip():
                    j += 1
                    continue
                if l2[:1].isspace() and l2.lstrip().startswith("-"):
                    item = l2.lstrip()[1:].strip()
                    items.append(_odetnij_komentarz(item))
                    j += 1
                elif l2[:1].isspace():
                    # wielolinijkowa wartość skalarna — poza zakresem reguł lintu, pomiń
                    j += 1
                else:
                    break
            data[klucz] = items if items else None
            i = j
            continue
        if reszta.startswith("["):
            # Komentarz w tej samej linii może zawierać nawiasy kwadratowe
            # ([[linki]] w adnotacji — realny przypadek: `cluster_access: []  # … [[badacz]] …`,
            # definicja analityka_prawnego). Bez odcięcia komentarza rfind("]") łapał
            # nawias z komentarza i lista dostawała treść adnotacji jako elementy.
            pierwsza = _odetnij_komentarz(reszta)
            if "]" in pierwsza:
                reszta = pierwsza
            inner = reszta
            k = i
            while "]" not in inner and k + 1 < n:
                k += 1
                inner += " " + lines[k]
            inner = inner[: inner.rfind("]") + 1]
            inner = inner[1:-1]
            items = [
                _odetnij_komentarz(part) for part in inner.split(",") if part.strip()
            ]
            data[klucz] = items
            i = k + 1
            continue
        data[klucz] = _odetnij_komentarz(reszta)
        i += 1
    return data


WIKILINK_RE = re.compile(r"(?<!!)\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")


def linki_z_wartosci(wartosc) -> list[str]:
    """Wyciąga nazwy z [[linkow]] wewnątrz stringa lub listy stringów;
    jeśli string nie zawiera [[ ]], zwraca go jako pojedynczy element (przypadek
    pól, które trzymają gołą nazwę bez nawiasów, np. read_scope bywa ścieżką).
    Wynik jest w NFC — te nazwy są potem zestawiane z nazwami plików z dysku (NFD na
    macOS), więc normalizacja musi objąć obie strony, nie tylko jedną."""
    out = []
    vals = wartosc if isinstance(wartosc, list) else [wartosc]
    for v in vals:
        if v is None:
            continue
        v = str(v)
        found = WIKILINK_RE.findall(v)
        if found:
            out.extend(nfc(x.strip()) for x in found)
        else:
            out.append(nfc(v.strip()))
    return out


def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


WERSJA_RE = re.compile(r"^\s*(-?)([0-9]+)(?:\.([0-9]+))?\s*$")


def wersja_krotka(surowa) -> tuple[int, int] | None:
    """Parsuje 'major.minor' na krotkę (major, minor) do porównań; None = nie wersja.

    KROTKA, NIE float: float("2.10") == 2.1, więc v<n> wypadałoby PONIŻEJ v<n> i R4
    zgłaszał fałszywy regres na system/access_map.md v<n> — pierwszym pliku vaulta, który
    przekroczył x.9 (znalezisko z audytu finance, paczka C). "2.10" to numer wersji
    major.minor, a nie ułamek dziesiętny: minor 10 jest DZIESIĄTĄ rewizją po minor 9.

    Znak minusa przenosi się na OBA człony, żeby porządek był poprawny także w przedziale
    (-1, 0), gdzie major sam w sobie nie niesie znaku: "-0.5" → (0, -5) < (0, 0), więc R3
    dalej widzi tę wersję jako niedodatnią."""
    m = WERSJA_RE.match(str(surowa).strip().strip('"').strip("'"))
    if not m:
        return None
    znak = -1 if m.group(1) else 1
    return (znak * int(m.group(2)), znak * int(m.group(3) or 0))


# ---------------------------------------------------------------------------
# Parser tabeli access_map.md
# ---------------------------------------------------------------------------

# Kolejność kolumn w "# Mapa dostępów" od access_map v<n> (migracja K1, <data>):
#   Agent | Head | Klastry (wiki/) | Odczyt (poza wiki/) | Zapis | Web | MCP
# Poprzedni układ (do v<n>): Agent | Head | Odczyt | Tagi dodatkowe | Zapis | Web [| MCP]
# — kolumna "Tagi dodatkowe" zniknęła (mechanizm tag_access/tags_extra zlikwidowany),
# "Klastry" weszła na idx 2, "Odczyt" przesunął się na idx 3. Indeksy "zapis"/"web" bez
# zmian, więc R9 nie wymagał korekty; R1/R2 czytają "odczyt" po nazwie z tej listy.
KOLUMNY_MAPY = ["agent", "head", "klastry", "odczyt", "zapis", "web", "mcp"]


def parsuj_access_map(text: str) -> dict[str, dict[str, str]]:
    """Zwraca {nazwa_agenta: {"agent": ..., "head": ..., "odczyt": ..., ...}} —
    tylko wiersze zaczynające się od "| [[nazwa]]" (wiersze tabeli, nie separator/nagłówek)."""
    wiersze: dict[str, dict[str, str]] = {}
    for line in text.split("\n"):
        if not line.strip().startswith("|"):
            continue
        m = re.match(r"^\|\s*\[\[([a-z_]+)\]\]", line)
        if not m:
            continue
        agent = m.group(1)
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        wiersz = {}
        for idx, nazwa in enumerate(KOLUMNY_MAPY):
            wiersz[nazwa] = cols[idx] if idx < len(cols) else ""
        wiersze[agent] = wiersz
    return wiersze


def wystepuje_jako_token(nazwa: str, tekst: str) -> bool:
    """Czy `nazwa` (np. 'access_map', 'Nazwa_Artefaktu') występuje w `tekst` jako pełny
    token (granica słowa po obu stronach) — dopasowuje 'access_map' w
    'system/access_map.md' (kropka/ukośnik to granice non-word), ale nie dopasuje
    przypadkowego podciągu wewnątrz dłuższej nazwy.

    OBIE strony przechodzą przez NFC, bo w tym porównaniu spotykają się dwa różne źródła
    tekstu: nazwy plików z dysku (macOS zapisuje 'ó' jako NFD: o + U+0308) i nazwy wpisane
    ręcznie w access_map.md / frontmatterze (NFC: pojedynczy U+00F3). Bajtowo różne, dla
    człowieka identyczne — bez normalizacji R2 zgłaszał fałszywy brak dostępu do
    Nazwa_Artefaktu (audyt finance, paczka C)."""
    if not tekst:
        return False
    return re.search(r"\b" + re.escape(nfc(nazwa)) + r"\b", nfc(tekst)) is not None


SCIEZKA_TOKEN_RE = re.compile(r"[a-zA-Z_][a-zA-Z0-9_./]*")


def _katalogi_grantowane(tekst: str) -> set[str]:
    """Zwraca zbiór katalogów przyznanych W CAŁOŚCI w tekście kolumny Odczyt —
    czyli tokeny ścieżkowe, które SAME W SOBIE kończą się na '/' (np. 'system/heads/'
    jako osobna pozycja listy), a NIE tokeny, które tylko przypadkiem ZAWIERAJĄ
    '/' w środku dłuższej ścieżki do konkretnego pliku (np. w
    'system/artifacts/Artefakt_A.md' katalog 'system/artifacts/' nie
    jest przyznany w całości — to jest grant na JEDEN plik, nie na cały katalog).
    Dlatego dopasowujemy CAŁY spójny token ścieżkowy naraz i klasyfikujemy dopiero
    po jego końcówce, zamiast łapać '.../' w środku regexem zachłannym po '/'."""
    out = set()
    for tok in SCIEZKA_TOKEN_RE.findall(nfc(tekst)):
        if tok.endswith("/"):
            out.add(tok)
    return out


def _rozwiaz_artefakt(nazwa: str, vault_root: Path) -> str | None:
    """Próbuje zamienić tytuł z depends_on_artifacts (np. 'access_map', 'knowledge',
    'Nazwa_Artefaktu') na realną ścieżkę względną w vaultcie — potrzebne, żeby R1 wiedział,
    czy artefakt jest pokryty przez GRANT NA CAŁY KATALOG (np. 'system/heads/' bez
    wymieniania z nazwy każdego head'a), nie tylko przez dokładną nazwę pliku."""
    if nazwa == "access_map":
        return "system/access_map.md"
    # Nazwa może przyjść z frontmattera (NFC), a plik leżeć na dysku pod NFD — dlatego
    # szukamy po znormalizowanym stemie w liście plików, zamiast ufać, że dosłowna
    # konkatenacja ścieżki trafi w tę samą postać (APFS to wybacza, ext4/CI już nie).
    nazwa_nfc = nfc(nazwa)
    for katalog in ("artifacts", "heads"):
        base = vault_root / "system" / katalog
        if not base.is_dir():
            continue
        for kandydat in base.glob("*.md"):
            if nfc(kandydat.stem) == nazwa_nfc:
                return f"system/{katalog}/{nfc(kandydat.name)}"
    return None


def pokryty_zasiegiem(nazwa: str, sciezka: str | None, tekst_zasiegu: str) -> bool:
    """Artefakt jest pokryty, jeśli jego nazwa występuje wprost jako token w tekście
    zasięgu (typowy przypadek: 'Nazwa_Artefaktu.md' wymieniony wprost) LUB jeśli jego
    rozwiązana ścieżka zaczyna się od katalogu, który tekst zasięgu przyznaje w
    całości (np. 'system/heads/' bez wymieniania konkretnego head'a z nazwy —
    przypadek [[knowledge]] dla katalizatora/zwiadowcy, potwierdzony w audycie
    ręcznym jako NIE-luka)."""
    if wystepuje_jako_token(nazwa, tekst_zasiegu):
        return True
    if not sciezka:
        return False
    sciezka = nfc(sciezka)
    for katalog in _katalogi_grantowane(tekst_zasiegu):
        if sciezka.startswith(katalog):
            return True
    return False


# ---------------------------------------------------------------------------
# Wspólne indeksy (pliki agentów/skilli/artefaktów) — budowane raz per przebieg
# ---------------------------------------------------------------------------


class Vault:
    def __init__(self, root: Path):
        self.root = root
        self.unreadable: list[Finding] = []

    def zgłoś_nieczytelny(self, rule: str, rel: str, powod: str):
        self.unreadable.append(
            Finding(rule="UNREADABLE", title="Plik nieczytelny / uszkodzony frontmatter",
                    file=rel, message=f"[{rule}] {powod}")
        )

    def wczytaj_fm(self, path: Path, rule: str) -> tuple[dict, str] | None:
        """Wczytuje plik, zwraca (frontmatter_dict, body) albo None + rejestruje
        znalezisko UNREADABLE, jeśli plik nie istnieje / nie da się odczytać / nie
        ma poprawnego bloku frontmattera."""
        rel = path.relative_to(self.root).as_posix() if path.is_absolute() else str(path)
        text = czytaj(path)
        if text is None:
            self.zgłoś_nieczytelny(rule, rel, "nie udało się odczytać pliku (brak / kodowanie)")
            return None
        fm_text, body = rozdziel_frontmatter(text)
        if fm_text is None:
            self.zgłoś_nieczytelny(rule, rel, "brak poprawnego bloku frontmattera (--- ... ---)")
            return None
        try:
            data = parsuj_frontmatter(fm_text)
        except Exception as e:  # noqa: BLE001 — celowo szerokie, jak w czytaj(): parser ma nigdy nie wywrócić lintu
            self.zgłoś_nieczytelny(rule, rel, f"frontmatter nie do sparsowania: {e}")
            return None
        return data, body


# ---------------------------------------------------------------------------
# R1 — depends_on_artifacts (skille) vs Odczyt agenta (access_map + read_scope)
# ---------------------------------------------------------------------------


def rule_r1(v: Vault) -> RuleResult:
    res = RuleResult("R1", "depends_on_artifacts skilla vs zasięg odczytu agenta")
    map_path = v.root / "system" / "access_map.md"
    map_text = czytaj(map_path)
    if map_text is None:
        res.skipped = "brak system/access_map.md"
        return res
    mapa = parsuj_access_map(map_text)

    agent_dir = v.root / "system" / "agents"
    if not agent_dir.is_dir():
        res.skipped = "brak system/agents/"
        return res

    # zasięg odczytu per agent = kolumna Odczyt z mapy + własny read_scope z frontmattera
    zasieg: dict[str, str] = {}
    for agent_path in sorted(agent_dir.glob("*.md")):
        nazwa = nfc(agent_path.stem)  # klucz zestawiany z used_by z frontmattera (NFC)
        parsed = v.wczytaj_fm(agent_path, "R1")
        odczyt_mapa = mapa.get(nazwa, {}).get("odczyt", "")
        read_scope_txt = ""
        if parsed:
            fm, _ = parsed
            rs = fm.get("read_scope")
            if rs:
                read_scope_txt = " ".join(str(x) for x in (rs if isinstance(rs, list) else [rs]))
        zasieg[nazwa] = f"{odczyt_mapa} {read_scope_txt}"

    skills_dir = v.root / "system" / "skills"
    if not skills_dir.is_dir():
        res.skipped = "brak system/skills/"
        return res

    for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
        rel = skill_md.relative_to(v.root).as_posix()
        parsed = v.wczytaj_fm(skill_md, "R1")
        if not parsed:
            continue
        fm, _ = parsed
        used_by = linki_z_wartosci(fm.get("used_by"))
        depends = linki_z_wartosci(fm.get("depends_on_artifacts"))
        if not used_by or not depends:
            continue
        for agent in used_by:
            tekst_zasiegu = zasieg.get(agent)
            if tekst_zasiegu is None:
                res.findings.append(Finding(
                    "R1", res.title, rel,
                    f"skill wymienia used_by: [[{agent}]], ale nie ma takiego agenta w "
                    f"system/agents/ ani w access_map.md",
                ))
                continue
            for artefakt in depends:
                sciezka = _rozwiaz_artefakt(artefakt, v.root)
                if not pokryty_zasiegiem(artefakt, sciezka, tekst_zasiegu):
                    res.findings.append(Finding(
                        "R1", res.title, rel,
                        f"depends_on_artifacts zawiera [[{artefakt}]], ale agent [[{agent}]] "
                        f"(used_by) nie ma go w zasięgu odczytu wg access_map.md/read_scope",
                    ))
    return res


# ---------------------------------------------------------------------------
# R2 — symetria used_by (artefakty vs access_map)
# ---------------------------------------------------------------------------


def rule_r2(v: Vault) -> RuleResult:
    res = RuleResult("R2", "symetria used_by artefaktu vs access_map")
    map_path = v.root / "system" / "access_map.md"
    map_text = czytaj(map_path)
    if map_text is None:
        res.skipped = "brak system/access_map.md"
        return res
    mapa = parsuj_access_map(map_text)

    art_dir = v.root / "system" / "artifacts"
    if not art_dir.is_dir():
        res.skipped = "brak system/artifacts/"
        return res

    for art_path in sorted(art_dir.glob("*.md")):
        rel = art_path.relative_to(v.root).as_posix()
        parsed = v.wczytaj_fm(art_path, "R2")
        if not parsed:
            continue
        fm, _ = parsed
        used_by = set(linki_z_wartosci(fm.get("used_by")))
        stem = nfc(art_path.stem)  # NFD z dysku vs NFC w access_map.md — patrz wystepuje_jako_token
        mapowani = {
            agent for agent, wiersz in mapa.items()
            if wystepuje_jako_token(stem, wiersz.get("odczyt", ""))
        }
        brak_w_mapie = used_by - mapowani
        brak_w_used_by = mapowani - used_by
        for agent in sorted(brak_w_mapie):
            res.findings.append(Finding(
                "R2", res.title, rel,
                f"used_by wymienia [[{agent}]], ale wiersz {agent} w access_map.md nie "
                f"przyznaje odczytu tego artefaktu",
            ))
        for agent in sorted(brak_w_used_by):
            res.findings.append(Finding(
                "R2", res.title, rel,
                f"access_map.md przyznaje agentowi [[{agent}]] odczyt tego artefaktu, ale "
                f"used_by go nie wymienia",
            ))
    return res


# ---------------------------------------------------------------------------
# R3 — dodatniość wersji vault-wide
# ---------------------------------------------------------------------------


def rule_r3(v: Vault) -> RuleResult:
    res = RuleResult("R3", "version musi być dodatnie")
    for path, rel in chodz_md(v.root):
        text = czytaj(path)
        if text is None:
            continue  # R5/inne reguły już to zgłoszą jako nieczytelne przy okazji swojej pracy
        fm_text, _ = rozdziel_frontmatter(text)
        if fm_text is None:
            continue
        m = re.search(r"^version:\s*\"?(-?[0-9]+(?:\.[0-9]+)?)\"?", fm_text, re.MULTILINE)
        if not m:
            continue
        # Ta sama krotka co w R4 — tu chodzi wyłącznie o znak, więc float() nie kłamał,
        # ale wspólny parser trzyma obie reguły przy jednej definicji "co to jest wersja".
        wartosc = wersja_krotka(m.group(1))
        if wartosc is None:
            continue
        if wartosc <= (0, 0):
            res.findings.append(Finding(
                "R3", res.title, rel,
                f"version: {m.group(1)} nie jest dodatnie (incydent tej klasy już wystąpił "
                f"<data>: Artefakt_A/Artefakt_B)",
            ))
    return res


# ---------------------------------------------------------------------------
# R4 — version ≥ max(Historia zmian), zawężone do system/artifacts/ + access_map.md
# ---------------------------------------------------------------------------

HISTORIA_NAGLOWEK_RE = re.compile(r"^#\s*(Historia zmian|Rejestr zmian)\s*$", re.MULTILINE)
HISTORIA_BULLET_RE = re.compile(r"^-\s*\d{4}-\d{2}-\d{2}\s*\(v([0-9]+(?:\.[0-9]+)?)\)", re.MULTILINE)


def _max_historia(body: str) -> tuple[tuple[int, int], str] | None:
    """Zwraca (krotka_wersji, surowy_zapis) najwyższej wersji z sekcji zmian — surowy
    zapis wraca razem z krotką, żeby komunikat znaleziska cytował to, co stoi w pliku
    ('2.10'), a nie wewnętrzną reprezentację ('(2, 10)')."""
    m = HISTORIA_NAGLOWEK_RE.search(body)
    if not m:
        return None
    reszta = body[m.end():]
    kolejny = re.search(r"^#\s", reszta, re.MULTILINE)
    if kolejny:
        reszta = reszta[: kolejny.start()]
    wersje = [
        (krotka, surowa)
        for surowa, krotka in (
            (surowa, wersja_krotka(surowa)) for surowa in HISTORIA_BULLET_RE.findall(reszta)
        )
        if krotka is not None
    ]
    return max(wersje, key=lambda para: para[0]) if wersje else None


def rule_r4(v: Vault) -> RuleResult:
    res = RuleResult("R4", "version ≥ max(Historia zmian) [system/artifacts/ + access_map.md]")
    cele = []
    art_dir = v.root / "system" / "artifacts"
    if art_dir.is_dir():
        cele.extend(sorted(art_dir.glob("*.md")))
    map_path = v.root / "system" / "access_map.md"
    if map_path.is_file():
        cele.append(map_path)
    if not cele:
        res.skipped = "brak system/artifacts/ i access_map.md"
        return res

    for path in cele:
        rel = path.relative_to(v.root).as_posix()
        parsed = v.wczytaj_fm(path, "R4")
        if not parsed:
            continue
        fm, body = parsed
        version_raw = fm.get("version")
        if version_raw is None:
            continue
        version = wersja_krotka(version_raw)
        if version is None:
            continue
        max_hist = _max_historia(body)
        if max_hist is None:
            continue  # reguła nie dotyczy — brak sekcji zmian, nie ma z czym porównać
        max_krotka, max_surowa = max_hist
        if version < max_krotka:
            res.findings.append(Finding(
                "R4", res.title, rel,
                f"version: {str(version_raw).strip()} < najwyższa wersja w Historii/Rejestrze "
                f"zmian: {max_surowa}",
            ))
    return res


# ---------------------------------------------------------------------------
# R5 — liczniki logów router + kolizja ID między log.md a log_vps.md
# ---------------------------------------------------------------------------

ID_LINE_RE = re.compile(r"^## \[ID: ([^\]]+)\]\s*$", re.MULTILINE)


def _log_ids(body: str) -> list[str]:
    return ID_LINE_RE.findall(body)


def rule_r5(v: Vault) -> RuleResult:
    res = RuleResult("R5", "liczniki logów router (entry_count/last_entry) + kolizja ID")
    log_paths = {
        "log.md": v.root / "outputs" / "router" / "log.md",
        "log_vps.md": v.root / "outputs" / "router" / "log_vps.md",
    }
    ids_per_plik: dict[str, list[str]] = {}
    for nazwa, path in log_paths.items():
        if not path.is_file():
            continue
        parsed = v.wczytaj_fm(path, "R5")
        if not parsed:
            continue
        fm, body = parsed
        ids = _log_ids(body)
        ids_per_plik[nazwa] = ids
        rel = path.relative_to(v.root).as_posix()

        # Rotacja kwartalna (nota w router.md): wpisy sprzed bieżącego kwartału żyją w
        # log_RRRRQn.md OBOK, a liczniki entry_count/last_entry pliku głównego są
        # KONTYNUOWANE bez resetu — więc do porównania licznika doliczamy wpisy
        # z plików archiwum. Ujawnione pierwszą rotacją <data> (log.md: 79 vs 3).
        zrotowane = 0
        for arch in sorted(path.parent.glob(path.stem + "_*Q*.md")):
            zrotowane += len(_log_ids(arch.read_text(encoding="utf-8")))

        entry_count_raw = fm.get("entry_count")
        if entry_count_raw is not None:
            try:
                entry_count = int(str(entry_count_raw))
                if entry_count != len(ids) + zrotowane:
                    res.findings.append(Finding(
                        "R5", res.title, rel,
                        f"entry_count we frontmatterze = {entry_count}, faktyczna liczba "
                        f"wpisów '## [ID: ...]' = {len(ids) + zrotowane}"
                        + (f" (w tym {zrotowane} w archiwach log_*Q*.md)" if zrotowane else ""),
                    ))
            except ValueError:
                res.findings.append(Finding(
                    "R5", res.title, rel, f"entry_count nie jest liczbą: {entry_count_raw!r}",
                ))

        last_entry = fm.get("last_entry")
        if last_entry is not None:
            last_entry = str(last_entry).strip('"')
            faktyczny_ostatni = ids[-1] if ids else None
            if last_entry != faktyczny_ostatni:
                res.findings.append(Finding(
                    "R5", res.title, rel,
                    f"last_entry we frontmatterze = {last_entry!r}, faktyczny ostatni wpis = "
                    f"{faktyczny_ostatni!r}",
                ))

    if len(ids_per_plik) == 2:
        (nazwa_a, ids_a), (nazwa_b, ids_b) = ids_per_plik.items()
        kolizje = set(ids_a) & set(ids_b)
        for kolidujace_id in sorted(kolizje):
            res.findings.append(Finding(
                "R5", res.title, f"outputs/router/{{{nazwa_a},{nazwa_b}}}",
                f"ID '{kolidujace_id}' występuje w obu plikach ({nazwa_a} i {nazwa_b}) — "
                f"ID przestaje być unikalne globalnie w systemie logów routera",
            ))
    return res


# ---------------------------------------------------------------------------
# R6 — sieroty w wiki/
# ---------------------------------------------------------------------------


def rule_r6(v: Vault) -> RuleResult:
    res = RuleResult("R6", "sieroty w wiki/ (zero linków przychodzących)")
    wiki_dir = v.root / "wiki"
    if not wiki_dir.is_dir():
        res.skipped = "brak wiki/"
        return res
    wiki_stems = {nfc(p.stem) for p in wiki_dir.glob("*.md")}
    if not wiki_stems:
        return res

    incoming: set[str] = set()
    for path, rel in chodz_md(v.root):
        text = czytaj(path)
        if text is None:
            continue
        for m in WIKILINK_RE.finditer(text):
            target = nfc(m.group(1).strip())
            target_base = target.rsplit("/", 1)[-1]
            if target_base in wiki_stems and rel != f"wiki/{target_base}.md":
                incoming.add(target_base)

    for sierota in sorted(wiki_stems - incoming):
        res.findings.append(Finding(
            "R6", res.title, f"wiki/{sierota}.md",
            "brak jakiegokolwiek linku przychodzącego z reszty vaulta",
        ))
    return res


# ---------------------------------------------------------------------------
# R7 — martwe linki, zawężone (wg sekcji II.7 raportu)
# ---------------------------------------------------------------------------

R7_SKANOWANE_KATALOGI = ["wiki", "sources", "clusters", "moc", "system/artifacts", "system/heads"]


def _zbuduj_indeks_nazw(root: Path) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    """Indeks CELÓW linków (używany wyłącznie przez R7): zwraca (indeks_po_basename,
    indeks_po_pelnej_sciezce) — oba znormalizowane NFC, oba pomijają raw/ .obsidian/
    .git/ sandbox/.

    system/templates/ JEST tu uwzględnione, choć chodz_md je pomija. Zasada 8 access_map
    wyklucza templates z GREPOWANIA WIEDZY — ich frontmattery to przykłady, więc nie mogą
    być oceniane przez R2/R3/R6 ani skanowane jako ŹRÓDŁO linków (templates nie ma w
    R7_SKANOWANE_KATALOGI i to się nie zmienia). Ale ten indeks odpowiada na inne pytanie:
    "czy plik, na który wskazuje link, istnieje". [[template_epizod]] w Artefakt_B.md
    wskazuje na realny system/templates/template_epizod.md — link NIE jest martwy i
    zgłaszanie go było kłamstwem reguły, nie luką w vaultcie.

    Alternatywa — jawna lista wyjątków wśród celów R7 — została odrzucona: wymagałaby
    ręcznego dopisywania każdego nowego szablonu i wyciszałaby też PRAWDZIWIE martwy link
    [[template_czegos_co_nie_istnieje]]. Indeks celów mówi prawdę o istnieniu pliku,
    zamiast udawać, że pewne cele są nietykalne."""
    basename_idx: dict[str, list[str]] = defaultdict(list)
    fullpath_idx: dict[str, list[str]] = defaultdict(list)
    pliki = list(chodz_md(root))
    templates = root / "system" / "templates"
    if templates.is_dir():
        pliki += [(p, p.relative_to(root).as_posix()) for p in sorted(templates.rglob("*.md"))]
    for path, rel in pliki:
        rel_nfc = nfc(rel)
        stem = nfc(path.stem)
        basename_idx[stem].append(rel_nfc)
        noext = rel_nfc.removesuffix(".md")
        fullpath_idx[noext].append(rel_nfc)
        # Aliasy SKILL.md (konwencja szablonu, para z R8): [[nazwa_skilla]] rozwiązuje się
        # w Obsidianie przez pole `aliases`, więc dla R7 taki cel ISTNIEJE.
        if path.name == "SKILL.md":
            text = czytaj(path)
            if text:
                fm_text, _ = rozdziel_frontmatter(text)
                if fm_text:
                    try:
                        for alias in linki_z_wartosci(parsuj_frontmatter(fm_text).get("aliases")) or []:
                            basename_idx[nfc(alias)].append(rel_nfc)
                    except Exception:  # noqa: BLE001
                        pass
    return basename_idx, fullpath_idx

# Raport (kontrola 7, kategoria D) opisuje "[[...]]" jako placeholder składniowy
# używany w prozie agentów/skilli do ilustrowania "tu wstaw link" — ale ten sam
# dosłowny token występuje też w system/heads/knowledge.md:26, które JEST w zasięgu
# skanowania R7 (agenci/skille są wykluczeni z zasięgu, heads nie). Wykluczenie po
# katalogu nie wystarcza — token jest wykluczony wprost, niezależnie od pliku, bo to
# udokumentowana konwencja placeholdera w całym vaultcie, nie realny link.
PLACEHOLDER_LINKI = {"..."}


def rule_r7(v: Vault) -> RuleResult:
    res = RuleResult("R7", "martwe linki [[...]] (zawężone: wiki/sources/clusters/moc/"
                            "system/artifacts/system/heads, bez logów routera i bez agents/skills)")
    basename_idx, fullpath_idx = _zbuduj_indeks_nazw(v.root)
    if not basename_idx:
        res.skipped = "pusty vault / brak plików .md"
        return res

    # Propozycje w locie (v1.2; domyka pozycję [OTWARTE] ze Stanu akceptacji
    # knowledge_ingest v1.2): krok 4 ingestu WPROST wymaga linków do stron, które
    # leżą jeszcze jako prop_* w inbox/knowledge/. Taki link nie jest martwy — cel
    # istnieje i czeka na podpis Właściciela (przeniesienie = akceptacja, zasada 3
    # access_map). R7 uznaje go za rozwiązywalny; osobne znalezisko pojawia się
    # dopiero, gdy propozycja ZALEGA (>14 dni po mtime pliku; mtime to przybliżenie —
    # świeży checkout gita je odświeża, więc miara myli się wyłącznie w dół,
    # nigdy fałszywym alarmem).
    prop_dir = v.root / "inbox" / "knowledge"
    prop_stems: dict[str, Path] = {}
    if prop_dir.is_dir():
        for p_prop in sorted(prop_dir.glob("prop_*.md")):
            prop_stems[nfc(p_prop.stem.removeprefix("prop_"))] = p_prop

    for katalog in R7_SKANOWANE_KATALOGI:
        base = v.root / katalog
        if not base.exists():
            continue
        pliki = [base] if base.is_file() else sorted(base.rglob("*.md"))
        for path in pliki:
            rel = path.relative_to(v.root).as_posix()
            text = czytaj(path)
            if text is None:
                v.zgłoś_nieczytelny("R7", rel, "nie udało się odczytać pliku")
                continue
            for m in WIKILINK_RE.finditer(text):
                target = nfc(m.group(1).strip())
                if target in PLACEHOLDER_LINKI:
                    continue
                target_bez_md = target[:-3] if target.lower().endswith(".md") else target
                target_base = target_bez_md.rsplit("/", 1)[-1]
                if target_base in basename_idx:
                    continue
                if target_bez_md.strip("/") in fullpath_idx:
                    continue
                if target_base in prop_stems:
                    continue  # propozycja w locie — cel istnieje w inboxie, czeka na podpis
                linia = text.count("\n", 0, m.start()) + 1
                res.findings.append(Finding(
                    "R7", res.title, rel,
                    f"[[{m.group(1).strip()}]] nie wskazuje na żaden istniejący plik",
                    line=linia,
                ))

    DNI_ZALEGANIA = 14
    teraz = time.time()
    for stem, p_prop in prop_stems.items():
        wiek = int((teraz - p_prop.stat().st_mtime) // 86400)
        if wiek > DNI_ZALEGANIA:
            res.findings.append(Finding(
                "R7", res.title, p_prop.relative_to(v.root).as_posix(),
                f"propozycja zalega w inboxie od {wiek} dni — podpisz (przenieś do wiki/) albo odrzuć",
            ))
    return res


# ---------------------------------------------------------------------------
# R8 — linki międzyskillowe [[nazwa_skilla]] (wzorzec A z kontroli 7)
# ---------------------------------------------------------------------------


def rule_r8(v: Vault) -> RuleResult:
    res = RuleResult("R8", "linki [[nazwa_skilla]] muszą mieć odpowiadający alias w SKILL.md")
    skills_dir = v.root / "system" / "skills"
    if not skills_dir.is_dir():
        res.skipped = "brak system/skills/"
        return res

    # Klucz w NFC (zestawiany z tokenami [[...]] z treści), wartość to PRAWDZIWA ścieżka
    # z dysku — nazwy folderu nie wolno odtwarzać z klucza, bo poza APFS postać NFD/NFC
    # ścieżki nie jest wymienna.
    foldery_skilli = {nfc(p.name): p for p in skills_dir.iterdir() if p.is_dir()}
    if not foldery_skilli:
        return res

    aliasy: dict[str, set[str]] = {}
    for nazwa_folderu, folder_path in foldery_skilli.items():
        skill_md = folder_path / "SKILL.md"
        if not skill_md.is_file():
            aliasy[nazwa_folderu] = set()
            continue
        parsed = v.wczytaj_fm(skill_md, "R8")
        wartosci = set()
        if parsed:
            fm, _ = parsed
            al = fm.get("aliases")
            if al:
                wartosci = {nfc(str(x).strip()) for x in (al if isinstance(al, list) else [al])}
        aliasy[nazwa_folderu] = wartosci

    cele = list((v.root / "system" / "agents").glob("*.md")) if (v.root / "system" / "agents").is_dir() else []
    cele += [p / "SKILL.md" for p in foldery_skilli.values() if (p / "SKILL.md").is_file()]

    for path in cele:
        rel = path.relative_to(v.root).as_posix()
        text = czytaj(path)
        if text is None:
            continue
        for m in WIKILINK_RE.finditer(text):
            token = nfc(m.group(1).strip())
            if token not in foldery_skilli:
                continue
            if token in aliasy.get(token, set()):
                continue
            linia = text.count("\n", 0, m.start()) + 1
            res.findings.append(Finding(
                "R8", res.title, rel,
                f"[[{token}]] odwołuje się do skilla '{token}', ale system/skills/{token}/"
                f"SKILL.md nie ma pola aliases zawierającego '{token}' — plik nazywa się "
                f"SKILL.md, więc ten link nigdy się nie rozwiąże w Obsidianie",
                line=linia,
            ))
    return res


# ---------------------------------------------------------------------------
# R9 — access_map vs .claude/settings.json vs runtime (biała lista zapisu)
# ---------------------------------------------------------------------------

# Zasięg tej reguły jest CELOWO zawężony do agentów, których runtime sam siebie opisuje
# jako obsługujących (komentarze w runtime: "inbox/knowledge/ (propozycje katalizatora/
# zwiadowcy)... inbox/ops/ (propozycje asystenta...)") — to ten sam, wąski zestaw ścieżek co
# .claude/settings.json (commit <commit>, "incydent <data>"), więc oba porównania mają sens
# tylko dla tych trzech agentów. Reszta agentów (architekt→inbox/tech/, builder→sandbox/,
# rekruter→inbox/agents/, metodyk→inbox/skills/ itd.) ma zapis poza zasięgiem obu tych
# białych list z innych, udokumentowanych powodów (patrz raport, kontrola 9) — sprawdzanie
# ich tutaj dałoby wyłącznie fałszywe alarmy niepowiązane z incydentem <data>.
AGENCI_WSPOLNEJ_BIALEJ_LISTY = {"katalizator", "zwiadowca", "asystent"}

# Wyjątek 3a access_map (<data>): katalizator i zwiadowca mają w kolumnie Zapis wpis
# `wiki/`, ale jest to carve-out TREŚCIOWY (append odnośnika w sekcji „## Powiązane"),
# egzekwowany hookiem strażnik zapisu (opcjonalny hook) na treści edycji — nie warstwą ŚCIEŻKOWĄ
# .claude/settings.json. Porównywanie go z permissions.allow dawałoby stały fałszywy alarm:
# ten zapis CELOWO nie ma wpisu w allow, żeby sesje interaktywne dalej pytały Właściciela o zgodę
# (bramką w runtime'ach jest hook, a te i tak chodzą na bypassPermissions).
# Z porównaniem SCIEZKI_DO_DODANIA wiki/ ZOSTAJE — tam wpis jest twardo wymagany, bo
# `git add` operuje na ścieżkach i bez niego dopisek zrobiony na runtime ginie przy recreate.
R9_POMIJANE_W_SETTINGS = {"wiki/"}


def _sciezki_z_kolumny_zapis(tekst: str) -> list[str]:
    """Wyciąga tokeny wyglądające na ścieżki z tekstu kolumny Zapis access_map.md:
    coś/coś/ (katalog) albo coś/Plik.md (konkretny plik)."""
    return re.findall(r"[a-zA-Z_][a-zA-Z0-9_./]*(?:/|\.md)", tekst)


def _sciezki_z_settings_json(vault_root: Path) -> list[str] | None:
    path = vault_root / ".claude" / "settings.json"
    text = czytaj(path)
    if text is None:
        return None
    try:
        data = json.loads(text)
    except Exception:  # noqa: BLE001 — celowo szerokie, jak w czytaj(): plik może być uszkodzony na wiele sposobów
        return None
    allow = data.get("permissions", {}).get("allow", [])
    sciezki = []
    for wpis in allow:
        m = re.match(r"^(Write|Edit)\(([^)]+)\)$", wpis)
        if m:
            sciezki.append(m.group(2))
    return sciezki


def _sciezki_z_run_vps(runtime_path: Path | None) -> list[str] | None:
    if runtime_path is None:
        return None
    run_vps = runtime_path / "runtime.py"
    text = czytaj(run_vps)
    if text is None:
        return None
    m = re.search(r"SCIEZKI_DO_DODANIA\s*=\s*\[(.*?)\]", text, re.DOTALL)
    if not m:
        return None
    inner = m.group(1)
    return [
        _odetnij_komentarz(cz.strip())
        for cz in re.findall(r'"((?:[^"\\]|\\.)*)"', inner)
    ]


def _znormalizuj_dopuszczone(surowe: list[str]) -> list[str]:
    """Zamienia wzorce typu 'outputs/**' na prefiks 'outputs/'. Dopisuje też
    kończące '/' katalogom podanym BEZ niego (runtime pisze
    SCIEZKI_DO_DODANIA jako 'outputs', 'inbox/knowledge' — bez ukośnika na
    końcu — podczas gdy .claude/settings.json i access_map.md używają formy z
    ukośnikiem; bez tej normalizacji porównanie prefiksów fałszywie nie
    znajdowałoby pokrycia). Ścieżki do konkretnego pliku (zawierające kropkę,
    np. '*.md') zostają bez zmian — to nie katalogi."""
    out = []
    for s in surowe:
        s = s.strip()
        if s.endswith("/**"):
            s = s[:-2]  # "outputs/**" -> "outputs/"
        elif s.endswith("**"):
            s = s[:-2]
        if not s.endswith("/") and "." not in s.rsplit("/", 1)[-1]:
            s = s + "/"
        out.append(s)
    return out


def _pokryte(deklarowana: str, dopuszczone: list[str]) -> bool:
    if deklarowana in dopuszczone:
        return True
    for prefiks in dopuszczone:
        if prefiks.endswith("/") and deklarowana.startswith(prefiks):
            return True
    return False


def rule_r9(v: Vault, runtime_path: Path | None) -> RuleResult:
    res = RuleResult(
        "R9",
        "ścieżki zapisu: access_map.md vs .claude/settings.json vs runtime.py "
        "(SCIEZKI_DO_DODANIA), zawężone do agentów katalizator/zwiadowca/asystent",
    )
    map_path = v.root / "system" / "access_map.md"
    map_text = czytaj(map_path)
    if map_text is None:
        res.skipped = "brak system/access_map.md"
        return res
    mapa = parsuj_access_map(map_text)

    settings_paths = _sciezki_z_settings_json(v.root)
    vps_paths = _sciezki_z_run_vps(runtime_path)

    if settings_paths is None and vps_paths is None:
        res.skipped = (
            "brak .claude/settings.json w vaultcie i brak runtime.py pod --runtime-path — "
            "nie ma z czym porównać access_map"
        )
        return res

    settings_norm = _znormalizuj_dopuszczone(settings_paths) if settings_paths else None
    vps_norm = _znormalizuj_dopuszczone(vps_paths) if vps_paths else None

    for agent in sorted(AGENCI_WSPOLNEJ_BIALEJ_LISTY):
        wiersz = mapa.get(agent)
        if wiersz is None:
            continue
        deklarowane = _sciezki_z_kolumny_zapis(wiersz.get("zapis", ""))
        if not deklarowane:
            continue

        if settings_norm is not None:
            for sciezka in deklarowane:
                if sciezka in R9_POMIJANE_W_SETTINGS:
                    continue
                if not _pokryte(sciezka, settings_norm):
                    res.findings.append(Finding(
                        "R9", res.title, ".claude/settings.json",
                        f"agent [[{agent}]] ma w access_map.md prawo zapisu do '{sciezka}', "
                        f"ale .claude/settings.json (permissions.allow) tego nie pokrywa",
                    ))
        if vps_norm is not None:
            for sciezka in deklarowane:
                if not _pokryte(sciezka, vps_norm):
                    res.findings.append(Finding(
                        "R9", res.title,
                        str((runtime_path / "runtime.py").relative_to(runtime_path.parent))
                        if runtime_path else "run_vps",
                        f"agent [[{agent}]] ma w access_map.md prawo zapisu do '{sciezka}', "
                        f"ale SCIEZKI_DO_DODANIA w run_vps tego nie pokrywa",
                    ))
    return res


# ---------------------------------------------------------------------------
# R10 — warstwa deny w .claude/settings.json vs konstytucja access_map (paczka #2)
# ---------------------------------------------------------------------------

# Cel: naprawa z paczki audytowej #1 (<data>, znalezisko #2) nie może cofnąć się
# cicho. Trzy klasy regresji, każda była realna PRZED paczką: (1) powrót zapisu raw/**
# do allow (stan sprzed audytu), (2) zniknięcie całej sekcji deny (np. ręczna edycja
# "na chwilę"), (3) wykruszenie pojedynczych zakazów konstytucyjnych z deny.
# Reguła porównuje settings.json z LISTĄ STAŁĄ wyprowadzoną z zasady 3 access_map —
# celowo NIE parsuje access_map.md (zasada 3 to proza; stała lista jest stabilniejsza
# i czytelniejsza w utrzymaniu niż heurystyka na zdaniach — ta sama filozofia co
# zawężenie R9).

# Strefy, w których zasada 3 access_map zakazuje zapisu agentom — deny musi je pokrywać
# dla OBU narzędzi (Write i Edit):
R10_STREFY_PELNE = ["raw", "moc", "clusters"]
# system/, .claude/ i (od <data>) wiki/ mają w settings.json strukturę NIESYMETRYCZNĄ —
# sprawdzamy dokładnie te wpisy, które są minimum konstytucyjnym:
R10_WPISY_WYMAGANE_DODATKOWO = [
    "Write(system/**)",
    "Write(.claude/**)", "Edit(.claude/**)",
    # wiki/ — wyjątek 3a access_map (<data>). Write ZOSTAJE w deny bezwzględnie: to
    # warunek 1 wyjątku (Write nadpisuje cały plik, więc append-only nie jest weryfikowalny)
    # egzekwowany DRUGĄ, niezależną warstwą, obok hooka. Analogia do system/: całościowy
    # zakaz Write + wyjęty spod niego Edit.
    "Write(wiki/**)",
]
# ...a Edit(wiki/**) musi być POZA deny, inaczej wyjątek 3a nie działa w ŻADNYM runtime.
# Zmierzone na żywo (sonda buildera <data>, SDK <wersja>): permissions.deny bije
# ZARÓWNO permission_mode="bypassPermissions", JAK I jawną zgodę hooka PreToolUse — przy
# `deny: ["Edit(wiki/**)"]` edycja jest odrzucana mimo hooka zwracającego {}, a po usunięciu
# wpisu przechodzi. Oba runtime'y ładują setting_sources=["project"], więc dotyczy to i Maca,
# i runtime. Ta reguła pilnuje, żeby wpis nie wrócił „porządkująco" i nie wyłączył wyjątku po
# cichu — bez niej regresja byłaby niewidoczna dla wszystkich testów jednostkowych, bo te
# wołają hook bezpośrednio, z pominięciem warstwy settings.json.
R10_WPISY_ZAKAZANE_W_DENY = ["Edit(wiki/**)"]


def _r10_normalizuj(wpis: str) -> str:
    """'Write( raw/** )' → 'Write(raw/**)' — tolerancja na spacje, nic więcej."""
    m = re.match(r"^\s*(Write|Edit)\(\s*([^)]*?)\s*\)\s*$", wpis)
    return f"{m.group(1)}({m.group(2)})" if m else wpis.strip()


def rule_r10(v: Vault) -> RuleResult:
    res = RuleResult(
        "R10",
        "warstwa deny w .claude/settings.json vs konstytucja access_map "
        "(strażnik naprawy z paczki audytowej #1)",
    )
    path = v.root / ".claude" / "settings.json"
    rel = ".claude/settings.json"
    text = czytaj(path)
    if text is None:
        # Brak pliku to ZNALEZISKO, nie skip: settings.json jest od <data> warstwą
        # uprawnień czytaną przez subagentów — jego zniknięcie cofa dwa incydenty naraz.
        res.findings.append(Finding(
            "R10", res.title, rel,
            "brak pliku .claude/settings.json — warstwa uprawnień SDK (incydent <data>) "
            "i warstwa deny (paczka #1) nie istnieją",
        ))
        return res
    try:
        data = json.loads(text)
    except Exception:  # noqa: BLE001 — jak w R9: uszkodzony JSON to znalezisko, nie crash lintu
        res.findings.append(Finding(
            "R10", res.title, rel, "plik nie parsuje się jako JSON",
        ))
        return res

    perms = data.get("permissions", {}) or {}
    allow = [_r10_normalizuj(w) for w in (perms.get("allow") or [])]
    deny = [_r10_normalizuj(w) for w in (perms.get("deny") or [])]

    # (1) raw/** nie może wrócić do allow — dokładna klasa regresji sprzed audytu.
    for wpis in allow:
        m = re.match(r"^(Write|Edit)\((raw(/|$).*)\)$", wpis)
        if m:
            res.findings.append(Finding(
                "R10", res.title, rel,
                f"allow zawiera zapis do raw/ ({wpis}) — sprzeczne z zasadą 3 access_map "
                f"(raw/ jest niezmienne); stan sprzed paczki audytowej #1",
            ))

    # (2) sekcja deny musi istnieć i być niepusta.
    if not deny:
        res.findings.append(Finding(
            "R10", res.title, rel,
            "brak niepustej sekcji permissions.deny — konstytucja access_map przestaje "
            "być egzekwowalna w sesjach interaktywnych (regresja paczki #1 w całości)",
        ))
        return res  # bez deny sprawdzanie pojedynczych wpisów nie ma sensu

    # (3) komplet zakazów konstytucyjnych.
    wymagane = [f"{narz}({strefa}/**)"
                for strefa in R10_STREFY_PELNE for narz in ("Write", "Edit")]
    wymagane += R10_WPISY_WYMAGANE_DODATKOWO
    for wpis in wymagane:
        if wpis not in deny:
            res.findings.append(Finding(
                "R10", res.title, rel,
                f"w permissions.deny brakuje wpisu '{wpis}' (minimum konstytucyjne "
                f"z paczki audytowej #1)",
            ))

    # (4) wpisy, które MUSZĄ być poza deny — inaczej wyjątek 3a przestaje działać.
    for wpis in R10_WPISY_ZAKAZANE_W_DENY:
        if wpis in deny:
            res.findings.append(Finding(
                "R10", res.title, rel,
                f"permissions.deny zawiera '{wpis}' — to WYŁĄCZA wyjątek 3a access_map "
                f"(linkowanie zwrotne katalizatora i zwiadowcy) w OBU runtime'ach, bo deny "
                f"bije zarówno bypassPermissions, jak i zgodę hooka strażnik zapisu (opcjonalny hook). "
                f"Kontrolę treściową appendu pełni hook; Write(wiki/**) zostaje w deny",
            ))
    return res


# ---------------------------------------------------------------------------
# R11 — cluster_access (frontmatter agenta) ↔ kolumna Klastry (access_map), obustronnie
# ---------------------------------------------------------------------------

# Migracja K1 (access_map v<n>, <data>): zasięg treści wiki/ per persona wyznacza
# JEDEN mechanizm — pole `cluster_access` w definicji agenta, którego lustrem jest kolumna
# "Klastry (wiki/)" w tabeli mapy. Ta reguła zamyka klasę "zmiana jednej strony pary"
# (10 przypadków w ewidencji audytów; rozjazdy formy tags_extra D3/D4 przetrwały OSIEM
# wersji mapy właśnie dlatego, że dwie ręczne kopie normy nie miały strażnika).
# Trzy kontrole:
#   (a) obustronna równość zbiorów: klastry z frontmattera == klastry z kolumny
#       (wartość specjalna "all" musi stać po OBU stronach naraz);
#   (b) kompletność pary: agent z plikiem w system/agents/ musi mieć pole cluster_access
#       I wiersz w mapie; wiersz mapy musi mieć plik agenta;
#   (c) istnienie klastrów: każda nazwa z frontmattera musi odpowiadać plikowi
#       clusters/<Nazwa>.md (łapie literówki w nazwach wieloczłonowych ze spacjami).
# Porównanie w NFC po obu stronach (ta sama pułapka dysk↔treść co w R2/R7/R8).

R11_PUSTE = {"", "-", "–", "—"}


def _r11_zbior_z_kolumny(tekst: str) -> set[str] | str | None:
    """Kolumna Klastry: 'all' | 'Nazwa A, Nazwa B, ...' | pusta ('–'/'—'/'-', także
    Z ADNOTACJĄ w nawiasie: '— (brak klastra prawnego …)' — precedens wiersza
    [[persona_bez_klastrow]], korekta v<n>). Zwraca 'all', zbiór nazw (NFC) albo
    None dla pustej."""
    t = nfc(tekst.strip())
    if t in R11_PUSTE or (t and t[0] in "-–—"):
        return None
    if t == "all":
        return "all"
    return {czesc.strip() for czesc in t.split(",") if czesc.strip()}


def _r11_zbior_z_frontmattera(wartosc) -> set[str] | str | None:
    """Pole cluster_access: 'all' | lista '[[Nazwa]]' | JAWNIE pusta lista `[]`
    (świadome zero klastrów — praca na źródłach zewnętrznych, precedens
    [[persona_bez_klastrow]]) | brak pola. Zwraca 'all', zbiór (możliwie pusty) albo
    None wyłącznie dla BRAKU pola."""
    if wartosc is None:
        return None
    if isinstance(wartosc, str) and nfc(wartosc.strip()) == "all":
        return "all"
    if isinstance(wartosc, list) and not wartosc:
        return set()  # jawnie puste — NIE mylić z brakiem pola
    nazwy = linki_z_wartosci(wartosc)
    return {n for n in nazwy if n} or set()


def rule_r11(v: Vault) -> RuleResult:
    res = RuleResult(
        "R11",
        "cluster_access (frontmatter agenta) ↔ kolumna Klastry access_map, obustronnie "
        "(migracja K1, v<n>)",
    )
    map_path = v.root / "system" / "access_map.md"
    map_text = czytaj(map_path)
    if map_text is None:
        res.skipped = "brak system/access_map.md"
        return res
    mapa = parsuj_access_map(map_text)

    agent_dir = v.root / "system" / "agents"
    if not agent_dir.is_dir():
        res.skipped = "brak system/agents/"
        return res

    clusters_dir = v.root / "clusters"
    klastry_na_dysku = (
        {nfc(p.stem) for p in clusters_dir.glob("*.md")} if clusters_dir.is_dir() else None
    )

    pliki_agentow = {nfc(p.stem): p for p in sorted(agent_dir.glob("*.md"))}

    # kierunek 1: każdy plik agenta ma mieć pole i wiersz, a zbiory mają być równe
    for nazwa, path in pliki_agentow.items():
        rel = path.relative_to(v.root).as_posix()
        parsed = v.wczytaj_fm(path, "R11")
        if not parsed:
            continue
        fm, _ = parsed
        z_fm = _r11_zbior_z_frontmattera(fm.get("cluster_access"))
        wiersz = mapa.get(nazwa)

        if z_fm is None:
            res.findings.append(Finding(
                "R11", res.title, rel,
                "brak pola cluster_access we frontmatterze — od migracji K1 (v<n>) to "
                "JEDYNY mechanizm zasięgu treści wiki/; agent bez pola nie ma zasięgu wiki/ "
                "zdefiniowanego żadną normą",
            ))
            # bez pola nie ma czego porównywać z mapą; brak wiersza zgłosi się niżej per mapa
            continue

        # (c) istnienie klastrów — tylko dla list (nie dla 'all')
        if isinstance(z_fm, set) and klastry_na_dysku is not None:
            for klaster in sorted(z_fm - klastry_na_dysku):
                res.findings.append(Finding(
                    "R11", res.title, rel,
                    f"cluster_access wymienia klaster '{klaster}', ale clusters/{klaster}.md "
                    f"nie istnieje (literówka albo klaster usunięty bez aktualizacji pary)",
                ))

        if wiersz is None:
            res.findings.append(Finding(
                "R11", res.title, rel,
                f"agent ma pole cluster_access, ale w tabeli access_map.md nie ma wiersza "
                f"[[{nazwa}]] — para frontmatter↔mapa jest jednostronna",
            ))
            continue

        z_mapy = _r11_zbior_z_kolumny(wiersz.get("klastry", ""))
        if z_mapy is None:
            z_mapy = set()  # pusta/adnotowana kolumna == świadome zero klastrów
        if z_fm == "all" or z_mapy == "all":
            if z_fm != z_mapy:
                res.findings.append(Finding(
                    "R11", res.title, rel,
                    f"rozjazd 'all': frontmatter cluster_access = "
                    f"{'all' if z_fm == 'all' else sorted(z_fm) if z_fm else 'brak'}, "
                    f"kolumna Klastry = "
                    f"{'all' if z_mapy == 'all' else sorted(z_mapy) if z_mapy else 'pusta'} — "
                    f"wartość specjalna 'all' musi stać po obu stronach naraz",
                ))
            continue

        fm_set = z_fm if isinstance(z_fm, set) else set()
        mapa_set = z_mapy if isinstance(z_mapy, set) else set()
        for klaster in sorted(fm_set - mapa_set):
            res.findings.append(Finding(
                "R11", res.title, rel,
                f"cluster_access wymienia '{klaster}', ale kolumna Klastry wiersza "
                f"[[{nazwa}]] w access_map.md go nie zawiera (zmiana jednej strony pary)",
            ))
        for klaster in sorted(mapa_set - fm_set):
            res.findings.append(Finding(
                "R11", res.title, "system/access_map.md",
                f"kolumna Klastry wiersza [[{nazwa}]] zawiera '{klaster}', ale "
                f"cluster_access w system/agents/{nazwa}.md go nie wymienia "
                f"(zmiana jednej strony pary)",
            ))

    # kierunek 2: wiersz mapy bez pliku agenta
    for nazwa in sorted(set(mapa) - set(pliki_agentow)):
        res.findings.append(Finding(
            "R11", res.title, "system/access_map.md",
            f"tabela ma wiersz [[{nazwa}]], ale system/agents/{nazwa}.md nie istnieje — "
            f"kolumna Klastry nie ma swojego lustra we frontmatterze",
        ))
    return res


# ---------------------------------------------------------------------------
# R12 — read_scope (frontmatter agenta) ↔ kolumna "Odczyt (poza wiki/)", obustronnie
# ---------------------------------------------------------------------------

# Korekta v<n> (<data>): paczka v<n> domknęła oś cluster_access regułą R11,
# a oś read_scope↔Odczyt zostawiła bez strażnika — i w dniu wdrożenia wyprodukowała
# 5 nadań martwych (audyt doraźny knowledge <data>, §3a). Ta reguła domyka klasę.
# ZASIĘG ŚWIADOMIE ZAWĘŻONY: wyłącznie persony, których definicja MA pole read_scope
# (konwencja: persony działowe product/finance/brand mogą go nie mieć — ich artefakty
# żyją w prozie "Źródeł wiedzy"; BRAK pola to BRAK ODPOWIEDNIKA, nie rozjazd — tak
# rozstrzygnął audyt doraźny i tak zostaje).
# Dopasowanie tolerancyjne w OBIE strony:
#  - wpis read_scope jest pokryty, gdy jego pełna ścieżka LUB sam basename występuje
#    w tekście kolumny (mapa używa skrótów: "system/artifacts/A.md, B.md, C.md");
#  - token ścieżkowy z kolumny (kończący się na "/" albo ".md") jest pokryty, gdy
#    odpowiada wpisowi read_scope wprost, po basename, albo leży pod katalogiem
#    przyznanym w read_scope. Proza w nawiasach kolumny nie generuje tokenów
#    (tokeny = wyłącznie fragmenty wyglądające na ścieżki).

R12_TOKEN_RE = re.compile(r"[A-Za-z_\u00C0-\u024F\u0141\u0142][\w\u00C0-\u024F\u0141\u0142./-]*", re.UNICODE)


NAWIAS_RE = re.compile(r"\([^()]*\)")


def _bez_nawiasow(tekst: str) -> str:
    """Usuwa treść nawiasów okrągłych (adnotacje mapy: „outputs/ops/ (delta briefu…)").
    Konwencja mapy: GRANTY stoją poza nawiasami, w nawiasach żyje proza — która potrafi
    wymieniać pliki tytułem opisu kroku (np. „grep … w *_innowacja.md, kotwica do log.md")
    i bez tego cięcia produkowała fałszywe tokeny nadań."""
    poprzedni = None
    while poprzedni != tekst:
        poprzedni = tekst
        tekst = NAWIAS_RE.sub(" ", tekst)
    return tekst


def _r12_tokeny_z_kolumny(tekst: str) -> set[str]:
    """Tokeny ŚCIEŻKOWE z tekstu kolumny Odczyt PO zdjęciu adnotacji nawiasowych:
    katalogi ('outputs/ops/') i pliki ('.md' — z prefiksem katalogu albo skrótowo samym
    basename). Zwykłe słowa prozy i fragmenty globów ('_innowacja.md' po '*') odpadają."""
    out = set()
    for tok in R12_TOKEN_RE.findall(nfc(_bez_nawiasow(tekst))):
        if tok.startswith("_"):
            continue  # ogon globu typu *_innowacja.md — nie jest grantem
        if tok.endswith("/") or tok.endswith(".md"):
            out.add(tok)
    return out


def _r12_pokryty_w_kolumnie(wpis: str, kolumna: str) -> bool:
    if wystepuje_jako_token(wpis.rstrip("/"), kolumna):
        return True
    base = wpis.rstrip("/").rsplit("/", 1)[-1]
    return wystepuje_jako_token(base, kolumna)


def _r12_pokryty_w_read_scope(tok: str, wpisy: list[str]) -> bool:
    tok_n = nfc(tok)
    base_tok = tok_n.rstrip("/").rsplit("/", 1)[-1]
    for w in wpisy:
        w_n = nfc(w)
        if tok_n == w_n:
            return True
        if w_n.endswith("/") and tok_n.startswith(w_n):
            return True
        if base_tok == w_n.rstrip("/").rsplit("/", 1)[-1]:
            return True
    return False


def rule_r12(v: Vault) -> RuleResult:
    res = RuleResult(
        "R12",
        "read_scope (frontmatter agenta) ↔ kolumna Odczyt access_map, obustronnie "
        "(wyłącznie persony z polem read_scope; korekta v<n>)",
    )
    map_path = v.root / "system" / "access_map.md"
    map_text = czytaj(map_path)
    if map_text is None:
        res.skipped = "brak system/access_map.md"
        return res
    mapa = parsuj_access_map(map_text)
    agent_dir = v.root / "system" / "agents"
    if not agent_dir.is_dir():
        res.skipped = "brak system/agents/"
        return res

    for path in sorted(agent_dir.glob("*.md")):
        nazwa = nfc(path.stem)
        rel = path.relative_to(v.root).as_posix()
        parsed = v.wczytaj_fm(path, "R12")
        if not parsed:
            continue
        fm, _ = parsed
        rs = fm.get("read_scope")
        if rs is None:
            continue  # konwencja: brak pola = brak odpowiednika, nie rozjazd
        wpisy = [str(x).strip() for x in (rs if isinstance(rs, list) else [rs]) if str(x).strip()]
        wiersz = mapa.get(nazwa)
        if wiersz is None:
            continue  # brak wiersza zgłasza R11 — nie dublujemy
        kolumna = wiersz.get("odczyt", "")

        for wpis in wpisy:
            if not _r12_pokryty_w_kolumnie(wpis, kolumna):
                res.findings.append(Finding(
                    "R12", res.title, rel,
                    f"read_scope zawiera '{wpis}', ale kolumna Odczyt wiersza [[{nazwa}]] "
                    f"w access_map.md go nie niesie (definicja szersza niż mapa — "
                    f"zmiana jednej strony pary)",
                ))
        for tok in sorted(_r12_tokeny_z_kolumny(kolumna)):
            if not _r12_pokryty_w_read_scope(tok, wpisy):
                res.findings.append(Finding(
                    "R12", res.title, "system/access_map.md",
                    f"kolumna Odczyt wiersza [[{nazwa}]] niesie '{tok}', a read_scope w "
                    f"system/agents/{nazwa}.md go nie niesie (NADANIE MARTWE — klasa "
                    f"5 przypadków z dnia wdrożenia v<n>)",
                ))
    return res



# ---------------------------------------------------------------------------
# R13 — wymagany_odczyt skilla vs zasięg odczytu agenta (bliźniak R1 dla ŚCIEŻEK)
# ---------------------------------------------------------------------------
# R1 pilnuje pary skill ↔ mapa dla ARTEFAKTÓW (`depends_on_artifacts`). Ścieżki i
# katalogi, których procedura wymaga do odczytu (`outputs/knowledge/audyt_*.md`,
# `system/agents/*.md`, `clusters/`), żyły dotąd WYŁĄCZNIE w prozie kroków — żadne pole
# ich nie deklarowało, więc żadna reguła ich nie porównywała. Klasa udokumentowana
# trzynastoma przypadkami w sześciu wersjach mapy (v<n> … v<n>); najczystszy:
# knowledge_audyt_zrodel czytał w krokach 1 i 3 `outputs/knowledge/audyt_*.md` oraz
# `*_zwiad.md` od v1.0, a wiersz [[zwiadowca]] nadawał z tego katalogu jeden plik —
# skill był niewykonalny w literze normy przez trzy przebiegi, przy CZYSTYM lincie,
# bo mapa i definicja były ze sobą zgodne (R11/R12 zielone). Rozjazd był między
# SKILLEM a mapą i tej pary nie pilnowało nic.
#
# Konwencja jak w R12: reguła dotyczy WYŁĄCZNIE skilli MAJĄCYCH pole `wymagany_odczyt`.
# Brak pola = brak deklaracji, nie rozjazd — dzięki temu retrofit 33 skilli może iść
# przyrostowo, skill po skillu, bez zatrzymywania lintu na czerwono.
#
# Kierunek JEDEN: skill wymaga ⊆ persona ma. Nadmiar w mapie nie jest błędem tej reguły
# (od nadmiaru jest R12 i audyt dostępów) — brak jest.

# Ścieżki czytelne dla KAŻDEJ persony z mocy zasady 4 access_map („strukturę taksonomii
# czytasz jak każda persona") — nie występują w kolumnie „Odczyt (poza wiki/)", bo nie są
# nadaniem indywidualnym. Bez tego wyjątku R13 dałby fałszywy alarm przy pierwszym skillu
# deklarującym `clusters/` (np. knowledge_audyt_zrodel, krok 1: tags_owned wszystkich klastrów).
R13_UNIWERSALNE = {"moc/", "clusters/"}


def _r13_granty(kolumna: str, read_scope: list[str]) -> set[str]:
    """Suma nadań odczytu persony: tokeny ścieżkowe z kolumny Odczyt mapy + wpisy
    read_scope z definicji. Jedno źródło prawdy dla dopasowania w R13."""
    granty = {nfc(t) for t in _r12_tokeny_z_kolumny(kolumna)}
    granty |= {nfc(w.strip()) for w in read_scope if w.strip()}
    return granty


def _r13_pokryty(wpis: str, kolumna: str, read_scope: list[str], cluster_access) -> bool:
    """Czy ścieżka wymagana przez skill mieści się w zasięgu odczytu persony.

    Dopasowanie CELOWO SUROWSZE niż w R12 i to jest sedno tej reguły. R12 porównuje
    dwa opisy TEGO SAMEGO nadania (mapa vs definicja) i może być tolerancyjny w obie
    strony. R13 porównuje ŻĄDANIE z NADANIEM — a wtedy nadanie pojedynczego pliku
    NIE pokrywa żądania całego katalogu. Pierwsza wersja tej funkcji dziedziczyła
    pobłażliwość po R12 i przepuszczała dokładnie incydent, dla którego reguła
    powstała (`outputs/knowledge/log.md` w mapie vs `outputs/knowledge/` w skillu) —
    wychwycone testem `test_pozytywny_odtworzenie_incydentu_zwiadowcy`.

    Wyjątek `wiki/`: zasięg treści wiki/ niesie `cluster_access` (zasada 4 po K1),
    a nie kolumna Odczyt — niepusta lista albo `all` pokrywa wpis.
    """
    w = nfc(wpis).strip()
    if w.rstrip("/") == "wiki":
        if isinstance(cluster_access, str):
            return cluster_access.strip().lower() == "all"
        if isinstance(cluster_access, list):
            return len(cluster_access) > 0
        return False

    if w.rstrip("/") + "/" in R13_UNIWERSALNE:
        return True

    zada_katalog = w.endswith("/")
    w_norm = w.rstrip("/")
    base_w = w_norm.rsplit("/", 1)[-1]

    for g in _r13_granty(kolumna, read_scope):
        g_norm = g.rstrip("/")
        if g_norm == w_norm:
            return True
        # nadanie katalogu pokrywa wszystko pod nim (także żądany podkatalog)
        if g.endswith("/") and (w_norm + "/").startswith(g_norm + "/"):
            return True
        if zada_katalog:
            continue  # żądanie KATALOGU: nadanie pliku go nie pokrywa
        # skrót konwencji mapy: „system/artifacts/A.md, B.md" — dopasowanie po basename,
        # dopuszczalne WYŁĄCZNIE dla żądania plikowego
        if base_w and base_w == g_norm.rsplit("/", 1)[-1]:
            return True
    return False


def rule_r13(v: Vault) -> RuleResult:
    res = RuleResult(
        "R13",
        "wymagany_odczyt skilla ↔ zasięg odczytu agenta z used_by "
        "(wyłącznie skille z polem wymagany_odczyt)",
    )
    map_path = v.root / "system" / "access_map.md"
    map_text = czytaj(map_path)
    if map_text is None:
        res.skipped = "brak system/access_map.md"
        return res
    mapa = parsuj_access_map(map_text)

    agent_dir = v.root / "system" / "agents"
    if not agent_dir.is_dir():
        res.skipped = "brak system/agents/"
        return res

    zasieg: dict[str, tuple[str, list[str], object]] = {}
    for agent_path in sorted(agent_dir.glob("*.md")):
        nazwa = nfc(agent_path.stem)
        kolumna = mapa.get(nazwa, {}).get("odczyt", "")
        read_scope: list[str] = []
        cluster_access = None
        parsed = v.wczytaj_fm(agent_path, "R13")
        if parsed:
            fm, _ = parsed
            rs = fm.get("read_scope")
            if rs:
                read_scope = [str(x).strip() for x in (rs if isinstance(rs, list) else [rs])
                              if str(x).strip()]
            cluster_access = fm.get("cluster_access")
        zasieg[nazwa] = (kolumna, read_scope, cluster_access)

    skills_dir = v.root / "system" / "skills"
    if not skills_dir.is_dir():
        res.skipped = "brak system/skills/"
        return res

    for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
        rel = skill_md.relative_to(v.root).as_posix()
        parsed = v.wczytaj_fm(skill_md, "R13")
        if not parsed:
            continue
        fm, _ = parsed
        wymagane = fm.get("wymagany_odczyt")
        if wymagane is None:
            continue  # konwencja: brak pola = brak deklaracji, nie rozjazd
        wpisy = [str(x).strip() for x in (wymagane if isinstance(wymagane, list) else [wymagane])
                 if str(x).strip()]
        used_by = linki_z_wartosci(fm.get("used_by"))
        if not wpisy:
            continue
        if not used_by:
            res.findings.append(Finding(
                "R13", res.title, rel,
                "skill deklaruje wymagany_odczyt, ale nie ma pola used_by — nie da się "
                "sprawdzić, czyj zasięg ma go pokrywać",
            ))
            continue
        for agent in used_by:
            wpis_zasiegu = zasieg.get(agent)
            if wpis_zasiegu is None:
                res.findings.append(Finding(
                    "R13", res.title, rel,
                    f"skill wymienia used_by: [[{agent}]], ale nie ma takiego agenta w "
                    f"system/agents/ ani w access_map.md",
                ))
                continue
            kolumna, read_scope, cluster_access = wpis_zasiegu
            for wpis in wpisy:
                if not _r13_pokryty(wpis, kolumna, read_scope, cluster_access):
                    res.findings.append(Finding(
                        "R13", res.title, rel,
                        f"wymagany_odczyt zawiera '{wpis}', ale agent [[{agent}]] (used_by) "
                        f"nie ma tej ścieżki w zasięgu odczytu wg access_map.md/read_scope "
                        f"— procedura nakazuje odczyt spoza normy",
                    ))
    return res


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

WSZYSTKIE_REGULY = ["R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10", "R11", "R12", "R13"]


def uruchom_wszystko(vault_root: Path, runtime_path: Path | None) -> tuple[Vault, list[RuleResult]]:
    v = Vault(vault_root)
    wyniki = [
        rule_r1(v),
        rule_r2(v),
        rule_r3(v),
        rule_r4(v),
        rule_r5(v),
        rule_r6(v),
        rule_r7(v),
        rule_r8(v),
        rule_r9(v, runtime_path),
        rule_r10(v),
        rule_r11(v),
        rule_r12(v),
        rule_r13(v),
    ]
    return v, wyniki


# ---------------------------------------------------------------------------
# Baseline — świadomie zaakceptowane znaleziska (wyciszane w raporcie, nie usuwane z reguł)
# ---------------------------------------------------------------------------


@dataclass
class WpisBaseline:
    rule: str  # np. "R8" — do jakiej reguły należy znalezisko
    match: str  # substring szukany w Finding.message — stabilny identyfikator, NIGDY numer linii
    accepted: str  # data akceptacji (string, np. "<data>")
    reason: str  # jedno zdanie: dlaczego to świadoma decyzja, nie bug
    file: str | None = None  # opcjonalne dodatkowe zawężenie do jednego pliku (domyślnie: cały vault)


def wczytaj_baseline(path: Path | None) -> list[WpisBaseline]:
    """Wczytuje listę zaakceptowanych znalezisk z JSON. Brak pliku = pusta lista — baseline
    jest opcjonalny, bez niego lint działa dokładnie jak wcześniej, nic się nie chowa."""
    if path is None or not path.is_file():
        return []
    try:
        dane = json.loads(path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001 — uszkodzony baseline ma być zignorowany, nie wywrócić lintu
        return []
    wpisy = []
    for w in dane:
        wpisy.append(WpisBaseline(
            rule=w["rule"],
            match=w["match"],
            accepted=w.get("accepted", ""),
            reason=w.get("reason", ""),
            file=w.get("file"),
        ))
    return wpisy


def dopasuj_baseline(f: Finding, baseline: list[WpisBaseline]) -> WpisBaseline | None:
    for w in baseline:
        if w.rule != f.rule:
            continue
        if w.match not in f.message:
            continue
        if w.file is not None and w.file != f.file:
            continue
        return w
    return None


def podziel_na_aktywne_i_wyciszone(
    wyniki: list[RuleResult], baseline: list[WpisBaseline]
) -> tuple[list[RuleResult], dict[str, list[tuple[Finding, WpisBaseline]]]]:
    """Zwraca (te same RuleResult, ale findings zawężone do AKTYWNYCH, czyli spoza baseline;
    {rule: [(finding, wpis_baseline), ...]} — co i dlaczego zostało wyciszone)."""
    wyciszone: dict[str, list[tuple[Finding, WpisBaseline]]] = defaultdict(list)
    aktywne_wyniki = []
    for res in wyniki:
        aktywne = []
        for f in res.findings:
            trafienie = dopasuj_baseline(f, baseline)
            if trafienie is not None:
                wyciszone[res.rule].append((f, trafienie))
            else:
                aktywne.append(f)
        aktywne_wyniki.append(RuleResult(rule=res.rule, title=res.title, findings=aktywne, skipped=res.skipped))
    return aktywne_wyniki, wyciszone


def raport_tekstowy(
    v: Vault,
    wyniki: list[RuleResult],
    wyciszone: dict[str, list[tuple[Finding, WpisBaseline]]],
    pokaz_wyciszone: bool,
) -> tuple[str, int]:
    linie = []
    total = 0
    for res in wyniki:
        if res.skipped:
            linie.append(f"[{res.rule}] {res.title} — POMINIĘTA: {res.skipped}")
            continue
        if not res.findings:
            continue
        linie.append(f"[{res.rule}] {res.title} — {len(res.findings)} znalezisk")
        for f in res.findings:
            loc = f.file + (f":{f.line}" if f.line else "")
            linie.append(f"  - {loc}: {f.message}")
        total += len(res.findings)

    if v.unreadable:
        linie.append(f"[NIECZYTELNE] pliki nie do sparsowania — {len(v.unreadable)}")
        for f in v.unreadable:
            linie.append(f"  - {f.file}: {f.message}")
        total += len(v.unreadable)

    liczba_regul = len({res.rule for res in wyniki if res.findings})
    if v.unreadable:
        liczba_regul += 1

    liczba_wyciszonych = sum(len(lista) for lista in wyciszone.values())
    linie_wyciszone = []
    if pokaz_wyciszone and liczba_wyciszonych:
        linie_wyciszone.append(f"\n[WYCISZONE] zaakceptowane w baseline — {liczba_wyciszonych}")
        for rule in sorted(wyciszone):
            for f, w in wyciszone[rule]:
                loc = f.file + (f":{f.line}" if f.line else "")
                linie_wyciszone.append(f"  - [{rule}] {loc}: {f.message}")
                linie_wyciszone.append(f"      (baseline {w.accepted}: {w.reason})")

    if total == 0:
        if liczba_wyciszonych == 0:
            return "lint spójności: czysto, 0 znalezisk w 0 regułach.", 0
        if not pokaz_wyciszone:
            komunikat = (
                f"lint spójności: czysto, 0 aktywnych znalezisk "
                f"({liczba_wyciszonych} wyciszonych w baseline — użyj --show-baselined, by je zobaczyć)."
            )
            return komunikat, 0
        naglowek = "lint spójności: czysto, 0 aktywnych znalezisk."
        return naglowek + "\n" + "\n".join(linie_wyciszone), 0

    podsumowanie = f"\n{total} znalezisk w {liczba_regul} regułach."
    if liczba_wyciszonych and not pokaz_wyciszone:
        podsumowanie += (
            f" ({liczba_wyciszonych} dodatkowych wyciszonych w baseline — użyj --show-baselined.)"
        )
    return "\n".join(linie) + podsumowanie + "\n".join(linie_wyciszone), 1


def raport_json(
    v: Vault,
    wyniki: list[RuleResult],
    wyciszone: dict[str, list[tuple[Finding, WpisBaseline]]],
    pokaz_wyciszone: bool,
) -> tuple[str, int]:
    out = {"rules": []}
    total = 0
    for res in wyniki:
        wpis = {
            "rule": res.rule,
            "title": res.title,
            "skipped": res.skipped,
            "findings": [
                {"file": f.file, "line": f.line, "message": f.message} for f in res.findings
            ],
        }
        out["rules"].append(wpis)
        total += len(res.findings)
    out["unreadable"] = [{"file": f.file, "message": f.message} for f in v.unreadable]
    total += len(v.unreadable)
    out["total_findings"] = total

    liczba_wyciszonych = sum(len(lista) for lista in wyciszone.values())
    out["baselined_count"] = liczba_wyciszonych
    if pokaz_wyciszone:
        out["baselined"] = [
            {
                "rule": rule,
                "file": f.file,
                "line": f.line,
                "message": f.message,
                "accepted": w.accepted,
                "reason": w.reason,
            }
            for rule in sorted(wyciszone)
            for f, w in wyciszone[rule]
        ]

    return json.dumps(out, ensure_ascii=False, indent=2), (0 if total == 0 else 1)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Lint spójności vaulta (czysto odczytowy).")
    parser.add_argument("--vault", default=".",
                         help="Ścieżka do vaulta (domyślnie: bieżący katalog).")
    parser.add_argument("--runtime-path", default=None,
                         help="Ścieżka do katalogu z run_vps (dla reguły R9, run_vps). "
                              "Jeśli brak, część R9 dot. run_vps zostanie pominięta bez błędu.")
    parser.add_argument("--json", action="store_true", help="Wypisz wynik jako JSON.")
    parser.add_argument(
        "--baseline", default=None,
        help="Ścieżka do baseline.json ze świadomie zaakceptowanymi znaleziskami "
             "(domyślnie: baseline.json obok lint.py). Nieistniejący plik = brak baseline, "
             "bez błędu.",
    )
    parser.add_argument(
        "--show-baselined", action="store_true",
        help="Dodaj do raportu sekcję z wyciszonymi (baseline) znaleziskami, żeby dało się "
             "je świadomie przejrzeć zamiast zapomnieć o nich na zawsze.",
    )
    args = parser.parse_args(argv)

    vault_root = Path(args.vault).expanduser().resolve()
    if not vault_root.is_dir():
        print(f"Ścieżka vaulta nie istnieje lub nie jest katalogiem: {vault_root}", file=sys.stderr)
        return 1

    runtime_path = None
    if args.runtime_path:
        candidate = Path(args.runtime_path).expanduser().resolve()
        if candidate.is_dir():
            runtime_path = candidate

    if args.baseline:
        baseline_path = Path(args.baseline).expanduser().resolve()
    else:
        baseline_path = Path(__file__).resolve().parent / "baseline.json"
    baseline = wczytaj_baseline(baseline_path)

    v, wyniki_surowe = uruchom_wszystko(vault_root, runtime_path)
    wyniki, wyciszone = podziel_na_aktywne_i_wyciszone(wyniki_surowe, baseline)

    if args.json:
        tekst, kod = raport_json(v, wyniki, wyciszone, args.show_baselined)
    else:
        tekst, kod = raport_tekstowy(v, wyniki, wyciszone, args.show_baselined)

    print(tekst)
    return kod


if __name__ == "__main__":
    sys.exit(main())
