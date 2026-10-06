#!/usr/bin/env python3
"""
sanityzacja_check — bramka „czy ten vault nadaje się do oddania komuś innemu".

Skanuje pliki tekstowe vaulta pod kątem śladów, które NIE powinny opuścić komputera
Właściciela: ścieżek domowych, adresów e-mail, tokenów/kluczy, adresów IP, numerów
telefonów oraz słów z listy własnej (imiona, nazwy klientów, pracodawców).
Czysto odczytowy. Wynik: lista trafień z plikiem i linią; kod 0 = czysto, 1 = są trafienia.

Użycie (z katalogu vaulta):
    python3 narzedzia/sanityzacja_check.py [--vault .] [--slowa slowo1,slowo2,...] [--plik-slow PLIK]
`--plik-slow`: plik tekstowy, jedno słowo/fraza na linię (np. imiona i nazwy firm Właściciela) —
trzymaj go POZA vaultem, bo sam jest listą rzeczy wrażliwych.

Kiedy uruchamiać: przed każdym udostępnieniem vaulta (zip, repozytorium, kopia dla kogoś),
oraz kwartalnie — ślady wchodzą po cichu (wklejony alert, log z pełną ścieżką).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

WYKLUCZONE = {".git", ".obsidian", "narzedzia", "_to_delete"}
ROZSZERZENIA = {".md", ".json", ".txt", ".yaml", ".yml", ".css", ".py", ".sh"}

WZORCE = {
    "ścieżka domowa": re.compile(r"(/Users/[A-Za-z0-9._-]+|/home/[A-Za-z0-9._-]+|C:\\Users\\[A-Za-z0-9._-]+)"),
    "e-mail": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    "adres IP": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    "token / klucz": re.compile(r"(sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{20,}|xox[abp]-[A-Za-z0-9-]{10,}|AKIA[0-9A-Z]{16}|eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,})"),
    "telefon": re.compile(r"(?<![\d/.-])(\+?48[ -]?)?\d{3}[ -]?\d{3}[ -]?\d{3}(?![\d/.-])"),
    "sekret w przypisaniu": re.compile(r"(?i)(api[_-]?key|secret|password|hasło|haslo|token)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}"),
}
# wyjątki: przykłady w dokumentacji, które celowo wyglądają jak wzorzec
WYJATKI = ("example.org", "example.com", "RRRR-MM-DD", "127.0.0.1", "0.0.0.0")


def skanuj(vault: Path, slowa: list[str]) -> list[tuple[str, int, str, str]]:
    trafienia = []
    slowa_re = [re.compile(re.escape(s), re.IGNORECASE) for s in slowa if s.strip()]
    for p in sorted(vault.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in ROZSZERZENIA:
            continue
        if any(part in WYKLUCZONE for part in p.relative_to(vault).parts):
            continue
        try:
            linie = p.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        rel = p.relative_to(vault).as_posix()
        for nr, linia in enumerate(linie, 1):
            if any(w in linia for w in WYJATKI):
                continue
            for nazwa, wz in WZORCE.items():
                m = wz.search(linia)
                if m:
                    trafienia.append((rel, nr, nazwa, m.group(0)))
            for wz in slowa_re:
                m = wz.search(linia)
                if m:
                    trafienia.append((rel, nr, "słowo z listy własnej", m.group(0)))
    return trafienia


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Bramka sanityzacji vaulta przed udostępnieniem.")
    ap.add_argument("--vault", default=".")
    ap.add_argument("--slowa", default="", help="Słowa/frazy rozdzielone przecinkami.")
    ap.add_argument("--plik-slow", default=None, help="Plik z listą słów (jedno na linię), trzymany poza vaultem.")
    args = ap.parse_args(argv)
    vault = Path(args.vault).expanduser().resolve()
    slowa = [s for s in args.slowa.split(",") if s.strip()]
    if args.plik_slow:
        pl = Path(args.plik_slow).expanduser()
        if pl.is_file():
            slowa += [l.strip() for l in pl.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
    tr = skanuj(vault, slowa)
    if not tr:
        print("sanityzacja: czysto — brak śladów ścieżek, e-maili, tokenów, IP, telefonów" + (" ani słów z listy własnej" if slowa else "") + ".")
        return 0
    print(f"sanityzacja: {len(tr)} trafień — przejrzyj każde, zanim udostępnisz vault:")
    for rel, nr, nazwa, frag in tr:
        print(f"  - {rel}:{nr}  [{nazwa}]  {frag[:60]}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
