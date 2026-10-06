---
name: knowledge_tworzenie_agenta
aliases: ["knowledge_tworzenie_agenta"]              # plik nazywa się SKILL.md — alias pozwala linkować [[knowledge_tworzenie_agenta]] w Obsidianie (lint R8)
description: "Procedura projektowania definicji nowego agenta (persony): od opisu potrzeby do kompletnej paczki w inbox/agents/ — definicja + separator odcięcia + sekcja „Do akceptacji" + osobny plik z gotowym wierszem tabeli access_map + placeholdery brakujących artefaktów. Zaczyna od testu duplikacji (nowy agent to ostateczność — rozszerzenie istniejącego ma pierwszeństwo), dobiera zasięg „od zera w górę" wyłącznie mechanizmem cluster_access + read_scope, pisze description jako regułę triage w budżecie 300–900 znaków. Używaj przy każdym zleceniu typu 'stwórz agenta', 'zaprojektuj rolę', 'brakuje mi specjalisty od X' — również gdy wynikiem ma być rekomendacja rozszerzenia istniejącego agenta zamiast nowego. NIE jest tym skillem: projektowanie skilla (→ metodyk), przegląd istniejącego agenta wobec przebiegów (→ knowledge_przeglad_agenta), tworzenie działu (head)."
# --- pola własne ---
type: skill
skill_type: procedure
used_by:
  - "[[rekruter]]"
depends_on_artifacts:
  - "[[access_map]]"                # krok 4 (mechanizm zasięgu, zasady least privilege) i krok 9 (format wiersza tabeli)
wymagany_odczyt:                    # ŚCIEŻKI (nie artefakty), które procedura czyta; komentarz wskazuje krok
  - system/agents/                  # krok 2 (test duplikacji) i krok 5 (test kolizji description)
  - system/heads/                   # krok 3 (przypisanie działu)
  - system/access_map.md            # krok 4 i krok 9
  - system/templates/               # krok 6 (template_agent) i krok 7 (template_artifact)
  - system/artifacts/               # krok 7 — wyłącznie frontmattery (pole used_by), nie treść
  # świadomie NIEobecne: clusters/ i moc/ — czytelne dla każdej persony z mocy zasady 4 [[access_map]],
  # nie wymagają nadania (krok 4 czyta frontmattery clusters/, żeby nazwy klastrów istniały);
  # wiki/ — ta procedura nie czyta treści notatek, zasięg wiki/ wyznacza cluster_access persony.
inputs: "TWARDE: opis potrzeby ('potrzebuję agenta do X') + 2–3 przykładowe zlecenia, które rola ma obsługiwać (brak → dopytaj, nie zgaduj). OPCJONALNE: wskazanie działu, wskazanie artefaktu, na którym rola ma stać."
output_format: "paczka w inbox/agents/: [nazwa].md (definicja + separator odcięcia + '## Do akceptacji') + [nazwa].wiersz_mapy.md (jedna linia tabeli access_map) + opcjonalnie artefakt_*.md (placeholdery). Zero zapisów poza inbox/agents/."
version: 1.0
updated: 2026-09-05
---
# Kiedy używać
Każde projektowanie roli agenta — nowej albo rozszerzenia istniejącej. Wynikiem bywa
równie często rekomendacja „rozszerz agenta Y o dwa zdania" jak paczka nowego agenta;
oba są pełnoprawnym wynikiem tego skilla.

**NIE jest tym skillem** (test rozróżniający: co jest PRZEDMIOTEM projektowania):
- procedura / skill → [[metodyk]]; test: jeśli zlecenie opisuje *jak wykonać powtarzalne
  zadanie*, a nie *kto i z jakim zasięgiem* — to skill, nie agent;
- przegląd ISTNIEJĄCEGO agenta wobec jego realnych przebiegów → [[knowledge_przeglad_agenta]];
  test: jeśli wejściem jest log routera i wyniki w `outputs/`, to przegląd, nie tworzenie;
- audyt, czy persona ma w zasięgu wiedzę leżącą w vaultcie → [[knowledge_audyt_dostepow]];
- tworzenie działu (head) — decyzja strukturalna Właściciela; brak pasującego działu jest
  eskalacją (krok 3), nie powodem do utworzenia działu w tej procedurze;
