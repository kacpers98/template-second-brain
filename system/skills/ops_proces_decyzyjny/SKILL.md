---
name: ops_proces_decyzyjny
aliases: ["ops_proces_decyzyjny"]              # plik nazywa się SKILL.md — alias pozwala linkować [[ops_proces_decyzyjny]] w Obsidianie (lint R8)
description: "Sześciokrokowa, sztywno uporządkowana procedura higieny decyzyjnej: ramowanie szerokie z testem fałszywej dychotomii, perspektywa zewnętrzna i base rates PRZED analizą szczegółów, 2–3 warianty (nigdy jeden, nigdy więcej niż trzy) z testem odwracalności dla każdego, pre-mortem wariantu wiodącego, checklist czterech biasów odniesiona do TEJ decyzji, 3–5 pytań kontrolnych na końcu. Dokument NIGDY nie zawiera rekomendacji — ani wprost, ani zawoalowanej; decyzja zawsze należy do Właściciela. Używaj przy KAŻDYM zleceniu „przeprowadź mnie przez decyzję X", „przygotuj strukturę decyzyjną", „zrób pre-mortem dla planu Z". NIE jest tym skillem: brief (→ ops_brief), plan z transkrypcji, sama decyzja lub jej zapis."
# --- pola własne ---
type: skill
skill_type: procedure
used_by:
  - "[[doradca]]"
depends_on_artifacts:
  - "[[Profil_Wlasciciela]]"
wymagany_odczyt:                    # ŚCIEŻKI wymagane przez procedurę (artefakt żyje w depends_on_artifacts)
  - outputs/ops/                    # krok 0 — sprawdzenie, czy ta decyzja nie ma już notatki decyzyjnej (kontynuacja zamiast duplikatu)
# Świadomie NIEobecne: wiki/ — zasięg klastrowy [[doradca]]y niesie cluster_access, nie to pole.
inputs: "TWARDE: pytanie decyzyjne + dostępny kontekst (dane, ograniczenia, termin) — wprost od Właściciela albo przekazane przez [[asystent]]a jako pozycja „czeka na decyzję". Pytanie niejasne („pomóż mi z X" bez wyboru do rozstrzygnięcia) → dopytaj o konkretne opcje, nie zgaduj. Zakłada, że przesiew domenowy (czy decyzja leży w mandacie [[doradca]]y) odbył się na poziomie agenta PRZED wywołaniem."
output_format: "notatka decyzyjna outputs/ops/decyzja_[skrót]_RRRR-MM-DD.md z sekcjami 1–6 w sztywnej kolejności, kończąca się WYŁĄCZNIE pytaniami kontrolnymi"
version: 1.0
updated: 2026-09-05
---
# Kiedy używać
Każde zlecenie prowadzenia przez decyzję: wybór między opcjami, ocena planu, samodzielny pre-mortem. Dziedzina jest dowolna (zawodowa, organizacyjna, osobista) — procedura jest niezależna od branży. Skill zakłada, że [[doradca]] wykonał już własny przesiew domenowy z definicji agenta i nie powtarza go.

NIE jest tym skillem (test rozróżniający: co jest PRODUKTEM):
- generowanie briefu (→ [[ops_brief]]) — produktem jest stan bieżący, nie materiał do wyboru;
- plan działania z transkrypcji (→ [[ops_transkrypcja_na_plan]]) — produktem są ustalenia już podjęte, nie warianty;
- sama decyzja albo jej zapis — ten skill produkuje MATERIAŁ do decyzji, nigdy decyzję; tę podejmuje zawsze Właściciel.

# Wymagane wejście
Jasno sformułowane pytanie decyzyjne + kontekst (dane, ograniczenia, termin, co już wiadomo). Jeśli na starcie nie ma konkretnego wyboru do rozstrzygnięcia — dopytaj o opcje lub o pytanie, zanim zaczniesz krok 1. Krok 0: sprawdź `outputs/ops/`, czy ta decyzja nie ma już notatki — jeśli ma, pracujesz jako kontynuacja (nowy plik z sufiksem `_02`, linkujący poprzedni), nie od zera.

Z [[Profil_Wlasciciela]] czytasz sekcję o podejmowaniu decyzji (styl, tolerancja ryzyka, limit wariantów). Jeśli Profil jest jeszcze pusty (wzorzec niewypełniony) — stosujesz domyślne 2–3 warianty i odnotowujesz to w sekcji 1 wyniku.

# Podstawa metodyczna (Grounding)
- {{UZUPEŁNIJ: notatka o modelu WRAP i czterech „złoczyńcach" decyzji (Heath, „Decyduj!")}} → cała procedura — szkielet sekwencji kroków 1–4: poszerz opcje, sprawdź założenia rzeczywistością, zdystansuj się, przygotuj na błąd.
- {{UZUPEŁNIJ: notatka o ramowaniu wąskim i szerokim (Kahneman)}} → krok 1 — ramowanie szerokie i test fałszywej dychotomii.
- {{UZUPEŁNIJ: notatka o poszerzaniu opcji: test znikających opcji i multitracking (Heath)}} → kroki 1 i 3 — technika dochodzenia do 2–3 realnych wariantów.
- {{UZUPEŁNIJ: notatka o złudzeniu planowania i perspektywie zewnętrznej (Kahneman)}} → krok 2 — outside view i base rates przed analizą szczegółów.
- {{UZUPEŁNIJ: notatka o opcjonalności i asymetrii wypłat (Taleb)}} → krok 3 — test odwracalności: struktura o ograniczonej stracie i otwartym zysku.
- {{UZUPEŁNIJ: notatka o przygotowaniu na błąd: pre-mortem, bookending, tripwire (Heath)}} → krok 4 — pre-mortem wariantu wiodącego.
- {{UZUPEŁNIJ: notatka o WYSIATI i heurystyce substytucji (Kahneman)}} → krok 5 — bias „istnieje tylko to, co widzisz".
- {{UZUPEŁNIJ: notatka o kosztach utopionych}} → krok 5 — faworyzowanie wariantu z powodu tego, co już zainwestowano.
- {{UZUPEŁNIJ: notatka o confirmation bias}} → krok 5 — aktywne szukanie dowodów PRZECIW preferowanemu wariantowi.
- {{UZUPEŁNIJ: notatka o granicach przewidywalności i arogancji epistemicznej (Taleb)}} → krok 5 — kalibracja przedziału niepewności.

