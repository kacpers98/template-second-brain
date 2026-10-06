---
name: knowledge_przeglad_agenta
aliases: ["knowledge_przeglad_agenta"]              # plik nazywa się SKILL.md — alias pozwala linkować [[knowledge_przeglad_agenta]] w Obsidianie (lint R8)
description: "Procedura przeglądu istniejącego, zaakceptowanego agenta wg zasady 'definicja to hipoteza': zestawia definicję z realnymi przebiegami z outputs/router/log.md i outputs/[dział]/, identyfikuje rozjazdy obietnica-vs-wykonanie w OBIE strony, wykrywa aparat poprzedniej propozycji osiadły w definicji (krok 2a), wybiera kandydata na sekcję few-shot (tylko przebieg z oceną w logu), proponuje zmiany definicji z testem kolizji description po zmianie i oddaje wynik jako PEŁNĄ TREŚĆ DOCELOWĄ definicji + aparat przeglądu pod separatorem odcięcia. Agent bez przebiegów = uczciwy komunikat, nie przegląd teoretyczny. Używaj przy zleceniach 'przejrzyj agenta X', 'sprawdź, czy definicja Y się sprawdza w praktyce', 'przegląd kwartalny person działu Z'. NIE jest tym skillem: projektowanie nowego agenta (→ knowledge_tworzenie_agenta), audyt zasięgu vs wiedza w vaultcie (→ knowledge_audyt_dostepow)."
# --- pola własne ---
type: skill
skill_type: procedure
used_by:
  - "[[rekruter]]"
depends_on_artifacts:
  - "[[access_map]]"                # krok 4 (granice zmian dostępów) i krok 5 (zasada podpisu przez inbox/)
wymagany_odczyt:                    # ŚCIEŻKI (nie artefakty), które procedura czyta; komentarz wskazuje krok
  - system/agents/                  # krok 1 (definicja przeglądanego agenta), krok 4 (test kolizji z pozostałymi)
  - outputs/router/log.md           # krok 1 (wpisy routingu do agenta, pewność, ocena)
  - outputs/                        # krok 1 i 3 — pliki wyników z frontmatterem `agent: [nazwa]`, wszystkie działy
  - system/access_map.md            # krok 4
  # świadomie NIEobecne: wiki/ (procedura nie ocenia treści wiedzy — to [[knowledge_audyt_dostepow]]);
  # system/skills/ — czytane WARUNKOWO (tylko gdy rozjazd dotyka skilla przypisanego), z klauzulą
  # degradacji „rozjazd zgłoszony bez wglądu w skill", więc nie wchodzi do pola.
inputs: "TWARDE: nazwa agenta do przeglądu (plik istnieje w system/agents/). Skill sam odnajduje materiał: log routera + wyniki w outputs/[dział]/. OPCJONALNE: zakres dat, hipoteza do sprawdzenia w pierwszej kolejności."
output_format: "propozycja aktualizacji definicji w inbox/agents/[nazwa].md — pełna treść docelowa definicji, separator odcięcia, sekcja '## Przegląd — [data]'; nigdy bezpośrednia edycja system/agents/. Agent bez przebiegów: komunikat w odpowiedzi (bez pliku), chyba że krok 2a dał znalezisko."
version: 1.0
updated: 2026-09-05
---
# Kiedy używać
Zlecenie przeglądu ISTNIEJĄCEGO, zaakceptowanego agenta (`system/agents/[nazwa].md`) w świetle
realnych przebiegów — nie teoretyczna ponowna lektura definicji. **„Definicja to hipoteza"**
(rzemiosło [[rekruter]]a): każda definicja jest hipotezą o tym, jak agent będzie działał
w praktyce — ten skill ją TESTUJE względem faktycznych danych z `outputs/router/log.md`
i `outputs/[dział]/`, zamiast czytać opis na nowo i oceniać „z wyczucia", czy brzmi dobrze.

**NIE jest tym skillem** — **test rozróżniający: punkt startowy**:
- projektowanie NOWEGO agenta → [[knowledge_tworzenie_agenta]]; punkt startowy: opis potrzeby,
  nie istniejący plik;