- bezpośrednia zmiana tabeli [[access_map]] — mapa zmienia się wyłącznie aktem podpisu
  (`akceptuj.py --wiersz-mapy`) albo ręcznie przez Właściciela; ten skill wiersz PROPONUJE.

# Wymagane wejście
Opis potrzeby. Jeśli brakuje przykładowych zleceń, które rola ma obsługiwać — poproś
o 2–3, zanim zaczniesz: bez nich nie da się napisać testowalnego `description` ani
ocenić kolizji z istniejącymi agentami. Nie wymyślaj zleceń za Właściciela — wymyślone
zlecenia przechodzą test kolizji, którego realne by nie przeszły.

Czytane na żywo przy każdym przebiegu, nie z pamięci: wszystkie `description`
w `system/agents/`, sekcje Misja i Granice decyzyjności w `system/heads/`, zasady
i tabela [[access_map]], nazwy plików w `clusters/`, [[template_agent]],
[[template_artifact]], frontmattery `system/artifacts/` (pole `used_by`).

# Podstawa metodyczna (Grounding)
- {{UZUPEŁNIJ: notatka o projektowaniu promptów systemowych i ról}} → krok 6 — definicja persony
  JEST promptem systemowym: dobór roli, tonu, granic i kolejności sekcji wg zasad projektowania
  promptów systemowych.
- {{UZUPEŁNIJ: notatka o pisaniu description pod trafne wyzwalanie}} → krok 5 — reguły pisania
  opisu tak, żeby router wyzwalał trafnie i nie wahał się między personami.
- {{UZUPEŁNIJ: notatka o przykładach few-shot — kiedy i ile}} → krok 6 (sekcja few-shot definicji)
  — kiedy przykład w definicji nowego agenta ma sens od pierwszego dnia, a kiedy czekać na
  realne przebiegi.

Vault startowy nie zawiera tych notatek; do czasu ingestu kroki 5–6 wykonuj z oznaczeniem
[wiedza własna modelu].

Podstawa normatywna paczki wynikowej (separator, wiersz mapy, placeholdery, model uprawnień):
[[access_map]] i [[template_agent]] — to nie jest luka wiedzy, tylko norma systemu.

# Procedura
1. **Parafraza potrzeby + założenia o roli**: misja w jednym zdaniu, typy zleceń, kształt
   wyniku. Zapisz je jawnie — to jest hipoteza, którą reszta procedury testuje.
2. **Test duplikacji.** Przejrzyj `description` WSZYSTKICH agentów w `system/agents/`. Dla
   każdego z 2–3 przykładowych zleceń odpowiedz: czy istniejący agent obsłużyłby je już dziś,
   albo obsłuży po korekcie 1–2 zdań? Jeśli tak — **ZAREKOMENDUJ rozszerzenie** (konkretny
   diff definicji, do `inbox/agents/[istniejący].md` jako pełna treść docelowa z separatorem
   jak w kroku 8) **i ZAKOŃCZ**. **Nowy agent to ostateczność**: każda dodatkowa persona
   kosztuje przy każdym zleceniu (router czyta wszystkie `description`) i przy każdym audycie.
   Wynik „nowy agent" ma pisemne uzasadnienie, dlaczego rozszerzenie nie wystarcza.
3. **Przypisz dział**: dopasuj do Misji i Granic decyzyjności headów w `system/heads/`.
   Brak pasującego → eskalacja do Właściciela jako decyzja strukturalna; nie twórz działu
   i nie wciskaj roli do najbliższego działu „żeby wypełnić pole".
