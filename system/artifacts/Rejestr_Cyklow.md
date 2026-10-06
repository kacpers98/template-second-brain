---
type: artifact
artifact_type: registry
title: "Rejestr Cyklów"
owner_head: "[[ops]]"
used_by:
  - "[[asystent]]"
  - "[[doradca]]"
inject: on_reference
scope: "Jedyne źródło prawdy o powtarzalnych czynnościach (rytmach) — systemowych i pozasystemowych. Zadania jednorazowe żyją poza vaultem, na liście zadań Właściciela."
authority: binding
review_every: 90d
version: 1.0
created: 2026-09-05
updated: 2026-09-05
---
# Rejestr Cyklów

# Cel dokumentu
Jedno miejsce prawdy o RYTMACH: co się powtarza, jak często, kiedy najbliżej i jakim mechanizmem. Wiążący dla [[asystent|asystenta]] (brief czyta stąd tabelę *Cykle*) i [[doradca|doradcy]] (kontekst zobowiązań cyklicznych przy procesach decyzyjnych). Zadania jednorazowe NIE są tu prowadzone — mają własny master poza vaultem.

# Zasady prowadzenia
1. **Zakres**: wyłącznie czynności powtarzalne z rytmem — systemowe (przeglądy, linty, audyty, rotacje) i pozasystemowe (rytmy życia i pracy Właściciela, które Właściciel chce mieć w polu widzenia briefu). Zadania jednorazowe (next actions) NIGDY tu nie trafiają — ich jedynym masterem jest lista zadań Właściciela (np. Google Tasks, Todoist, papier) — {{UZUPEŁNIJ: nazwa Twojej listy zadań}}. Cykle, których treść jest prywatna (np. zdrowotne), prowadź jako wydarzenia cykliczne w kalendarzu, nie tutaj — ten rejestr czytają agenci i trafia do briefów.
2. **Architektura źródeł — rozłączne mastery**: dwa mastery o ROZŁĄCZNYCH zakresach — lista zadań Właściciela (zadania jednorazowe) i ten rejestr (rytmy); kalendarz jest wyłącznie projekcją do briefu, nigdy bazą zadań. Synchronizacja dwukierunkowa między jakąkolwiek parą tych źródeł jest zakazana projektowo: ryzyko podwójnego mastera nie znika przez podział — znika przez rozłączność zakresów i jednokierunkowość. Dopływ do briefu: zadania i wydarzenia trafiają do [[asystent|asystenta]] W TREŚCI ZLECENIA (wklejone przez Właściciela); brief niczego nie zapisuje zwrotnie do żadnego źródła ([[Rytm_Przegladow]] zasada 3).
3. **Konwencja `[Z]`**: tytuł zadania na liście zadań zaczynający się od `[Z] ` oznacza zobowiązanie ZEWNĘTRZNE wobec osób trzecich — uruchamia zasadę ciszy asystenta ([[Rytm_Przegladow]] zasada 5) i daje pierwszeństwo przy remisach w Top-3 briefu tygodniowego. Brak prefiksu = zobowiązanie wewnętrzne.
4. **Granica twórca/użytkownik**: rejestr i lista zadań obejmują życie Właściciela oraz OPERACYJNE utrzymanie działającego systemu. ROZWÓJ i budowa systemu (nowe funkcje, nowe persony, refaktory struktury) żyją poza tymi źródłami — po to, żeby briefy mierzyły UŻYCIE systemu, nie majsterkowanie przy nim. Agenci nie proponują pozycji rozwojowych do tego rejestru; propozycje rozwojowe idą do `inbox/` jako propozycje zmian, nie jako cykle.
5. **Zawieszenie zamiast usunięcia**: cykl, którego Właściciel chwilowo nie wykonuje, dostaje w kolumnie „Najbliższy" status `ZAWIESZONY (od RRRR-MM-DD, powód jednym zdaniem)` — wiersz zostaje. Usunięcie = cykl znika z briefów i z pamięci; zawieszenie = widoczna, świadoma decyzja. Wznowienie: Właściciel wpisuje datę w kolumnę „Najbliższy".
6. **Zmiany**: agenci proponują dodanie, edycję i usunięcie wiersza WYŁĄCZNIE przez `inbox/ops/`; zatwierdza Właściciel (akt podpisu: „akceptuję" w czacie → `narzedzia/akceptuj.py`). Wpisy na listę zadań wykonuje wyłącznie Właściciel; propozycje next actions z transkrypcji przygotowuje skill `ops_transkrypcja_na_plan` jako listę gotową do wklejenia.
7. **Kolumna „Najbliższy" należy do Właściciela**: przy cyklach ręcznych datę następnego wykonania przesuwa Właściciel po wykonaniu; agent może w wyniku zauważyć „termin minął", ale nie edytuje wiersza.

# Cykle (zadania powtarzalne i rytmy systemu)

| Cykl | Rytm | Najbliższy | Mechanizm | Wykonawca / skill |
| --- | --- | --- | --- | --- |
| Przegląd tygodniowy | co tydzień ({{UZUPEŁNIJ: dzień i godzina, np. niedziela 18:00}}) | {{UZUPEŁNIJ: data}} | ręcznie: Właściciel wkleja listę zadań i kalendarz do zlecenia → brief tygodniowy wg [[Rytm_Przegladow]] zasada 2 | Właściciel + [[asystent]] / `ops_brief` |
| Lint spójności | po KAŻDEJ sesji, która dotknęła `system/` + kwartalnie (pełny) | {{UZUPEŁNIJ: data najbliższego pełnego}} | `python3 narzedzia/lint.py --vault .` (uruchamia [[przewodnik]] lub Właściciel; wynik porównany z `narzedzia/baseline.json`) | [[przewodnik]] / Właściciel |
| Audyt źródeł | kwartalnie | {{UZUPEŁNIJ: data}} | przebieg w sesji, w której Właściciel jest obecny; wejście: [[Lista_Zrodel_Zwiadowcy]] + raporty zwiadu z kwartału | [[zwiadowca]] / `knowledge_audyt_zrodel` |
| Przegląd baseline lintu | kwartalnie (razem z pełnym lintem) | {{UZUPEŁNIJ: data}} | ręcznie: Właściciel przegląda `narzedzia/baseline.json` — każdy wyjątek albo naprawiony, albo świadomie pozostawiony z jednym zdaniem powodu | Właściciel (+ [[przewodnik]]) |
| {{UZUPEŁNIJ: cykle własne — np. przegląd kwartalny celów, rotacja sekretów wg [[Rejestr_Sekretow]], przegląd półroczny wg [[Checkpointy_Wlasciciela]]}} | | | | |

# Kontekst i uzasadnienie
Rejestr powstał z lekcji, że jedna lista „wszystkiego" (zadania jednorazowe + rytmy + rozwój systemu) staje się nieczytelna i zaczyna być kopiowana do innych narzędzi, po czym dwie kopie rozjeżdżają się i żadna nie jest prawdą. Rozłączność zakresów (zasada 2) załatwia to bez synchronizacji. Granica twórca/użytkownik (zasada 4) chroni przed pułapką, w której system mierzy sam siebie: brief pełen pozycji „popraw skill X" wygląda na produktywność, a jest kosztem utrzymania. Zawieszenie zamiast usunięcia (zasada 5) wynika z obserwacji, że usunięty cykl nie wraca — nikt o nim nie pamięta.

# Przykłady zastosowania
## Dobrze
Właściciel prowadzi co miesiąc przegląd faktur od dostawców. W tabeli pojawia się wiersz „Przegląd faktur dostawców | co miesiąc (5. dzień) | 2026-10-05 | ręcznie: Właściciel sprawdza skrzynkę i folder | Właściciel". Brief dzienny 4. dnia miesiąca pokazuje w `## ZA CHWILĘ`: „- przegląd faktur dostawców — jutro". Właściciel po wykonaniu przesuwa datę na 2026-11-05.
## Źle
Asystent, widząc w transkrypcji spotkania „trzeba wysłać ofertę do klienta do piątku", dopisuje wiersz do tabeli Cykle. Naruszona zasada 1 (to zadanie jednorazowe — należy na listę zadań, jako propozycja gotowa do wklejenia) i zasada 6 (agent nie edytuje rejestru bezpośrednio).

# Wyjątki i przypadki brzegowe
- Cykl, który jest jednocześnie rytmem i ma termin zewnętrzny (np. coroczne złożenie dokumentu): wiersz tutaj + osobne zadanie `[Z]` na liście zadań na konkretny termin. To nie jest dublowanie — rejestr niesie rytm, lista niesie egzekucję w tym roku.
- Cykl o częstotliwości rzadszej niż rocznie: dopuszczalny, ale kolumna „Najbliższy" musi mieć datę (inaczej brief go nie zobaczy).
- Wszystko inne: eskalacja do Właściciela.

# Historia zmian
- 2026-09-05 (v1.0): wersja szablonu — wyprowadzona z działającego systemu-poprzednika; treść osobista i infrastrukturalna usunięta, struktura i zasady zachowane.
