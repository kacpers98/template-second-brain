---
name: knowledge_audyt_dostepow
aliases: ["knowledge_audyt_dostepow"]              # plik nazywa się SKILL.md — alias pozwala linkować [[knowledge_audyt_dostepow]] w Obsidianie (lint R8)
description: "Audyt POKRYCIA WIEDZY vs ZASIĘG: czy persona ma w zasięgu wiedzę, która w vaultcie LEŻY i JEJ ZAKRESU DOTYCZY — oraz czy to, co jej definicja twierdzi o stanie vaulta i normy, jest nadal prawdą (klasa R3). Tryby: LEKKI (po ingeście: czy nowe notatki trafiły do klastrów, które ktoś czyta) i DORAŹNY (jedna persona po zmianie definicji, wiersza mapy lub skilla). Zasięg tylko z cluster_access i read_scope; pięć form naprawy od najtańszej; test odwrotny least privilege; wynik lintu jako wejście. Używaj przy: 'czy ten ingest kogokolwiek dosięgnie', 'zmieniłem definicję Y — czy zasięg się zgadza', 'czy persona X widzi to, czego wymaga jej skill'. NIE jest tym skillem: health-check notatek (→ knowledge_audyt), przegląd persony wobec przebiegów (→ knowledge_przeglad_agenta), nadanie tagu/klastra (→ knowledge_rozszerzenie_taksonomii)."
# --- pola własne ---
type: skill
skill_type: procedure
used_by:
  - "[[rekruter]]"
depends_on_artifacts:
  - "[[access_map]]"                # kroki 2, 5, 6 — mechanizm zasięgu, least privilege, konsultacja 7b
  - "[[knowledge]]"                 # standardy raportu
wymagany_odczyt:                    # ŚCIEŻKI (nie artefakty); komentarz wskazuje krok
  - system/agents/                  # kroki 2–3
  - system/skills/                  # krok 2 (Grounding, twarde wejścia skilli przypisanych)
  - system/access_map.md            # kroki 2 i 7
  # wiki/ (WYŁĄCZNIE frontmattery) — świadomie POZA tym polem: to imienny wyjątek zasady 4 nadany w read_scope rekrutera, nie zasięg klastrowy (R13 liczy wiki/ przez cluster_access)
  - outputs/knowledge/log.md        # krok 1 (sygnał: które ingesty się odbyły)
  # świadomie NIEobecne: clusters/ i moc/ (czytelne z mocy zasady 4, bez nadania).
inputs: "TWARDE: tryb (LEKKI: wskazanie ingestu; DORAŹNY: nazwa persony + co się zmieniło). OPCJONALNE (krok 7): WYNIK LINTU (`python3 narzedzia/lint.py --vault .`) uruchomionego przez Właściciela lub przewodnika — wykonawca nie ma powłoki. Brak trybu → dopytaj."
output_format: "raport outputs/knowledge/RRRR-MM-DD_rekruter-audyt-dostepow-[zakres][_NN].md (sekcje 0–6) + pełna treść docelowa definicji per persona w inbox/agents/[nazwa].md (separator + '## Do akceptacji'). Tryb lekki bez znalezisk: jedno zdanie w odpowiedzi, bez pliku."
version: 1.0
updated: 2026-09-05
---
# Kiedy używać
Czy persona **ma w zasięgu wiedzę, która w vaultcie leży i jej zakresu dotyczy** — oraz czy
**to, co jej definicja twierdzi o stanie vaulta i normy, jest nadal prawdą**. To audyt
PRZECIĘCIA zdrowych bytów: zdrowa notatka + poprawna persona + poprawna mapa — i mimo to
defekt, którego żadne narzędzie patrzące na jeden byt nie zobaczy.

**NIE jest tym skillem** — test rozróżniający: **punkt startowy**:
- health-check notatek → [[knowledge_audyt]]; tamten pyta „czy notatka jest zdrowa", ten —
  „czy ktokolwiek ją zobaczy";