4. **Dobierz zasięg metodą „od zera w górę".** Mechanizm zasięgu ma DOKŁADNIE DWA pola
   i żadnego innego:
   - `cluster_access` — zasięg treści `wiki/`: lista nazw klastrów z `clusters/` (każda nazwa
     musi mieć plik `clusters/<Nazwa>.md`) **albo** wartość `all`. Notatka należy do klastra,
     gdy jej tagi przecinają `tags_owned` tego klastra — ale **tagi są taksonomią, nie
     mechanizmem dostępu**: persona nie dostaje „tagu", dostaje klaster. Nie istnieje nadanie
     węższe niż klaster; jeśli rola potrzebuje kilku notatek z dużego klastra, rozważ
     konsultację punktową przez routera zamiast nadania (zasada konsultacji w [[access_map]]).
   - `read_scope` — ścieżki POZA `wiki/`: konkretne artefakty `system/artifacts/<Nazwa>.md`,
     katalogi `outputs/<dział>/`, pliki systemowe. **Punktowo**: pojedynczy plik przed
     katalogiem; katalog w całości tylko z osobnym uzasadnieniem. `moc/` i `clusters/`
     są czytelne dla każdej persony z mocy zasady 4 i nie wpisuje się ich.
   Zacznij od pustego zestawu (`cluster_access: []`, `read_scope: []`) i dodawaj pozycję
   wyłącznie z uzasadnieniem „bez tego rola nie wykona [konkretne zlecenie z wejścia]".
   `write_access` domyślnie `outputs/<dział>/` (+ `inbox/<strefa>/`, jeśli rola produkuje
   propozycje); `web_access: false` domyślnie. Każde odstępstwo (web, zapis poza outputs/,
   `all`) to jawna decyzja Właściciela w „Do akceptacji", nie domyślna wartość.
5. **Napisz `description` wg formuły reguły triage**: „Użyj, gdy [warunek / typ zlecenia].
   Zwraca [kształt wyniku]." + 2–3 przykładowe sformułowania zleceń + „NIE jest tym agentem:
   …". Budżet **300–900 znaków** — description ładuje się przy KAŻDYM zleceniu, więc jego
   długość jest kosztem stałym systemu, nie miarą staranności. Sformułuj lekko „pushy" (router
   częściej niedotrenowuje delegacji niż przetrenowuje). **Test kolizji**: dla każdego
   przykładowego zlecenia odpowiedz, czy router mógłby się zawahać między nowym agentem
   a KAŻDYM istniejącym — jeśli tak, zawęź jedno z description i zapisz kryterium rozgraniczenia.
6. **Wypełnij [[template_agent]] w całości**: Rola (z kontekstem Właściciela — przez odesłanie
   do [[Profil_Wlasciciela]], nie przez kopiowanie jego treści), Źródła wiedzy (żelazna zasada:
   klastry z `cluster_access` → co w nich jest filarem → co czyta w `read_scope`), Proces pracy
   z Samokontrolą, Format wyniku (frontmatter wg [[template_output]]), Skille przypisane (na
   start zwykle BRAK — **skill powstaje z 2–3 realnych, ocenionych przebiegów, nie z domysłu**;
   zapisz to zdaniem, nie pustym polem), Granice (czego NIE robi + kiedy eskaluje), few-shot
   jako placeholder: `[uzupełnić pierwszym zaakceptowanym wynikiem — few-shot musi cytować
   realny, oceniony przebieg z outputs/router/log.md]`.
7. **Analiza luk artefaktowych.** Dla każdego artefaktu, na którym rola stoi: istnieje →
   zgłoś aktualizację jego `used_by` w „Do akceptacji"; nie istnieje → placeholder
   `inbox/agents/artefakt_[Nazwa].md` wg [[template_artifact]] z `{{UZUPEŁNIJ: co tu ma być}}`
   i instrukcją zawartości przy KAŻDEJ sekcji (nie pusty szkielet). Próg dla nowego artefaktu:
   „bez tego rola jest NIEWYKONALNA, nie tylko niewygodna" — udowodnij grepem, że istniejący
   artefakt tej treści nie zawiera.
8. **Zamknij definicję SEPARATOREM ODCIĘCIA**, dopiero pod nim zbuduj sekcję „## Do akceptacji",
   i zapisz paczkę do `inbox/agents/`. Separator ma dokładnie tę postać (kopiuj dosłownie —
   ma być grepowalny; identyczny co do znaku z [[knowledge_przeglad_agenta]], zmieniać w obu
   naraz):

