---
name: knowledge_audyt_zrodel
aliases: ["knowledge_audyt_zrodel"]              # plik nazywa się SKILL.md — alias pozwala linkować [[knowledge_audyt_zrodel]] w Obsidianie (lint R8)
description: "Procedura kwartalnego audytu strategicznego pokrycia wiedzy i portfela źródeł: mapa tagi-vs-liczba notatek z trendem od poprzedniego audytu, waga luki w trzech poziomach (test dwuczłonowy: dostęp klastrowy persony wg [[access_map]] + głód całoklastrowy; człon 'tag nazwany wprost w definicji persony' jako wzorzec uśpiony z wyzwalaczem), status źródeł z Lista_Zrodel_Zwiadowcy (martwe vs nieproduktywne jako kandydaci do usunięcia), maksymalnie 5 nowych źródeł uzasadnionych per luka, rekomendacje w trzech koszykach wg zasady 'synteza przed zakupami'. Używaj przy zleceniu 'zrób audyt źródeł', 'czego brakuje w wiedzy', 'przejrzyj listę źródeł' oraz cyklicznie raz na kwartał. NIE jest tym skillem: health-check strukturalny (→ knowledge_audyt), rutynowy monitoring źródeł (→ knowledge_przebieg_zwiadu)."
type: skill
skill_type: procedure
used_by:
  - "[[zwiadowca]]"
depends_on_artifacts:
  - "[[access_map]]"
  - "[[Lista_Zrodel_Zwiadowcy]]"
wymagany_odczyt:                    # ŚCIEŻKI wymagane przez procedurę, po jednej linii, z komentarzem KTÓRY KROK
  - clusters/                       # krok 1: tags_owned wszystkich klastrów (czytelne dla każdej persony)
  - wiki/                           # krok 1: zliczanie notatek per tag
  - system/access_map.md            # krok 2 człon A: kolumna zasięgu klastrowego person jako jedyne źródło prawdy o zasięgu
  - outputs/knowledge/              # kroki 1 i 3: własne poprzednie raporty audyt_*.md (trend) i *_zwiad.md (status źródeł); krok 6: log
  - sources/                        # krok 5: koszyk „synteza z posiadanego"
# system/agents/ NIE jest tu wymieniony ŚWIADOMIE: krok 2 człon B (tag nazwany wprost w definicji
# persony) jest kryterium UŚPIONYM z jawną klauzulą degradacji — pole opisuje odczyty bezwarunkowe.
# Gdyby Właściciel kiedyś nadał ten odczyt, dopisz tu ścieżkę w tym samym akcie co zmianę mapy.
inputs: "brak wymaganego wejścia — audyt sam buduje mapę pokrycia z clusters/ i wiki/. OPCJONALNE: poprzedni audyt z outputs/knowledge/audyt_*.md do porównania trendu (brak → trend = 'pierwszy audyt, brak punktu odniesienia')."
output_format: "raport outputs/knowledge/audyt_RRRR-QN.md (drugi w tym samym kwartale → _02) z mapą pokrycia, wagą luk, statusem źródeł i rekomendacjami w trzech koszykach; sekcje 1–5 w stałej numeracji + wpis w outputs/knowledge/log.md"
version: 1.0
updated: 2026-09-05
---
# Kiedy używać
Cykliczny audyt strategiczny, rytm KWARTALNY (wiersz w [[Rejestr_Cyklow]]) albo wprost zlecenie Właściciela. Skill odpowiada na pytanie „czego nam brakuje i skąd to wziąć".

**NIE jest tym skillem** — testy rozstrzygające:
- *Czy pytanie dotyczy integralności technicznej (sieroty, zepsute linki, sprzeczności, zgodność z szablonami)?* → `knowledge_audyt`. Ten skill nie sprawdza, czy vault jest spójny, tylko czy jest KOMPLETNY względem potrzeb person.
- *Czy pytanie brzmi „co nowego pojawiło się w obserwowanych źródłach"?* → `knowledge_przebieg_zwiadu` (monitoring pojedynczych źródeł wg ich częstotliwości). Ten skill patrzy na cały portfel raz na kwartał, nie na pojedyncze adresy co tydzień.
- *Czy zlecenie brzmi „dodaj źródło X do listy"?* → rejestr prowadzi Właściciel; tu tylko REKOMENDUJESZ dodanie w koszyku „źródło cykliczne".
- *Czy pytanie brzmi „czy persona X widzi klaster Y"?* → `knowledge_audyt_dostepow`. Tu czytasz mapę, żeby ZWAŻYĆ lukę, nie żeby ją audytować.

