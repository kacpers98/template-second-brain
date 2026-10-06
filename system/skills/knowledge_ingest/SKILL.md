---
name: knowledge_ingest
aliases: ["knowledge_ingest"]              # plik nazywa się SKILL.md — alias pozwala linkować [[knowledge_ingest]] w Obsidianie (lint R8)
description: "Procedura przetwarzania nowego źródła: od surowego pliku w raw/ do notatki źródłowej w sources/ i propozycji stron koncepcji w inbox/knowledge/, z linkami zwrotnymi w notatkach docelowych i wpisem w logu. Używaj przy KAŻDYM zleceniu 'przetwórz źródło', 'zrób ingest', 'wchłoń ten materiał', 'dodaj to do wiedzy' oraz cyklicznie dla kolejki notatek ze status: captured. NIE jest tym skillem: audyt vaulta (→ knowledge_audyt), dodanie nowego tagu lub klastra (→ knowledge_rozszerzenie_taksonomii), monitoring listy źródeł (→ knowledge_przebieg_zwiadu), odpowiedź na pytanie Właściciela z istniejącej wiedzy (praca routera i person, nie ingest)."
type: skill
skill_type: procedure
used_by:
  - "[[katalizator]]"
  - "[[zwiadowca]]"
depends_on_artifacts:
  - "[[knowledge]]"
wymagany_odczyt:                    # ŚCIEŻKI (nie artefakty), po jednej linii, z komentarzem KTÓRY KROK tego wymaga
  - raw/                            # krok 1: pełny odczyt źródła
  - clusters/                       # krok 0 i 2: pula tagów z pól tags_owned wszystkich klastrów
  - wiki/                           # kroki 5 i 6a: sprzeczności; odczyt notatki docelowej przed linkiem zwrotnym
  - sources/                        # krok 0 (kolejka status: captured) i krok 5 (sprzeczności)
  - system/templates/               # kroki 4 i 6: template_source.md, template_wiki.md
  - outputs/knowledge/log.md        # krok 7: kotwica na końcu logu (odczyt wyłącznie końcówki)
# Świadomie NIEobecne w tym polu: system/agents/ (ocena, kto widzi nowe notatki, należy do
# knowledge_audyt_dostepow, nie do ingestu); moc/ (czytelne z mocy zasady dla każdej persony,
# ale żaden krok tej procedury go nie wymaga).
inputs: "TWARDE: ścieżka pliku w raw/ LUB notatka w sources/ ze status: captured (brak → pobierz kolejkę; kolejka pusta → zgłoś i zakończ). OPCJONALNE: wskazówka Właściciela, na co położyć nacisk — jej brak nie blokuje procedury."
output_format: "notatka w sources/ (status: processed) + propozycje inbox/knowledge/prop_*.md + linki zwrotne dopisane (append) w sekcjach „## Powiązane" notatek docelowych + wpis w outputs/knowledge/log.md (Edit z kotwicą) + podsumowanie na czacie"
version: 1.0
updated: 2026-09-05
---
# Kiedy używać
Nowy materiał trafił do `raw/` albo w `sources/` istnieje notatka ze `status: captured`. Skill uruchamia się na wprost zlecenie Właściciela („przetwórz to", „zrób ingest") lub w odgałęzieniu z `knowledge_przebieg_zwiadu` (krok 3 tamtej procedury), gdy [[zwiadowca]] zakwalifikował treść jako wartościową.

**NIE jest tym skillem** — testy rozstrzygające:
- *Czy zlecenie dotyczy JEDNEGO wskazanego materiału, który ma stać się wiedzą vaulta?* Tak → ten skill. Nie, chodzi o stan całego vaulta (sieroty, linki, sprzeczności) → `knowledge_audyt`.
- *Czy istniejąca pula tagów wystarcza, żeby opisać źródło bez naciągania?* Nie → STOP, `knowledge_rozszerzenie_taksonomii` (krok 0 niżej). Ten skill nigdy nie tworzy tagów ani klastrów.
- *Czy zadanie brzmi „sprawdź, co nowego w moich źródłach"?* → `knowledge_przebieg_zwiadu` (pętla zewnętrzna, która dopiero dobiera, co przetworzyć). Ingest jest pętlą wewnętrzną dla jednego materiału.
- *Czy Właściciel pyta o coś i chce odpowiedzi?* → to synteza z istniejącej wiedzy, praca routera i person; ingest nie odpowiada na pytania, tylko buduje wiedzę.