```
---

> **⬇ PONIŻEJ TEJ LINII: APARAT PROPOZYCJI — ODCIĄĆ PRZY PRZENOSZENIU DO `system/agents/`.**
> Sekcja „## Do akceptacji" nie jest częścią definicji. Persona czyta CAŁY swój plik jako
> normę, więc uzasadnienia dostępów, warianty A/B i listy kolizji przeczyta jako własne
> rozstrzygnięcia. Cięcie: usuń wszystko od tej linii do końca pliku.
```

   Wszystko powyżej separatora musi być gotową, samowystarczalną definicją: po odcięciu
   appendiksu plik ma być kompletny i spójny — zero odwołań w treści definicji do „wariantu A",
   „propozycji niżej" ani do czegokolwiek, co żyje wyłącznie pod separatorem. Separator jest
   zaadresowany do TEGO, KTO AKCEPTUJE (Właściciel / przewodnik), nie do persony.
9. **Dołącz gotowy wiersz tabeli access_map jako OSOBNY plik** `inbox/agents/[nazwa].wiersz_mapy.md`
   — jedna linia tabeli w formacie kolumn:
   `| Agent | Head | Klastry (wiki/) | Odczyt (poza wiki/) | Zapis | Web | MCP |`
   (wartości dosłownie z frontmatteru definicji: wikilink agenta, wikilink heada, lista klastrów albo
   `all`, ścieżki `read_scope` z ewentualnymi carve-outami, `write_access`, TAK/–, `–`).
   Przy podpisie (Właściciel mówi „akceptuję", przewodnik/router uruchamia
   `python3 narzedzia/akceptuj.py --vault . <ścieżki> --wiersz-mapy`) wiersz jest dopisywany
   do tabeli mapy **w tej samej operacji**, co przeniesienie definicji — dlatego frontmatter
   i wiersz muszą mówić DOKŁADNIE to samo (lint pilnuje tej pary). Wiersz w osobnym pliku,
   a nie w „Do akceptacji", bo narzędzie czyta plik, nie prozę appendiksu.

# Rzemiosło definicji
Stosuj przy krokach 5–6; przy konflikcie z konwencjami vaulta wygrywa vault.
1. **Jedna rola = jeden cel, jedno wejście, jeden kształt wyniku i jedna reguła przekazania
   dalej (handoff).** Rola „od wszystkiego w dziale" to błąd projektowy — zawęź albo podziel.
2. **Description steruje delegacją** — to jedyne, co router „widzi" przy wyborze. Pisz je jak
   pierwsze zdanie reguły triage (warunek → wynik), nie jak opis stanowiska. Budżet 300–900
   znaków: skrócenie zbyt długiego description zwykle nie usuwa ani jednej frazy-wyzwalacza.
3. **Minimalne narzędzia**: rola czytająca nie dostaje zapisu; zapis tylko tam, gdzie wynik
   tego wymaga. W sesji interaktywnej granice egzekwuje polityka `.claude/settings.json`
   (deny) + przegląd diffu przez Właściciela — ale `write_access` w definicji to pierwsza
   linia obrony i dokumentacja intencji.
4. **Izolacja kontekstu**: persona wstrzykiwana do delegacji NIE dziedziczy historii rozmowy —
   definicja musi być samowystarczalna: kontekst Właściciela, artefakty źródłowe i format
   wyniku jawnie wpisane/zalinkowane, zero założeń „wie z rozmowy". **Ta sama zasada uzasadnia
   separator z kroku 8**: persona nie odróżni propozycji od normy, bo widzi wyłącznie plik.
5. **Szczegółowy prompt bije zwięzły**: rola z kontekstem → proces krokowy → format wyniku →
   granice i eskalacje. Niedopowiedzenia wracają jako niespójne wyniki.
6. **Dobór modelu do wagi roli** (pole `model`): rutynowe/lekkie przebiegi mogą jechać na
   tańszym modelu; domyślnie `inherit`. Rekomendację odnotuj w „Do akceptacji"; decyzja
   należy do Właściciela.
7. **Definicja to hipoteza**: iteruj na podstawie realnych przebiegów (few-shot z pierwszego
   dobrego, ocenionego wyniku; korekty z logu routera), wersjonuj w git — nie szlifuj
   w próżni przed pierwszym użyciem. Przegląd hipotezy to [[knowledge_przeglad_agenta]].
