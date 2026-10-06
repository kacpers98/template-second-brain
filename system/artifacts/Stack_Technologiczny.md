---
type: artifact
artifact_type: normative
title: "Stack Technologiczny"
owner_head: "[[knowledge]]"
# used_by: nadać przy powołaniu działu tech (w szablonie nie ma działu tech; do tego czasu artefakt czyta Właściciel i przewodnik)
used_by: []
inject: on_reference
scope: "Wiążące ramy techniczne: warstwa intencji Właściciela (nadrzędna) + minimalna warstwa techniczna (Obsidian + git + Claude Code) + lista możliwych rozszerzeń z ryzykami"
authority: binding
review_every: 90d
version: 1.0
created: 2026-09-05
updated: 2026-09-05
---
# Stack Technologiczny

# Cel dokumentu
Ramy techniczne systemu. Dokument ma DWIE warstwy o różnych właścicielach: **warstwę intencji** (definiuje Właściciel — zmienia się rzadko i tylko jego decyzją) i **warstwę techniczną** (stan startowy szablonu; gdy Właściciel powoła dział tech, jego kustoszem zostaje persona techniczna, która utrzymuje ją propozycjami przez `inbox/tech/` — akceptacja: Właściciel). Właściciel systemu nie musi być programistą: stack istnieje po to, żeby AGENCI budowali spójnie, a Właściciel zachował kontrolę na poziomie intencji, nie składni.

# Zasady wiążące