# Wymagane wejście
Brak — audyt sam buduje mapę z `clusters/` i `wiki/`. Opcjonalnie: poprzedni audyt z `outputs/knowledge/audyt_*.md` do porównania trendu (krok 1) — jeśli brak, trend = „pierwszy audyt, brak punktu odniesienia". Liczbę tagów, klastrów i notatek ustalasz na żywo w tym przebiegu — nie zakładaj żadnej z nich z góry ani z poprzedniego raportu.

# Podstawa metodyczna (Grounding)
`brak — podstawa normatywna, nie epistemiczna: [[Lista_Zrodel_Zwiadowcy]] (portfel źródeł i jego reguły), [[access_map]] (kolumna zasięgu klastrowego jako składnik testu wagi luki)`. Mapa pokrycia i test dwuczłonowy wagi luki to metodyka własna systemu, zdefiniowana w tym skillu i artefaktach — nie metoda z literatury.

# Procedura
**1. Mapa pokrycia: tagi vs liczba notatek, z trendem.** Zbuduj listę wszystkich tagów z pola `tags_owned` WSZYSTKICH klastrów (`clusters/*.md`). Dla każdego tagu policz notatki w `wiki/` noszące ten tag (Grep po polu `tags`). Wypisz tagi CIENKIE (≤3 notatki). W świeżym vaulcie cienkie będą wszystkie — to poprawny wynik pierwszego audytu, nie alarm; wartość pojawia się od drugiego audytu, gdy widać trend. Znajdź NAJNOWSZY poprzedni raport `outputs/knowledge/audyt_*.md` — jeśli istnieje, dla każdego cienkiego tagu porównaj z jego stanem w tamtym audycie: nowo cienki / wciąż cienki bez zmiany / poprawił się (ale wciąż ≤3) / nie dotyczy (pierwszy audyt). **Trend liczysz WYŁĄCZNIE dla liczby notatek** — ta metryka jest ciągła przez całą serię. Wag z kroku 2 w trend NIE zestawiaj wstecz (patrz nota o nieporównywalności).