- przegląd persony wobec przebiegów → [[knowledge_przeglad_agenta]]; log routera i wyniki →
  tamten; listy klastrów, `tags_owned` i tabela mapy → ten;
- projektowanie nowej persony → [[knowledge_tworzenie_agenta]];
- nadanie tagu lub klastra → [[katalizator]] i [[knowledge_rozszerzenie_taksonomii]]; ten
  skill wykrywa potrzebę i **zatrzymuje się**.

# Wymagane wejście
Tryb i wyzwalacz. Czytane na żywo, nie z pamięci: [[access_map]] (zasady i wiersze person);
`system/agents/[persona].md` w całości; SKILL.md skilli przypisanych; `clusters/*.md`
(`tags_owned` — jedyne źródło prawdy tagów, `key_notes`); frontmattery `wiki/`. Opcjonalnie
wynik lintu — nie uruchamiasz go sam.

# Podstawa metodyczna (Grounding)
**brak — podstawa normatywna, nie epistemiczna: [[access_map]]** (uzupełniająco [[knowledge]]).
Procedura nie stosuje metody z literatury — egzekwuje normę systemu (czym jest zasięg, co
wolno osiągnąć linkiem, konsultacja zamiast nadania, least privilege). Notatka `wiki/` wpisana
tutaj nie przeszłaby testu usunięcia: w wyniku nie zmieniłoby się nic.

# Procedura
**0. Wybór trybu — zapisany jawnie w sekcji 0 wyniku.**

| tryb | wyzwalacz | zakres |
| --- | --- | --- |
| **LEKKI** | po KAŻDYM ingeście | nowe notatki × zasięg klastrowy wszystkich person + kontrola R3 person, w których zasięg notatki weszły — kroki 1, 3, (4–6 przy luce) |
| **DORAŹNY** | zmiana definicji persony, jej wiersza mapy, dodanie skilla lub klastra | JEDNA persona — kroki 2–8 |

Przy wątpliwości → DORAŹNY dla każdej dotkniętej persony (zmiana MECHANIZMU mapy = seria
przebiegów doraźnych). Lint nie wchodzi do trybu lekkiego: ingest nie zmienia frontmatteru ani
wiersza mapy — **kontrola bez związku z wyzwalaczem jest rytuałem, który uczy przewijać**.

**1. (LEKKI) Zbiór nowych notatek — log jest SYGNAŁEM, frontmattery ŹRÓDŁEM.** Z logu odczytaj
tylko, które ingesty się odbyły; tagi bierz z frontmatterów `wiki/` (po `created:`) — log jest
kroniką append-only, po korekcie tagu (forma 1) jego wpis jest nieprawdziwy na zawsze.
Propozycje w `inbox/knowledge/` NIE są notatkami — nie licz. **Przetnij**: dla każdej persony
zbierz `tags_owned` klastrów z jej `cluster_access` (`all` = widzi wszystko); notatka jest
w zasięgu, gdy choć jeden tag należy do zbioru. Licz wg kolumny „Klastry (wiki/)" mapy, notując
rozjazdy wobec frontmatteru. Notatka poza zasięgiem WSZYSTKICH person → luka: kroki 4–6.
Przecięcie niepuste dla każdej → luki nie ma, **ale to nie koniec** → krok 3. Tryb lekki **nie
orzeka o pokryciu persony** — może tylko DODAĆ znalezisko, nigdy zamknąć poprzedniej pozycji.

**2. (DORAŹNY) Zakres persony z trzech źródeł, w kolejności siły**: (a) procedury skilli —
Grounding, twarde wejścia, checklist (wiedza wymagana PER PRZEBIEG); (b) `description`;
(c) Rola / Źródła wiedzy / Format wyniku — zwłaszcza **typy wyniku, których żaden skill nie
obsługuje** (osobna lista; najbogatsze źródło znalezisk). Policz ZASIĘG w dwóch rodzajach:
**DETERMINISTYCZNY** (notatki z tagiem w `tags_owned` klastrów z `cluster_access`, albo całe
`wiki/` przy `all`; plus `read_scope`) i **OPORTUNISTYCZNY** (po wikilinkach do 2 skoków —
persona MOŻE tam trafić, nic tego nie gwarantuje; osiągalność linkiem **obniża wagę znaleziska
o stopień, nie kasuje go**). Przeskanuj klastry POZA `cluster_access`, których `tags_owned`
dotykają zakresu — tam leżą luki na granicach działów. Podaj liczby: klastry | notatek
deterministycznie | +2 skoki | filary (`key_notes`) X/Y; mianownik |wiki/|.

