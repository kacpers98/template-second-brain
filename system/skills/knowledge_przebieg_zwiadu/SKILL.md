---
name: knowledge_przebieg_zwiadu
aliases: ["knowledge_przebieg_zwiadu"]              # plik nazywa się SKILL.md — alias pozwala linkować [[knowledge_przebieg_zwiadu]] w Obsidianie (lint R8)
description: "Procedura przebiegu monitoringu Lista_Zrodel_Zwiadowcy: dobór pozycji po terminie (last_checked + częstotliwość), przegląd źródła przez WebFetch, filtr wartości i nowości, odgałęzienie do knowledge_ingest dla treści wartościowych, aktualizacja WYŁĄCZNIE kolumny last_checked, raport przebiegu + wpis w logu. Tryb domyślny: interaktywny — Właściciel jest obecny w sesji. Używaj przy KAŻDYM zleceniu 'przeskanuj moje źródła', 'co nowego w obserwowanych źródłach', 'sprawdź listę monitoringu', 'zrób przebieg zwiadu'. NIE jest tym skillem: przetworzenie jednego wskazanego materiału (→ knowledge_ingest bezpośrednio), dopisanie adresu do listy źródeł (rejestr prowadzi Właściciel; tu tylko zgłaszasz kandydatów), kwartalny audyt portfela źródeł (→ knowledge_audyt_zrodel)."
type: skill
skill_type: procedure
used_by:
  - "[[zwiadowca]]"
depends_on_artifacts:
  - "[[Lista_Zrodel_Zwiadowcy]]"
  - "[[knowledge]]"
wymagany_odczyt:                    # ŚCIEŻKI, po jednej linii, z komentarzem KTÓRY KROK tego wymaga
  - system/artifacts/Lista_Zrodel_Zwiadowcy.md   # krok 1 i 4: dobór pozycji po terminie; aktualizacja last_checked
  - wiki/                           # krok 2d: filtr dublowania (Grep po kluczowych pojęciach)
  - sources/                        # krok 2d: deduplikacja przed syntezą
  - clusters/                       # krok 2d i 3: tagi z kolumny „Zakres tematyczny" vs pula tags_owned
  - outputs/knowledge/              # krok 5 (raport), krok 7 (log), sekcja „Kandydaci do usunięcia?" (poprzednie raporty *_zwiad.md)
# Świadomie NIEobecne: raw/ — zwiad czyta źródła z sieci, nie z plików lokalnych; jeśli treść wymaga
# zapisu pliku przed ingestem, robi to odgałęzienie do knowledge_ingest wg jego reguł.
inputs: "brak wymaganego wejścia — przebieg startuje z [[Lista_Zrodel_Zwiadowcy]]. OPCJONALNE: zawężenie do wskazanych pozycji listy ('sprawdź tylko X i Y'); wskazówka, na co zwrócić uwagę. Tryb: interaktywny (domyślny i jedyny obecnie wspierany)."
output_format: "propozycje inbox/knowledge/prop_*.md + linki zwrotne (przez odgałęzienie do knowledge_ingest, krok 6a) + raport outputs/knowledge/RRRR-MM-DD_zwiad.md (kolizja → _02) w stałej numeracji sekcji 1–7 + wpis w outputs/knowledge/log.md; przypadek zerowy = raport jednolinijkowy"
version: 1.0
updated: 2026-09-05
---
# Kiedy używać
Każdy przebieg monitoringu zwiadowcy, wywołany przez Właściciela na czacie („przeskanuj moje źródła", „co nowego w obserwowanych tematach"). To ZEWNĘTRZNA pętla: dobiera, które pozycje z rejestru w ogóle sprawdzić, i rozlicza wynik przebiegu (raport, log, aktualizacja terminów). Samo przetwarzanie POJEDYNCZEGO zakwalifikowanego źródła na notatkę i propozycje wykonuje `knowledge_ingest`, wywoływany stąd jako krok 3, nie duplikowany.