Vault startowy nie zawiera tych notatek; do czasu ingestu kroki wykonuj z oznaczeniem [wiedza własna modelu] w treści wyniku. Nazwy metod powyżej są wskazówką, CO ingestować — kandydaci należą do klastra [[Przywództwo i Decyzje]]. Podstawa normatywna limitu wariantów: [[Profil_Wlasciciela]].

# Twarda granica formatu wyniku
Dokument NIE ZAWIERA rekomendacji „zrób X" w ŻADNEJ formie — ani wprost, ani zawoalowanej. „Wariant A wydaje się mocniejszy", „sugerowałbym B", „najrozsądniej byłoby…" to już rekomendacje — zakazane. Dokument kończy się WYŁĄCZNIE pytaniami z kroku 6. Jeśli w trakcie pisania fragment brzmi jak sugestia wyboru — przeformułuj go na neutralne zestawienie faktów („wariant A ma X, wariant B ma Y") bez konkluzji „więc X jest lepsze". Zero fabrykowanych statystyk w kroku 2.

# Procedura
Sześć kroków, kolejność SZTYWNA, każdy obowiązkowy (pominięcie wymaga jawnego uzasadnienia w wyniku, nie cichego przeskoczenia).

**1. Ramowanie szerokie.** Przeformułuj decyzję na MINIMUM DWA różne sposoby (zmień jednostkę analizy, przesuń horyzont czasowy, zapytaj „jaki problem to naprawdę rozwiązuje" zamiast „co wybrać"). Sprawdź, czy oryginalne sformułowanie nie jest FAŁSZYWĄ DYCHOTOMIĄ — czy realnych opcji nie jest więcej, niż sugeruje pytanie „A czy B". Jeśli reformulacje ujawniają, że pytanie było źle postawione, kontynuuj z wersją poprawioną, nie z oryginalną — i powiedz to w sekcji 1. Grounding: {{UZUPEŁNIJ: notatka o ramowaniu}} [wiedza własna modelu do czasu ingestu].

**2. Perspektywa zewnętrzna i base rates.** PRZED analizą szczegółów TEJ sytuacji ustal, jak wyglądają porównywalne przypadki: bazowa częstość sukcesu/niepowodzenia dla tej KLASY decyzji, niezależnie od specyfiki Właściciela. Jeśli wiedza w vaulcie ani dane od Właściciela nie wystarczają — napisz to wprost i zapytaj, czym dysponuje; nigdy nie zmyślaj statystyk. Grounding: {{UZUPEŁNIJ: notatka o perspektywie zewnętrznej}}.

**3. 2–3 realne warianty z kryteriami, trade-offami i testem odwracalności.** NIGDY jeden wariant (to potwierdzenie z góry przyjętego wyboru, nie analiza), NIGDY więcej niż trzy ([[Profil_Wlasciciela]], sekcja o decyzjach). Dla każdego: co zyskujesz / co tracisz / co byś sprawdził. **OBOWIĄZKOWY test odwracalności dla KAŻDEGO wariantu**: czy decyzję da się cofnąć małym kosztem i potraktować jak eksperyment (odwracalna — strata ograniczona, zysk otwarty), czy jest jednokierunkowa z wysokim kosztem cofnięcia (nieodwracalna — wymaga solidniejszego uzasadnienia w krokach 4–5, nie przyspieszonego tempa). Grounding: {{UZUPEŁNIJ: notatka o opcjonalności}}.

**4. Pre-mortem wariantu wiodącego.** Jeśli z kroków 1–3 wyłania się naturalny kandydat (z analizy, nie z Twojej preferencji) — wykonaj na NIM ćwiczenie: „minął odpowiedni okres i ta decyzja ewidentnie zawiodła — co się stało i dlaczego?". PRZED decyzją, nigdy jako post-mortem. Jeśli żaden wariant nie jest oczywistym liderem — pre-mortem dla najbardziej ryzykownego/nieodwracalnego (test z kroku 3 wskazuje który). Grounding: {{UZUPEŁNIJ: notatka o pre-mortem}}.

**5. Checklist biasów odniesiona do TEJ decyzji, nie do definicji.** Każdy z czterech biasów zastosuj WPROST do rozpatrywanej sytuacji — jeśli wynik brzmi jak definicja z podręcznika, przepisz go na pytanie o tę konkretną decyzję:
   - **WYSIATI** — jakich informacji, których dziś NIE masz, ta analiza może brakować, bo nikt o nich nie pomyślał?
   - **Koszty utopione** — czy któryś wariant jest faworyzowany z powodu tego, co już zainwestowano (czas, pieniądze, tożsamość), a nie z powodu przyszłej wartości?
   - **Potwierdzenie** — czy analiza aktywnie szukała dowodów PRZECIW naturalnie preferowanemu wariantowi, czy tylko za nim?
   - **Nadmierna pewność** — jak szeroki jest realistyczny przedział niepewności wokół kluczowych założeń i czy warianty z kroku 3 milcząco zakładają węższy?
   Grounding: cztery pozycje kroku 5 z sekcji „Podstawa metodyczna".

**6. Pytania kontrolne dla Właściciela (3–5).** Zamykają dokument. Pytania, nie stwierdzenia — każde ma pomóc Właścicielowi podjąć WŁASNĄ decyzję, żadne nie sugeruje odpowiedzi. Wzorce do adaptacji (nie kopiuj dosłownie): „Co musiałoby być prawdą, żeby wariant [X] był oczywistym wyborem?", „Który koszt jesteś gotów ponieść, żeby uniknąć ryzyka z kroku 4?", „Czy istnieje wersja tej decyzji, którą możesz przetestować małym kosztem przed pełnym zaangażowaniem?".

# Szablon wyniku
`outputs/ops/decyzja_[skrót]_RRRR-MM-DD.md`, frontmatter wg template_output (type: output, agent: doradca, task: "proces decyzyjny: [skrót]", date, head: "[[ops]]", linked_sources: ["[[Profil_Wlasciciela]]"], status: draft). Sekcje w TEJ kolejności, numerowane 1–6 dosłownie; sekcja niewykonana = „nie dotyczy" z uzasadnieniem, nie usunięcie:
```
# Proces decyzyjny — [skrót] — RRRR-MM-DD

## 1. Ramowanie
[pytanie oryginalne; ≥2 reformulacje; wynik testu fałszywej dychotomii; wersja przyjęta do dalszej pracy]
## 2. Perspektywa zewnętrzna i base rates
[klasa decyzji; co wiadomo o porównywalnych przypadkach; czego NIE wiadomo — wprost]
## 3. Warianty (z testem odwracalności per wariant)
[A / B / (C): zyskujesz — tracisz — sprawdziłbyś — odwracalność]
## 4. Pre-mortem
[dla którego wariantu i dlaczego ten; scenariusz porażki; przyczyny]
## 5. Checklist biasów (odniesiona do decyzji)
[WYSIATI / koszty utopione / potwierdzenie / nadmierna pewność — każdy jako pytanie o TĘ decyzję]
## 6. Pytania kontrolne
[3–5 pytań; nic po nich]
```
Fragmenty oparte na wiedzy modelu (brak notatki w vaulcie) oznaczone inline `[wiedza własna modelu]`.

# Checklist przed oddaniem
- [ ] Krok 1: minimum 2 reformulacje + jawny test fałszywej dychotomii.
- [ ] Krok 2: base rates PRZED analizą szczegółów; brak danych nazwany, nie zastąpiony zmyśloną liczbą.
- [ ] Krok 3: dokładnie 2 lub 3 warianty, KAŻDY z jawnym testem odwracalności.
- [ ] Krok 4: pre-mortem PRZED decyzją, dla wariantu wiodącego lub najbardziej nieodwracalnego — z uzasadnieniem wyboru.
- [ ] Krok 5: cztery biasy zastosowane WPROST do tej decyzji, żaden nie brzmi jak definicja.
- [ ] Krok 6: 3–5 pytań; ostatnia linia dokumentu jest pytaniem.
- [ ] Zero „rekomenduję / proponuję / najlepszy wariant / wydaje się mocniejszy" ani ich zawoalowanych form w całym dokumencie.
- [ ] Sekcje w kolejności 1–6, żadna nie pominięta bez jawnego uzasadnienia.
- [ ] Zgodność z [[Profil_Wlasciciela]] (limit wariantów; Profil pusty → odnotowane w sekcji 1).
- [ ] Sekcja „Podstawa metodyczna" obecna; pozycje `{{UZUPEŁNIJ}}` odzwierciedlone oznaczeniem [wiedza własna modelu] w wyniku.

# Wzorcowy przykład
[uzupełnić pierwszym zaakceptowanym wynikiem — few-shot musi cytować realny, oceniony przebieg z outputs/router/log.md]

# Stan akceptacji
- Dokument nigdy nie zawiera rekomendacji; kończy się wyłącznie pytaniami — granica mandatu [[doradca]]y, nie ograniczenie formy. WDROŻONE.
- Liczba wariantów: 2–3, nigdy 1 (potwierdzenie gotowego wyboru), nigdy >3; limit umocowany w [[Profil_Wlasciciela]], a przy pustym Profilu stosowany domyślnie z adnotacją. WDROŻONE.
- Podstawa metodyczna w szablonie startowym to placeholdery `{{UZUPEŁNIJ}}` — nazwy metod wskazują, co ingestować; do czasu ingestu procedura biegnie na wiedzy własnej modelu z jawnym oznaczeniem, nie udając pokrycia. WDROŻONE.
- Przesiew domenowy (czy decyzja leży w mandacie doradcy) należy do definicji agenta, nie do skilla — skill go nie powtarza. WDROŻONE.
- Kontynuacja decyzji już opisanej w `outputs/ops/` = nowy plik z sufiksem `_02` linkujący poprzedni, nie nadpisanie. WDROŻONE.

# Historia zmian
- 2026-09-05 (v1.0): wersja szablonu — wyprowadzona z działającego systemu-poprzednika; treść osobista i infrastrukturalna usunięta, struktura i zasady zachowane.