## Warstwa intencji Właściciela (nadrzędna)
1. **Koszty**: żadna nowa płatna usługa, subskrypcja ani zasób chmurowy bez jawnej zgody Właściciela; preferencja: darmowe i lokalne, dopóki skala nie wymusi inaczej.
2. **Bezpieczeństwo**: sekrety wyłącznie poza vaultem (plik środowiskowy poza repozytorium albo menedżer haseł) — nigdy w kodzie, vaulcie, repozytorium ani `outputs/`; rejestr NAZW sekretów prowadzi [[Rejestr_Sekretow]]. Nic nie jest wystawiane publicznie (porty, adresy, webhooki) bez jawnej zgody Właściciela.
3. **Human-in-the-loop**: agenci wykonują pracę, ale działania nieodwracalne lub skierowane na zewnątrz (wysyłka, publikacja, transakcja, usunięcie) zawsze czekają na akceptację Właściciela. W szablonie egzekwuje to polityka `.claude/settings.json` (deny) + przegląd diffu przez Właściciela + akt podpisu przez `narzedzia/akceptuj.py`.
4. **Prostota i utrzymywalność**: rozwiązanie, którego przepływu Właściciel nie jest w stanie zrozumieć na poziomie prostego schematu („co wchodzi → co się dzieje → co wychodzi"), jest złym rozwiązaniem niezależnie od elegancji kodu; mniej ruchomych części > sprytniej.
5. **AI jako dźwignia**: kod i konfigurację piszą agenci; rolą Właściciela jest specyfikacja, akceptacja i rozumienie przepływu — nie utrzymanie składni. Wybory techniczne mają maksymalizować zdolność agentów do samodzielnej, bezpiecznej pracy.
6. **Zmiany wynikają z użycia, nie z pomysłu**: każde rozszerzenie stacku musi wskazać konkretny, POWTARZAJĄCY SIĘ przebieg z `outputs/`, który bez rozszerzenia jest uciążliwy. „Fajnie by było" nie jest uzasadnieniem.

## Warstwa techniczna (stan startowy szablonu — minimalna)
7. **Obsidian** jako interfejs Właściciela do vaulta. Wtyczki: `dataview` (widoki w KOKPIT), `obsidian-git` (automatyczne commity — kopia i historia). Innych wtyczek szablon nie wymaga.
8. **git** jako kręgosłup: historia każdej zmiany, możliwość cofnięcia, kopia zapasowa (zdalne repozytorium PRYWATNE — {{UZUPEŁNIJ: czy i gdzie trzymasz zdalne repo}}). Właściciel nie musi znać komend — obsługuje je `obsidian-git` i [[przewodnik]] w sesji.
9. **Claude Code w sesji interaktywnej** uruchomiony w katalogu vaulta — JEDYNY runtime agentów w szablonie. Persony są wcielane w sesji (definicja wstrzykiwana przez [[router]]), Właściciel jest obecny przy każdym przebiegu. Uprawnienia zapisu: `.claude/settings.json`.
10. **Python 3.10+ (tylko biblioteka standardowa)** dla narzędzi w `narzedzia/` (lint, akceptacja, kontrola sanityzacji). Uruchamia je [[przewodnik]] lub Właściciel gotową komendą; żadnych dodatkowych pakietów do instalowania.

# Możliwe rozszerzenia (dopiero gdy system jest UŻYWANY)
Każde z poniższych jest opcją na później, nie elementem szablonu. Warunek wejścia: zasada 6 (dowód z użycia) + zgoda Właściciela + wpis w [[Rejestr_Sekretow]] dla każdego nowego sekretu.
- **Automatyzacje cykliczne** (brief lub zwiad uruchamiane bez obecności Właściciela, np. z harmonogramu na osobnej maszynie). Ryzyko: przebieg bez człowieka pisze do vaulta bez przeglądu diffu — wymaga osobnego mechanizmu odbioru wyników i osobnego rozstrzygnięcia, kto łączy zmiany przy konflikcie.
- **Kanał mobilny** (dostarczanie briefu do komunikatora lub maila). Ryzyko: kanał staje się drugim miejscem prawdy i kusi, żeby pisać „pod kanał" — [[Rytm_Przegladow]] zasada 4 (plik kanoniczny, kanał = projekcja) musi obowiązywać od pierwszego dnia.
- **Narzędzia zewnętrzne** (odczyt kalendarza, listy zadań, poczty przez integrację zamiast wklejania). Ryzyko: każda integracja to sekret do rotowania i nowa powierzchnia wycieku danych osobistych do wyników agentów — zaczynaj od trybu wyłącznie-odczyt i od zamkniętej listy źródeł.

# Kontekst i uzasadnienie
System-poprzednik rozrósł się do rozbudowanej infrastruktury (osobny serwer, automatyzacje, kilka kanałów, wiele integracji) i znaczna część czasu Właściciela szła na jej utrzymanie zamiast na użycie wiedzy. Wnioski (bez szczegółów — [[Lekcje_Poprzednika]]): warstwa intencji przetrwała bez zmian i okazała się najcenniejsza; warstwa techniczna zmieniała się co tydzień. Dlatego szablon startuje od minimum, które działa na jednym komputerze, i nazywa rozszerzenia wraz z ich ceną.

# Przykłady zastosowania
## Dobrze
Właściciel po sześciu tygodniach użycia zauważa w `outputs/ops/`, że brief tygodniowy powstaje regularnie, ale za każdym razem musi ręcznie wklejać kalendarz. Prosi przewodnika o propozycję integracji odczytu kalendarza. Propozycja idzie do `inbox/tech/` z: dowodem z użycia (6 przebiegów), trybem wyłącznie-odczyt, wpisem do [[Rejestr_Sekretow]] i jednym zdaniem ryzyka. Właściciel akceptuje.
## Źle
Agent w pierwszym tygodniu proponuje „od razu postawić serwer i automatyczne briefy o 7:00, bo tak będzie wygodniej". Naruszone: zasada 6 (brak dowodu z użycia), zasada 1 (koszt bez zgody), zasada 4 (przepływu, którego Właściciel jeszcze nie rozumie).

# Wyjątki i przypadki brzegowe
- Odstępstwo od warstwy technicznej (7–10): dozwolone z jawnym uzasadnieniem w wyniku („odstępstwo od stacku: powód") i zgodą Właściciela.
- Odstępstwo od warstwy intencji (1–6): nie istnieje ścieżka poza jawną zmianą tego dokumentu przez Właściciela.
- Konflikt między prostotą (4) a wymaganiem funkcjonalnym: eskalacja z dwoma wariantami (prostszy z ograniczeniami vs pełny ze złożonością) — wybiera Właściciel.

# Historia zmian
- 2026-09-05 (v1.0): wersja szablonu — wyprowadzona z działającego systemu-poprzednika; treść osobista i infrastrukturalna usunięta, struktura i zasady zachowane.