**Tryb domyślny: interaktywny** — Właściciel jest obecny w sesji, czyta tezy przed zapisem (krok 3 ingestu) i widzi raport od razu. **Tryb cykliczny (przebieg bez Właściciela, uruchamiany z harmonogramu) to opcja PRZYSZŁA, dziś niewspierana:** gdyby kiedyś powstał, wymagałby osobnego zaostrzenia (pominięcie prezentacji tez z zapisem ich do raportu; przy wątpliwości co do linku zwrotnego — propozycja przez inbox zamiast dopisku; brak zgody na rozszerzenie taksonomii = tagowanie warunkowe bez czekania) oraz decyzji Właściciela o mechanizmie uruchamiania — nie zakładaj jego istnienia i nie projektuj kroków „na wypadek, gdyby nikt nie czytał".

**NIE jest tym skillem** — testy rozstrzygające:
- *Czy Właściciel wskazał JEDEN konkretny materiał, o którym już wie?* → `knowledge_ingest` bezpośrednio, bez przechodzenia przez dobór terminów.
- *Czy zlecenie brzmi „dodaj stronę X do obserwowanych"?* → rejestr prowadzi Właściciel; zwiadowca w tym skillu wyłącznie ZGŁASZA kandydatów w raporcie.
- *Czy pytanie brzmi „czego brakuje w mojej wiedzy" albo „które źródła są martwe"?* → `knowledge_audyt_zrodel` (kwartalny przegląd całego portfela). Ten skill odwiedza pozycje po terminie, nie ocenia portfela.
- *Czy treść nie mieści się w taksonomii?* → `knowledge_rozszerzenie_taksonomii`, jako odgałęzienie z kroku 3, nie osobne wywołanie.

# Wymagane wejście
Żadne — procedura sama wczytuje [[Lista_Zrodel_Zwiadowcy]] i sama ustala, co jest do zrobienia. Opcjonalnie: zawężenie do wskazanych pozycji albo wskazówka, na co zwrócić uwagę. Listę czytasz na żywo w tym przebiegu — liczba pozycji, ich częstotliwości i daty `last_checked` nie są znane z góry. W świeżym vaulcie lista jest pustym wzorcem: jeśli nie ma w niej żadnej pozycji, zakończ jednym zdaniem i zaproponuj Właścicielowi, jak ją wypełnić (instrukcja w samym artefakcie).

# Podstawa metodyczna (Grounding)
`brak — podstawa normatywna, nie epistemiczna: [[Lista_Zrodel_Zwiadowcy]] (zamknięta pula adresów, kadencje, jedyna dozwolona modyfikacja: last_checked)`. Procedura jest pętlą monitoringu normy; ocena wartości treści odgałęzia się do `knowledge_ingest`, który ma własny Grounding.

# Procedura
1. **Wczytaj [[Lista_Zrodel_Zwiadowcy]] i wyznacz pozycje do sprawdzenia.** Dla KAŻDEJ pozycji: `last_checked` puste (nigdy niesprawdzane) → PO TERMINIE; `last_checked` + wartość z kolumny „Częstotliwość" < dziś → PO TERMINIE; w przeciwnym razie → pomiń (częstotliwość to minimalny odstęp, nie sugestia — nie odwiedzaj „na wszelki wypadek"). Zbierz listę pozycji po terminie **i zapisz pełną tabelę rozliczenia terminów** (wszystkie pozycje: częstotliwość / last_checked / termin / status) — trafi do raportu jako dowód, dlaczego sprawdzono właśnie te.
   - Jeśli lista po terminie jest pusta → przejdź od razu do kroku 6 (przypadek zerowy), pomijając kroki 2–5 w całości.