# Wymagane wejście
- **Twarde:** ścieżka do pliku źródłowego w `raw/` LUB notatka w `sources/` ze `status: captured`. Jeśli nie podano — pobierz kolejkę: Grep po `sources/` za `status: captured`. Jeśli kolejka pusta — zgłoś to jednym zdaniem i zakończ; pusta kolejka to poprawny wynik, nie porażka.
- **Opcjonalne:** wskazówka Właściciela, na co położyć nacisk. Jej brak nie blokuje procedury i nie zastępujesz jej własnym domysłem o priorytetach.
- Wszystko czytane na żywo z plików, nie z pamięci o tym, „co zwykle jest w klastrach".

# Podstawa metodyczna (Grounding)
Vault startowy nie zawiera poniższych notatek; do czasu ich ingestu kroki wykonuj z oznaczeniem `[wiedza własna modelu]` w podsumowaniu. Pozycje są slotami do wypełnienia przez przewodnika lub Właściciela po pierwszych ingestach literatury o pracy z wiedzą.
- {{UZUPEŁNIJ: notatka o mechanice systemu notatek Luhmanna (Zettelkasten)}} → krok 6 — zasada atomowości (jedna idea = jedna strona) i wartość powstająca z ŁĄCZENIA notatek: propozycje mają linki wychodzące wpisane w treść, nie luzem na końcu.
- {{UZUPEŁNIJ: notatka o trzech typach notatek (chwilowe / literaturowe / stałe)}} → kroki 4 i 6 — rozdział notatki źródłowej (literaturowej, w `sources/`) od stron koncepcji (stałych, w `wiki/`) jako dwa różne artefakty destylacji.
- {{UZUPEŁNIJ: notatka o przepływie od czytania do pisania własnymi słowami}} → kroki 1 i 6 — czytanie całości i przepisanie WŁASNYMI słowami jako test zrozumienia; chroni przed kopiowaniem streszczeń autora.
- {{UZUPEŁNIJ: notatka o oddolnym wzroście taksonomii z treści}} → kroki 0, 2 i 6 — taksonomia rośnie z materiału, nie z góry; uzasadnia odgałęzienie do rozszerzenia taksonomii zamiast naciągania istniejącego tagu.

Podstawa normatywna kroków 6, 6a i 8 (miejsce propozycji, wyjątek linków zwrotnych, akt podpisu): [[access_map]] oraz [[knowledge]].

