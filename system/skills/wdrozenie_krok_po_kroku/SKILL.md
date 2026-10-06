---
name: wdrozenie_krok_po_kroku
aliases: ["wdrozenie_krok_po_kroku"]              # plik nazywa się SKILL.md — alias pozwala linkować [[wdrozenie_krok_po_kroku]] w Obsidianie (lint R8)
description: "Procedura wdrożenia systemu od zera: osiem etapów (0 kontrola środowiska → 1 wywiad → 2 profil i granice → 3 taksonomia → 4 pierwsze źródła → 5 pierwsza persona domenowa → 6 rytmy → 7 przekazanie do użytku), każdy z pytaniami, bramką wyjścia sprawdzaną plikowo i ostrzeżeniami z doświadczeń poprzednika. Używaj przy KAŻDEJ sesji, w której stan wdrożenia < 7, oraz przy każdej późniejszej zmianie STRUKTURY systemu (nowy dział, warstwa, klaster, persona, automatyzacja). NIE jest tym skillem: ingest źródła (knowledge_ingest), projekt persony (knowledge_tworzenie_agenta), audyt (knowledge_audyt) — te wywołuje jako kroki."
type: skill
skill_type: procedure
used_by:
  - "[[przewodnik]]"
depends_on_artifacts:
  - "[[Lekcje_Poprzednika]]"
  - "[[access_map]]"
  - "[[Profil_Wlasciciela]]"
  - "[[Rejestr_Cyklow]]"
wymagany_odczyt:
  - outputs/wdrozenie/           # krok 0 każdej sesji: STAN_WDROZENIA.md, wywiad.md
  - system/                      # etapy 2–6: szablony, mapa, persony, artefakty-wzorce
  - moc/                         # etap 3: warstwy do potwierdzenia
  - clusters/                    # etap 3–4: klastry, tags_owned
  - sources/                     # bramka etapu 4: liczba źródeł
  - inbox/                       # każda akceptacja: prezentacja propozycji
  - outputs/router/log.md        # bramki etapów 5 i 7: przebiegi z oceną
  - outputs/knowledge/log.md     # bramka etapu 4: wpisy ingestów
  - narzedzia/                   # akceptuj.py, lint.py
