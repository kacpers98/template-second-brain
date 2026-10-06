---
name: ops_transkrypcja_na_plan
aliases: ["ops_transkrypcja_na_plan"]              # plik nazywa się SKILL.md — alias pozwala linkować [[ops_transkrypcja_na_plan]] w Obsidianie (lint R8)
description: "Procedura zamiany transkrypcji spotkania (plik w raw/transkrypcje/) na plan działania: każde ustalenie trafia do DOKŁADNIE jednej z czterech kategorii (decyzja > next action > pytanie otwarte > parking lot), niejasny właściciel lub termin oznaczony `[do potwierdzenia]` zamiast zgadywany, next actions jako osobna propozycja w inbox/ops/ — lista gotowa do przeniesienia na listę zadań Właściciela, nigdy bezpośredni wpis do żadnego źródła. Prefiks `[Z]` oznacza zobowiązanie zewnętrzne; przy niepewności BEZ prefiksu. Używaj przy KAŻDYM zleceniu „przetwórz transkrypcję X na plan działania", „co ustaliliśmy na spotkaniu Y", „zrób next actions z tej rozmowy". NIE jest tym skillem: brief (→ ops_brief), ingest wiedzy z raw/ (→ knowledge_ingest), transkrybowanie audio."
# --- pola własne ---
type: skill
skill_type: procedure
used_by:
  - "[[asystent]]"
depends_on_artifacts:
  - "[[Rejestr_Cyklow]]"           # konwencja [Z] (zobowiązanie zewnętrzne) używana w kroku 5; cykle wykryte w transkrypcji → propozycja do rejestru
wymagany_odczyt:                    # ŚCIEŻKI wymagane przez procedurę
  - raw/transkrypcje/               # krok 1 — odczyt transkrypcji źródłowej (tylko odczyt; raw/ jest niezmienne)
  - outputs/ops/                    # „Wymagane wejście" — wybór najnowszej NIEPRZETWORZONEJ transkrypcji (porównanie z istniejącymi plan_*.md)
# Świadomie NIEobecne: lista zadań Właściciela — nie jest ścieżką vaulta; propozycja trafia do inbox/ops/, przeniesienie robi Właściciel ręcznie.
inputs: "TWARDE: ścieżka/nazwa pliku tekstowego w raw/transkrypcje/ wskazana w zleceniu LUB brak wskazania → najnowsza nieprzetworzona (gdy nie da się ustalić jednoznacznie — dopytaj, nie zgaduj). Plik audio/wideo nie jest wejściem — zgłoś i zatrzymaj się."
output_format: "dwa pliki: plan działania outputs/ops/plan_[nazwa]_RRRR-MM-DD.md (sekcje 1–6) + propozycja next actions inbox/ops/prop_[nazwa]_RRRR-MM-DD.md jako lista pozycji do przeniesienia na listę zadań Właściciela (tytuł z ew. prefiksem [Z] + termin + uwagi)"
version: 1.0
updated: 2026-09-05
---
# Kiedy używać
Zlecenie przetworzenia konkretnej transkrypcji spotkania lub rozmowy na plan działania — wskazanej wprost albo domyślnie najnowszej nieprzetworzonej w `raw/transkrypcje/`. Transkrypcja spotkania to operacyjny wsad do zadań i cykli, nie wiedza do syntezy w `wiki/`.

NIE jest tym skillem (test rozróżniający: czym jest wejście i dokąd idzie wynik):
- cykliczny brief (→ [[ops_brief]]) — wejściem jest data i stan bieżący, nie plik rozmowy;
- ingest źródła wiedzy (książka, artykuł, dokumentacja) leżącego w `raw/` (→ [[katalizator]], [[knowledge_ingest]]) — wynik idzie do `sources/` i `wiki/`, nie do zadań; test: czy z tego materiału ma powstać NOTATKA WIEDZY czy LISTA DZIAŁAŃ;
- klasyfikacja luźnych notatek wg GTD niepochodzących z transkrypcji — prostsza zdolność własna [[asystent]]a poza tym skillem;
- transkrybowanie nagrania — plik audio/wideo nie jest wejściem; zgłoś i zatrzymaj się.

