---
name: ops_brief
aliases: ["ops_brief"]              # plik nazywa się SKILL.md — alias pozwala linkować [[ops_brief]] w Obsidianie (lint R8)
description: "Procedura briefu dziennego lub tygodniowego wg [[Rytm_Przegladow]] w UKŁADZIE SEKCYJNYM: tylko nagłówki `##`, jedna pozycja = jedna linia, terminy względne, sekcja pusta pomijana, jedna linia „Źródła:" ze statusem każdego wejścia. Brief AGREGUJE zamkniętą listę wejść: tabelę Cykle z [[Rejestr_Cyklow]] oraz listę zadań i kalendarz wklejone przez Właściciela w zleceniu albo wskazane plikiem — nigdy nie wymyśla stanu. Dzienny: DZIŚ / ZA CHWILĘ / TŁO, limit 5 pozycji z licznikiem nadmiaru. Tygodniowy: Top-3 / Terminy zagrożone / Czeka na decyzję / Parking lot / Delta / TŁO. Wynik nadpisuje `outputs/ops/brief_ostatni_[tryb].md`, czytany przed nadpisaniem (delta). Używaj przy KAŻDYM zleceniu „wygeneruj brief dzienny/tygodniowy", „co na dziś", „przegląd tygodnia". NIE jest tym skillem: plan z transkrypcji, prowadzenie decyzji."
# --- pola własne ---
type: skill
skill_type: procedure
used_by:
  - "[[asystent]]"
depends_on_artifacts:
  - "[[Rejestr_Cyklow]]"
  - "[[Rytm_Przegladow]]"
wymagany_odczyt:                    # ŚCIEŻKI wymagane przez procedurę (nie artefakty — te żyją w depends_on_artifacts)
  - outputs/ops/                    # krok 0 — odczyt poprzedniego brief_ostatni_[tryb].md PRZED nadpisaniem (data poprzedniego briefu + stan do Delty w trybie B)
# Świadomie NIEobecne w tym polu: lista zadań i kalendarz Właściciela — nie są ścieżkami vaulta,
# wchodzą jako treść zlecenia albo wskazany przez Właściciela plik (patrz „Wymagane wejście").
inputs: "TWARDE: tryb `dzienny` | `tygodniowy` (brak → dopytaj, nie zgaduj). OPCJONALNE, w treści zlecenia albo jako wskazany plik: lista zadań Właściciela (z terminami, jeśli są) i wydarzenia kalendarza w horyzoncie trybu; pozycje „czeka na decyzję", jeśli Właściciel je jawnie przekaże. Wejście niedostarczone = brief bez niego + status „nie dostarczono" w linii „Źródła:"."
output_format: "plik outputs/ops/brief_ostatni_[tryb].md — NADPISYWANY przy każdym przebiegu (pamięć ostatniego stanu, nie archiwum; historię trzyma git) — w układzie sekcyjnym, z jedną linią „Źródła:" na końcu"
version: 1.0
updated: 2026-09-05
---
# Kiedy używać
Każde zlecenie briefu: „wygeneruj brief dzienny", „co na dziś", „zrób przegląd tygodnia", „brief tygodniowy". Dwa tryby, jedna procedura: dzienny i tygodniowy dzielą krok 0 (zebranie wejść) i wspólny kontrakt formatu, a różnią się od kroku A/B w dół. Przebieg odbywa się w sesji, w której Właściciel jest obecny — to on dostarcza wejścia spoza vaulta.

NIE jest tym skillem (test rozróżniający: punkt startowy zlecenia):
- przetwarzanie transkrypcji spotkania na plan (→ [[ops_transkrypcja_na_plan]]) — punktem startowym jest PLIK w `raw/transkrypcje/`, nie data;
- prowadzenie procesu decyzyjnego dla pozycji „czeka na decyzję" (→ [[doradca]], [[ops_proces_decyzyjny]]) — brief wyłącznie WYMIENIA takie pozycje, nie rozstrzyga niczego;
- klasyfikacja luźnych notatek wg GTD — osobna, prostsza zdolność [[asystent]]a poza tym skillem; nie miesza się formatu briefu z formatem klasyfikacji next actions.

# Wymagane wejście
**Tryb** (twarde): `dzienny` lub `tygodniowy`. Rytm obu trybów opisuje [[Rytm_Przegladow]]. Bez jawnie podanego trybu — dopytaj; nie wnioskuj go z dnia tygodnia.