# Procedura
0. **Test klastra — zanim cokolwiek przeczytasz do końca.** Przejrzyj `clusters/` (nazwy i pola `summary` / `tags_owned`). Jeśli w `clusters/` nie ma klastra, do którego to źródło w ogóle należy (nie „pasuje idealnie", tylko „należy do tej dziedziny") → **STOP** → uruchom `knowledge_rozszerzenie_taksonomii` i wróć tutaj po decyzji Właściciela. Vault startowy ma dwa klastry przykładowe ([[Wydajność i Skupienie]], [[Przywództwo i Decyzje]]) — w pierwszych tygodniach ten STOP będzie częsty i jest właściwym zachowaniem, nie przeszkodą.
1. **Przeczytaj CAŁE źródło** od początku do końca. Nie pracuj na fragmencie, spisie treści ani streszczeniu wydawcy. Grounding: {{UZUPEŁNIJ: notatka o przepływie od czytania do pisania własnymi słowami}}.
2. **Zbuduj pulę dozwolonych tagów:** Grep pól `tags_owned` ze wszystkich plików w `clusters/`. Dopasuj 1–3 tagi i klaster do treści źródła. **Tagi pochodzą WYŁĄCZNIE z tej puli** — żadnego tagu „przy okazji", żadnego tagu z pamięci. Jeśli klaster jest, ale żaden jego tag nie pasuje bez naciągania → przerwij i uruchom `knowledge_rozszerzenie_taksonomii`; wróć tu po decyzji. Grounding: {{UZUPEŁNIJ: notatka o oddolnym wzroście taksonomii z treści}}.
3. **Przedstaw Właścicielowi na czacie:** 3–5 kluczowych tez źródła, proponowaną taksonomię (klaster + tagi), dostrzeżone możliwości powiązań z istniejącymi notatkami. Czekaj na reakcję, jeśli Właściciel jest obecny; w odgałęzieniu z przebiegu zwiadu ten krok wykonuje się tak samo (tryb domyślny zwiadu jest interaktywny).
4. **Utwórz notatkę źródłową w `sources/`** wg `system/templates/template_source.md` (nazwa: małe litery, łączniki; frontmatter kompletny; `status: processed`; `distilled_to:` puste albo z linkami do proponowanych stron, które na razie leżą jako `prop_*` w inboxie — ten stan jest zamierzony). Grounding: {{UZUPEŁNIJ: notatka o trzech typach notatek (chwilowe / literaturowe / stałe)}}.
4a. **GRANICE KOMPRESJI — jawna deklaracja cięcia.** Wypełnij sekcję „## Granice kompresji" notatki źródłowej TREŚCIĄ Z TEGO ŹRÓDŁA (nie boilerplatem): (a) co świadomie pominięto i dlaczego (wątki, rozdziały, zastrzeżenia autora); (b) gdzie oryginał niuansuje mocniej, niż oddaje notatka (teza w oryginale warunkowa, w notatce brzmi ogólnie); (c) twierdzenia, których nie da się zweryfikować bez powrotu do oryginału — każde z lokalizacją (strony/rozdział egzemplarza, którego paginację cytujesz). Cel: ciche cięcie jest głównym mechanizmem propagacji błędu pierwotnego po ingeście; granica kompresji zamienia je w cięcie jawne, które tryb wierności `knowledge_audyt` umie skontrolować. Jeśli niczego nie pominięto (źródło krótkie, wchłonięte w całości) — napisz to wprost jednym zdaniem; sekcja nigdy nie zostaje pusta.
5. **Sprawdź sprzeczności:** Grep `wiki/` i `sources/` po kluczowych pojęciach źródła. Jeśli nowe źródło przeczy istniejącemu twierdzeniu — udokumentuj wg zasad [[knowledge]]: znacznik `[CONTRADICTION]`, obie strony sporu z cytowaniem, bez rozstrzygania.
6. **Przygotuj propozycje do `inbox/knowledge/`:** strony koncepcji dla głównych idei (wg `template_wiki.md`), z linkami WYCHODZĄCYMI do istniejących notatek wpisanymi wprost w treść. Każda propozycja = osobny plik `inbox/knowledge/prop_[nazwa].md`. Grounding: {{UZUPEŁNIJ: notatka o mechanice systemu notatek Luhmanna (Zettelkasten)}}.
   **ŻELAZNA ZASADA MIEJSCA: każda propozycja powstaje JAKO PLIK W `inbox/knowledge/` z prefiksem `prop_` — i nigdzie indziej.** Zakazane bez wyjątków: pisanie „wersji finalnych" do katalogów tymczasowych, scratchpadów czy innych lokalizacji poza vaultem; nazywanie plików docelowymi slugami wiki zamiast `prop_`; przygotowywanie dla Właściciela komend, które przenoszą treść prosto do `wiki/`, `clusters/`, `moc/` lub `system/`. Powód nie jest techniczny, a ustrojowy: wg [[access_map]] **przeniesienie pliku z inboxa = podpis Właściciela**, czyli akt akceptacji treści. Propozycja przygotowana poza inboxem i przeniesiona jedną komendą zamienia ten podpis w mechaniczne wykonanie polecenia — obchodzi kontrolę, dla której cały mechanizm istnieje. Jeśli polityka `deny` w `.claude/settings.json` odmówi zapisu do `wiki/` — to NIE jest usterka do obejścia, to norma działająca poprawnie: zapisz propozycję w inboxie i zgłoś odmowę w podsumowaniu (krok 8).