- audyt, czy persona ma w zasięgu wiedzę leżącą w vaultcie → [[knowledge_audyt_dostepow]];
  punkt startowy: **log routera i pliki wyników → ten skill; listy klastrów, `tags_owned`
  i tabela [[access_map]] → tamten**. Tamten pyta „czy w ogóle miała czym", ten — „czy działała
  dobrze na tym, co robiła";
- przegląd agenta bez dostępnych przebiegów — to świadomie NIE jest ten skill, tylko uczciwy
  komunikat o niemożności (przypadek brzegowy niżej).

# Wymagane wejście
Nazwa agenta. Skill sam odnajduje materiał, czytany na żywo, nie z pamięci:
- `outputs/router/log.md` — wpisy, w których pole „routing" wskazuje tego agenta bezpośrednio
  albo w łańcuchu delegacji, z polami „pewność routingu" i „ocena";
- `outputs/[dział]/` — pliki z polem frontmatteru `agent: [nazwa]`;
- `system/agents/[nazwa].md` — CAŁY plik, łącznie z Historią zmian.
Brak logu albo pustego katalogu wyników nie jest błędem wejścia — to przypadek brzegowy.

# Podstawa metodyczna (Grounding)
- {{UZUPEŁNIJ: notatka o przykładach few-shot — kiedy i ile}} → krok 3 — kiedy przykład
  w definicji pomaga, ile ich ma sens i czym różni się dobry przykład od zapchajdziury.
- {{UZUPEŁNIJ: notatka o pisaniu description pod trafne wyzwalanie}} → krok 4 — te same reguły
  trafnego wyzwalania stosują się do description agenta względem pozostałych person.

Vault startowy nie zawiera tych notatek; do czasu ingestu kroki 3–4 wykonuj z oznaczeniem
[wiedza własna modelu].

Podstawa normatywna zasady „definicja to hipoteza, przebiegi to dane": rzemiosło [[rekruter]]a
i [[access_map]] (podpis przez inbox/) — norma systemu, nie literatura.

# Procedura
**1. Zestaw definicję z realnymi przebiegami.** Wczytaj `system/agents/[nazwa].md` ORAZ wszystkie
wpisy w `outputs/router/log.md`, gdzie pole „routing" wskazuje tego agenta — WSZYSTKIE, nie
próbkę. Dla każdego przebiegu sprawdź:
   - **Trafność delegacji** — czy „pewność routingu" była wysoka, czy średnia/niska? KAŻDY wpis
     ze średnią/niską pewnością to sygnał, że `description` nie jest wystarczająco rozłączne —
     wypisz, między kim router się wahał i dlaczego (log to notuje, gdy pewność nie jest wysoka).
   - **Format wyniku** — otwórz linkowany plik wyniku i porównaj jego strukturę z sekcją „Format
     wyniku" definicji: czy sekcje się zgadzają, czy agent trzymał zadeklarowany format, czy
     improwizował.
   - **Granice testowane** — czy w uwagach routera albo w wyniku pojawia się sytuacja dotykająca
     którejś z granic/eskalacji definicji (brak wejścia, próba działania poza zasięgiem, odmowa)?
     To dowód, że granica jest realnie egzekwowana, nie tylko zapisana. **Odmowa zgodna
     z granicą to norma działająca, nie usterka.**
   - **Ocena Właściciela** — pole „ocena" (1–5 + poprawka) per wpis: przebiegi z niską oceną
     to pierwsze miejsce szukania rozjazdów; przebiegi BEZ oceny odnotuj osobno (są danymi
     o wykonaniu, ale nie o jakości).

**2. Zidentyfikuj rozjazdy: definicja obiecuje X, przebiegi pokazują Y.** Każdy rozjazd zapisz
w formacie „definicja mówi: [cytat/parafraza] / przebieg pokazuje: [co się stało, z linkiem do
wpisu w logu lub wyniku]". **Rozjazd idzie w OBIE strony**: agent robi mniej, niż obiecuje
definicja (luka do naprawy) ALBO agent radzi sobie z sytuacją, której definicja nie przewidziała
(materiał do rozszerzenia, nie błąd). Odróżnij rozjazd DEFINICJI od jednorazowego błędu
wykonania — ten drugi nie uzasadnia zmiany normy.