**Wejścia z vaulta** (czytane na żywo, nie z pamięci):
- [[Rejestr_Cyklow]] — tabela *Cykle* z kolumną „Najbliższy": pozycje cykliczne i normatywne. Brief bierze te, których „Najbliższy" wypada w horyzoncie trybu.
- `outputs/ops/brief_ostatni_[tryb].md` — poprzedni brief TEGO SAMEGO trybu; czytany w kroku 0, ZANIM zostanie nadpisany.

**Wejścia przekazywane przez Właściciela** — w treści zlecenia albo jako wskazany plik (np. `inbox/ops/zadania.md`). To projekcje JEDNOKIERUNKOWE: czytasz, nie zapisujesz zwrotnie, nie proponujesz do nich wpisów, nie przenosisz ich pozycji do [[Rejestr_Cyklow]] ani odwrotnie.
- **Lista zadań Właściciela** — zadania jednorazowe, prowadzone w narzędziu Właściciela (np. Google Tasks, Todoist, papier) — {{UZUPEŁNIJ: nazwa narzędzia, w którym Właściciel prowadzi listę zadań}}. Jeśli lista przychodzi już rozłożona na kubełki (`zaległe / na dziś / bez terminu lub późniejsze` dla dziennego; `zaległe / w tym tygodniu / dalsze` dla tygodniowego) — przyjmujesz podział jak jest. Jeśli przychodzi płasko z terminami — rozkładasz ją na kubełki MECHANICZNIE po terminie względem daty briefu (termin minął → zaległe; dziś / w tym tygodniu → odpowiedni kubełek; brak terminu lub później → ostatni kubełek). Nie zmieniasz treści pozycji, nie oceniasz ich ważności, nie dopisujesz brakujących terminów.
- **Kalendarz** — wydarzenia w horyzoncie trybu (dziś dla dziennego; nadchodzący tydzień dla tygodniowego). Wydarzenie nigdy nie staje się pozycją rejestru ani propozycją do `inbox/ops/`.
- **Pozycje „czeka na decyzję"** — WYŁĄCZNIE gdy Właściciel jawnie je przekaże; żadne wejście nie niesie takiego statusu samo z siebie.

**Wejście niedostarczone**: brief powstaje bez niego, a linia „Źródła:" mówi o tym wprost („lista zadań — nie dostarczono"). Nie zgadujesz, ile jest zadań, jeśli listy nie dostałeś. Rozróżniaj: **lista dostarczona i pusta** (status „sprawdzono, 0 pozycji") od **listy niedostarczonej** (status „nie dostarczono") — te dwa stany muszą być widoczne osobno, bo w treści briefu wyglądają identycznie.

Zamknięta lista wejść to cztery pozycje powyżej. Wejście spoza listy (np. skrzynka pocztowa, newslettery) wymaga zmiany [[Rytm_Przegladow]] i tego skilla; w szablonie startowym nie występuje, a gdyby weszło — tą samą drogą (treść zlecenia albo plik) i z własnym statusem w linii „Źródła:".

# Podstawa metodyczna (Grounding)
- {{UZUPEŁNIJ: notatka o przeglądzie tygodniowym (weekly review) w GTD}} → tryb B — struktura i funkcja przeglądu tygodniowego (domknięcie pętli + plan), z której wynika zestaw sekcji Top-3 / zagrożone / parking lot.
- {{UZUPEŁNIJ: notatka o pięciu etapach przepływu pracy GTD (capture / clarify / organize / reflect / engage)}} → krok 0 i A.1 — rozdział etapów uzasadnia, dlaczego brief AGREGUJE gotowe kubełki, zamiast reklasyfikować pozycje.
- {{UZUPEŁNIJ: notatka o horyzontach ostrości / poziomach przeglądu w GTD}} → sekcje TŁO — oddzielenie kontekstu (TŁO) od działań bieżących.

Vault startowy nie zawiera tych notatek; do czasu ingestu kroki wykonuj z oznaczeniem [wiedza własna modelu]. Kandydaci do ingestu leżą w klastrze [[Wydajność i Skupienie]].

Podstawa normatywna formatu, limitów i listy wejść: [[Rytm_Przegladow]], [[Rejestr_Cyklow]].