inputs: "TWARDE: stan wdrożenia (plik). Opcjonalne: odpowiedź Właściciela na bieżące pytanie etapu."
output_format: "STAN_WDROZENIA.md (nadpisywany), wywiad.md (dopisywany), propozycje w inbox/*, komendy do zgody Właściciela"
version: 1.0
updated: 2026-09-05
---
# Kiedy używać
Zawsze, gdy `outputs/wdrozenie/STAN_WDROZENIA.md` ma `etap < 7`, oraz później na żądanie Właściciela przy zmianie struktury (nowy dział, klaster, warstwa, persona, pierwsza automatyzacja — wtedy wykonujesz tylko właściwy etap jako „dobudowę", z tą samą bramką).
**NIE jest tym skillem:** wykonanie ingestu, projektu persony, skilla, briefu — to kroki, które ten skill ZLECA właściwym personom i sprawdza ich wynik przy bramce. Test rozróżniający: „czy wynik tej czynności to zmiana STANU WDROŻENIA (etap, decyzja, struktura), czy TREŚĆ (notatka, persona, brief)?" — treść robi ktoś inny.

# Wymagane wejście
TWARDE: `STAN_WDROZENIA.md` (brak pliku = etap 0, utwórz go z wersji startowej). Każda sesja zaczyna się od jego przeczytania i od jednej wiadomości otwarcia (definicja przewodnika, Proces pkt 1). Odpowiedzi Właściciela zapisujesz DOSŁOWNIE (nie parafrazuj — Profil_Wlasciciela wymaga cytatów).

# Podstawa metodyczna (Grounding)
- brak — podstawa normatywna, nie epistemiczna: [[Lekcje_Poprzednika]] (procedura stosuje doświadczenie poprzednika i normy systemu; nie ma literatury, która by ją zastąpiła). Uzasadnienie testem usunięcia: bez Lekcji przewodnik prowadziłby wdrożenie „rozsądnie", ale nie umiałby powiedzieć, DLACZEGO nie zakładać dziesięciu klastrów ani DLACZEGO automatyzacja jest na końcu — a to jest cała jego wartość.

# Procedura

## Zasady wspólne wszystkich etapów
- Jedno pytanie naraz. Odpowiedź → zapis → następne pytanie.
- Każda zmiana w `system/`, `moc/`, `clusters/` = propozycja w `inbox/` → „akceptuję" → `python3 narzedzia/akceptuj.py --vault . <ścieżka>`. Przy pierwszej akceptacji wyjaśnij jednym zdaniem: „Claude Code zapyta, czy zgadzasz się na tę komendę — Twoje «tak» jest podpisem; to jedyny moment, w którym coś trafia do części systemu, której agenci nie mogą zmieniać".
- Bramka wyjścia sprawdzana PLIKOWO. Podnosisz `etap` we frontmatterze STAN_WDROZENIA dopiero, gdy wszystkie warunki są spełnione. Wymuszenie przez Właściciela → wpis w „Ostrzeżenia odrzucone świadomie".
- Ostrzeżenie ma format z definicji przewodnika (⚠ + cytat numeru lekcji + pytanie „czy mimo to"). Raz. Nie wracasz do tematu, dopóki nie pojawi się skutek.
- Koniec każdej sesji: linia w dzienniku wdrożenia, lint (jeśli dotknięto `system/`), propozycja commita, zapowiedź następnego kroku.

## Etap 0 — Kontrola środowiska
Cel: Właściciel widzi działający pulpit, a vault ma historię od pierwszego dnia.
Kroki:
1. Poproś o otwarcie `KOKPIT.md` w Obsidianie. Pytanie: „Czy tabele są widoczne, czy widzisz surowy tekst w ramkach?" Surowy tekst = brak wtyczki Dataview → wskaż START_TUTAJ krok 2 (Ustawienia → Wtyczki społeczności → wyłącz tryb ograniczony → przeglądaj → „Dataview" → zainstaluj i włącz; to samo dla „Obsidian Git"). Czekaj na potwierdzenie.
2. `git status` (Bash). Jeśli „not a git repository" → `git init && git add -A && git commit -m "Start: vault z szablonu"`. Wyjaśnij jednym zdaniem: git to historia każdej zmiany; nic nie ginie. ⚠ Lekcja III.1 (poprzednik pracował 10 dni bez gita) — nie pomijaj.
3. Pytanie o kopię zapasową: „Gdzie ten folder będzie miał kopię poza tym komputerem? (dysk zewnętrzny, chmura, zdalne repozytorium)". Zapisz odpowiedź w STAN_WDROZENIA (dziennik). Jeśli „nigdzie" → ⚠ jedno zdanie o ryzyku, nie blokuj etapu (to decyzja Właściciela), ale zapisz jako odrzucone ostrzeżenie.
4. Pytanie o czas: „Ile czasu tygodniowo realnie dasz temu systemowi przez pierwszy miesiąc?" Zapisz. Jeśli < 2 h → powiedz wprost, że etapy 3–5 zajmą wtedy 4–6 tygodni, i zaproponuj węższy zakres (1 klaster, 1 persona).
Bramka: KOKPIT renderuje tabele (Właściciel potwierdził); `git log` ma ≥1 commit; odpowiedzi o kopii i czasie zapisane.

## Etap 1 — Wywiad
Cel: `outputs/wdrozenie/wywiad.md` z odpowiedziami DOSŁOWNIE, z datą. Pytania zadawaj pojedynczo, w tej kolejności; dopytuj, gdy odpowiedź jest ogólnikiem („pomagać mi w pracy" → „w jakiej czynności, którą robiłeś w tym tygodniu?").
1. „Czym się zajmujesz — co robisz w typowym tygodniu, dla kogo?" (rola, branża, odbiorcy)
2. „Wymień trzy rzeczy, które robiłeś w ostatnim miesiącu więcej niż raz i które Cię męczą lub zajmują za dużo czasu." (kandydaci na skille i persony — TO jest najważniejsze pytanie; bez powtarzalnych czynności system nie ma czego usprawniać)
3. „Skąd bierzesz wiedzę fachową: książki, normy, kursy, strony, ludzie? Wymień 3–5 konkretnych tytułów/adresów, do których wracasz." (kandydaci na pierwsze źródła i Listę Źródeł)
4. „Co chciałbyś, żeby ten system pamiętał za Ciebie?" (zakres wiedzy vs zakres zadań)
5. „Kto oprócz Ciebie będzie z tego korzystał albo widział wyniki?" (jednoosobowy vs zespół — jeśli zespół, zanotuj: role wieloosobowe są POZA zakresem szablonu, wymagają osobnej decyzji)
6. „Co z Twojej pracy jest poufne — dane klientów, pracodawcy, pacjentów, umowy?" (etap 2: Granica_Pracy_Zawodowej) ⚠ Jeśli Właściciel chce wprowadzać takie dane do vaulta — Lekcja II.11 i zasada 14 access_map; wskaż, że dane klientów żyją POZA vaultem, a vault dostaje wyłącznie METODĘ (test przedmiotu).
7. „Jak wolisz dostawać wyniki: krótko i z rekomendacją, czy z wariantami do wyboru? Ile wariantów to za dużo?" (Profil_Wlasciciela: preferencje formatu)
8. „Kiedy w tygodniu masz naturalny moment na przegląd — poniedziałek rano, niedziela wieczór?" (etap 6: rytmy)
9. „Czego się obawiasz przy tym systemie?" (ryzyka nazwane przez Właściciela — wrócą w etapie 7)
Bramka: `wywiad.md` ma odpowiedzi na wszystkie 9 pytań (dopuszczalne „nie wiem" z datą); co najmniej 2 powtarzalne czynności i co najmniej 2 konkretne źródła nazwane.

## Etap 2 — Profil i granice
Cel: [[Profil_Wlasciciela]] i decyzja o granicy pracy zawodowej.
1. Z wywiadu (pyt. 7, 9 + obserwacje z rozmowy) przygotuj propozycję wypełnienia WARSTWY WYWNIOSKOWANEJ Profilu: każdy wzorzec ze statusem HIPOTEZA (bo masz jedno wystąpienie) i dowodem = cytat z wywiadu. Warstwę MIERZONĄ zostaw pustą z instrukcją (testy — decyzja Właściciela, nie Twoja). Zapisz do `inbox/ops/prop_Profil_Wlasciciela.md`, pokaż PO LUDZKU: „Zapisałem o Tobie pięć obserwacji jako hipotezy; sprawdź, czy któraś jest nieprawdziwa". Po „akceptuję" → akceptuj.py (typ: artefakt → nadpisuje wzorzec w `system/artifacts/` — flaga `--nadpisz`).
2. Granica pracy zawodowej: jeśli pyt. 6 ujawniło dane poufne → pokaż [[Granica_Pracy_Zawodowej]] w trzech zdaniach (co nie wchodzi; test przedmiotu; gdzie żyje praca dla innych) i zapytaj: „Czy zakładamy osobny folder poza vaultem na pracę dla klientów/pracodawcy?" Zapisz decyzję w STAN_WDROZENIA. Nie konfiguruj tego folderu (poza zakresem szablonu) — wystarczy decyzja i nazwa folderu.
3. Zaproponuj wypełnienie „Kontekst właściciela" w `system/heads/knowledge.md` i `ops.md` (2–3 zdania z pyt. 1 i 4) → `inbox/agents/prop_head_knowledge.md`, `prop_head_ops.md` → akceptuj.py (typ: head, `--nadpisz`).
Bramka: `grep -c "UZUPEŁNIJ" system/artifacts/Profil_Wlasciciela.md` — w warstwie wywnioskowanej 0 (w mierzonej mogą zostać); heady bez `{{UZUPEŁNIJ}}` w Kontekście właściciela; decyzja o granicy zapisana.

## Etap 3 — Taksonomia (najważniejszy etap — tu rodzą się błędy, które kosztują przebudowę)
Cel: warstwy potwierdzone lub przemianowane, 2–6 klastrów startowych z definicjami tagów, lint 0.
1. **Warstwy.** Pokaż pięć pytań z `moc/` (dlaczego chcą → jak się utrzymuje → jak dowozimy → jak działa od środka → Ty jako system) i zapytaj: „Które z tych pytań są w Twojej pracy realne, a które puste? Czy brakuje jakiegoś?" Typowo: warstwa Techniczna (rzemiosło) jest największa; Behawioralna i Biznesowa bywają puste u osób na etacie. Pusta warstwa ZOSTAJE jako plik (koszt zero), ale nie dostaje klastrów. Zmiana nazwy warstwy → propozycja `inbox/knowledge/moc_<nazwa>.md` (cały plik) → akceptuj.py (typ: moc). ⚠ Lekcja II.17 i III: nazwy zmieniasz TERAZ, nie po stu notatkach.
2. **Klastry — z czynności i źródeł, nie z wyobraźni.** Weź z wywiadu powtarzalne czynności (pyt. 2) i źródła (pyt. 3). Dla każdej zaproponuj: „to wymaga wiedzy o X — X byłby klastrem w warstwie Y". Jeśli branży nie znasz — WebSearch: „jak dzieli się wiedza fachowa w [branża]" — wynik jako propozycja z adnotacją „z researchu". Zaproponuj 2–6 klastrów, NIE więcej. ⚠ Gdy Właściciel chce 10+ od razu: Lekcja I.1 vs V (7% notatek cytowanych) — pusty klaster to dług, nie plan; klastry dokłada się, gdy istniejący pęka (>40 notatek albo dwie wyraźne granice w środku).
3. **Dla każdego klastra — ramowanie PRZED nazwą:** (a) czym jest w dwóch zdaniach; (b) czym NIE jest → który inny klaster; (c) 1–4 tagi z jednozdaniowymi definicjami (tag należy do DOKŁADNIE jednego klastra w całym vaultcie — sprawdź `grep -r "tag" clusters/`); (d) warstwa. Konwencja tagów: małe litery, podkreślenia, bez polskich znaków (np. `instalacje_elektryczne`), bo tag to identyfikator, nie tytuł. Propozycja: `inbox/knowledge/tax_nowy_klaster_<nazwa>.md` wg [[template_cluster]] (bez sekcji Do akceptacji — plik przenosi się w całości) + zaktualizowany PEŁNY plik warstwy `inbox/knowledge/moc_<MOC>.md` (z nowym akapitem w Mapie klastrów i klastrem w polu `clusters`) — akceptuj.py przenosi go z flagą `--nadpisz`; lint sprawdzi lustro tagów.
4. **Dwa klastry przykładowe** ([[Wydajność i Skupienie]], [[Przywództwo i Decyzje]]): zapytaj, czy zostają. Jeśli Właściciel nie planuje z nich korzystać — mogą zostać (koszt zero) albo wylecieć; jeśli wylatują, persony asystent/doradca dostają `cluster_access: []` (propozycja zmiany definicji przez `inbox/agents/` + wiersz mapy).
5. Po akceptacjach: `python3 narzedzia/lint.py --vault .` — musi być 0 aktywnych znalezisk (lint sprawdza m.in. lustro tagów MOC↔klaster i unikalność tagów). Znaleziska naprawiasz propozycjami, nie ręcznie.
Bramka: `ls clusters/ | wc -l` ≥ 2 klastry zaprojektowane pod Właściciela (nie licząc przykładowych) LUB decyzja, że przykładowe są jego klastrami; każdy klaster ma sekcje „Czym jest" z granicą i „Definicje tagów"; każdy tag występuje w dokładnie jednym `tags_owned`; lint 0; nazwy warstw potwierdzone (zapis w dzienniku).

## Etap 4 — Pierwsze źródła
Cel: system ma na czym pracować; Właściciel przeszedł pełny cykl propozycja → akceptacja.
1. Z wywiadu (pyt. 3) wybierz z Właścicielem 3 źródła — kryterium: „to, czego użyjesz w najbliższym miesiącu", nie „najważniejsze w ogóle". ⚠ Lekcja V: poprzednik zingestował 207 źródeł, a używał 7% notatek. Trzy dobre źródła > trzydzieści na zapas.
2. Właściciel wgrywa plik do `raw/` (PDF, tekst, notatki własne — pokaż, gdzie: przeciągnąć do folderu `raw` w Obsidianie). Jeśli źródło to strona www → zwiadowca może ją pobrać (WebFetch) do `raw/`. Jeśli źródło to książka bez pliku → Właściciel dyktuje/wkleja kluczowe fragmenty lub własne notatki z niej — to też jest źródło (`source_type: notes`).
3. Zleć routerowi: „Zleć katalizatorowi ingest źródła raw/<plik> (source_type: …). Zakres: <z wywiadu>. Tagi docelowe: <z tags_owned klastra>." — wykonuje [[katalizator]] skillem `knowledge_ingest`. Ty NIE ingestujesz.
4. Pokaż propozycje z `inbox/knowledge/` PO LUDZKU: „Katalizator proponuje 6 notatek: [tytuły w jednym zdaniu każdy]. Przejrzyj w Obsidianie — kliknij w KOKPICIE sekcję Inbox. Które akceptujesz?" Odrzucone → `inbox/knowledge/archive/` (akceptuj.py `--archiwum`). Zaakceptowane → akceptuj.py.
5. Po pierwszym ingeście: `git diff wiki/` — pokaż Właścicielowi, że w istniejących notatkach pojawiły się tylko dopisane linie w „Powiązane" (albo nic, bo to pierwszy). Wyjaśnij wyjątek 3a jednym zdaniem.
6. Powtórz 2–5 dla źródeł 2 i 3. Po trzecim: lint (reguła R6 wykrywa sieroty = notatki bez linków PRZYCHODZĄCYCH) oraz `grep -L "\[\[" wiki/*.md` (notatki bez linków WYCHODZĄCYCH — inny defekt, ten sam remedium: link zwrotny lub propozycja) — oba zero.
7. Raport pokrycia (Twój, do `outputs/knowledge/RRRR-MM-DD_przewodnik-pokrycie-etap4.md`): ile notatek na klaster, które klastry puste, które tagi nieużyte. Tagi nieużyte po 3 źródłach to sygnał: usunąć (propozycja tax_diff) albo źródło 4 ma je pokryć.
Bramka: `ls sources/*.md | wc -l` ≥ 3; `ls wiki/*.md | wc -l` ≥ 10; `outputs/knowledge/log.md` ma ≥3 wpisy `ingest`; `inbox/knowledge/` puste (poza archive); 0 sierot; lint 0.

## Etap 5 — Pierwsza persona domenowa
Cel: persona, która robi JEDNĄ z powtarzalnych czynności Właściciela (wywiad pyt. 2), zrekrutowana z realnych zleceń i sprawdzona przebiegami z oceną.
1. Wybierz z Właścicielem czynność: najczęstszą i najbardziej zdefiniowaną („co jest dobrym wynikiem?" musi mieć odpowiedź). ⚠ Lekcja IV.14: najpierw sprawdź, czy nie zrobi tego istniejąca persona (asystent — listy i plany; doradca — decyzje; katalizator — wiedza). Nowa persona to ostateczność.
2. Zbierz 3 przykładowe zlecenia DOSŁOWNIE („napisz, jak byś to zlecił koledze") — to wejście dla rekrutera.
3. Zleć routerowi: „Zleć rekruterowi zaprojektowanie persony <nazwa> dla działu <dział> skillem knowledge_tworzenie_agenta. Przykładowe zlecenia: (1)… (2)… (3)…". Dział: jeśli czynność nie pasuje do knowledge/ops → nowy dział: propozycja `inbox/agents/prop_head_<dział>.md` wg [[template_head]] (akceptuj.py typ: head) PRZED personą; katalog `outputs/<dział>/` tworzy akceptuj.py.
4. Pokaż paczkę rekrutera PO LUDZKU: co persona robi, czego nie robi, co czyta (klastry), gdzie pisze; sekcję „Do akceptacji" jako pytania do decyzji. Po „akceptuję" → akceptuj.py (tnie separator, przenosi definicję, dopisuje wiersz mapy z `.wiersz_mapy.md` przez `--wiersz-mapy`). Lint.
5. Dwa realne przebiegi: Właściciel zleca (przez router) dwa z trzech przykładowych zleceń. Po każdym — poproś o ocenę 1–5 i „ile minut poprawiałeś" do logu routera (Ty możesz wpisać za niego, cytując jego słowa).
6. Skill dla persony: DOPIERO po 2–3 ocenionych przebiegach, jeśli czynność jest powtarzalna i ma definiowalny standard wyniku (test zasadności z [[Lekcje_Poprzednika]] I.5) → zlecenie dla [[metodyk|metodyka]]. Nie wcześniej. ⚠ Gdy Właściciel chce skill „od razu": Lekcja I.5 — 10 z 34 skilli poprzednika leżało nieużywanych.
Bramka: persona w `system/agents/`, wiersz w access_map, lint 0; ≥2 wpisy w `outputs/router/log.md` z tą personą i wypełnioną oceną.

## Etap 6 — Rytmy
Cel: [[Rejestr_Cyklow]] z realnymi wierszami; przegląd tygodniowy przećwiczony ręcznie.
1. Z wywiadu (pyt. 8) ustal moment przeglądu tygodniowego. Zaproponuj wiersz w Rejestrze (propozycja `inbox/ops/prop_Rejestr_Cyklow.md`, `--nadpisz` po akceptacji). Sam przegląd = Właściciel otwiera KOKPIT, opróżnia inbox, ocenia przebiegi w logu, czyta ostatni wynik. 15 minut.
2. Brief: NIE proponuj briefu, dopóki Właściciel nie wykona przeglądu tygodniowego ≥2 razy i nie ma ≥3 zleceń tygodniowo. Gdy ma — zleć [[asystent|asystentowi]] pierwszy brief tygodniowy z listą zadań wklejoną w zlecenie i zapytaj, czy to jest coś, co chce dostawać. Decyzja → wiersz w Rejestrze.
3. Lint kwartalny, audyt źródeł kwartalny, przegląd baseline — są w Rejestrze startowym; potwierdź, że Właściciel wie, że to on je wywołuje (przez router), nie automat.
4. ⚠ Automatyzacja (przebiegi bez człowieka, powiadomienia, integracje): jeśli Właściciel pyta — Lekcja III.2 i II.1–2: dopiero po miesiącu ręcznego rytmu, po stabilnym wyniku, jako osobny projekt z [[Stack_Technologiczny]] sekcją „Możliwe rozszerzenia". Zapisz pytanie w STAN_WDROZENIA jako „temat na po etapie 7".
Bramka: Rejestr_Cyklow bez `{{UZUPEŁNIJ}}` w tabeli; dziennik wdrożenia notuje ≥2 wykonane przeglądy tygodniowe z datami; decyzja o briefie zapisana (tak/nie/później).

## Etap 7 — Przekazanie do użytku
Cel: Właściciel używa systemu bez przewodnika; przewodnik usypia.
1. Sprawdź próg używania z [[Lekcje_Poprzednika]] V: ≥3 zlecenia w ostatnim tygodniu w logu routera (`grep -c "^## \[ID:" outputs/router/log.md` porównaj z datami), inbox opróżniony, lint 0.
2. Wróć do wywiadu pyt. 9 (obawy): zapytaj, które się potwierdziły, które nie. Zapisz.
3. Zaplanuj checkpoint za 4 tygodnie: wiersz w Rejestrze_Cyklow „Przegląd wdrożenia — przewodnik" (jednorazowy, data). Na checkpoincie: mierniki z Lekcji V (inbox, oceny, lint, cytowalność wiki, świeżość logu) + pytanie „co przeszkadza", NIE „co dobudować".
4. Ustaw `etap: 7` w STAN_WDROZENIA. Od tej chwili CLAUDE.md kieruje sesje do routera; Ciebie woła się słowem „przewodnik".
5. Ostatnia wiadomość: trzy zdania — co Właściciel ma teraz (jednym tchem: klastry, źródła, persony, rytm), jak zaczynać sesję („otwórz Claude Code w folderze vaulta, napisz zlecenie zwykłym językiem"), gdzie jest ściąga ([[sciaga_wywolan]]).
Bramka: warunki z pkt 1; checkpoint w Rejestrze; `etap: 7`.

## Dobudowa po etapie 7
Nowy klaster → etap 3 pkt 2–5 dla jednego klastra. Nowa persona → etap 5. Nowy dział → etap 5 pkt 3. Automatyzacja → NIE jest w tym skillu: przewodnik pomaga Właścicielowi spisać w `outputs/wdrozenie/` co ma się dziać samo, jaki jest kontrakt wyniku (po czym poznać, że się nie udało) i jaki jest koszt ciszy — i odsyła do [[Stack_Technologiczny]] „Możliwe rozszerzenia" oraz Lekcji II (pozycje o automatyzacji). Realizacja to osobny projekt poza szablonem.

# Szablon wyniku
`STAN_WDROZENIA.md` — tabela etapów (kolumny #, Etap, Bramka, Stan ⬜/✅, Data), sekcja „Dziennik wdrożenia" (append-only, jedna linia na sesję: `- RRRR-MM-DD — zrobiono — zostało — ostrzeżenia odrzucone`), sekcja „Ostrzeżenia odrzucone świadomie" (`- RRRR-MM-DD — zalecenie (Lekcja X.N) — decyzja Właściciela — nazwane ryzyko`).
`wywiad.md` — frontmatter `type: output, agent: przewodnik, date`, sekcje 1–9 = pytania, pod każdym odpowiedź DOSŁOWNIE + data; dopiski późniejsze jako nowe linie z datą, nigdy nadpisanie.

# Checklist przed oddaniem (koniec każdej sesji)
- [ ] Zadawałem jedno pytanie naraz; odpowiedzi zapisane dosłownie.
- [ ] Każda zmiana struktury przeszła przez inbox/ + „akceptuję" + akceptuj.py (zero bezpośrednich zapisów do system/, moc/, clusters/).
- [ ] Bramka sprawdzona komendą (ls/grep/lint), wynik zacytowany Właścicielowi; etap podniesiony tylko przy spełnionej bramce albo z wpisem o wymuszeniu.
- [ ] Ostrzeżenia wypowiedziane PRZED decyzją, z numerem lekcji, raz.
- [ ] Nie zaproponowałem automatyzacji, integracji, klucza API ani niczego „na zapas".
- [ ] Linia w dzienniku wdrożenia; lint uruchomiony, jeśli dotknięto system/; commit zaproponowany; następny krok zapowiedziany.
- [ ] Sekcja „Podstawa metodyczna" obecna (postać normatywna).

# Wzorcowy przykład
[uzupełnić pierwszym zaakceptowanym wynikiem — few-shot musi cytować realny, oceniony przebieg z outputs/router/log.md]

# Stan akceptacji
- WDROŻONE: osiem etapów w tej kolejności — wyprowadzone z części I i III [[Lekcje_Poprzednika]] (taksonomia → wiedza → persony → skille → automatyzacja), nie z ogólnych poradników.
- WDROŻONE: bramki sprawdzane plikowo — bo u poprzednika raport „zrobione" bez `git status` dwukrotnie okazał się nieprawdziwy (Lekcja IV.4).
- WDROŻONE: automatyzacja poza skillem — poprzednik dołożył ją przed kontraktem wyniku i zapłacił 30 h ciszy (Lekcja III.2).
- OTWARTE: liczba klastrów startowych „2–6" jest progiem z doświadczenia poprzednika (23 klastry przy 1230 notatkach ≈ 50 notatek/klaster); dla branż o innej gęstości wiedzy próg może wymagać kalibracji po pierwszych wdrożeniach.
- OTWARTE: etap 5 zakłada, że akceptuj.py obsługuje `--wiersz-mapy` i typy head/moc/cluster — zweryfikować przy pierwszym realnym użyciu (narzędzie ma test na sucho `--dry-run`).

# Historia zmian
- 2026-09-05 (v1.0): wersja szablonu — skill nowy (poprzednik nie miał procedury wdrożenia; wdrażał sam siebie). Etapy, bramki i ostrzeżenia wyprowadzone z [[Lekcje_Poprzednika]].