2. **Dla każdej pozycji po terminie, pojedynczo** (błąd jednej nie może zablokować pozostałych):
   a. Spróbuj przejrzeć treść źródła opublikowaną po `last_checked` (od zawsze, jeśli puste). Narzędzie: **WebFetch** na adresie z rejestru (i na podstronach-listingach, jeśli pozycja je wskazuje). Do artykułów wchodzisz WYŁĄCZNIE adresami odczytanymi z listingu — **zakaz zgadywania slugów, ścieżek archiwum i map witryny**: wiele serwisów przekierowuje nieznane ścieżki na stronę główną bez błędu 404, więc odpowiedź wygląda na poprawną, choć dotyczy innej strony (sygnał ostrzegawczy: tytuł i treść identyczne ze stroną główną). REGUŁA: wyzwanie JS/anty-bot ≠ paywall — pierwsze to niedostępność techniczna (2b), drugie granica (2c).
   b. **Przypadek brzegowy — źródło niedostępne** (błąd sieci, 404, blokada renderowania, strona zmieniła strukturę): NIE aktualizuj `last_checked` tej pozycji (nie udawaj, że sprawdzono coś, czego nie sprawdzono); odnotuj w raporcie jako „niedostępne" + krótki powód; przejdź do następnej pozycji. Zero ponawiania w pętli.
   c. **Przypadek brzegowy — paywall / wymaga logowania:** odnotuj w raporcie jako „paywall"; **NIE próbuj żadnego obejścia** (scraper, cache, archiwum, kopie) — paywall to granica, nie wyzwanie; NIE aktualizuj `last_checked`; przejdź dalej. Drugie wystąpienie tego samego paywalla w kolejnych przebiegach → rekomendacja zmiany trybu monitoringu (ręczny przegląd przez Właściciela / usunięcie z listy) w sekcji „Kandydaci do usunięcia?", decyzja Właściciela.
   d. **Jeśli źródło dostępne: filtr wartości** — (i) czy treść pasuje do tagów z kolumny „Zakres tematyczny" tej pozycji (tagi muszą istnieć w `tags_owned` klastrów) lub wnosi coś do taksonomii vaulta; (ii) czy nie dubluje wiedzy już obecnej w `wiki/` i `sources/` (Grep po kluczowych pojęciach, z jawnym potwierdzeniem „net-new" per teza). Przy wątpliwości: POMIŃ i odnotuj powód w raporcie — lepiej przegapić niż zaśmiecić inbox. Gdy jedno źródło ma kilka wartościowych pozycji, zsyntetyzuj najbardziej wyróżniającą się, resztę zgłoś jako kandydatów na kolejny przebieg — żeby nie przeważać jednym autorem.
3. **Dla treści zakwalifikowanych jako wartościowe: wykonaj `knowledge_ingest`** od jego kroku 0 (test klastra) i dalej w całości, łącznie z krokiem 3 (prezentacja tez Właścicielowi na czacie przed zapisem).
   - Brak klastra lub tagu → odgałęzienie do `knowledge_rozszerzenie_taksonomii`; czekaj na decyzję Właściciela, jak w każdym ingeście.
   - **Krok 6a `knowledge_ingest` (linki zwrotne) OBOWIĄZUJE także tutaj** — wyjątek 3a [[access_map]] obejmuje [[zwiadowca]] imiennie; dopisujesz odnośniki do sekcji „## Powiązane" notatek docelowych, zamiast zostawiać nową wiedzę jako sierotę. Przy wątpliwości co do RELACJI (nie tematu) — propozycja przez inbox, nie dopisek. Notatki bez sekcji „## Powiązane" zgłaszasz w raporcie do ręcznego dopisku; odmowa polityki `deny` to zachowanie poprawne, nie usterka.
   - **Zestawienie tagów** nowych notatek zbierasz na bieżąco — trafia do raportu (sekcja 6) jako fakt.