6a. **LINKI ZWROTNE — wykonujesz je SAM (wyjątek 3a [[access_map]]).** Linki wychodzące z nowej propozycji to połowa powiązania; bez odnośnika w notatce DOCELOWEJ nowa strona zostaje sierotą, a graf rozpada się na wyspy. Dla KAŻDEJ istniejącej notatki `wiki/`, która powinna wskazywać na nową:
   a. **Przeczytaj notatkę docelową** — nie decydujesz o powiązaniu z nazwy pliku ani z tagów; masz pełny odczyt `wiki/` i masz z niego skorzystać.
   b. **Dopisz JEDNĄ linię** do sekcji „## Powiązane" narzędziem **Edit** (nigdy Write), techniką kotwiczenia jak w kroku 7: `old_string` = dokładny tekst ostatniej linii tej sekcji, `new_string` = ten sam tekst + nowa linia. Format wiążący: `- [[nazwa-nowej-notatki]] — uzasadnienie RELACJI.`
   c. **Uzasadnienie opisuje RELACJĘ, nie temat.** „— o skupieniu" jest za słabe. „— pokazuje odwrotny mechanizm: tam przerwanie kosztuje czas powrotu, tu jest planowanym punktem odpoczynku" jest właściwe. **TEST NAZWY PLIKU:** jeśli uzasadnienie dałoby się napisać z samej nazwy pliku, nie przeczytałeś notatki docelowej — linia wraca do poprawy. To jednocześnie dowód, że wyjątek nie zamienił się w automatyczne linkowanie po tytułach.
   d. **Granice tego kroku** (w sesji interaktywnej egzekwowane przeglądem `git diff wiki/` przez Właściciela po każdym ingeście — dlatego każda linia musi być obronna sama z siebie): wyłącznie append — zero modyfikacji i usuwania istniejących linii; wyłącznie wewnątrz „## Powiązane"; brak tej sekcji w pliku = NIE tworzysz jej, tylko zgłaszasz notatkę w podsumowaniu jako wymagającą ręcznego dopisku (utworzenie sekcji to zmiana struktury, nie append); zero edycji treści merytorycznej, frontmatteru (w tym `sources`/`distilled_to`) i zero sprostowań — te nadal idą jako propozycje przez `inbox/knowledge/`.
   e. **Powściągliwość:** dopisujesz linki zwrotne tylko tam, gdzie powiązanie jest realne i wynika z przeczytanej treści. Pięć trafnych linków jest warte więcej niż dwadzieścia mechanicznych; nadmiar zaszumia graf tak samo skutecznie, jak sieroty go rozspajają. Przy wątpliwości co do RELACJI — propozycja przez inbox, nie dopisek.