**3. Kontrola normy — klasa R3. Obowiązkowa w OBU trybach.** Dla każdej persony (LEKKI:
w której zasięg weszła nowa notatka; DORAŹNY: audytowanej) przeczytaj Źródła wiedzy,
Samokontrolę i adnotacje few-shota, szukając **twierdzeń o stanie vaulta albo normy, które są
już nieprawdziwe** — wzorce do grepu: „vault nie zawiera X", „brak notatki
o Y", „oznaczaj jako [wiedza własna modelu]", „zgłoś brak wejścia", „nie masz dostępu do B",
„to nie Twój zakres" (sprawdzane w drugą stronę: czy klaster tego obszaru nie leży
w `cluster_access`). Znaleziskiem jest każde takie zdanie — persona ma dostęp, a norma każe jej
z niego nie korzystać. Waga domyślna ISTOTNA. **Dowód: dwa cytaty** —
zdanie z definicji wobec faktu z vaulta/mapy; zweryfikuj TREŚĆ notatki, nie sam tag.
**Naprawa jest spoza pięciu form kroku 6** — to nieaktualna treść, nie luka dostępu:
przepisanie zdania na stan faktyczny + zdjęcie wynikających z niego etykiet wszędzie, gdzie się
powtarzają. R3 wyzwala ingest i zmiana normy — stąd obecność w obu trybach.

**4. Dowód „dotyczy zakresu" — jeden z czterech, wg siły:** (a) skill nazywa notatkę wprost
(Grounding) — rozstrzygający; (b) notatka jest `key_notes` klastra z Roli — mocny; (c) leży
w klastrze, którego `tags_owned` pokrywa czasownik z `description` — mocny; (d) `summary`
odpowiada na pytanie kroku skilla — wystarczający. **Nazwa pliku — nigdy.**

**5. TEST ODWROTNY (least privilege) — przed KAŻDĄ propozycją, z JAWNYM wynikiem także
negatywnym.** Wskaż skill albo frazę `description`, która tej wiedzy wymaga; nie umiesz → nie
proponuj. Naprawa wciągająca **więcej notatek spoza zakresu niż w zakresie** → nie proponuj,
zapisz **świadome pozostawienie z liczbami**. Wynik negatywny **jest wynikiem i musi być
w raporcie** (sekcja 4), nie zniknięciem z listy. **Nie każda twarda zależność skilla
musi rozszerzać zasięg** — notatka o tym samym mechanizmie już w zasięgu → forma 2.

**6. PIĘĆ FORM NAPRAWY — kolejność wiążąca, od najtańszej; wybierz jedną i uzasadnij.**
1. **KOREKTA TAGU notatki** (zgłoszenie do [[katalizator]]a): notatka wypada z zasięgu przez
   niespójne otagowanie w obrębie własnej serii. Warunek: tag już istnieje w `tags_owned`.
2. **PRZEPISANIE KROKU** skilla na źródło, które wykonawca już ma (zgłoszenie do [[metodyk]]a).
3. **KONSULTACJA PUNKTOWA — zasada 7b [[access_map]]**: potrzeba okazjonalna → persona oznacza
   w wyniku „pytanie poza zasięgiem → właściciel: [wikilink persony]", router deleguje
   konsultację w tym samym przebiegu. Koszt trwały zero. NIE wystarcza, gdy wiedza jest
   wejściem KAŻDEGO przebiegu.