4. **Zaktualizuj `last_checked` WYŁĄCZNIE dla pozycji faktycznie sprawdzonych** w krokach 2a–2d do końca (źródło było dostępne, niezależnie od tego, czy treść zakwalifikowano czy pominięto w filtrze wartości) — ustaw na dzisiejszą datę. Pozycje niedostępne, zablokowane paywallem lub pominięte w kroku 1 z powodu niewygasłego terminu NIE są aktualizowane. To jedyna dozwolona modyfikacja artefaktu i dotyczy wyłącznie tej jednej kolumny; wykonujesz ją narzędziem Edit na dokładnej komórce, nigdy Write całego pliku. Jeśli polityka zapisu odmówi — dołącz do raportu gotowy do naniesienia fragment („patch": pozycja → nowa data) i zgłoś odmowę jako fakt; nie obchodź granicy.
5. **Zbuduj i zapisz raport przebiegu** w `outputs/knowledge/RRRR-MM-DD_zwiad.md` wg szablonu niżej.
6. **Przypadek zerowy** (lista z kroku 1 była pusta): zapisz jednolinijkowy raport „brak źródeł do sprawdzenia dzisiaj (najbliższy termin: [źródło] za [X] dni)" wraz z tabelą rozliczenia terminów — NIE wymyślaj pracy, nie odwiedzaj niczego „żeby coś zrobić". Krótki przebieg to poprawny wynik, nie porażka.
7. **Dopisz wpis do `outputs/knowledge/log.md`** (append-only, ten sam plik co katalizator) WYŁĄCZNIE narzędziem Edit — nigdy Write całego pliku. Technika kotwiczenia na końcu pliku: odczytaj wyłącznie końcówkę (Read z offsetem blisko końca, np. ostatnie ~30 linii, albo Grep po ostatnim nagłówku `## [`) — nie wczytuj ani nie odtwarzaj całego pliku. Skopiuj dokładny tekst ostatniej linii jako `old_string`; jako `new_string` podaj ten sam tekst + nowy wpis: `## [RRRR-MM-DD] zwiad | X sprawdzonych (z Y w rejestrze) | Z syntez | W pominięć | V niedostępnych/paywall`. Dlaczego: log rośnie z każdym przebiegiem, a odtworzenie całego pliku ryzykuje cichą amputację historii — Edit z kotwicą eliminuje to ryzyko strukturalnie. Technika identyczna jak w `knowledge_ingest` (krok 7); oba skille piszą do tego samego logu i muszą jej używać tak samo.

# Szablon wyniku
Raport: `outputs/knowledge/RRRR-MM-DD_zwiad.md` (kolizja → `_02`), frontmatter wg `template_output.md` (`type: output`, `agent: zwiadowca`, `task: przebieg monitoringu`, `date`, `head: "[[knowledge]]"`, `linked_sources`, `status`). Sekcje w stałej numeracji (pusta = „brak" — nieobecność JEST informacją, sekcji nie usuwaj):
```
## 1. Rozliczenie terminów (tabela: pozycja → częstotliwość → last_checked → termin → status: sprawdzona / niewymagalna / niedostępna / paywall)
## 2. Zsyntetyzowane (linki do notatek w sources/ + propozycje w inbox/knowledge/prop_*)
## 3. Pominięte (tytuł + jednolinijkowy powód: nie pasuje do taksonomii / dubluje istniejącą wiedzę / poniżej progu jakości / odłożone, by nie przeważać jednym autorem)
## 4. Niedostępne / paywall (tytuł + powód; jawnie: „last_checked NIE zaktualizowano")
## 5. Kandydaci do usunięcia lub aktualizacji? (martwe/przeniesione — przy nawrocie, nie po jednym wystąpieniu; rebrand/nowa domena = kandydat do AKTUALIZACJI adresu, nie usunięcia)
## 6. Linki zwrotne i tagi nowych notatek (ścieżka + dopisana linia; notatki wymagające ręcznego dopisku; zestawienie `plik → tagi` w formie mechanicznie przetwarzalnej — fakt, bez oceny pokrycia person)
## 7. Wykryte sprzeczności (wg [[knowledge]]: znacznik [CONTRADICTION], obie strony, bez rozstrzygania; napięcie interpretacyjne ≠ sprzeczność — nazwij je, nie oznaczaj) — albo „brak"
```
Przypadek zerowy: jedna linia + sekcja 1 zamiast pełnej struktury (krok 6).

# Checklist przed oddaniem
- [ ] Każda pozycja z minionym terminem (krok 1) została albo sprawdzona, albo jawnie odnotowana jako niedostępna/paywall — żadna nie zniknęła bez śladu; tabela rozliczenia terminów w raporcie.
- [ ] Trzy rodzaje „niesprawdzonych" rozróżnione: niewymagalna (termin nieminiony) / pominięta w filtrze wartości (dostępna, treść poniżej progu) / niedostępna lub paywall.
- [ ] `last_checked` zaktualizowany WYŁĄCZNIE dla pozycji faktycznie dostępnych i sprawdzonych do końca — zero aktualizacji zbiorczych; zmiana tylko w tej jednej kolumnie, przez Edit.
- [ ] Zero prób obejścia paywalla — bez wyjątków.
- [ ] Zero zgadywania adresów — każdy odwiedzony artykuł ma adres odczytany z listingu lub z rejestru.
- [ ] Przypadek zerowy zakończony jedną linią + tabelą terminów, bez wymyślonej pracy.
- [ ] Każda propozycja treści przeszła przez `knowledge_ingest` (od kroku 0) — zero własnego, równoległego formatu syntez w tym skillu.
- [ ] Linki zwrotne dopisane wg kroku 6a `knowledge_ingest` i wymienione w raporcie; notatki bez sekcji kanonicznej zgłoszone, nie „naprawione" utworzeniem sekcji.
- [ ] Zestawienie `plik → tagi` obecne dla WSZYSTKICH nowych notatek — bez oceny pokrycia person.
- [ ] Raport i log zaktualizowane w tej samej pętli, log wyłącznie przez Edit z kotwicą (krok 7).
- [ ] Zgodność z [[Lista_Zrodel_Zwiadowcy]] (żadna modyfikacja poza `last_checked`) i [[knowledge]] (standard sprzeczności); sekcja „Podstawa metodyczna" obecna (postać normatywna).

# Wzorcowy przykład
[uzupełnić pierwszym zaakceptowanym wynikiem — few-shot musi cytować realny, oceniony przebieg z outputs/router/log.md]

Docelowo dwa przebiegi: jeden bogaty (kilka pozycji po terminie, co najmniej jedna synteza, jedno pominięcie z powodem, jedna niedostępność bez aktualizacji `last_checked`) i jeden zerowy (kompletny raport bez ani jednej syntezy — z tabelą terminów i wskazaniem najbliższej wymagalnej daty). Zachowania, które przykład ma pokazać: rozliczenie terminów udokumentowane, nie tylko zastosowane; paywall jako granica; nawrót niedostępności zgłoszony jako kandydat, nie zniesiony samowolnie; rebrand źródła jako kandydat do aktualizacji, nie usunięcia; deduplikacja przed syntezą z potwierdzeniem „net-new"; napięcie interpretacyjne nazwane, nie oznaczone jako sprzeczność.

# Stan akceptacji
Rozstrzygnięcia przyjęte z doświadczenia poprzednika (bezosobowo; szczegóły w [[Lekcje_Poprzednika]]):
- **Nie aktualizuj `last_checked`, gdy nie sprawdzono.** Data w tej kolumnie jest jedynym dowodem, że źródło zostało obejrzane; aktualizacja zbiorcza „bo przebieg się odbył" niszczy ten dowód i ukrywa martwe źródła na wiele cykli.
- **Trzy różne „niesprawdzone" muszą być rozróżnione** (niewymagalne / pominięte w filtrze / niedostępne). Zlanie ich w jedną kategorię zaciera obraz i psuje `last_checked`.
- **Paywall to granica, nie wyzwanie; zero obejść.** U poprzednika istniał wyjątek dla źródeł, do których Właściciel miał opłacony dostęp, obsługiwany osobnym narzędziem — w szablonie ta gałąź została usunięta w całości, bo wymaga infrastruktury poza sesją; reguła bazowa zostaje bez ustępstw.
- **Zakaz zgadywania adresów** — serwisy przekierowujące nieznane ścieżki na stronę główną zwracają odpowiedź, która wygląda na poprawną i jest cicho fałszywa. Do treści wchodzi się wyłącznie adresami odczytanymi z listingu.
- **Przebieg zerowy jest poprawnym wynikiem; częstotliwość to minimalny odstęp, nie sugestia.** Wymyślanie pracy „żeby coś zrobić" zaśmieca inbox i fałszuje statystyki źródeł.
- **Tryb domyślny w szablonie: interaktywny.** Poprzednik zakładał domyślnie tryb bez człowieka, bo taki miał mechanizm uruchamiania; szablon nie ma takiego mechanizmu, więc bezpieczniejsze założenie odwraca się — Właściciel jest obecny, a tryb cykliczny pozostaje opcją przyszłą opisaną w „Kiedy używać".

# Historia zmian
- 2026-09-05 (v1.0): wersja szablonu — wyprowadzona z działającego systemu-poprzednika; treść osobista i infrastrukturalna usunięta, struktura i zasady zachowane.