7. **Dopisz wpis do `outputs/knowledge/log.md` WYŁĄCZNIE narzędziem Edit** — nigdy Write całego pliku. Technika kotwiczenia na końcu pliku: odczytaj wyłącznie końcówkę (Read z offsetem blisko końca, np. ostatnie ~30 linii, albo Grep po ostatnim nagłówku `## [`) — nie wczytuj ani nie odtwarzaj całego pliku w żadnym kroku. Skopiuj dokładny tekst ostatniej linii i użyj go jako `old_string`; jako `new_string` podaj ten sam tekst + nowy wpis (format w Szablonie wyniku). Dlaczego: log rośnie z każdym przebiegiem, a pełny odczyt i ponowny zapis całego pliku ryzykuje cichą amputację historii, jeśli przy odtwarzaniu pominie się lub obetnie fragment — Edit z kotwicą eliminuje to ryzyko strukturalnie, bo nigdy nie przechodzi przez resztę pliku. Jedyny wyjątek: plik `log.md` jeszcze nie istnieje (pierwszy ingest w świeżym vaulcie) — wtedy utwórz go z nagłówkiem `# Log działu knowledge` i pierwszym wpisem; od drugiego wpisu obowiązuje wyłącznie Edit.
8. **Zwróć Właścicielowi podsumowanie:** link do notatki źródłowej; lista propozycji w inboxie (ścieżki `inbox/knowledge/prop_*`); **lista notatek, do których dopisano linki zwrotne (ścieżka + dopisana linia)** — to jest Twoje wejście do przeglądu `git diff wiki/`; notatki wymagające ręcznego dopisku (brak sekcji „## Powiązane"); tagi wszystkich nowych notatek (fakt, nie ocena — wejście do trybu lekkiego `knowledge_audyt_dostepow` u [[rekruter]], który sprawdza, czy nowa wiedza leży w klastrze widocznym dla właściwych person); wykryte sprzeczności. Jeśli któryś zapis został odrzucony polityką `deny` — zacytuj dokładną ścieżkę i komunikat odmowy jako fakt. W podsumowaniu NIE umieszczasz gotowych komend przenoszących treść do stref chronionych (`wiki/`, `clusters/`, `moc/`, `system/`) — decyzję o przeniesieniu i sam akt akceptacji (`narzedzia/akceptuj.py`, uruchamiany po słowie „akceptuję") wykonuje Właściciel lub przewodnik na jego polecenie, po przeczytaniu propozycji. Możesz natomiast wprost napisać, KTÓRE propozycje uważasz za gotowe i dlaczego (rekomendacja to nie egzekucja).

# Szablon wyniku
**Wpis w logu** (`outputs/knowledge/log.md`, append-only, grepowalne prefiksy):
```
## [RRRR-MM-DD] ingest | Tytuł źródła
- source: [[sources/nazwa-zrodla]]
- taksonomia: [[Klaster]] / #tag1 #tag2
- propozycje: inbox/knowledge/prop_..., prop_...
- linki zwrotne: wiki/notatka-a.md, wiki/notatka-b.md (N dopisanych) | brak
- ręczny dopisek wymagany: wiki/notatka-c.md (brak sekcji „## Powiązane") | brak
- sprzeczności: brak | [CONTRADICTION] z [[notatka]]
```
**Notatka źródłowa:** frontmatter i sekcje wg `template_source.md`, w tym obowiązkowa „## Granice kompresji" (krok 4a).
**Propozycje stron koncepcji:** frontmatter wg `template_wiki.md` (tagi wyłącznie z `tags_owned`), treść własnymi słowami z linkami wychodzącymi w tekście, na końcu sekcja „## Uzasadnienie propozycji" (2 zdania: dlaczego ta idea zasługuje na osobną stronę).

# Checklist przed oddaniem
- [ ] Krok 0 wykonany: klaster dla źródła istnieje w `clusters/` — albo procedura zatrzymała się na `knowledge_rozszerzenie_taksonomii`.
- [ ] Źródło przeczytane w całości, nie na próbce.
- [ ] Wszystkie tagi istnieją w `tags_owned` (zero tagów spoza puli, zero tagów „warunkowych" bez adnotacji z rozszerzenia taksonomii).
- [ ] Każde twierdzenie faktograficzne w propozycjach ma cytowanie (źródło: plik) wg [[knowledge]].
- [ ] Sekcja „## Granice kompresji" wypełniona treścią z TEGO źródła (pominięcia + niuanse + twierdzenia nieweryfikowalne, każde z lokalizacją) — nie boilerplate i nie pusta (krok 4a).
- [ ] Zero zapisów do `moc/`, `clusters/`, `system/` oraz do TREŚCI i frontmatterów `wiki/` — koncepty i sprostowania tylko jako propozycje w `inbox/knowledge/`.
- [ ] Linki zwrotne dopisane (krok 6a) dla każdego realnego powiązania: format `- [[nazwa]] — uzasadnienie relacji.`, wyłącznie append w „## Powiązane", notatka docelowa PRZECZYTANA.
- [ ] Żadne uzasadnienie linku zwrotnego nie dałoby się napisać z samej nazwy pliku (test z kroku 6c).
- [ ] Notatki bez sekcji „## Powiązane" zgłoszone w podsumowaniu, nie „naprawione" przez utworzenie sekcji.
- [ ] Zero plików propozycji poza vaultem — każda fizycznie leży w `inbox/knowledge/` z prefiksem `prop_`.
- [ ] Zero komend przenoszących do stref chronionych w podsumowaniu — przeniesienie z inboxa jest podpisem Właściciela, nie krokiem procedury.
- [ ] `raw/` nietknięte.
- [ ] Log zaktualizowany w tej samej pętli co notatka źródłowa, wyłącznie przez Edit z kotwicą na końcu pliku (krok 7) — zero Write całego `log.md` (poza utworzeniem pustego pliku przy pierwszym ingeście).
- [ ] Zgodność z [[knowledge]] (standard cytowania, znacznik sprzeczności) i [[access_map]] (miejsce propozycji, wyjątek 3a).
- [ ] Sekcja „Podstawa metodyczna" obecna; pozycje `{{UZUPEŁNIJ}}` nierozwiązane oznaczone w podsumowaniu jako `[wiedza własna modelu]`.

# Wzorcowy przykład
[uzupełnić pierwszym zaakceptowanym wynikiem — few-shot musi cytować realny, oceniony przebieg z outputs/router/log.md]

Oczekiwany kształt przykładu: wejście (nazwa źródła w `raw/`) → wynik kroku 0 (który klaster) → notatka źródłowa z cytatem sekcji „Granice kompresji" → 2 propozycje z inboxa → 2–3 dopisane linki zwrotne z uzasadnieniami, które przechodzą test nazwy pliku. Czego NIE powtarzać: zostanie dopisane po pierwszym przebiegu ocenionym poniżej 5.

# Stan akceptacji
Rozstrzygnięcia przyjęte z doświadczenia poprzednika (przepisane bezosobowo; szczegóły ślepych uliczek w [[Lekcje_Poprzednika]]):
- **Żelazna zasada miejsca** powstała po przebiegu, w którym persona — po poprawnej odmowie zapisu do `wiki/` — zapisała „wersje finalne" poza vaultem i przedstawiła gotowe komendy przenoszące. Granica została utrzymana technicznie, ale podpis zamieniłby się w mechaniczne wykonanie trzech komend. Stąd: propozycja wyłącznie w inboxie, zero komend przenoszących w podsumowaniu, rekomendacja „to jest gotowe" dozwolona.
- **Linki zwrotne jako obowiązek wykonawcy (wyjątek 3a)** — procedura początkowo przewidywała WYKRYCIE powiązań, ale nie ich naniesienie, bo wykonawca nie miał zapisu do `wiki/`. Nowe notatki wchodziły bez linków przychodzących i zostawały sierotami. Wyjątek został zawężony do appendu jednej linii w jednej sekcji, z testem nazwy pliku przeciw linkowaniu po tytułach.
- **Log przez Edit z kotwicą, nigdy Write całości** — log rośnie do setek kilobajtów, a odtworzenie całego pliku przez model ryzykuje cichą amputację historii. Kotwica na końcu eliminuje ryzyko strukturalnie.
- **Granice kompresji + tryb wierności po drugiej stronie** — ciche cięcie przy ingeście uznano za główny mechanizm propagacji błędu pierwotnego; jawna deklaracja cięcia w notatce daje audytowi coś do skontrolowania.
- **Tagi wyłącznie z `tags_owned`** — pula tagów jest własnością klastrów, nie ingestu; luka w puli to sygnał do rozszerzenia taksonomii przez inbox, nie do improwizacji.
- **W szablonie egzekucja granic zapisu przeniesiona z kontroli na poziomie narzędzia na politykę `deny` w `.claude/settings.json` + przegląd `git diff wiki/` przez Właściciela** — sesja jest zawsze interaktywna, więc przegląd diffu po każdym ingeście jest wykonalny i zastępuje kontrolę treściową na poziomie narzędzia.

# Historia zmian
- 2026-09-05 (v1.0): wersja szablonu — wyprowadzona z działającego systemu-poprzednika; treść osobista i infrastrukturalna usunięta, struktura i zasady zachowane.
