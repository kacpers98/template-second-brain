# Ściąga wywołań — gotowe zlecenia

Forma: piszesz w sesji Claude Code (otwartej w folderze vaulta) zwykłym językiem. Router sam dobierze personę; poniższe wzory pomagają, gdy chcesz być precyzyjny. Zmienna do podmiany: `[TREŚĆ]`.

## WDROŻENIE (przewodnik)
- Start / kontynuacja: `zacznijmy` albo `co dalej`
- Stan: `na jakim jesteśmy etapie?`
- Dobudowa po wdrożeniu: `przewodnik: chcę dodać nowy obszar wiedzy o [TEMAT]` · `przewodnik: chcę nową personę do [CZYNNOŚĆ]`
- Akceptacja propozycji z inboxa: `akceptuję [nazwa pliku lub „wszystko z inboxa"]` · odrzucenie: `odrzuć [nazwa] — [jedno zdanie dlaczego]`

## WIEDZA (knowledge)
- Ingest: `Zleć katalizatorowi ingest źródła raw/[PLIK] (source_type: book/article/doc/notes). Zakres: [CZEGO DOTYCZY]. Tagi docelowe: [TAGI Z tags_owned klastra].`
- Synteza z posiadanego: `Zlecenie syntezy dla katalizatora: utwórz 2–3 notatki dla tagu #[TAG] wyłącznie z zaingestowanych źródeł ([ŹRÓDŁA]). Propozycje przez inbox/knowledge/.`
- Nowy tag / klaster: `Zleć katalizatorowi rozszerzenie taksonomii: propozycja tagu #[TAG] w klastrze [[KLASTER]] z definicją i uzasadnieniem (przez inbox).`
- Zwiad (sprawdzenie źródeł z Listy): `Wykonaj przebieg zwiadowcy: pozycje z Lista_Zrodel_Zwiadowcy po terminie, nowości do inbox/knowledge/, aktualizacja last_checked i log.`
- Audyt źródeł (kwartalny): `Zleć zwiadowcy skill knowledge_audyt_zrodel za [KWARTAŁ]. Poprzedni audyt: [LINK lub „pierwszy"].`
- Audyt vaulta (health-check): `Zleć katalizatorowi skill knowledge_audyt. Zakres: [cały vault / KLASTER]. Wynik do outputs/knowledge/.`
- Nowa persona: `Zleć rekruterowi zaprojektowanie persony [NAZWA] dla działu [DZIAŁ] skillem knowledge_tworzenie_agenta. Przykładowe zlecenia: (1) […], (2) […], (3) […]. Paczka do inbox/agents/.`
- Przegląd persony: `Zleć rekruterowi skill knowledge_przeglad_agenta dla persony [NAZWA]. Materiał: log routera + outputs/[DZIAŁ]/.`
- Audyt dostępów (po ingeście lub dla jednej persony): `Zleć rekruterowi skill knowledge_audyt_dostepow, tryb [LEKKI: ingest DATA/ŹRÓDŁO | DORAŹNY: persona NAZWA].`
- Nowy skill (po 2–3 ocenionych przebiegach!): `Zleć metodykowi: stwórz skill "[NAZWA]" dla persony [PERSONA]. Procedura: [KROKI]. Wejście: […]. Wynik do outputs/[DZIAŁ]/. Paczka do inbox/skills/.`

## OPS
- Brief dzienny: `Zleć asystentowi skill ops_brief w trybie dziennym. Lista zadań: [WKLEJ]. Kalendarz: [WKLEJ].`
- Brief tygodniowy: `Zleć asystentowi skill ops_brief w trybie tygodniowym. Lista zadań: [WKLEJ]. Kalendarz na 7 dni: [WKLEJ].`
- Transkrypcja → plan: `Zleć asystentowi skill ops_transkrypcja_na_plan dla raw/transkrypcje/[PLIK].md.`
- Proces decyzyjny: `Zleć doradcy skill ops_proces_decyzyjny dla decyzji: [DECYZJA + KONTEKST + OGRANICZENIA].`

## KONTROLA I HIGIENA
- Lint spójności (po każdej zmianie w system/, i kwartalnie): `przewodnik: uruchom lint`
- Przebieg kontrolny (wynik o wysokiej stawce): dopisz do zlecenia `Po wykonaniu: przebieg kontrolny.` — router deleguje drugą personę adwersaryjnie.
- Ocena przebiegu: po ważniejszym wyniku wpisz w `outputs/router/log.md` ocenę 1–5 i „ile minut poprawiałeś" — albo powiedz to routerowi, on wpisze za Ciebie.

## Zasady szybkie
1. Linki zamiast streszczeń w przekazywaniu pracy między personami (persona z wymaganym wejściem odmówi bez linku — celowo).
2. Wyniki → `outputs/[dział]/`; propozycje zmian wiedzy/systemu → `inbox/` → Twoja akceptacja.
3. Po dobrym pierwszym przebiegu nowego typu: rozważ few-shot przez `knowledge_przeglad_agenta`.
4. Skill dopiero po 2–3 ocenionych przebiegach; persona dopiero, gdy trzy przykładowe zlecenia nie mieszczą się w żadnej istniejącej.
5. Nic „na zapas" — [[Lekcje_Poprzednika]], część V.