8. **Propozycja nie jest źródłem prawdy dla [[access_map]].** Wariant przedstawiony w appendiksie
   jest pytaniem, nie rekomendacją do wykonania — wiersz mapy wchodzi po PRZECZYTANIU
   propozycji i decyzji Właściciela („akceptuję" → `akceptuj.py --wiersz-mapy`), nie przez
   samo istnienie pliku w inboxie. Dlatego każdą wariantowość oznaczaj tak, żeby nie dała się
   przeczytać jako rozstrzygnięcie: nagłówek „DECYZJA OTWARTA", opcje A/B i jawne zdanie
   „nie wykonałem żadnej z nich w tej propozycji". Plik `.wiersz_mapy.md` zawiera wyłącznie
   wariant DOMYŚLNY (najwęższy) — alternatywy żyją w „Do akceptacji".

# Szablon wyniku
Pliki w `inbox/agents/`: `[nazwa].md`, `[nazwa].wiersz_mapy.md`, opcjonalnie `artefakt_*.md`.
Nazwa snake_case, bez polskich znaków, bez prefiksu `agent_`.

Struktura `[nazwa].md` — trzy części:
1. **Definicja** (wszystko powyżej separatora) — pełna treść wg [[template_agent]], frontmatter
   kompletny (`name, description, tools, model, type, head, cluster_access, read_scope,
   write_access, web_access, trigger, version, updated`), samowystarczalna, gotowa do
   przeniesienia bez żadnej edycji.
2. **Separator odcięcia** w postaci dosłownej z kroku 8.
3. **Sekcja „## Do akceptacji"** (wszystko poniżej):
   - wynik testu duplikacji (dlaczego rozszerzenie nie wystarcza);
   - uzasadnienie KAŻDEJ pozycji `cluster_access` i `read_scope` osobno („bez tego rola nie
     wykona: …"); odesłanie do pliku `.wiersz_mapy.md`;
   - lista kolizji `description` z kryterium rozgraniczenia per istniejący agent;
   - sekcja Artefakty: `used_by` do aktualizacji / placeholdery / wpis do `context_sources`
     heada;
   - potrzeby wykraczające poza standard (web, zapis poza outputs/, `all`, model) jako jawne
     decyzje Właściciela;
   - DECYZJE OTWARTE oznaczone wg rzemiosła pkt 8.

Struktura `[nazwa].wiersz_mapy.md`: jedna linia tabeli (bez nagłówka), format kolumn
`| Agent | Head | Klastry (wiki/) | Odczyt (poza wiki/) | Zapis | Web | MCP |`.

# Checklist przed oddaniem
- [ ] Krok 2 wykonany naprawdę: wynik „nowy agent" ma pisemne uzasadnienie, dlaczego
      rozszerzenie nie wystarcza; przy wyniku „rozszerzenie" paczka zawiera konkretny diff.
- [ ] `description` 300–900 znaków, zawiera przykładowe sformułowania zleceń i „NIE jest tym
      agentem", przeszło test kolizji z KAŻDYM istniejącym agentem (nie tylko oczywistym).
- [ ] Zasięg minimalny: każda pozycja `cluster_access` i `read_scope` ma 1-zdaniowe
      uzasadnienie zleceniem z wejścia; zero `web_access: true`, zero `all`, zero zapisu poza
      `outputs/<dział>/` bez jawnej decyzji w „Do akceptacji".
- [ ] Zasięg opisany WYŁĄCZNIE polami `cluster_access` (nazwy z `clusters/` albo `all`)
      i `read_scope` (ścieżki poza wiki/); zero „tagów dostępowych", „MOC-ów dostępowych"
      ani innych mechanizmów — tagi to taksonomia. Każda nazwa klastra ma plik
      `clusters/<Nazwa>.md`; head istnieje w `system/heads/`.
- [ ] Placeholdery artefaktów kompletne (frontmatter wg [[template_artifact]] + `{{UZUPEŁNIJ}}`
      z instrukcją przy każdej sekcji), linkowane docelową nazwą.
- [ ] **SEPARATOR ODCIĘCIA obecny w postaci dosłownej z kroku 8, bezpośrednio przed
      „## Do akceptacji", sformułowany do akceptującego, nie do persony.** Bez separatora
      appendiks wejdzie do żywej definicji i persona przeczyta warianty A/B jako własną normę.
- [ ] **Test odcięcia wykonany na sucho:** definicja przeczytana bez wszystkiego poniżej
      separatora — kompletna i spójna, zero odwołań do „wariantu A", „propozycji niżej",
      „tabeli na końcu". Jeśli nie — brakująca treść przeniesiona NAD separator.
- [ ] Każda decyzja wariantowa w appendiksie oznaczona jako DECYZJA OTWARTA z jawnym
      „nie wykonałem żadnej z opcji" (rzemiosło pkt 8).
- [ ] **Plik `[nazwa].wiersz_mapy.md` obecny; jedna linia w formacie 7 kolumn; wartości
      identyczne z frontmatterem definicji** (cluster_access ↔ Klastry, read_scope ↔ Odczyt,
      write_access ↔ Zapis, web_access ↔ Web).
- [ ] Sekcja few-shot definicji to placeholder z instrukcją, nie zmyślony przykład; „Skille
      przypisane" mówi wprost, że skill powstanie z 2–3 ocenionych przebiegów.
- [ ] Sekcja „Podstawa metodyczna" obecna: pozycje `{{UZUPEŁNIJ}}` albo postać „brak"
      z dopiskiem; pozycje niezweryfikowane oznaczone jako KANDYDAT.
- [ ] Zero zapisów poza `inbox/agents/`.

# Wzorcowy przykład
[uzupełnić pierwszym zaakceptowanym wynikiem — few-shot musi cytować realny, oceniony przebieg
z outputs/router/log.md]

Czego NIE powtarzać (lekcje poprzednika, bez odniesienia do konkretnego przebiegu — pełniejszy
opis w [[Lekcje_Poprzednika]]):
- **Description ponad budżet** — ładuje się przy każdym zleceniu; skrócenie o połowę nie usunęło
  ani jednej frazy-wyzwalacza. Długość description to koszt stały systemu.
- **`read_scope` na cały katalog artefaktów** zamiast punktowo na jeden potrzebny plik —
  naruszenie least privilege; wyliczaj z nazwy, katalog tylko z osobnym uzasadnieniem.
- **Appendiks bez separatora** — paczki przeniesione razem z „Do akceptacji" sprawiły, że
  wariant A/B z propozycji został odczytany jako rozstrzygnięcie i wszedł do mapy jako nadanie
  martwe (persona nigdy by z niego nie skorzystała). To błąd GRANICY propozycji, nie jej treści
  — i naprawia się go separatorem, nie lepszym pisaniem. Instrukcja prozą też zawiodła:
  propozycja niosła zdanie o odcięciu i została przeniesiona razem z nim, bo przeniesienie to
  operacja bez czytania.

# Stan akceptacji
- WDROŻONE: mechanizm zasięgu `wiki/` to wyłącznie `cluster_access`; zasoby poza `wiki/` —
  wyłącznie `read_scope`. Tagi i warstwy MOC są taksonomią i nawigacją, nie mechanizmem dostępu;
  ich nazwy nie występują w treści normatywnej jako nadania.
- WDROŻONE: separator odcięcia identyczny co do znaku w [[knowledge_tworzenie_agenta]]
  i [[knowledge_przeglad_agenta]] (różni się wyłącznie nazwą odcinanej sekcji); każda korekta
  brzmienia — w obu naraz. Wspólny wzorzec do grepu: `PONIŻEJ TEJ LINII: APARAT PROPOZYCJI`.
- WDROŻONE: wiersz mapy jako osobny plik `.wiersz_mapy.md`, dopisywany do tabeli przez
  `akceptuj.py --wiersz-mapy` w akcie podpisu; „Do akceptacji" niesie uzasadnienia, nie wiersz.
- WDROŻONE: checklist sprawdza obecność i postać separatora oraz samowystarczalność definicji —
  nie samo cięcie, bo cięcie wykonuje inna osoba w innym momencie.
- WDROŻONE: `narzedzia/akceptuj.py` odcina aparat propozycji AUTOMATYCZNIE (wszystko od
  ostatniego separatora `---` poprzedzającego „## Do akceptacji"); brak separatora przy obecnym
  nagłówku = ODMOWA skryptu, nie zgadywanie miejsca cięcia. Przewodnik niczego nie tnie ręcznie.

# Historia zmian
- 2026-09-05 (v1.0): wersja szablonu — wyprowadzona z działającego systemu-poprzednika; treść osobista i infrastrukturalna usunięta, struktura i zasady zachowane.