# Wymagane wejście
- Ścieżka/nazwa pliku w `raw/transkrypcje/`. Bez wskazania — wybierz NAJNOWSZĄ NIEPRZETWORZONĄ: porównaj pliki w `raw/transkrypcje/` z planami w `outputs/ops/plan_*.md` (transkrypcja jest przetworzona, jeśli istnieje plan cytujący ją w `linked_sources`). Gdy nie da się tego ustalić jednoznacznie (nazwy niejasne, brak powiązania) — dopytaj Właściciela, nie zgaduj.
- Transkrypcja musi być tekstem czytelnym wprost. Skąd pochodzi (dyktafon, notatki ręczne, narzędzie do transkrypcji) — bez znaczenia dla procedury; sposób jej wytwarzania: {{UZUPEŁNIJ: jak Właściciel wytwarza transkrypcje i wrzuca je do raw/transkrypcje/}}.
- Z [[Rejestr_Cyklow]] czytasz konwencję prefiksu `[Z]` oraz istniejące cykle (żeby nie proponować cyklu, który już tam jest).

# Podstawa metodyczna (Grounding)
- {{UZUPEŁNIJ: notatka o pięciu etapach przepływu pracy GTD (etap clarify)}} → krok 2 — każda pozycja przechodzi test „czy wymaga działania i jakiego", z którego wynika czwórpodział decyzja / next action / pytanie / parking lot.
- {{UZUPEŁNIJ: notatka o kontekstowych listach następnych działań (GTD)}} → krok 5 — next action jako NAJBLIŻSZA fizyczna czynność z czasownikiem; format pozycji propozycji stosuje tę definicję wprost.
- {{UZUPEŁNIJ: notatka o naturalnym planowaniu projektu (GTD)}} → kroki 2 i 5 — rozpoznanie, że ustalenie jest projektem (wiele kroków) albo cyklem, nie pojedynczym działaniem — stąd osobne oznaczenia.

Vault startowy nie zawiera tych notatek; do czasu ingestu kroki wykonuj z oznaczeniem [wiedza własna modelu]. Kandydaci do ingestu należą do klastra [[Wydajność i Skupienie]]. Podstawa normatywna prefiksu `[Z]` i cykli: [[Rejestr_Cyklow]].

