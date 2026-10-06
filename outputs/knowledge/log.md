---
type: log
title: "Log operacji na wiedzy"
owner: "[[knowledge]]"
scope: "Append-only rejestr operacji działu knowledge: ingesty, audyty, zmiany taksonomii, przebiegi zwiadu."
append_only: true
version: 1.0
created: 2026-09-05
updated: 2026-09-05
---
# Log operacji na wiedzy

Format wpisu (grepowalne prefiksy): `## [RRRR-MM-DD] typ | Tytuł`
Typy: `ingest` | `lint` | `taxonomy` | `zwiad` | `audyt` | `setup` | `korekta` | `decyzja`

Wpis ingestu ma stałe podpola (jedna linia każde; „brak" jest poprawną wartością): `source` (link do notatki źródłowej + paginacja, którą cytujesz) · `taksonomia` (klaster / tagi; „warunkowo" gdy tag czeka na podpis) · `propozycje (N)` (ścieżki w inbox/knowledge/) · `linki zwrotne` (pliki wiki/, do których dopisano linię; wynik `git diff wiki/` = N plików, N wstawień, 0 usunięć) · `sprzeczności` ([CONTRADICTION] + z czym) · `pominięcia świadome` · `luki taksonomiczne` · `odmowy polityki zapisu`.

Dopisuj narzędziem Edit z kotwicą na końcu pliku (nigdy Write całego pliku — ryzyko cichej amputacji).

---

## [2026-09-05] setup | Vault utworzony z szablonu
- stan: 0 notatek wiki, 0 źródeł, 2 klastry przykładowe ([[Wydajność i Skupienie]], [[Przywództwo i Decyzje]]), 5 warstw MOC do potwierdzenia lub przemianowania w etapie 3 wdrożenia
- następny wpis powstaje przy pierwszym ingeście (etap 4) — do tego czasu ten log jest pusty i TAK MA BYĆ