**2. Zestawienie z potrzebami person — waga luki (test dwuczłonowy, trzy poziomy).** Dla KAŻDEGO cienkiego tagu ustal klaster-właściciel (klaster, w którego `tags_owned` figuruje ten tag), po czym rozważ dwa niezależne człony:

   - **Człon A — dostęp klastrowy (kto ma ten materiał w zasięgu).** W kolumnie zasięgu klastrowego [[access_map]] — jedynym źródle prawdy o zasięgu — znajdź persony, których lista obejmuje klaster-właściciela. **Persony z zasięgiem `all` są z ważenia WYŁĄCZONE**: obejmują każdy klaster, więc występują przy KAŻDYM cienkim tagu i z definicji nie różnicują wagi. Odnotuj je w raporcie jednym zdaniem („materiał czytelny dla X, waga bez zmiany"), nie w tabeli wag. Czytaj wyłącznie mapę — **kontrola zgodności pola `cluster_access` w definicjach person NIE należy do tego audytu** (robi ją lint i `knowledge_audyt_dostepow`), a odczyt `system/agents/` jest poza zasięgiem wykonawcy i w tym przebiegu ZABRONIONY.
   - **Człon B — zadeklarowana potrzeba tagowa (kto nazywa ten tag wprost w swojej definicji). STATUS: KRYTERIUM UŚPIONE — NIE WYKONUJ.** Wzorzec zostaje w procedurze jako zapis kryterium: trafienie liczyłoby się, gdy tag występuje w treści roboczej definicji persony („Rola", „Źródła wiedzy", „Proces pracy", „Granice"), z pominięciem „Historii zmian". Kryterium jest uśpione, bo pomiar u poprzednika pokazał, że jest praktycznie zawarte w członie A (listy zasięgu klastrowego powstały z tych samych deklaracji) i nie rozdzielało ani jednego cienkiego tagu — a jego wykonanie wymagałoby nadania wykonawcy odczytu definicji person. **WYZWALACZ obudzenia:** pierwszy audyt, w którym nazwanie tagu wprost rozdzieliłoby coś, czego nie rozdziela dostęp klastrowy — wtedy zgłoś to w sekcji „Materiał dla metodyka" raportu jako wniosek o nadanie odczytu i uruchomienie członu B. Do tego czasu ważysz wg gałęzi niżej.

   **Poziomy wagi (gałąź obowiązująca — człon B uśpiony):** **WYSOKA** — istnieje konsument zawężony (persona z klastrem-właścicielem w zasięgu, nie `all`) ORAZ zachodzi głód całoklastrowy (WSZYSTKIE tagi klastra-właściciela cienkie: persona ma klaster w zasięgu i nie ma w nim na czym pracować). **ŚREDNIA** — istnieje konsument zawężony, ale klaster-właściciel jest skądinąd zasilony (luka lokalna). **NISKA** — brak konsumenta zawężonego. Przy każdej pozycji wskaż KTÓREJ persony dotyczy i z którego członu wynika. Oznacz KAŻDĄ pozycję tabeli dopiskiem „człon B uśpiony" i odnotuj stan w sekcji rozjazdów raportu — ważenie podane bez tej informacji wygląda w kolejnym audycie jak wynik pełnego testu dwuczłonowego.

   **Poziomy wagi (gałąź pełna — tylko gdyby człon B został obudzony):** WYSOKA — zachodzą OBA człony; ŚREDNIA — dokładnie jeden; NISKA — żaden.

   **Klucz porządkujący WEWNĄTRZ jednego poziomu wagi** (bez niego krok 5 nie ma czym uszeregować luk, które trafiły w ten sam poziom — stan typowy, nie wyjątkowy): (a) liczba konsumentów zawężonych — malejąco; (b) liczba notatek z kroku 1 — rosnąco; (c) flaga „głód całoklastrowy" — **na gałęzi obowiązującej POMIJASZ**, bo wchodzi do samej wagi i zastosowana dwa razy niczego nie rozdziela. Klucz zapisz w raporcie jawnie, tak jak wagę.

   **NOTA O NIEPORÓWNYWALNOŚCI WAG — obowiązkowa, gdy w serii raportów zmienił się mechanizm ważenia.** Zmiana wagi bez zmiany liczby notatek NIE jest sygnałem o wiedzy, tylko artefaktem normy — i tak ją opisuj. Porównuj wagi wyłącznie między audytami wykonanymi wg tej samej wersji skilla; przy zmianie wersji zaznacz w raporcie, od którego audytu seria jest porównywalna.

**3. Status źródeł z [[Lista_Zrodel_Zwiadowcy]].** Dla każdej pozycji w rejestrze sprawdź dwa oddzielne stany:
   - **Martwe/przeniesione** — błąd dostępu w ostatnich przebiegach `knowledge_przebieg_zwiadu` (sprawdź ostatnie raporty `outputs/knowledge/*_zwiad.md`).
   - **Nieproduktywne** — źródło DOSTĘPNE, ale zero wartościowych syntez od N=3 kolejnych przebiegów. To INNA kategoria niż martwe: sygnał „źródło już nie wnosi tego, co wnosiło", nie awaria techniczna. Rozróżniaj przy tym „zero z deduplikacji" (treść była, ale dublowała wiedzę) od „zera z braku wartości" — pierwsze nie nalicza N.
   - Źródła, dla których detekcja nowości jest strukturalnie niewykonalna (brak dat publikacji): oznacz „niemierzalne", nie „nieproduktywne".
   Oba typy → kandydaci „do usunięcia?" w raporcie, nigdy usunięcie bezpośrednie (pozycje dopisuje i usuwa Właściciel).

**4. Nowe źródła warte rozważenia (web), maksymalnie 5.** Użyj WebSearch/WebFetch WYŁĄCZNIE do sprawdzenia, czy istnieją nowe źródła adresujące KONKRETNE luki z kroków 1–2 — nie ogólny research „co ciekawego się pojawiło". Każda propozycja z UZASADNIENIEM PER LUKA: „źródło X adresuje cienki tag Y (waga: [z kroku 2])" — propozycja bez powiązania z konkretną luką nie kwalifikuje się, niezależnie jak interesująca. Limit pięciu — przy nadmiarze kandydatów wybierz te o najwyższej wadze luki.

**5. Rekomendacje w trzech koszykach, zasada „synteza przed zakupami".** Dla KAŻDEJ zidentyfikowanej luki zaklasyfikuj rekomendację do JEDNEGO z trzech koszyków, w tej kolejności priorytetu:
   - **Synteza z posiadanego** — czy materiał wypełniający lukę JUŻ istnieje w `sources/` (albo w nieprzetworzonej części istniejących źródeł), tylko nie został jeszcze zsyntetyzowany pod tym kątem? Jeśli tak — PIERWSZEŃSTWO: nie proponuj ingestu nowego źródła, gdy odpowiedź czeka w tym, co Właściciel już ma.
   - **Ingest** — konkretne nowe źródło (z kroku 4) wskazane do jednorazowego przetworzenia.
   - **Źródło cykliczne** — rekomendacja dodania pozycji do [[Lista_Zrodel_Zwiadowcy]], gdy temat wymaga bieżącego monitoringu, nie jednorazowego wchłonięcia (tematy szybko zmieniające się).
   Domyślnie synteza > ingest > cykliczne, chyba że charakter luki jasno wskazuje inaczej. **Kolejność rekomendacji: najpierw wg wagi z kroku 2, wewnątrz tej samej wagi wg klucza porządkującego** — nie wg kolejności, w jakiej luki wypadły w kroku 1.

**6. Zapisz raport i dopisz wpis do `outputs/knowledge/log.md`** wyłącznie narzędziem Edit z kotwicą na końcu pliku (technika jak w kroku 7 `knowledge_ingest`): `## [RRRR-MM-DD] audyt źródeł | RRRR-QN | X tagów cienkich (W wysokich) | Y źródeł do usunięcia? | Z nowych źródeł`.

# Szablon wyniku
`outputs/knowledge/audyt_RRRR-QN.md` (np. `audyt_2026-Q4.md`; drugi w tym samym kwartale → `_02`), frontmatter wg `template_output.md` (`type: output`, `agent: zwiadowca`, `task: audyt źródeł`, `date`, `head: "[[knowledge]]"`, `linked_sources`, `status`). Sekcje w stałej numeracji (pusta = „nie dotyczy"):
```
## 1. Mapa pokrycia (tabela: tag → klaster → liczba notatek → trend vs poprzedni audyt)
## 2. Luki z wagą konsumenta (tabela: tag cienki → waga → człon A (persona/klaster) → człon B („uśpiony") → miejsce w kluczu porządkującym)
   + nota o nieporównywalności wag, jeśli seria zmieniła mechanizm
   + jedno zdanie o personach z zasięgiem `all`
## 3. Status źródeł (martwe/przeniesione, nieproduktywne, niemierzalne — kandydaci „do usunięcia?")
## 4. Nowe źródła warte rozważenia (max 5, uzasadnienie per luka)
## 5. Rekomendacje w trzech koszykach (synteza / ingest / cykliczne), uporządkowane wg wagi i klucza z kroku 2
## 6. Materiał dla metodyka (rozjazdy procedury z praktyką, wyzwalacz członu B, granice zasięgu napotkane w przebiegu) — albo „brak"
```

# Checklist przed oddaniem
- [ ] Mapa pokrycia obejmuje WSZYSTKIE tagi z `tags_owned`, nie próbkę; liczby policzone na żywo.
- [ ] Trend policzony względem NAJNOWSZEGO poprzedniego audytu lub jawnie „pierwszy audyt" — i policzony na LICZBIE NOTATEK, nie na wagach.
- [ ] Każda luka ma wagę z gałęzi obowiązującej (konsument zawężony + głód całoklastrowy) z dopiskiem „człon B uśpiony"; persony `all` wyłączone z ważenia i odnotowane osobnym zdaniem.
- [ ] Zero odczytów `system/agents/` w tym przebiegu; jeśli człon B rozdzieliłby coś, czego nie rozdziela człon A — wyzwalacz zgłoszony w sekcji 6, nie wykonany samowolnie.
- [ ] Luki w tym samym poziomie wagi mają jawnie zapisany klucz porządkujący.
- [ ] Status źródeł rozróżnia martwe/przeniesione (błąd dostępu) od nieproduktywnych (dostępne, bez wartości) i niemierzalnych — to różne kategorie.
- [ ] Maksymalnie 5 nowych źródeł, każde z uzasadnieniem powiązanym z konkretną luką, nie generycznym „ciekawe".
- [ ] Rekomendacje przechodzą przez koszyk „synteza z posiadanego" PRZED „ingest" — zasada rzeczywiście zastosowana (sprawdzono `sources/`), nie tylko zadeklarowana.
- [ ] Kandydaci „do usunięcia?" i „źródło cykliczne" to propozycje, nie bezpośrednia zmiana [[Lista_Zrodel_Zwiadowcy]].
- [ ] Log zaktualizowany przez Edit z kotwicą.
- [ ] Zgodność z [[access_map]] i [[Lista_Zrodel_Zwiadowcy]]; sekcja „Podstawa metodyczna" obecna (postać normatywna).

# Wzorcowy przykład
[uzupełnić pierwszym zaakceptowanym wynikiem — few-shot musi cytować realny, oceniony przebieg z outputs/router/log.md]

Oczekiwany kształt: cytat tabeli z sekcji 2 (co najmniej jedna luka WYSOKA i jedna NISKA z wypisanym członem A i kluczem), cytat jednej pozycji z sekcji 3 rozróżniającej „martwe" od „nieproduktywne", oraz przykład rekomendacji z koszyka „synteza", która zatrzymała propozycję ingestu.

# Stan akceptacji
Rozstrzygnięcia przyjęte z doświadczenia poprzednika (bezosobowo; szczegóły w [[Lekcje_Poprzednika]]):
- **Procedura, której litera zwraca zero trafień po zmianie mechanizmu zasięgu, daje raport formalnie poprawny i całkowicie bezużyteczny.** Krok ważenia przepisano na aktualny mechanizm (zasięg klastrowy z mapy), a metoda audytu została nietknięta — zmieniono mechanizm, nie filozofię.
- **Kryterium odrzucone zostaje w procedurze jako UŚPIONE z wyzwalaczem.** Człon B zmierzono przed decyzją: nie rozdzielał ani jednego cienkiego tagu i wymagałby nadania odczytu definicji person. Usunięcie akapitu skasowałoby ślad, dlaczego odrzucono — dlatego zostaje jako wzorzec z warunkiem obudzenia.
- **Zmiana wagi bez zmiany liczby notatek to artefakt normy, nie sygnał o wiedzy.** Trend liczy się wyłącznie na liczbie notatek; wagi porównuje się tylko w obrębie jednej wersji mechanizmu.
- **Klucz porządkujący wewnątrz poziomu wagi jest obowiązkowy**, bo trzy poziomy nie ustawiają kolejności, gdy kilka luk trafia w ten sam poziom — a to stan typowy.
- **Wykonawca dostał odczyt całego `outputs/knowledge/`, nie dwóch wzorców plików** — węższy wariant zostawiłby tę samą klasę „zapis nie daje odczytu" przy następnym typie raportu. Stąd pole `wymagany_odczyt` w tym pliku.
- **Trzeci kandydat na człon wagi (obecność tagu pod notatką filarową klastra) odrzucono jako szum udający kryterium** — nie korelował z niedoborem.

# Historia zmian
- 2026-09-05 (v1.0): wersja szablonu — wyprowadzona z działającego systemu-poprzednika; treść osobista i infrastrukturalna usunięta, struktura i zasady zachowane.
