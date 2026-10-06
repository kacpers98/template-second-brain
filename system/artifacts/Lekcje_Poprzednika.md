---
type: artifact
artifact_type: reference
title: "Lekcje Poprzednika"
owner_head: "[[knowledge]]"
used_by:
  - "[[przewodnik]]"
  - "[[rekruter]]"
  - "[[metodyk]]"
  - "[[katalizator]]"
inject: on_reference
scope: "Baza doświadczeń systemu-poprzednika: co zbudował i wycofał, jakie zasady wyrosły z incydentów, gdzie zła kolejność kosztowała przebudowę. Przewodnik cytuje stąd ostrzeżenia; nie jest to norma, lecz materiał dowodowy."
authority: reference
review_every: 365d
version: 1.0
created: 2026-09-05
updated: 2026-09-05
---
# Lekcje Poprzednika

# Cel dokumentu
Ten szablon nie powstał na desce kreślarskiej. Został wyprowadzony z systemu, który jedna osoba budowała i używała intensywnie przez kilka miesięcy: 19 person, 34 procedury, ponad 1200 notatek wiedzy, warstwa automatyzacji na osobnym serwerze, ponad 150 zarejestrowanych przebiegów z oceną, kilkanaście incydentów z pełną diagnozą. Część tego, co zbudował, wycofał — i te wycofania są cenniejsze niż to, co zostało, bo pokazują, gdzie NIE iść. [[przewodnik]] cytuje stąd ostrzeżenia, gdy Właściciel chce postąpić inaczej niż wynika z tych doświadczeń. Dokument jest materiałem dowodowym, nie normą: Właściciel może zdecydować wbrew każdej z tych lekcji — ale wtedy przewodnik zapisuje tę decyzję w `outputs/wdrozenie/STAN_WDROZENIA.md` jako świadomą, z nazwanym ryzykiem.

# Część I — Właściwa kolejność budowy (potwierdzona, nie teoretyczna)

Poprzednik zapisał jawny kamień milowy „punkt startowy architektury agentowej" i to, co było przed nim, okazało się właściwą kolejnością:

1. **Taksonomia PRZED wiedzą.** Lista tagów należących do klastrów (`tags_owned`) istniała, zanim wchłonięto pierwsze masowe źródła. Każda notatka od pierwszego dnia miała pełny frontmatter (typ, warstwa, klaster, tagi z puli). Skutek: ponad tysiąc notatek później taksonomia miała 0 tagów-duplikatów i 0 notatek bez przypisania.
2. **Wiedza PRZED personami.** Persony dostały pierwsze przebiegi, gdy było na czym pracować (kilkadziesiąt źródeł). Persona bez wiedzy w vaultcie improwizuje z pamięci modelu i nie różni się od zwykłego czatu.
3. **Syntezy i stanowiska Właściciela PO ingeście, PRZED produkcją.** Gdy źródła się kłóciły, poprzednik pisał krótką notatkę „stanowisko właściciela" rozstrzygającą spór — dopiero wtedy persony mogły cytować jedną linię zamiast wahać się między dwiema.
4. **Persony testowane INTERAKTYWNIE, zanim cokolwiek działało samo.** Każda persona miała kilka przebiegów z oceną 1–5 w logu, zanim dostała skill.
5. **Skill wyprowadzony z 2–3 OCENIONYCH przebiegów, nie napisany na zapas.** Test zasadności skilla: czynność powtarzalna + definiowalny standard wyniku + więcej niż jedno wystąpienie. Skille pisane „bo się przydadzą" leżały nieużywane (10 z 34 miało status „uśpiony" bez ani jednego przebiegu).
6. **Automatyzacja NA KOŃCU, po stabilnym kontrakcie wyniku.** Poprzednik uruchomił cykliczne przebiegi bez człowieka zanim ustalił, jak rozpoznać, że przebieg się nie udał — i zapłacił 30 godzinami ciszy, w której system wyglądał na zdrowy, a nie dostarczał nic.

**Reguła nadrzędna, którą poprzednik sformułował po tych doświadczeniach: zmiany z UŻYCIA, nie z inspiracji.** Każda zmiana systemu ma wynikać z realnego bólu zapisanego w logu, nie z pomysłu „fajnie by było".

# Część II — Ślepe uliczki (zbudowane, użyte, wycofane)

Każda pozycja: co to było → dlaczego nie działało → czym zastąpiono. Bez dat i szczegółów technicznych poprzednika; z mechanizmem, bo mechanizm się przenosi.

