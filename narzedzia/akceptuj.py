#!/usr/bin/env python3
"""
akceptuj — mechanizacja AKTU PODPISU.

Zamienia uważność przy akceptacji propozycji z inbox/ na krótki przegląd `git diff`.
Powód istnienia (z doświadczeń systemu-poprzednika): reguły PAMIĘCIOWE przy akcie
podpisu zawodziły — definicje przenoszone razem z aparatem propozycji, sekcje
niekanoniczne, appendiksy żyjące tygodniami w system/. Reguła wykonawcza zamiast
pamięciowej: to skrypt wykonuje podpis, Właściciel go AUTORYZUJE (mówi „akceptuję",
a zgoda na komendę w Claude Code jest podpisem).

CO ROBI (wg położenia w inbox/ i pola `type` we frontmatterze):
  inbox/knowledge/prop_*.md            type: note     -> wiki/<nazwa-bez-prefiksu>.md
  inbox/knowledge/prop_*.md            type: source   -> sources/<nazwa-bez-prefiksu>.md
  inbox/knowledge/tax_nowy_klaster_*   type: cluster  -> clusters/<title>.md   (całość; --nadpisz przy zmianie istniejącego)
  inbox/knowledge/moc_* / tax_diff_*   type: moc      -> moc/<title>.md        (całość; --nadpisz)
  inbox/agents/<n>.md                  type: agent    -> system/agents/<n>.md  (aparat: ODCIĘTY; --wiersz-mapy dopisuje wiersz access_map)
  inbox/agents/prop_head_*.md          type: head     -> system/heads/<name>.md (--nadpisz przy zmianie istniejącego)
  inbox/agents|ops/*.md                type: artifact -> system/artifacts/<title|nazwa>.md (--nadpisz przy wypełnianiu wzorca)
  inbox/skills/<s>/SKILL.md            type: skill    -> system/skills/<s>/SKILL.md (aparat: KONWERSJA na "Stan akceptacji")
  inbox/ops/prop_*.md (type: output)                  -> ODMOWA: listy zadań przenosi Właściciel na swoją listę zadań ręcznie.
  --archiwum PLIK                                     -> inbox/knowledge/archive/ (odrzucenie z zachowaniem śladu)

KROKI: (1) rozpoznanie typu i celu; (2) obsługa aparatu propozycji (separator `---`
+ "## Do akceptacji"); (3) normalizacja nagłówka powiązań do "## Powiązane";
(4) linki zwrotne z sekcji aparatu "## Linki zwrotne (propozycja)" — format wpisu:
`- cel: [[notatka-docelowa]] | wpis: - [[nazwa-nowej]] — uzasadnienie relacji.`;
(5) mv (git mv, fallback os.rename); (6) naprawa linków [[prop_<nazwa>]];
(7) opcjonalnie wiersz mapy; (8) CHECKLIST rzeczy nie do automatu; (9) lint.

CZEGO ŚWIADOMIE NIE ROBI: nie zmienia ZASAD access_map (tylko dopisuje wiersz tabeli
na wyraźną flagę), nie aktualizuje used_by artefaktów, nie tworzy sekcji "## Powiązane"
w cudzych notatkach, nie dotyka raw/.

Użycie:
    python3 narzedzia/akceptuj.py --vault . [--dry-run] [--nadpisz] [--wiersz-mapy] [--archiwum] [--bez-lintu] PLIK [PLIK...]
Kody wyjścia: 0 = akceptacja + lint czysto; 1 = odmowa/błąd; 2 = przeniesione, ale lint
zgłosił znaleziska.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

SEP_NAGLOWEK_RE = re.compile(r"(?m)^## Do akceptacji\b.*$")
SEP_STRZALKA = "> **⬇ PONIŻEJ TEJ LINII"
POWIAZANE_KANON = "## Powiązane"
POWIAZANE_WARIANTY_RE = re.compile(
    r"(?m)^##\s+(Powi[ąa]zane(\s+(Strony|notatki|linki))?|Powi[ąa]zania z vaultem)\s*$", re.IGNORECASE
)
LINK_ZWROTNY_RE = re.compile(
    r"(?m)^-\s*cel:\s*\[\[([^\]]+)\]\]\s*\|\s*wpis:\s*(- \[\[[^\]]+\]\][^\n]*)$"
)
MAKS_DLUGOSC_LINII = 300  # limit wyjątku 3a — skrypt trzyma ten sam kontrakt


def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def czytaj_fm(text: str) -> dict:
    """Minimalny odczyt skalarów frontmattera (bez PyYAML)."""
    if not text.startswith("---"):
        return {}
    koniec = text.find("\n---", 3)
    if koniec == -1:
        return {}
    fm = {}
    for linia in text[3:koniec].splitlines():
        m = re.match(r"^([\w-]+):\s*(.*?)\s*$", linia)
        if m:
            wart = m.group(2)
            if len(wart) >= 2 and wart[0] == wart[-1] and wart[0] in "\"'":
                wart = wart[1:-1]
            fm[m.group(1)] = wart
    return fm


def znajdz_aparat(text: str) -> int | None:
    kandydaci = []
    ms = list(SEP_NAGLOWEK_RE.finditer(text))
    if ms:
        kandydaci.append(ms[-1].start())
    idx = text.rfind(SEP_STRZALKA)
    if idx != -1:
        kandydaci.append(idx)
    if not kandydaci:
        return None
    cel = min(kandydaci)
    przed = text[:cel]
    m = re.search(r"\n---\n\s*\Z", przed)
    if not m:
        return None
    return m.start()


def wyciagnij_linki_zwrotne(aparat: str) -> list[tuple[str, str]]:
    m = re.search(r"(?m)^##\s+Linki zwrotne\b.*$", aparat)
    if not m:
        return []
    blok = aparat[m.end():]
    nastepny = re.search(r"(?m)^## ", blok)
    if nastepny:
        blok = blok[: nastepny.start()]
    return [(nfc(c.strip()), w.strip()) for c, w in LINK_ZWROTNY_RE.findall(blok)]


def dopisz_link_zwrotny(vault: Path, cel: str, wpis: str, dry: bool) -> str:
    if not re.match(r"^- \[\[[^\]]+\]\] — .+\.$", wpis):
        return f"POMINIĘTY (format wpisu niezgodny z kontraktem 3a): {wpis[:60]}"
    if len(wpis) > MAKS_DLUGOSC_LINII:
        return f"POMINIĘTY (linia > {MAKS_DLUGOSC_LINII} zn.): {wpis[:60]}"
    sciezka = None
    for katalog in ("wiki", "sources"):
        for p in (vault / katalog).glob("*.md"):
            if nfc(p.stem) == cel:
                sciezka = p
                break
        if sciezka:
            break
    if sciezka is None:
        return f"POMINIĘTY (cel [[{cel}]] nie istnieje w wiki/ ani sources/)"
    text = sciezka.read_text(encoding="utf-8")
    m = re.search(r"(?m)^## Powiązane\s*$", text)
    if not m:
        return f"POMINIĘTY (cel [[{cel}]] bez sekcji '## Powiązane' — propozycja przez inbox/)"
    if wpis in text:
        return f"POMINIĘTY (wpis już istnieje w [[{cel}]])"
    blok_start = m.end()
    nastepny = re.search(r"(?m)^## ", text[blok_start:])
    blok_koniec = blok_start + (nastepny.start() if nastepny else len(text) - blok_start)
    if nastepny:
        nowy = text[:blok_koniec].rstrip() + "\n" + wpis + "\n\n" + text[blok_koniec:].lstrip("\n")
    else:
        nowy = text[:blok_koniec].rstrip() + "\n" + wpis + "\n"
    if not dry:
        sciezka.write_text(nowy, encoding="utf-8")
    return f"DOPISANY do [[{cel}]]: {wpis}"


def normalizuj_powiazane(text: str) -> tuple[str, bool]:
    zmienione = False

    def zamien(m):
        nonlocal zmienione
        if m.group(0).strip() != POWIAZANE_KANON:
            zmienione = True
        return POWIAZANE_KANON

    return POWIAZANE_WARIANTY_RE.sub(zamien, text), zmienione


def konwertuj_aparat_skilla(text: str) -> tuple[str, bool]:
    ms = list(re.finditer(r"(?m)^(#+) Do akceptacji\b(.*)$", text))
    if not ms:
        return text, False
    m = ms[-1]
    nowy = f"{m.group(1)} Stan akceptacji{m.group(2)}"
    text = text[: m.start()] + nowy + text[m.end():]
    # separator `---` bezpośrednio nad skonwertowaną sekcją nie jest już potrzebny
    text = re.sub(r"\n---\n(\s*)(#+ Stan akceptacji)", r"\n\1\2", text, count=1)
    return text, True


def git_mv(vault: Path, zrodlo: Path, cel: Path, dry: bool) -> None:
    if dry:
        return
    cel.parent.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(
            ["git", "-C", str(vault), "--no-optional-locks", "mv", "-f",
             str(zrodlo.relative_to(vault)), str(cel.relative_to(vault))],
            check=True, capture_output=True, text=True,
        )
    except Exception:
        zrodlo.replace(cel)


def odetnij_uzasadnienie(text: str) -> tuple[str, bool]:
    m = re.search(r"(?m)^## Uzasadnienie propozycji\s*$", text)
    if not m:
        return text, False
    if re.search(r"(?m)^## ", text[m.end():]):
        return text, False
    return text[:m.start()].rstrip() + "\n", True


def napraw_linki_prop(vault: Path, stara: str, nowa: str, dry: bool) -> list[str]:
    naprawione = []
    wzor = re.compile(r"\[\[" + re.escape(stara) + r"(\]\]|\|)")
    for katalog in ("wiki", "sources", "inbox/knowledge"):
        base = vault / katalog
        if not base.is_dir():
            continue
        for p in sorted(base.glob("*.md")):
            text = p.read_text(encoding="utf-8")
            if not wzor.search(text):
                continue
            if not dry:
                p.write_text(wzor.sub(lambda m: "[[" + nowa + m.group(1), text), encoding="utf-8")
            naprawione.append(p.relative_to(vault).as_posix())
    return naprawione


def dopisz_wiersz_mapy(vault: Path, plik_wiersza: Path, dry: bool) -> str:
    """Dopisuje JEDEN wiersz tabeli do access_map.md, na końcu tabeli (przed
    '# Rejestr zmian'). Wiersz musi zaczynać się od '| [[' i mieć 7 kolumn."""
    if not plik_wiersza.is_file():
        return f"POMINIĘTY (brak pliku wiersza: {plik_wiersza.name})"
    wiersze = [l.strip() for l in plik_wiersza.read_text(encoding="utf-8").splitlines()
               if l.strip().startswith("| [[")]
    if len(wiersze) != 1:
        return f"POMINIĘTY ({plik_wiersza.name} ma {len(wiersze)} wierszy tabeli, oczekiwano 1)"
    wiersz = wiersze[0]
    if wiersz.count("|") != 8:
        return "POMINIĘTY (wiersz nie ma 7 kolumn: Agent | Head | Klastry | Odczyt | Zapis | Web | MCP)"
    mapa = vault / "system" / "access_map.md"
    text = mapa.read_text(encoding="utf-8")
    if wiersz.split("|")[1].strip() in text:
        return "POMINIĘTY (persona ma już wiersz w mapie)"
    linie = text.split("\n")
    ostatni = max(i for i, l in enumerate(linie) if l.startswith("| [["))
    linie.insert(ostatni + 1, wiersz)
    if not dry:
        mapa.write_text("\n".join(linie), encoding="utf-8")
        plik_wiersza.unlink()
    return f"DOPISANY do access_map: {wiersz[:70]}…  (pamiętaj: wpis w '# Rejestr zmian' mapy — ręcznie, jedno zdanie)"


def akceptuj_plik(vault: Path, plik: Path, dry: bool, nadpisz: bool, wiersz_mapy: bool) -> tuple[bool, list[str]]:
    raport: list[str] = []
    rel = plik.relative_to(vault).as_posix()
    text = plik.read_text(encoding="utf-8")
    fm = czytaj_fm(text)
    typ = fm.get("type")
    czesci = rel.split("/")

    if czesci[0] != "inbox":
        return False, [f"ODMOWA: {rel} nie leży w inbox/ — akt podpisu dotyczy propozycji."]

    linki_zwrotne: list[tuple[str, str]] = []
    stara_nazwa = plik.stem
    strefa = czesci[1]

    def tytul_lub_nazwa(prefiksy: str) -> str:
        t = fm.get("title") or re.sub(prefiksy, "", plik.stem)
        return t

    if strefa == "skills":
        if typ != "skill" or plik.name != "SKILL.md":
            return False, [f"ODMOWA: {rel} — w inbox/skills/ akceptuję wyłącznie SKILL.md o type: skill (jest: {typ})."]
        cel = vault / "system" / "skills" / plik.parent.name / "SKILL.md"
        text, skonw = konwertuj_aparat_skilla(text)
        raport.append("aparat: " + ("skonwertowany na 'Stan akceptacji'" if skonw else "brak sekcji decyzji (nic do konwersji)"))
        for pomocniczy in sorted(plik.parent.iterdir()):
            if pomocniczy.is_file() and pomocniczy.name != "SKILL.md":
                git_mv(vault, pomocniczy, cel.parent / pomocniczy.name, dry)
                raport.append(f"plik pomocniczy: {pomocniczy.name} -> {(cel.parent / pomocniczy.name).relative_to(vault).as_posix()}" + (" [DRY-RUN]" if dry else ""))
    elif strefa == "agents" and typ == "agent":
        cel = vault / "system" / "agents" / plik.name
        idx = znajdz_aparat(text)
        if idx is not None:
            linki_zwrotne = wyciagnij_linki_zwrotne(text[idx:])
            text = text[:idx].rstrip() + "\n"
            raport.append("aparat: ODCIĘTY (definicja czyta cały plik jako normę)")
        elif SEP_NAGLOWEK_RE.search(text):
            return False, [f"ODMOWA: {rel} ma '## Do akceptacji' bez separatora `---` — nie zgaduję miejsca cięcia; popraw propozycję."]
        else:
            raport.append("aparat: brak (propozycja bez appendiksu)")
    elif strefa == "agents" and typ == "head":
        nazwa = fm.get("name") or re.sub(r"^prop_head_", "", plik.stem)
        cel = vault / "system" / "heads" / f"{nazwa}.md"
        if not dry:
            (vault / "outputs" / nazwa).mkdir(parents=True, exist_ok=True)
            (vault / "outputs" / nazwa / ".gitkeep").touch()
        raport.append(f"head: cel {cel.relative_to(vault).as_posix()}; katalog outputs/{nazwa}/ zapewniony")
    elif strefa in ("agents", "ops") and typ == "artifact":
        nazwa = re.sub(r"^(artefakt_|prop_)", "", plik.stem)
        cel = vault / "system" / "artifacts" / f"{nazwa}.md"
        raport.append(f"artefakt: cel {cel.relative_to(vault).as_posix()}")
    elif strefa == "knowledge" and typ in ("note", "source"):
        nowa_nazwa = re.sub(r"^prop_", "", plik.name)
        cel = vault / ("wiki" if typ == "note" else "sources") / nowa_nazwa
        idx = znajdz_aparat(text)
        if idx is not None:
            linki_zwrotne = wyciagnij_linki_zwrotne(text[idx:])
            text = text[:idx].rstrip() + "\n"
            raport.append("aparat: ODCIĘTY")
        text, uz = odetnij_uzasadnienie(text)
        if uz:
            raport.append("aparat: sekcja '## Uzasadnienie propozycji' ODCIĘTA")
        text, znorm = normalizuj_powiazane(text)
        if znorm:
            raport.append(f"sekcja powiązań: znormalizowana do '{POWIAZANE_KANON}'")
    elif strefa == "knowledge" and typ == "cluster":
        cel = vault / "clusters" / f"{tytul_lub_nazwa(r'^(tax_nowy_klaster_|prop_)')}.md"
        raport.append(f"klaster: cel {cel.relative_to(vault).as_posix()} (całość pliku)")
    elif strefa == "knowledge" and typ == "moc":
        cel = vault / "moc" / f"{tytul_lub_nazwa(r'^(moc_|tax_diff_|prop_)')}.md"
        raport.append(f"MOC: cel {cel.relative_to(vault).as_posix()} (całość pliku)")
    elif strefa == "ops":
        return False, [f"ODMOWA: {rel} (type: {typ}) — propozycje list zadań/planów z inbox/ops/ przenosi Właściciel na SWOJĄ listę zadań ręcznie; akceptuj.py przenosi z inbox/ops/ wyłącznie type: artifact."]
    else:
        return False, [f"ODMOWA: {rel} (type: {typ}) — nieznana para położenie×typ; akceptuj ręcznie albo rozszerz skrypt świadomie."]

    if cel.exists() and not nadpisz:
        return False, [f"ODMOWA: cel {cel.relative_to(vault).as_posix()} już istnieje — nie nadpisuję bez flagi --nadpisz (świadoma decyzja Właściciela)."]

    if not dry:
        plik.write_text(text, encoding="utf-8")
    git_mv(vault, plik, cel, dry)
    raport.append(f"mv: {rel} -> {cel.relative_to(vault).as_posix()}" + (" [DRY-RUN]" if dry else ""))

    for celnazwa, wpis in linki_zwrotne:
        raport.append("link zwrotny: " + dopisz_link_zwrotny(vault, celnazwa, wpis, dry))
    if strefa == "knowledge" and typ in ("note", "source") and not linki_zwrotne:
        raport.append("UWAGA: propozycja bez sekcji 'Linki zwrotne' — jeśli ingest szedł poza wyjątkiem 3a, dopisz linki zwrotne przez inbox/ (inaczej R6: sierota).")

    if stara_nazwa.startswith("prop_"):
        napr = napraw_linki_prop(vault, stara_nazwa, cel.stem, dry)
        if napr:
            raport.append(f"linki [[{stara_nazwa}]] -> [[{cel.stem}]] naprawione w: " + ", ".join(napr))

    if typ == "agent":
        pw = plik.parent / f"{plik.stem}.wiersz_mapy.md"
        if wiersz_mapy:
            raport.append("wiersz mapy: " + dopisz_wiersz_mapy(vault, pw, dry))
        else:
            raport.append("CHECKLIST: wiersz w access_map — uruchom ponownie z --wiersz-mapy (jeśli rekruter przygotował "
                          f"{pw.name}) albo dopisz ręcznie; lint R11/R12 zaraz to sprawdzi.")
    if typ == "artifact":
        raport.append("CHECKLIST: used_by artefaktu i kolumna Odczyt person, które go dostają — RĘCZNIE (R2 sprawdzi symetrię).")
    if typ == "cluster":
        raport.append("CHECKLIST: akapit klastra w MOC (Mapa klastrów) z tą samą listą tagów — osobna propozycja type: moc (lint sprawdzi lustro).")
    return True, raport


def archiwizuj(vault: Path, plik: Path, dry: bool) -> tuple[bool, list[str]]:
    rel = plik.relative_to(vault).as_posix()
    if not rel.startswith("inbox/"):
        return False, [f"ODMOWA: {rel} nie leży w inbox/."]
    cel = vault / "inbox" / "knowledge" / "archive" / plik.name
    git_mv(vault, plik, cel, dry)
    return True, [f"ARCHIWUM (odrzucenie z zachowaniem śladu): {rel} -> {cel.relative_to(vault).as_posix()}" + (" [DRY-RUN]" if dry else "")]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Akt podpisu: akceptacja propozycji z inbox/.")
    ap.add_argument("pliki", nargs="+", help="Ścieżki propozycji (względem vaulta albo absolutne).")
    ap.add_argument("--vault", default=".")
    ap.add_argument("--dry-run", action="store_true", help="Pokaż plan, niczego nie zmieniaj.")
    ap.add_argument("--nadpisz", action="store_true", help="Pozwól nadpisać istniejący plik docelowy (świadomie).")
    ap.add_argument("--wiersz-mapy", action="store_true", help="Przy personie: dopisz wiersz z <nazwa>.wiersz_mapy.md do access_map.")
    ap.add_argument("--archiwum", action="store_true", help="Zamiast akceptować — przenieś do inbox/knowledge/archive/ (odrzucenie).")
    ap.add_argument("--bez-lintu", action="store_true", help="Nie uruchamiaj lintu na końcu.")
    args = ap.parse_args(argv)

    vault = Path(args.vault).expanduser().resolve()
    if not (vault / "system" / "access_map.md").is_file():
        print(f"To nie wygląda na vault (brak system/access_map.md): {vault}", file=sys.stderr)
        return 1

    ok_wszystkie = True
    for surowa in args.pliki:
        p = Path(surowa)
        if not p.is_absolute():
            p = vault / p
        p = p.resolve()
        if not p.is_file():
            print(f"[BŁĄD] nie ma pliku: {surowa}")
            ok_wszystkie = False
            continue
        try:
            if args.archiwum:
                ok, raport = archiwizuj(vault, p, args.dry_run)
            else:
                ok, raport = akceptuj_plik(vault, p, args.dry_run, args.nadpisz, args.wiersz_mapy)
        except Exception as e:  # noqa: BLE001
            ok, raport = False, [f"BŁĄD: {e}"]
        print(f"== {surowa} ==")
        for linia in raport:
            print("  " + linia)
        ok_wszystkie = ok_wszystkie and ok

    if not ok_wszystkie:
        return 1
    if args.dry_run or args.bez_lintu or args.archiwum:
        return 0
    lint_py = Path(__file__).resolve().parent / "lint.py"
    if lint_py.is_file():
        wynik = subprocess.run([sys.executable, str(lint_py), "--vault", str(vault)], capture_output=True, text=True)
        print(wynik.stdout.strip())
        return 0 if wynik.returncode == 0 else 2
    print("(lint.py nieznaleziony — uruchom ręcznie)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
