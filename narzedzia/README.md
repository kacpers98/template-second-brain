# narzedzia/ — trzy skrypty, które uruchamia za Ciebie przewodnik

Wszystkie: Python 3.10+, wyłącznie biblioteka standardowa (bez instalowania czegokolwiek), uruchamiane z katalogu vaulta. Żaden nie wymaga sieci. Persony NIE mają prawa ich edytować (`.claude/settings.json`).

| Skrypt | Co robi | Kiedy | Komenda |
|---|---|---|---|
| `akceptuj.py` | **Akt podpisu.** Przenosi propozycję z `inbox/` do właściwego miejsca (wiki/, sources/, clusters/, moc/, system/agents/, heads/, artifacts/, skills/), odcina lub konwertuje sekcję „Do akceptacji", dopisuje linki zwrotne, naprawia linki `[[prop_…]]`, opcjonalnie dopisuje wiersz do `access_map`, na końcu uruchamia lint. | Gdy mówisz „akceptuję" — przewodnik/router uruchamia go, Claude Code pyta o zgodę, Twoje „tak" jest podpisem. | `python3 narzedzia/akceptuj.py --vault . [--dry-run] [--nadpisz] [--wiersz-mapy] [--archiwum] PLIK…` |
| `lint.py` | **Kontrola spójności.** 13 reguł pilnujących par (persona ↔ mapa dostępów, skill ↔ zasięg persony, artefakt ↔ used_by, martwe linki, sieroty, liczniki logu, warstwa deny). Czysto odczytowy. | Po każdej sesji, która zmieniła coś w `system/`; kwartalnie; automatycznie po każdej akceptacji. | `python3 narzedzia/lint.py --vault . [--show-baselined] [--json]` |
| `sanityzacja_check.py` | **Bramka przed udostępnieniem.** Szuka ścieżek domowych, e-maili, tokenów, IP, telefonów i słów z Twojej listy (imiona, klienci). | Zanim komukolwiek dasz kopię vaulta; kwartalnie. | `python3 narzedzia/sanityzacja_check.py --vault . --plik-slow ~/moje_slowa_wrazliwe.txt` |

**Uwaga do `sanityzacja_check.py`:** bez listy słów wykrywa WYŁĄCZNIE wzorce techniczne (ścieżki, e-maile, tokeny, IP, telefony). Gołe imię, nazwisko czy nazwa firmy NIE zostaną złapane — dlatego przed każdym udostępnieniem uruchamiaj go z `--plik-slow` zawierającym Twoje imię, nazwisko, nazwy klientów i pracodawcy. Plik z listą trzymaj poza vaultem.

`baseline.json` — lista znalezisk lintu zaakceptowanych świadomie (z powodem i datą). Nie dopisuj tu niczego „żeby było zielone"; każdy wpis to decyzja. Przegląd kwartalny: `lint.py --show-baselined`.

Pochodzenie: `akceptuj.py` i `lint.py` są adaptacją narzędzi systemu-poprzednika (opisanego w `system/artifacts/Lekcje_Poprzednika.md`); usunięto z nich zależności od jego infrastruktury. `sanityzacja_check.py` jest nowy.