# Procedura
1. **Przeczytaj CAŁĄ transkrypcję** od początku do końca — nie fragment, nie pierwsze akapity jako proxy całości. Zidentyfikuj uczestników (kto mówi / kto jest wymieniony) i kontekst (temat, cel, powiązana inicjatywa, jeśli wynika z rozmowy).
2. **Wyekstrahuj KAŻDE ustalenie i przypisz je do DOKŁADNIE JEDNEJ z czterech kategorii.** Gdy pasuje do dwóch — wybierz bardziej konkretną wg priorytetu: **decyzja > next action > pytanie otwarte > parking lot**.
   - **Decyzja podjęta** — coś ostatecznie postanowione w trakcie spotkania (nie propozycja, nie „może warto"; realne zamknięcie wątku).
   - **Next action** — czasownik + kontekst + właściciel + termin, JEŚLI termin faktycznie padł (nie padł → pole puste, nie wymyślaj).
   - **Pytanie otwarte** — zasygnalizowane jako niejasne/nierozstrzygnięte, z właścicielem odpowiedzi, jeśli wynika z rozmowy.
   - **Parking lot** — temat poboczny, świadomie odłożony, bez przypisanego działania.
   Grounding: {{UZUPEŁNIJ: notatka o etapie clarify}} [wiedza własna modelu do czasu ingestu].
3. **Niejasne przypisania → `[do potwierdzenia]`, nigdy domysł.** Jeśli właściciel next action lub pytania nie jest jednoznaczny z transkrypcji („ktoś powinien to sprawdzić"; przypisanie wynikałoby z Twojej interpretacji tonu, nie z wypowiedzianego zdania) — wpisz `[do potwierdzenia]` w polu właściciela. To samo dla terminów pośrednich („niedługo", „na następnym spotkaniu") — pole puste + `[do potwierdzenia: dokładny termin]`; nie przekładaj przybliżenia na datę.
4. **Złóż PLAN DZIAŁANIA** i zapisz do `outputs/ops/plan_[nazwa-transkrypcji]_RRRR-MM-DD.md` (sekcje w „Szablonie wyniku"), ze zbiorczą listą WSZYSTKICH `[do potwierdzenia]` na końcu — Właściciel ma widzieć wszystkie niepewności w jednym miejscu, nie rozproszone po sekcjach.
5. **Dla KAŻDEJ pozycji typu next action** (wyłącznie tej kategorii — decyzje, pytania i parking lot NIE trafiają do zadań) przygotuj pozycję w formacie gotowym do przeniesienia na listę zadań Właściciela ({{UZUPEŁNIJ: nazwa narzędzia — np. Google Tasks, Todoist, papierowa lista}}):
   `- [tytuł: czasownik + kontekst, z prefiksem [Z] gdy zobowiązanie zewnętrzne] | termin: RRRR-MM-DD lub brak | uwagi: właściciel jeśli nie Właściciel systemu, źródło (nazwa transkrypcji + plan)`.
   Prefiks `[Z]` (konwencja [[Rejestr_Cyklow]]) ustal wg tego, czy zobowiązanie jest wobec osoby/organizacji SPOZA systemu Właściciela. **Przy niepewności — domyślnie BEZ prefiksu** i odnotuj wątpliwość w uwadze: błąd w stronę „wewnętrzne" jest bezpieczniejszy niż fałszywe uruchomienie reguł dla zobowiązań zewnętrznych. Pozycję o charakterze CYKLU (powtarzalny rytm) oznacz osobno jako propozycję do [[Rejestr_Cyklow]] — po sprawdzeniu, że takiego cyklu tam jeszcze nie ma. Zapisz WSZYSTKIE pozycje w JEDNYM pliku `inbox/ops/prop_[nazwa-transkrypcji]_RRRR-MM-DD.md`. Grounding: {{UZUPEŁNIJ: notatka o next action}}.
6. **Samokontrola** (Checklist) i raport zwrotny: liczba ustaleń per kategoria, liczba `[do potwierdzenia]`, liczba pozycji `[Z]`.

Akceptacja przez Właściciela i ręczne przeniesienie na listę zadań (lub do rejestru — dla cykli) to JEDYNA droga do źródeł. Żelazna zasada miejsca: propozycja żyje w `inbox/ops/`; nie podajesz komend przenoszących ani nie wykonujesz przeniesienia sam.

# Szablon wyniku
**1. `outputs/ops/plan_[nazwa-transkrypcji]_RRRR-MM-DD.md`** — frontmatter wg template_output (type: output, agent: asystent, task: "plan działania z transkrypcji", date, head: "[[ops]]", linked_sources: ["raw/transkrypcje/[nazwa]"], status: draft). Sekcje numerowane, stała kolejność; sekcja pusta = „nie dotyczy", nie usunięcie:
```
# Plan działania — [nazwa spotkania] — RRRR-MM-DD

## 1. Uczestnicy i kontekst
## 2. Decyzje
## 3. Next actions
- [czasownik + kontekst] — właściciel: [imię/rola lub [do potwierdzenia]] — termin: [data lub brak / [do potwierdzenia: dokładny termin]]
## 4. Pytania otwarte
## 5. Parking lot
## 6. Do potwierdzenia (lista zbiorcza)
```
**2. `inbox/ops/prop_[nazwa-transkrypcji]_RRRR-MM-DD.md`** — WYŁĄCZNIE next actions:
```
# Propozycja next actions — [nazwa spotkania] — RRRR-MM-DD
Źródło: raw/transkrypcje/[nazwa] → outputs/ops/plan_[nazwa]_RRRR-MM-DD.md

## Do przeniesienia na listę zadań
- [Z] [tytuł] | termin: RRRR-MM-DD | uwagi: …
- [tytuł] | termin: brak | uwagi: właściciel [do potwierdzenia]

## Propozycje cykli do [[Rejestr_Cyklow]] (jeśli są)
- [nazwa cyklu] — rytm: … — pierwszy termin: …
```

# Checklist przed oddaniem
- [ ] Cała transkrypcja przeczytana, nie próbka z początku.
- [ ] Każde ustalenie w DOKŁADNIE jednej z czterech kategorii; kolizje rozstrzygnięte priorytetem decyzja > next action > pytanie > parking lot.
- [ ] Żaden właściciel ani termin nie jest zgadnięty — niepewne pozycje mają jawne `[do potwierdzenia]`; sekcja 6 planu zbiera je wszystkie.
- [ ] Next actions w planie i w propozycji SPÓJNE (ta sama treść w obu plikach, nie dwie rozjeżdżające się wersje).
- [ ] Każda pozycja propozycji ma rozstrzygnięty prefiks `[Z]` albo jego brak; przy niepewności brak + odnotowana wątpliwość.
- [ ] Propozycje cykli sprawdzone wobec istniejących pozycji [[Rejestr_Cyklow]] — bez duplikatów.
- [ ] Zero zapisu do [[Rejestr_Cyklow]] i do listy zadań Właściciela — wyłącznie plik w `inbox/ops/`; zero komend przenoszących w podsumowaniu.
- [ ] Transkrypcja źródłowa nietknięta (`raw/` niezmienne).
- [ ] Zero next actions i decyzji ponad to, co faktycznie padło w rozmowie; zero zobowiązań wobec osób trzecich — skill ekstrahuje i proponuje, nigdy nie wysyła ani nie odpowiada w imieniu Właściciela.
- [ ] Sekcja „Podstawa metodyczna" obecna; kroki na `{{UZUPEŁNIJ}}` oznaczone [wiedza własna modelu] do czasu ingestu.

# Wzorcowy przykład
[uzupełnić pierwszym zaakceptowanym wynikiem — few-shot musi cytować realny, oceniony przebieg z outputs/router/log.md]

# Stan akceptacji
- Niejasne przypisanie właściciela lub terminu → `[do potwierdzenia]`, nigdy domysł; przybliżenie czasowe nie jest przekładane na datę. WDROŻONE.
- Przy niepewności co do zobowiązania zewnętrznego pozycja idzie BEZ prefiksu `[Z]` — błąd w stronę „wewnętrzne" jest tańszy niż fałszywe uruchomienie reguł zewnętrznych. WDROŻONE.
- Next actions trafiają wyłącznie do `inbox/ops/` jako propozycja; przeniesienie na listę zadań Właściciela (narzędzie: `{{UZUPEŁNIJ}}`) i do rejestru wykonuje Właściciel — skill nie ma i nie proponuje kanału zwrotnego. WDROŻONE.
- Wsad do zadań (transkrypcja) i wsad do wiedzy (źródło w `raw/`) rozdzielone testem „notatka wiedzy czy lista działań", nie lokalizacją pliku. WDROŻONE.
- Skill wchodzi do szablonu jako aktywny mimo pustego `raw/transkrypcje/` — pierwszy przebieg kalibruje Wzorcowy przykład. OTWARTE do pierwszego przebiegu.

# Historia zmian
- 2026-09-05 (v1.0): wersja szablonu — wyprowadzona z działającego systemu-poprzednika; treść osobista i infrastrukturalna usunięta, struktura i zasady zachowane.