**2a. Sprawdź, czy w definicji nie osiadł APARAT POPRZEDNIEJ PROPOZYCJI.** Przeszukaj plik pod
kątem sekcji, które są aparatem decyzyjnym, a nie normą roli: „## Do akceptacji",
„## Przegląd — [data]", proponowany wiersz [[access_map]], warianty A/B, uzasadnienia dostępów,
listy kolizji `description`, separator `PONIŻEJ TEJ LINII: APARAT PROPOZYCJI`. Jeśli cokolwiek
z tego tam jest — **to jest rozjazd do zgłoszenia i do usunięcia w Twojej propozycji**, nie
kosmetyka: persona czyta CAŁY swój plik jako normę, więc wariant przedstawiony kiedyś jako
pytanie czyta dziś jako rozstrzygnięcie; kolejny audyt bierze propozycję za decyzję; do zasięgu
wchodzą nadania, których nikt nie podjął. Usuwasz taką sekcję **razem z uzasadnieniem w Historii
zmian**, żeby usunięcie nie wyglądało na przypadkową utratę treści. Koszt kroku jest bliski
zeru — plik i tak jest otwarty.

**3. Kandydat na few-shot.** Sekcja „Przykład dobrego wyniku (few-shot)" ma NAJWIĘKSZĄ dźwignię
jakościową w definicji (kalibruje przyszłe wyniki przykładem, nie opisem) — i w vaulcie
startowym jest we wszystkich definicjach placeholderem. Z przejrzanych przebiegów wybierz
NAJLEPSZY (kompletny, zgodny z formatem, bez rozjazdów z kroku 2) i zaproponuj go jako
wypełnienie sekcji — fragment lub całość, z komentarzem, DLACZEGO to dobry przykład (które
cechy definicji ilustruje). **Wymóg twardy:** cytowany przebieg musi mieć wpis Z OCENĄ
w `outputs/router/log.md`, a każde twierdzenie o zachowaniu w few-shocie musi mieć pokrycie
w treści cytowanego wyniku (sprawdź w pliku, nie odtwarzaj z pamięci). Brak oceny → oznacz
jawnie i nie wpisuj jako wzorca. Jeśli żaden przebieg nie jest wystarczająco dobry — powiedz
to wprost; **nie wybieraj „najmniej złego" tylko po to, żeby wypełnić pole.**

**4. Propozycje zmian definicji, z testem kolizji po zmianie.** Dla każdego rozjazdu z kroku 2
wskazującego na potrzebę zmiany definicji — sformułuj konkretną zmianę (dopisek / usunięcie /
przeformułowanie) z UZASADNIENIEM per zmiana (który przebieg ją motywuje). PO zebraniu
wszystkich zmian: jeśli którakolwiek dotyka `description` — wykonaj TEST KOLIZJI zmienionego
opisu względem `description` WSZYSTKICH pozostałych agentów w `system/agents/` (ten sam test,
co przy projektowaniu nowego agenta). **Zmiana, która naprawia jeden rozjazd, ale wprowadza
kolizję z innym agentem, jest złą zmianą, nawet jeśli lokalnie uzasadniona.** Zmiana pól
`cluster_access` / `read_scope` / `write_access` / `web_access` jest zmianą dostępu: opisz ją
jako DECYZJĘ OTWARTĄ Właściciela z wariantami, dołącz nowy wiersz mapy w osobnym pliku
`inbox/agents/[nazwa].wiersz_mapy.md` (format z [[knowledge_tworzenie_agenta]], krok 9)
i nie wykonuj jej w treści definicji bez tego oznaczenia.