# Format briefu — kontrakt wspólny dla obu trybów
Obowiązuje KAŻDY brief, niezależnie od trybu. Jest wiążący tak samo jak kroki procedury.

1. **Wyłącznie sekcje.** Cała treść żyje w sekcjach z nagłówkiem markdown DRUGIEGO poziomu (`## NAZWA`). Poza sekcjami wolno wystąpić trzem rzeczom: frontmatterowi, tytułowi `# Brief [tryb] — RRRR-MM-DD` i końcowej linii „Źródła:". Zero preambuł, zero zdań między tytułem a pierwszą sekcją.
2. **Jedna pozycja = jeden punkt = jedna linia.** Punkt zaczyna się od `- `. Bez zdań podrzędnych o pochodzeniu danych („pozycja z tabeli Cykle") — to idzie do linii „Źródła:". Bez zagnieżdżeń, bez łamania pozycji na dwie linie.
3. **Terminy WZGLĘDNIE.** `za 3 dni (pon 08.09)`, `jutro (sob 06.09)`, `dziś`, `zaległe 4 dni (pon 01.09)`. Sama data ISO w treści punktu jest błędem formatu — dystans ma być czytelny bez liczenia.
4. **Sekcja bez zawartości jest POMIJANA.** Nigdy pusty nagłówek, nigdy słowo „brak" jako wypełniacz. Nieobecność sekcji JEST informacją. Jedyny wyjątek: element statusowy — linia „Źródła:" (pkt 5) jest STAŁA i niesie status każdego wejścia, bo tylko tam „sprawdzono, pusto" i „nie dostarczono" dają się odróżnić.
5. **Proweniencja w JEDNEJ linii na końcu pliku**, zaczynającej się od `Źródła:` — każde wejście z zamkniętej listy ze statusem: `sprawdzono (N pozycji)` / `nie dostarczono` / dla poprzedniego briefu `odczytano (data)` albo `brak pliku`. Wikilinki żyją WYŁĄCZNIE w tej linii i we frontmatterze; wewnątrz punktów ich nie ma.
6. **Nazwy sekcji nie są dowolne** — bierzesz je z trybu: dzienny → `## DZIŚ`, `## ZA CHWILĘ`, `## TŁO`; tygodniowy → `## Top-3`, `## Terminy zagrożone`, `## Czeka na decyzję`, `## Parking lot`, `## Delta`, opcjonalnie `## TŁO` na końcu. Kolejność stała. Ujednolicony jest KONTRAKT UKŁADU, nie nazwy: dzienne klasyfikują po horyzoncie czasu, tygodniowe po funkcji w przeglądzie — to osie ortogonalne, nie dwa słowniki na to samo.
7. **Kanał dostarczenia Cię nie dotyczy.** Piszesz plik do `outputs/ops/` — on jest wersją kanoniczną. Gdyby Właściciel kiedyś dostarczał brief dalej (mail, komunikator), byłaby to projekcja pliku. Nie piszesz pod kanał: żadnych emoji dekoracyjnych, HTML-a, znaczników formatowania ani ręcznego escapowania.

# Procedura

## Krok 0 — wspólny dla obu trybów
1. Wczytaj [[Rejestr_Cyklow]] — tabelę *Cykle* (kolumna „Najbliższy").
2. Odczytaj wejścia od Właściciela (lista zadań, kalendarz, ewentualne pozycje decyzyjne) — z treści zlecenia albo ze wskazanego pliku. Listę płaską rozłóż na kubełki mechanicznie (patrz „Wymagane wejście"); listę już rozłożoną przyjmij jak jest. Zanotuj, których wejść NIE dostarczono.
3. Wczytaj istniejący `outputs/ops/brief_ostatni_[tryb].md` — ZANIM go nadpiszesz. Bierzesz z niego datę poprzedniego briefu (przypadek „zaległy brief") i poprzedni stan do Delty (tryb B). Brak pliku → zanotuj „brak pliku".

Jeśli WSZYSTKIE wejścia są puste (Cykle bez pozycji w horyzoncie, lista bez pozycji, kalendarz bez wydarzeń) — to POPRAWNY stan, nie błąd: tryb A wygeneruje „czysto" (A.6), tryb B — brief z samą Deltą i linią „Źródła:". Nie przerywasz procedury i nie wymyślasz pracy.

## Tryb A — dzienny
1. **Zbierz kandydatów.** Cykle z „Najbliższy" = dziś lub jutro (wchodzą wprost, bez rywalizacji). Lista zadań: kubełki `zaległe` i `na dziś` w całości; kubełek `bez terminu lub późniejsze` WYŁĄCZNIE jako licznik (do TŁO) — jego pozycji nie wyliczasz. Kalendarz: wydarzenia dzisiejsze.
2. **Blokery**: pozycje jawnie oznaczone jako blokujące w tytule lub uwadze (np. „blokuje: …"). Bez takiego oznaczenia krok jest naturalnie pusty — nie wnioskujesz blokowania z treści.
3. **Decyzje czekające**: wyłącznie pozycje jawnie przekazane przez Właściciela; najwyżej JEDNA wchodzi do TŁO. Bez przekazania — krok pomijasz.
4. **Rozłóż na sekcje** (kolejność stała, pusta pomijana):
   - `## DZIŚ` — kubełki `zaległe` i `na dziś`, Cykle z „Najbliższy" = dziś, blokery, wydarzenia z dzisiaj. Reguła osądu: cykl, którego „Najbliższy" minął, a który blokuje inne zadanie lub zobowiązanie zewnętrzne, wchodzi do DZIŚ mimo brzmienia filtra — z jawną adnotacją w raporcie zwrotnym, że to osąd, nie automatyczne dopasowanie. Filtr terminu jest domyślny, nie nadrzędny wobec sensu briefu.
   - `## ZA CHWILĘ` — Cykle z „Najbliższy" = jutro. (Zadania z terminem jutrzejszym leżą w kubełku `bez terminu lub późniejsze` — wchodzą do licznika w TŁO.)
   - `## TŁO` — maks. 1 decyzja czekająca; JEDNA zbiorcza linia z licznikiem kubełka `bez terminu lub późniejsze` (jeśli lista przyszła); jedna informacja odciążająca (najbliższy termin POZA horyzontem), gdy DZIŚ i ZA CHWILĘ są puste — czytelnik ma wiedzieć, że filtr zadziałał, a nie że wszystko zniknęło.
5. **Limit: maksymalnie 5 POZYCJI merytorycznych łącznie** (nagłówki, puste linie i linia „Źródła:" nie liczą się). Gdy kwalifikuje się więcej: pierwszeństwo DZIŚ → ZA CHWILĘ → TŁO, a nadmiar sygnalizujesz JEDNĄ zbiorczą linią z licznikiem w sekcji, z której go wyciąłeś (np. `- +4 dalsze zaległe`). Ciche skrócenie jest zabronione — skrócenie ma być widoczne.
6. **Nic się nie kwalifikuje** → jedna sekcja `## DZIŚ` z jedną linią `- czysto` (opcjonalnie z informacją odciążającą). Zero pustych nagłówków, zero treści dopisanej, żeby brief „wyglądał na pełny".
7. **Linia „Źródła:"** ze statusem każdego wejścia i zapis do `outputs/ops/brief_ostatni_dzienny.md` przez nadpisanie.

## Tryb B — tygodniowy
Sekcje ZAWSZE w tej kolejności, całość na jednym ekranie (twardy limit), sekcja bez zawartości pomijana.
1. **`## Top-3`** — kandydaci: kubełki `zaległe` i `w tym tygodniu`. Kwalifikacja W TEJ KOLEJNOŚCI: (a) zaległe przed terminowymi (najdłużej zaległe pierwsze; wśród terminowych — bliskość terminu); (b) remis → prefiks `[Z]` (zobowiązanie zewnętrzne, konwencja z [[Rejestr_Cyklow]]) przed pozycjami bez prefiksu; (c) dalszy remis → kolejność z listy. Maks. 3 — mniej kandydatów = mniej pozycji, nie dopychaj. Cykle z „Najbliższy" w nadchodzącym tygodniu dołącz WPROST, poza limitem 3 i bez rywalizacji.
2. **`## Terminy zagrożone`** — pozycje z kubełków `zaległe` i `w tym tygodniu`, które NIE weszły do Top-3 (bez duplikacji między sekcjami); zaległe pierwsze, dalej wg bliskości terminu. Cykli nie duplikuj — są w B.1.
3. **`## Czeka na decyzję`** — WYŁĄCZNIE pozycje jawnie przekazane przez Właściciela. To surowe wejście, z którego Właściciel może skierować pozycję do [[doradca]]; Ty nic tu nie rozstrzygasz.
4. **`## Parking lot`** — temat w kilku słowach, bez rozwinięcia; tylko to, co Właściciel lub lista jawnie oznacza jako odłożone.
5. **`## Delta`** — poprzedni stan to treść `brief_ostatni_tygodniowy.md` wczytana w kroku 0. Porównaj Top-3 i Terminy zagrożone: co nowe, co zniknęło, co przesunięte.
   - Brak poprzedniego pliku → Delta = dosłownie „pierwszy brief". Nie konstruuj porównania z niczego.
   - **Uczciwość delty**: lista zadań nie niesie historii ani pozycji ukończonych. Pozycję obecną w poprzednim briefie i nieobecną teraz opisujesz jako „zniknęła ze źródła (wykonana lub przeplanowana)" — NIGDY jako „zrobiona"; tego nie wiesz.
   - Poprzedni brief jest punktem odniesienia dla RÓŻNICY, nie źródłem stanu — stan bierzesz z wejść kroku 0.
6. **`## TŁO`** (opcjonalna, na końcu) — plan tygodnia z kalendarza (jedna linia na wydarzenie albo jedna zbiorcza) + JEDNA linia z licznikiem kubełka `dalsze`. Istnieje po to, żeby kontekst nie wracał jako zakazana preambuła ani nie zaśmiecał Parking lot. Pusta → pomijana.
7. **Linia „Źródła:"** i zapis do `outputs/ops/brief_ostatni_tygodniowy.md` przez nadpisanie.

## Przypadki brzegowe wspólne
- **Zaległy brief po przerwie**: jeśli poprzedni brief TEGO SAMEGO trybu ma datę starszą niż jeden oczekiwany cykl (>1 dzień roboczy dla dziennego, >1 tydzień dla tygodniowego) — dodaj JEDEN punkt adnotacji w pierwszej sekcji („- brief opóźniony (poprzedni: [data względnie]), nie nadrabiam zaległych") i kontynuuj dla BIEŻĄCEGO stanu. Nie rekonstruuj dzień po dniu, co działo się w przerwie.
- **Kubełek pusty vs kubełek niedostarczony**: pierwszy pomijasz w treści (sekcja pusta → pominięta), drugiego nie zgadujesz. Oba mają osobny status w linii „Źródła:".
- **Puste wejścia**: patrz krok 0 — poprawny stan, nie błąd.

# Szablon wyniku
**Brief dzienny** (`outputs/ops/brief_ostatni_dzienny.md`, nadpisywany), frontmatter wg template_output (type: output, agent: asystent, task: "brief dzienny", date, head: "[[ops]]", linked_sources: ["[[Rejestr_Cyklow]]"], status: draft):
```
# Brief dzienny — RRRR-MM-DD

## DZIŚ
- [pozycja — jedna linia, termin względny, bez wzmianki o źródle]
- [wydarzenie z dzisiaj — godzina + nazwa]

## ZA CHWILĘ
- [cykl z terminem jutrzejszym]

## TŁO
- [maks. 1 decyzja czekająca]
- [licznik, np. „12 zadań bez terminu lub z terminem późniejszym"]

Źródła: [[Rejestr_Cyklow]] — tabela Cykle (sprawdzono); lista zadań Właściciela — sprawdzono (17 pozycji), projekcja jednokierunkowa; kalendarz — sprawdzono (2 wydarzenia); poprzedni brief — odczytano (wczoraj).
```
Wariant „czysto":
```
# Brief dzienny — RRRR-MM-DD

## DZIŚ
- czysto — najbliższe zobowiązanie za 3 dni (pon 08.09)

Źródła: [[Rejestr_Cyklow]] — tabela Cykle (sprawdzono); lista zadań Właściciela — nie dostarczono; kalendarz — sprawdzono (0 wydarzeń); poprzedni brief — brak pliku.
```
**Brief tygodniowy** (`outputs/ops/brief_ostatni_tygodniowy.md`, nadpisywany), frontmatter jw. z task: "brief tygodniowy". Kolejność sekcji (nagłówki bez zawartości w prawdziwym pliku NIE występują — to spis kolejności, nie szkielet):
```
# Brief tygodniowy — RRRR-MM-DD

## Top-3
## Terminy zagrożone
## Czeka na decyzję
## Parking lot
## Delta
[## TŁO — plan tygodnia + licznik kubełka „dalsze"]

Źródła: [...]
```

# Checklist przed oddaniem
**Format:**
- [ ] Cała treść w sekcjach `## NAZWA`; poza nimi wyłącznie frontmatter, tytuł i linia „Źródła:". Zero preambuły.
- [ ] Każda pozycja = jeden punkt `- ` w JEDNEJ linii, bez zdania o pochodzeniu danych.
- [ ] Terminy WZGLĘDNIE (dystans + dzień tygodnia i data w nawiasie), nigdy sama data ISO.
- [ ] Żadna sekcja pusta nie została wypisana; nigdzie słowo „brak" jako wypełniacz.
- [ ] Dokładnie JEDNA linia „Źródła:" — każde z czterech wejść ze statusem (sprawdzono N / nie dostarczono / odczytano / brak pliku). Rozróżnione „sprawdzono, pusto" od „nie dostarczono".
- [ ] Zero wikilinków wewnątrz punktów; nazwy i kolejność sekcji z trybu; zero pisania pod kanał.

**Zawartość:**
- [ ] Brief agreguje WYŁĄCZNIE wejścia z kroku 0 — zero wymyślonego stanu, zero pozycji spoza zamkniętej listy.
- [ ] Tabela *Cykle* [[Rejestr_Cyklow]] wczytana na żywo.
- [ ] Lista zadań przyjęta jak przyszła (rozłożona → nieprzekwalifikowana; płaska → rozłożona mechanicznie po terminie); zero propozycji zapisu zwrotnego.
- [ ] Limit dotrzymany: 5 pozycji (dzienny) / jeden ekran (tygodniowy); każde skrócenie zasygnalizowane licznikiem `+N dalsze`, nie ciche.
- [ ] Top-3 policzone w kolejności zaległe → bliskość terminu → tie-break `[Z]`; maks. 3; Cykle wprost poza limitem.
- [ ] Delta = „pierwszy brief" przy braku poprzedniego pliku; pozycja nieobecna = „zniknęła ze źródła", nigdy „zrobiona".
- [ ] Zaległy brief = jeden punkt adnotacji + bieżący stan, nie seria nadrabianych sztuk.
- [ ] Poprzedni `brief_ostatni_[tryb].md` wczytany PRZED nadpisaniem; wynik zapisany przez NADPISANIE, bez plików datowanych.
- [ ] Zgodność z [[Rytm_Przegladow]] i [[Rejestr_Cyklow]]; sekcja „Podstawa metodyczna" obecna, pozycje `{{UZUPEŁNIJ}}` oznaczone [wiedza własna modelu] do czasu ingestu.

# Wzorcowy przykład
[uzupełnić pierwszym zaakceptowanym wynikiem — few-shot musi cytować realny, oceniony przebieg z outputs/router/log.md]

# Stan akceptacji
- Wejścia spoza vaulta (lista zadań, kalendarz) wchodzą wyłącznie jako treść zlecenia albo plik wskazany przez Właściciela — bez integracji z jakimkolwiek narzędziem. Skill nie ma kanału zwrotnego do żadnego z nich. WDROŻONE.
- Miarą limitu dziennego są POZYCJE merytoryczne, nie linie; nadmiar zawsze widoczny licznikiem. WDROŻONE.
- Ujednolicony jest kontrakt układu, nie nazwy sekcji — słownik nazw jest per tryb, bo osie klasyfikacji (horyzont czasu vs funkcja w przeglądzie) są ortogonalne. WDROŻONE.
- Linia „Źródła:" jest elementem STAŁYM ze statusem każdego wejścia — jedyna derogacja od reguły pomijania, bo „sprawdzono, pusto" i „nie dostarczono" w treści briefu są nierozróżnialne. WDROŻONE.
- Wynik to jeden plik kanoniczny nadpisywany per tryb; historię trzyma git, archiwum datowane nie powstaje. WDROŻONE.
- Sekcja monitorująca pocztę/newslettery i rozszerzenie kwartalne nie wchodzą do szablonu; ich wprowadzenie wymaga najpierw zmiany [[Rytm_Przegladow]], potem skilla. OTWARTE.

# Historia zmian
- 2026-09-05 (v1.0): wersja szablonu — wyprowadzona z działającego systemu-poprzednika; treść osobista i infrastrukturalna usunięta, struktura i zasady zachowane.