1. **Dwa środowiska wykonawcze naraz** (lokalne na komputerze + zdalne na serwerze). Dwa pisarze tych samych plików logów → konflikty przy każdym scaleniu, przez miesiąc. Zastąpione: JEDNO środowisko; komputer Właściciela wyłącznie do sesji interaktywnych. *Dla Ciebie:* ten szablon ma jedno środowisko od początku. Nie dokładaj drugiego, dopóki nie boli.
2. **Automatyczny „strażnik zdrowia" na komputerze Właściciela.** Dublował inny mechanizm, a gdy komputer spał — nie działał. Zastąpione: jedna kontrola sprawdzająca ARTEFAKT WYNIKOWY (czy plik z dzisiejszą datą istnieje), nie proces. *Lekcja:* kontrola ma sprawdzać wynik, nie to, czy „coś się uruchomiło".
3. **Rejestracja person jako oficjalnych typów subagentów narzędzia.** Delegacja po nazwie kończyła się błędem „nie znaleziono" lub cichą utratą uprawnień. Zastąpione: router wstrzykuje pełną definicję persony w treść delegacji (albo wciela ją w wątku głównym). *Lekcja:* tożsamość persony niesie TEKST definicji, nie rejestr narzędzia. Nie rejestruj person.
4. **Dostęp do wiedzy „per tag".** Dwie ręczne kopie tej samej normy (mapa dostępów + frontmattery person) rozjeżdżały się 13 razy w sześciu wersjach mapy; nadania „martwe" (tag przyznany, notatek zero). Zastąpione: dostęp per KLASTER (`cluster_access`), tagi wyłącznie jako nawigacja. Koszt migracji: trzy audyty nieporównywalne, dwie procedury do przepisania. *Dla Ciebie:* szablon ma już model klastrowy. Nie wprowadzaj drobniejszego, dopóki nie zmierzysz, że klaster jest za gruby (poprzednik zmierzył: tag NIE rozdzielał ani jednej notatki ponad to, co rozdzielał klaster).
5. **Datowane pliki wyników cyklicznych** (`brief_2026-08-01.md`, `brief_2026-08-02.md`…). Katalog puchł o plik dziennie, a mechanizm dostawy raz wysłał wczorajszy plik jako dzisiejszy, bo szukał „najnowszego". Zastąpione: JEDEN plik kanoniczny nadpisywany (`brief_ostatni_dzienny.md`), historię trzyma git, dostawa sprawdza datę w pliku. *Lekcja:* wynik cykliczny = jeden plik, git = archiwum.
6. **Norma powtórzona w treści zlecenia automatyzacji** („rygor tymczasowy" doklejany do zlecenia). Duplikat normy ze skilla → rozjazd, gdy skill się zmienił. Zastąpione: skill jest JEDYNYM miejscem normy; zlecenie tylko woła skill. *Lekcja:* jedna norma, jedno miejsce.
7. **Liczniki wpisów inkrementowane „bo pisze tylko jeden"** — obalone, gdy Właściciel zaczął wpisywać oceny WEWNĄTRZ wpisów, które pisał automat. Zastąpione: liczniki przeliczane od zera + zasada „człowiek nie edytuje pliku w oknie, w którym pisze do niego automat". *Dla Ciebie:* w sesji interaktywnej ten problem nie istnieje — pojawi się dopiero, gdy dołożysz automatyzację. Wtedy wróć tutaj.
8. **Dziennik serwera w ulotnej warstwie** — kasowany przy każdym wdrożeniu nowej wersji; przy awarii nie było historii i diagnoza pochłonęła cztery błędne hipotezy. *Lekcja uniwersalna:* przy każdej awarii NAJPIERW dziennik (log), POTEM hipotezy. Log jest po to, żeby go czytać, nie żeby istniał.
9. **Persona „kreatywna" na cyklicznym przebiegu bez człowieka** (miała co miesiąc proponować niespodziewane połączenia między notatkami). Bez deduplikacji i pamięci poprzednich przebiegów produkowała trzy razy te same „odkrycia"; własne raporty pokazały degenerację. Zaorana razem ze skillem. *Lekcja:* przebieg bez człowieka w pętli wymaga deduplikacji i historii, inaczej produkuje szum. Kreatywność zostaw sesjom interaktywnym.
10. **Jeden rejestr na WSZYSTKIE zadania** (jednorazowe i cykliczne razem, w vaultcie). Stał się drugim, gorszym masterem obok listy zadań, której Właściciel i tak używał w telefonie. Zastąpione: zadania jednorazowe POZA vaultem (lista zadań Właściciela), w vaultcie wyłącznie RYTMY ([[Rejestr_Cyklow]]); zero synchronizacji dwukierunkowej, tylko projekcja jednokierunkowa do briefu. *Lekcja:* dwa mastery o ROZŁĄCZNYCH zakresach zamiast jednego, który udaje, że jest jedyny.
11. **Rejestr spraw zdrowotnych w vaultcie.** Wycofany w dniu, w którym poprzednik uświadomił sobie, że czytają go persony i trafia do briefów wysyłanych na telefon. Zastąpiony wydarzeniami cyklicznymi w prywatnym kalendarzu. *Lekcja:* dane wrażliwe (zdrowie, finanse z kwotami, osoby trzecie) NIE wchodzą do vaulta, który czytają agenci. Vault jest narzędziem AI — zapis do niego to wprowadzenie treści do narzędzia AI.
12. **Przyciski na pulpicie** (wtyczka do klikalnych komend w Obsidianie). Wtyczka nie działała stabilnie, godziny diagnozy, zero efektu. Zastąpione: komendy w terminalu i w sesji Claude Code. *Lekcja:* pulpit ma POKAZYWAĆ stan (tabele), nie WYKONYWAĆ akcji.
13. **Katalog „ulotne" w vaultcie na dane wrażliwe „tylko na chwilę".** Zlikwidowany: cokolwiek jest w vaultcie, jest w gicie, w synchronizacji i w zasięgu ingestu. Zastąpione: sesje na danych wrażliwych prowadzone w katalogu POZA vaultem. *Lekcja:* „tylko na chwilę" w vaultcie nie istnieje.
14. **Rozpoznawanie błędu po słowach kluczowych w tekście wyniku** („jeśli w wyniku jest słowo ‘błąd’, to alarm"). Fałszywe alarmy, gdy raport testów zawierał słowo „błąd" w opisie testu, który przeszedł. Zastąpione: jawny znacznik statusu z zamkniętego słownika jako ostatnia linia + kody powrotu. *Lekcja:* status to kontrakt, nie heurystyka.
15. **Sekcja „Do akceptacji" w propozycji bez mechanicznego separatora.** Trzy definicje person przyjęto razem z aparatem propozycji; persona czytała warianty A/B jako własną regułę, a kolejny audyt wziął propozycję za rozstrzygnięcie. Instrukcja PROZĄ („usuń tę sekcję przy akceptacji") też zawiodła — została przeniesiona razem z sekcją, bo przeniesienie pliku to operacja bez czytania. Zastąpione: separator `---` + nagłówek jako MECHANIZM, który narzędzie akceptacji tnie automatycznie. *Lekcja:* jeśli coś ma się stać przy każdej akceptacji, musi to robić narzędzie, nie pamięć człowieka.
16. **Klucz z prawem zapisu do repozytorium na serwerze, token w adresie URL automatyzacji, sekrety w eksportach kopii zapasowych.** Każde z nich wyciekło albo prawie wyciekło (jeden token trafił do czatu zewnętrznego przez wklejenie alertu). Zastąpione: rejestr NAZW sekretów bez wartości ([[Rejestr_Sekretow]]), sekrety wyłącznie w zmiennych środowiskowych, alert traktowany jako sekret. *Lekcja:* w szablonie nie masz sekretów — i to jest stan pożądany. Każdy nowy klucz API = wiersz w rejestrze PRZED użyciem.
17. **Nazwa klastra zmieniona dzień po utworzeniu** (bo ramowanie „poziom jednostki, nie firmy" ustalono po fakcie). Koszt mały, bo wcześnie — ale ta sama zmiana po stu notatkach kosztowałaby przebudowę. *Lekcja:* ramowanie klastra (czym jest, czym NIE jest, granica → inny klaster) ustalasz PRZED nazwą.

# Część III — Błędy kolejności (gdzie „za wcześnie" lub „za późno" kosztowało)

1. **Kod produkcyjny przed kontrolą wersji** — dziesięć dni działania bez gita; potem duże pliki w historii repozytorium i dwie operacje „ścięcia historii". *Dla Ciebie:* `git init` to krok 0, zanim powstanie pierwsza notatka. Pliki PDF nigdy do gita (jest w `.gitignore`).
2. **Automatyzacja przed kontraktem wyniku** — cykliczne briefy ruszyły tygodnie przed tym, jak system umiał rozpoznać, że brief nie powstał. 30 godzin ciszy. *Dla Ciebie:* etap 6 (rytmy) jest ręczny. Automatyzacja to osobna decyzja PO tym, jak używasz rytmu ręcznie przez kilka tygodni.
3. **Model dostępu wprowadzony przed pomiarem, czy rozdziela** — patrz II.4.
4. **Skill na cyklu przed redakcją po zmianie normy** — gdy zmienił się model dostępu, dwie procedury cykliczne przez trzy przebiegi zwracały „zero trafień" formalnie poprawnie i całkowicie bezużytecznie, i trzy razy z rzędu ZGŁASZAŁY rozjazd, zanim ktoś zareagował. *Lekcja:* instrument bez reakcji to rytuał. Jeśli log pokazuje sygnał, ktoś musi go czytać.
5. **Few-shot (przykład wzorcowy) napisany PRZED ocenionym przebiegiem** — audyt wykrył sfabrykowany szczegół w przykładzie w definicji persony i cytowanie przebiegów, których nikt nie ocenił. *Dla Ciebie:* wszystkie few-shoty w szablonie są placeholderami. Wypełniasz je z realnych, ocenionych wyników — nigdy z wyobraźni.
6. **Ingest bez sekcji kanonicznej** — trzy notatki przyjęte z nagłówkiem „## Powiązania z vaultem" zamiast „## Powiązane" nigdy nie dostaną linku zwrotnego (mechanizm szuka dokładnego nagłówka), a lint tego nie łapie. *Lekcja:* szablon notatki obowiązuje od pierwszej notatki; drobny dryf nazewnictwa to trwała dziura.
7. **Norma zapisana zanim istniał kod ją egzekwujący** (pole „wstrzykuj zawsze" w headach, którego nic nie wstrzykiwało). *Lekcja:* jeśli norma mówi „system robi X automatycznie", sprawdź, że coś to robi. Jeśli nie — norma ma brzmieć „persona ma obowiązek zrobić X" (tak jest w tym szablonie: `inject: by_persona`).

# Część IV — Zasady, które wyrosły z incydentów (do stosowania od dnia 1)

1. **Jedna strona pary.** Najczęstsza klasa błędu w całym systemie (13 udokumentowanych wystąpień): zmiana jednej strony pary bez drugiej — frontmatter persony bez wiersza mapy, skill bez zasięgu persony, artefakt bez `used_by`. Dlatego istnieje `narzedzia/lint.py`: uruchamiaj po każdej sesji, która dotyka `system/`.
2. **Merge przed sesją, ocena po sesji.** Nie edytuj pliku, do którego w tym samym oknie pisze ktoś inny (dziś: nikt; jutro: automat).
3. **Log przed hipotezami.** Przy każdej awarii najpierw czytasz zapis, potem zgadujesz.
4. **Weryfikacja plikowa, nie deklaratywna.** Raport persony, który mówi „zapisałem plik X" nie jest dowodem — dowodem jest `git status`. Router weryfikuje przed wpisem do logu.
5. **Odmowa polityki zapisu to norma działająca, nie usterka do obejścia.** Persona zgłasza odmowę w wyniku; nikt nie szuka drogi naokoło.
6. **Description persony to koszt stały** (ładuje się przy każdym zleceniu): 300–900 znaków, tekst routingowy, nie opis stanowiska.
7. **Skill nie przechowuje danych, które dezaktualizują się po cichu** (stawki, progi, limity, adresy) — ustala je ze źródła przy każdym przebiegu.
8. **Brak danych = zapis „brak danych".** Zero szacowania z trendu, zero „dopełniania, żeby wyglądało na pełne". Wstrzymanie, „bez zmian", przebieg zerowy — to pełnoprawne wyniki.
9. **Ciche skrócenie zabronione; skrócenie z licznikiem dozwolone** („+4 dalsze").
10. **„Sprawdzono, pusto" ≠ „niesprawdzono".** Każdy wynik agregujący wejścia mówi, które wejścia sprawdził — inaczej cisza przy awarii wejścia wygląda jak spokój.
11. **Zapis do katalogu nie daje odczytu.** Kolumny Odczyt i Zapis są niezależne.
12. **Norma wiążąca zmienia się w artefakcie, nigdy „wykładnią" w procedurze.** Skill sprzeczny z artefaktem = zmiana artefaktu (decyzja Właściciela), nie interpretacja w skillu.
13. **Test przedmiotu** dla wszystkiego, co przychodzi z pracy dla innych: zdejmij okoliczności zlecenia — jeśli zostaje METODA, może wejść do vaulta; jeśli zostaje twierdzenie o kliencie/pracodawcy — nie. Anonimizacja jest konieczna, niewystarczająca.
14. **Nowy agent to ostateczność.** Najpierw rozszerzenie istniejącego; nowa persona dopiero, gdy trzy przykładowe zlecenia nie mieszczą się w żadnej.
15. **Mechanika w skillu, rola w definicji persony.** Po przyjęciu skilla tnie się few-shot persony do zachowań, nie kroków.
16. **Sekret nigdy w vaultcie, alert z sekretem jest sekretem, `printenv NAZWA` zamiast zrzutu całego środowiska.**
17. **Zmiany z użycia, nie z inspiracji.** Miernik zdrowia: briefy/wyniki czytane, inbox opróżniany w <7 dni, ≥1 łańcuch person w realnej pracy tygodniowo. Gdy „nie" — upraszczaj, nie dobudowuj.

# Część V — Mierniki zdrowia i definicja „używania"

Poprzednik zmierzył po trzech miesiącach: **z 1230 notatek wiki tylko 87 (7%) było kiedykolwiek zacytowanych w jakimkolwiek wyniku.** Reszta to „wieczne sieroty" — koszt ingestu bez zwrotu. To najważniejsza liczba w tym dokumencie, bo przeczy intuicji „im więcej wiedzy, tym lepiej".

Mierniki, które poprzednik uznał za miarodajne (od najtańszego):
1. **Inbox = 0** w ciągu 7 dni od propozycji (propozycja leżąca 14 dni = sygnał, że system produkuje więcej, niż Właściciel konsumuje).
2. **Ocena 1–5 + „poprawka w minutach"** per przebieg w logu routera (0 min = wynik użyty bez zmian). Oceny 4 dotyczyły u poprzednika niemal wyłącznie rzetelności faktograficznej (rok, liczba, nazwisko), nie procesu.
3. **Lint: 0 aktywnych znalezisk** (po każdej sesji dotykającej `system/`, i kwartalnie).
4. **Odsetek notatek wiki cytowanych w wynikach** — kwartalnie (`narzedzia/lint.py` nie liczy tego; przewodnik potrafi policzyć grepem). Rosnący = wiedza pracuje; płaski przy rosnącej liczbie notatek = ingestujesz na zapas.
5. **Świeżość logu routera** — tydzień bez wpisu przy „działającym" systemie = system nie jest używany.

**Definicja używania** (przyjęta przez poprzednika jako próg): brief lub inny wynik czytany w dni robocze, przegląd tygodniowy wykonany, **≥3 realne zlecenia tygodniowo**, propozycje domykane tego samego tygodnia. Tydzień poniżej progu nie jest porażką — jest sygnałem do pytania „co przeszkadza", nie „co dobudować".

**Przejście z roli twórcy do roli użytkownika** jest jawnym checkpointem (etap 7 wdrożenia). Poprzednik odkrył, że budowanie systemu jest przyjemniejsze niż jego używanie — i że bez jawnego progu buduje się w nieskończoność. Granica twórca/użytkownik: rozwój systemu NIE liczy się jako jego użycie.

# Wyjątki i przypadki brzegowe
- Właściciel może zdecydować wbrew każdej lekcji. Przewodnik ma wtedy obowiązek: nazwać ryzyko jednym zdaniem, zapisać decyzję w `STAN_WDROZENIA.md` (sekcja „Ostrzeżenia odrzucone świadomie") i NIE wracać do tematu, dopóki nie pojawi się skutek.
- Lekcje z części II dotyczące automatyzacji (1, 2, 5, 6, 7, 8, 9, 14) stają się aktualne dopiero, gdy Właściciel dokłada przebiegi bez człowieka w pętli. Przewodnik nie obciąża nimi Właściciela na etapach 0–6.

# Historia zmian
- 2026-09-05 (v1.0): wersja szablonu — wyprowadzona z działającego systemu-poprzednika; treść osobista i infrastrukturalna usunięta, struktura i zasady zachowane. Źródła: historia git trzech repozytoriów poprzednika, dwa logi (routera i wiedzy — ok. 360 wpisów), raporty techniczne z incydentów, dokumentacja techniczna v1.19.