**5. Zapisz wynik jako propozycję do `inbox/agents/`, NIGDY bezpośrednią edycję.** Nawet dla
drobnej zmiany (jedno zdanie w Granicach) — to wciąż `system/agents/`, wciąż wymaga podpisu
Właściciela (akceptacja przez `akceptuj.py`, ta sama zasada co przy nowych agentach).
**Plik ma dwie części rozdzielone SEPARATOREM ODCIĘCIA** (postać dosłowna w „Szablon wyniku"):
powyżej — pełna treść docelowa definicji z podbitą wersją i wpisem w Historii zmian, gotowa do
przeniesienia bez żadnej edycji; poniżej — „## Przegląd — [data]" z materiałem źródłowym,
rozjazdami i uzasadnieniami. **Aparat przeglądu nie jest częścią definicji** i przy akceptacji
jest odcinany.

**Przypadek brzegowy — agent bez przebiegów.** Jeśli w `outputs/router/log.md` NIE MA żadnego
wpisu wskazującego tego agenta (i `outputs/[dział]/` nie ma jego wyników) — PRZEGLĄD JEST
NIEMOŻLIWY w sensie tego skilla. Zwróć UCZCIWY komunikat: „brak danych z przebiegów — agent
[nazwa] nie był jeszcze routowany; przegląd na tej podstawie byłby spekulacją, nie testem
hipotezy". NIE wykonuj przeglądu teoretycznego (ponownej lektury definicji z komentarzem
„wygląda dobrze") jako namiastki — to złamałoby przesłankę „definicja to hipoteza testowana
danymi". Zaproponuj: poczekać na pierwsze przebiegi, a jeśli Właściciel chce czegoś teraz —
przegląd statyczny jako ODRĘBNE, jawnie nazwane zadanie SPOZA tego skilla.
**Wyjątek od wyjątku:** krok 2a wykonujesz ZAWSZE, także przy braku przebiegów — nie wymaga
danych z logu, tylko przeczytania pliku, a defekt, którego szuka, psuje każdy kolejny przebieg
persony. Zgłoś go w komunikacie o niemożliwości przeglądu jako osobne, wykonalne znalezisko
(wtedy plik w `inbox/agents/` powstaje — wyłącznie z tą jedną zmianą).

# Szablon wyniku
`inbox/agents/[nazwa].md` — **pełna treść docelowa definicji** (z wprowadzonymi zmianami,
podbitą wersją i wpisem w Historii zmian), następnie separator odcięcia, następnie
„## Przegląd — [data]".

Separator kopiuj dosłownie — ma być grepowalny i identyczny co do znaku z tym
w [[knowledge_tworzenie_agenta]] (różni się wyłącznie nazwą odcinanej sekcji):

```
---

> **⬇ PONIŻEJ TEJ LINII: APARAT PROPOZYCJI — ODCIĄĆ PRZY PRZENOSZENIU DO `system/agents/`.**
> Sekcja „## Przegląd — [data]" nie jest częścią definicji. Persona czyta CAŁY swój plik jako
> normę, więc materiał źródłowy, rozjazdy i uzasadnienia zmian przeczyta jako własne
> rozstrzygnięcia. Cięcie: usuń wszystko od tej linii do końca pliku.
```

Sekcja pod separatorem — numeracja stała, sekcja pusta zostaje z treścią „brak":
```
## Przegląd — [data]
1. Materiał źródłowy (linki do przejrzanych wpisów w outputs/router/log.md i plików
   w outputs/[dział]/; liczba wpisów z oceną / bez oceny)
2. Rozjazdy zidentyfikowane (definicja vs przebiegi, z dowodami, w obie strony) — w tym
   aparat poprzedniej propozycji osiadły w definicji (krok 2a), jeśli był
3. Kandydat na few-shot (link + uzasadnienie + potwierdzenie oceny w logu,
   LUB „brak wystarczająco dobrego / ocenionego przebiegu")
4. Propozycje zmian z uzasadnieniem per zmiana + wynik testu kolizji description
   (jeśli dotyczy) + DECYZJE OTWARTE dotyczące dostępów (jeśli dotyczy)
```

# Checklist przed oddaniem
- [ ] Wszystkie wpisy w `outputs/router/log.md` wskazujące tego agenta przejrzane, nie próbka;
      liczba wpisów z oceną i bez oceny podana.
- [ ] Pewność routingu sprawdzona dla każdego wpisu — wahania routera wypisane wprost z powodem.
- [ ] Format wyniku porównany z definicją dla przynajmniej jednego realnego wyniku.
- [ ] Każdy rozjazd ma dowód (link do konkretnego wpisu/wyniku), nie ogólne wrażenie; rozjazdy
      w obie strony rozróżnione od jednorazowych błędów wykonania.
- [ ] **Krok 2a wykonany: plik sprawdzony pod kątem aparatu poprzedniej propozycji
      („## Do akceptacji", „## Przegląd — [data]", wiersz mapy, warianty A/B, separator).
      Znaleziony aparat usunięty w propozycji, z uzasadnieniem w Historii zmian.**
- [ ] Kandydat na few-shot wybrany świadomie LUB jawnie odrzucony — nie wybrany na siłę;
      twierdzenia o zachowaniu sprawdzone w treści wyniku; **brak oceny w logu = nie wzorzec**.
- [ ] Każda proponowana zmiana `description` przeszła test kolizji względem WSZYSTKICH innych
      agentów, nie tylko oczywistych.
- [ ] Zmiany pól dostępowych oznaczone jako DECYZJA OTWARTA z wariantami; przy zmianie —
      plik `[nazwa].wiersz_mapy.md` dołączony.
- [ ] **SEPARATOR ODCIĘCIA obecny w postaci dosłownej, bezpośrednio przed „## Przegląd —
      [data]", sformułowany do akceptującego, nie do persony.** Ryzyko jest tu WYŻSZE niż przy
      nowym agencie: plik wygląda jak gotowa definicja i kusi do przeniesienia bez czytania —
      akceptujący „wie, co w pliku jest, i przewija".
- [ ] **Test odcięcia na sucho:** definicja przeczytana bez wszystkiego poniżej separatora —
      kompletna i spójna, zero odwołań do „rozjazdu nr 2", „tabeli przeglądu", „uzasadnienia
      niżej". Jeśli nie — brakująca treść przeniesiona nad separator.
- [ ] Wersja definicji podbita, wpis w jej Historii zmian mówi CO i DLACZEGO (który przebieg).
- [ ] Zero bezpośredniej edycji `system/agents/` — wyłącznie propozycja w `inbox/agents/`.
- [ ] Przypadek „brak przebiegów" zwrócony jako uczciwy komunikat, nie zastąpiony przeglądem
      teoretycznym — z wykonanym mimo to krokiem 2a.
- [ ] Sekcja „Podstawa metodyczna" obecna: pozycje `{{UZUPEŁNIJ}}` albo postać „brak"
      z dopiskiem.

# Wzorcowy przykład
[uzupełnić pierwszym zaakceptowanym wynikiem — few-shot musi cytować realny, oceniony przebieg
z outputs/router/log.md]

Wzorzec cząstkowy dla kroku 2a (jak ma wyglądać ZGŁOSZENIE, nie cytat z przebiegu): aparat
propozycji osiadły w definicji opisuje się przez **mechanizm i jego trzy konsekwencje** —
(1) persona czyta appendiks jako normę, bo widzi wyłącznie plik; (2) kolejny audyt bierze
propozycję za rozstrzygnięcie; (3) do zasięgu wchodzą nadania bez pokrycia w roli — a nie jako
„niechlujstwo formatowania". Pełniejszy opis tej ślepej uliczki poprzednika: [[Lekcje_Poprzednika]].

# Stan akceptacji
- WDROŻONE: podział ról między dwoma skillami rekrutera — [[knowledge_tworzenie_agenta]]
  ZAPOBIEGA (separator w nowych paczkach), ten skill WYKRYWA (krok 2a na plikach już
  przyjętych); bez detekcji naprawiony byłby wyłącznie strumień nowych propozycji, a stan
  zastany czekałby na przypadkowe wykrycie.
- WDROŻONE: krok 2a wykonuje się także przy braku przebiegów — nie wymaga danych z logu.
- WDROŻONE: few-shot wyłącznie z przebiegu ocenionego w logu; brak oceny blokuje wpis jako
  wzorca, nie tylko go oznacza.
- WDROŻONE: zmiana pól dostępowych w przeglądzie idzie tą samą drogą co przy tworzeniu
  (DECYZJA OTWARTA + osobny plik wiersza mapy), żeby przegląd nie stał się bocznym wejściem
  do [[access_map]].
- OTWARTE: kadencja przeglądu (kwartalnie per dział razem z [[knowledge_audyt_dostepow]])
  — {{UZUPEŁNIJ: potwierdzić w Rytm_Przegladow po pierwszym kwartale używania}}.

# Historia zmian
- 2026-09-05 (v1.0): wersja szablonu — wyprowadzona z działającego systemu-poprzednika; treść osobista i infrastrukturalna usunięta, struktura i zasady zachowane.