4. **NADANIE PLIKU** — `read_scope` + kolumna Odczyt (poza wiki/): pojedynczy plik przed
   katalogiem; podaj, który krok której procedury tego wymaga.
5. **NADANIE KATALOGU / KLASTRA** — klaster do `cluster_access` + kolumny Klastry (wiki/) albo
   katalog do `read_scope`. Koszt w notatkach wchodzących do zasięgu (`|klaster| − część
   wspólna`), rozbity na „w zakresie" / „poza" — bez tego test odwrotny nie ma czym operować.
   Nie istnieje nadanie węższe niż klaster; „coś mniejszego" to forma 1–3.

**Poza zbiorem:** świadome pozostawienie (pełnoprawny wynik); naprawa R3; **STOP
taksonomiczny** — żaden tag nie pokrywa obszaru albo trzeba rozbić klaster → [[katalizator]] /
[[knowledge_rozszerzenie_taksonomii]], nigdy nie nadawaj tagu sam; wiedzy nie ma w vaulcie
WCALE → kandydat do ingestu z **dowodem braku**, nie znalezisko tego audytu.

**7. (DORAŹNY) Lint frontmatter ↔ wiersz mapy — wynik lintu jest WEJŚCIEM.**
`python3 narzedzia/lint.py --vault .` uruchamia Właściciel lub [[przewodnik]]; Ty nie masz
powłoki. Rozgałęzienie: (i) dostarczony, czysto → „lint: czysto, wejście z [data / kto]";
(ii) dostarczony z listą → przenieś dosłownie, dla każdego ustal, która strona niesie DECYZJĘ
(Rejestr zmian mapy / Historia zmian definicji); (iii) **wejścia NIE MA**
→ porównaj ręcznie `head`↔Head, `cluster_access`↔Klastry, `read_scope`↔Odczyt,
`write_access`↔Zapis, `web_access`↔Web (obustronnie, z carve-outami) i zapisz **jawnie jako
ręczne** + pytanie, czy lint był uruchamiany. **„Lint nieuruchomiony" i „lint czysty" to DWA
RÓŻNE WYNIKI** — zapisanie (iii) jako (i) jest fałszem o stanie systemu. Kierunek decyduje
o wadze: mapa szersza niż definicja = **nadanie martwe** (persona o nim nie wie); definicja
szersza = praca poza normą. Przy nadaniu martwym sprawdź definicję pod kątem sprzężonego R3
(„nie masz dostępu do…") — naprawa zdejmuje oba zapisy naraz; „brak sprzężenia" też zapisz.

**8. Zapis.** Raport wg szablonu. Naprawy: **pełna treść docelowa definicji**
w `inbox/agents/[persona].md` + separator odcięcia + „## Do akceptacji"; zmiana wiersza mapy
jako `[persona].wiersz_mapy.md` (oba wg [[knowledge_tworzenie_agenta]], kroki 8–9). Persona
spoza zakresu przebiegu → naprawa co do zdania w raporcie, bez pełnej treści definicji.

# Szablon wyniku
`outputs/knowledge/RRRR-MM-DD_rekruter-audyt-dostepow-[zakres][_NN].md`, frontmatter wg
[[template_output]] (`type: output`, `agent: rekruter`, `task`, `date`, `head: "[[knowledge]]"`,
`linked_sources`, `status: draft`). **Numeracja stała**, sekcja pusta zostaje z treścią „brak":
```
0. Zlecenie, TRYB, wyzwalacz; LEKKI: zbiór notatek (N), zgodność log ↔ frontmattery N/N;
   DORAŹNY: liczby zasięgu (klastry | deterministycznie | +2 skoki | filary X/Y; |wiki/|)
1. Znaleziska wg wagi BLOKUJĄCE / ISTOTNE / KOSMETYCZNE — kolumny stałe: # | persona | rzecz
   (notatka poza zasięgiem ALBO twierdzenie R3) | dowód (a–d / dwa cytaty) | co konkretnie
   zmieniłoby się w wynikach | naprawa (forma 1–5 / korekta R3 / pozostawienie)
2. Przypadki ODWROTNE — zasięg bez uzasadnienia zakresem (n i %). Także „brak"
3. Lint (DORAŹNY): STAN WEJŚCIA (czysto / z listą / brak → ręcznie) jako pierwszy; rozjazdy
   z kierunkiem; sprzężenia z R3
4. Testy odwrotne z wynikiem NEGATYWNYM — liczby i zamiennik (czy nie 7b). Także „brak"
5. STOP taksonomiczny → [[katalizator]] oraz kandydaci do ingestu z dowodem braku — osobno
6. Poza zleceniem + pytania do Właściciela + (gdy audytujesz personę działu knowledge, w tym
   siebie) nazwany konflikt interesu: rozszerzenie własnego zasięgu wyłącznie jako decyzja
   Właściciela z wariantami, zawężenie — normalnie
```

# Checklist przed oddaniem
- [ ] Tryb i wyzwalacz w sekcji 0; LEKKI: zero orzekania o pokryciu, zbiór z frontmatterów
      `wiki/`, log tylko jako sygnał.
- [ ] **R3 sprawdzone ZAWSZE** (także przy niepustym przecięciu); każde R3 ma dwa cytaty
      i weryfikację TREŚCI; naprawa oznaczona jako spoza pięciu form.
- [ ] Zasięg w DWÓCH rodzajach; 2 skoki obniżyły wagę, nie skasowały; klastry poza
      `cluster_access` przeskanowane.
- [ ] Każde znalezisko ma dowód (a)–(d); zero uzasadnień z nazwy pliku.
- [ ] Test odwrotny dla KAŻDEJ propozycji; negatywne w sekcji 4 z liczbami.
- [ ] Formy naprawy w kolejności 1→5; koszt formy 5 rozbity „w zakresie" / „poza".
- [ ] **STAN WEJŚCIA LINTU jednoznaczny; nigdzie „lint czysto" bez dostarczonego wyniku.**
- [ ] Nadania martwe sprawdzone pod kątem sprzężonego R3; strona niosąca DECYZJĘ ustalona.
- [ ] Zero edycji [[access_map]], `system/agents/`, `wiki/`; zero tagu/klastra nadanego
      samodzielnie; propozycje tylko w `inbox/agents/` z separatorem; wiersz mapy tylko jako
      plik `.wiersz_mapy.md`.
- [ ] Sekcje 0–6 w stałej numeracji; zgodność z [[knowledge]].

# Wzorcowy przykład
[uzupełnić pierwszym zaakceptowanym wynikiem — few-shot musi cytować realny, oceniony przebieg
z outputs/router/log.md]

Postawa do naśladowania (szerzej w [[Lekcje_Poprzednika]]): odpowiedź dowodem, nie deklaracją;
odmowa fabrykacji naprawy pod przygotowany scenariusz; znaleziska R3 przy zerowej luce pokrycia
— wynik, dla którego istnieje krok 3; negatywny test odwrotny zapisany, choć ograniczał
własną odpowiedź.

# Stan akceptacji
- WDROŻONE: tylko tryb LEKKI i DORAŹNY; tryb pełny (dział na raz) nie istnieje w szablonie —
  zastępuje go seria przebiegów doraźnych.
- WDROŻONE: zasięg liczony wyłącznie z `cluster_access` + `read_scope`; tagi są taksonomią.
- WDROŻONE: wynik lintu jest wejściem od Właściciela/przewodnika; brak wejścia = brak wejścia.
- WDROŻONE: korekta tagu i przepisanie kroku sprawdzane PRZED każdą formą rozszerzającą zasięg.
- OTWARTE: {{UZUPEŁNIJ: po trzech ingestach — czy R3 dla person z `cluster_access: all`
  (odpala przy każdym ingeście) jest wykonalne kosztowo, czy wymaga zawężenia}}.

# Historia zmian
- 2026-09-05 (v1.0): wersja szablonu — wyprowadzona z działającego systemu-poprzednika; treść osobista i infrastrukturalna usunięta, struktura i zasady zachowane.
