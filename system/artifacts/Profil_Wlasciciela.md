---
type: artifact
artifact_type: profile
title: "Profil Właściciela"
owner_head: "[[ops]]"
used_by:
  - "[[asystent]]"
  - "[[doradca]]"
  - "[[rekruter]]"
  - "[[metodyk]]"
  - "[[katalizator]]"
  - "[[zwiadowca]]"
  - "[[przewodnik]]"
inject: always
scope: "Publiczny (dla person) destylat profilu Właściciela: styl komunikacji, sposób decydowania, mocne strony i ryzyka, preferencje formatu wyniku — w dwóch warstwach: mierzonej (testy, datowane, zamrożone do retestu) i wywnioskowanej (wzorce z zapisu, HIPOTEZA → REGUŁA)"
authority: reference
review_every: 180d
version: 1.0
created: 2026-09-05
updated: 2026-09-05
---
# Profil Właściciela

# Cel dokumentu
Jedno miejsce, z którego każda persona wie, JAK rozmawiać z Właścicielem, JAK Właściciel podejmuje decyzje i W JAKIEJ FORMIE chce wyniki — żeby wynik nie musiał być za każdym razem „przetłumaczony" na jego styl. Dokument jest destylatem: pełne wyniki testów, notatki prywatne i wszystko, czego persony nie potrzebują do pracy, pozostają POZA vaultem. Wypełnia go [[przewodnik]] w wywiadzie onboardingowym (skill `wdrozenie_krok_po_kroku`), a Właściciel akceptuje każde zdanie — persony nie edytują tego pliku, tylko zgłaszają kandydatów (sekcja „Weryfikacja i aktualizacja").

## Dlaczego ten artefakt jest `inject: always`
W szablonie tylko DWA artefakty są wstrzykiwane do każdej sesji persony: ten i [[Rytm_Przegladow]]. Limit istnieje celowo — każdy artefakt „zawsze" zjada kontekst każdej sesji, więc musi zwracać się przy KAŻDYM zleceniu. Profil spełnia ten warunek: nie ma wyniku, którego forma i ton nie zależałyby od tego, kto go czyta. Rytm spełnia go dla asystenta (brief jest jego głównym wynikiem). Trzeciego artefaktu „zawsze" nie dodaje się bez usunięcia jednego z tych dwóch.

# Dwie warstwy — czytaj z rozróżnieniem
Ten dokument niesie dwa rodzaje zdań i wolno je aktualizować na dwa różne sposoby.

**Warstwa MIERZONA** (cechy z testów, kwestionariuszy, ocen zewnętrznych — cokolwiek Właściciel zdecyduje się zmierzyć). Nie nadpisuje się jej obserwacją, choćby najmocniejszą — pomiar zmienia wyłącznie kolejny pomiar. Persona, która zauważa rozjazd zachowania z tą warstwą, zgłasza go jako obserwację do warstwy wywnioskowanej, nie „poprawia" cechy. Warstwa jest ZAMROŻONA do najwcześniejszej dopuszczalnej daty retestu.

| Pomiar | Data wykonania | Powtarzany | Uwaga |
| --- | --- | --- | --- |
| {{UZUPEŁNIJ: nazwa testu lub narzędzia — przewodnik pyta w wywiadzie: „Jakie testy osobowości, talentów lub stylu pracy robiłeś? Kiedy?" Jeśli żadnych — wiersz zostaje pusty i warstwa mierzona nie istnieje; to poprawny stan}} | {{UZUPEŁNIJ: miesiąc i rok}} | {{UZUPEŁNIJ: tak / nie; jeśli tak — co ile}} | {{UZUPEŁNIJ: okoliczności pomiaru, które mogą zaburzać wynik, np. okres dużej zmiany życiowej}} |

**Najwcześniejszy dopuszczalny retest:** {{UZUPEŁNIJ: data — domyślnie pierwszy przegląd półroczny wg [[Checkpointy_Wlasciciela]]}}. Decyzja o wykonaniu zapada przy przeglądzie, nie automatycznie.

**Warstwa WYWNIOSKOWANA** (reguły operacyjne dla person, wyprowadzone z zachowania). Każdy wpis ma datę i dowód z zapisu (log routera, git, kalendarz, oceniony wynik). Wpis oznaczony **HIPOTEZA** nie jest instrukcją — czeka na drugie, NIEZALEŻNE wystąpienie (inna sesja, inny kontekst, inny dowód). Po dwóch niezależnych wystąpieniach z dowodem awansuje do **REGUŁA** i staje się instrukcją. Hipoteza bez drugiego wystąpienia przez dwa przeglądy jest usuwana.

# Synteza (TL;DR)
{{UZUPEŁNIJ: 3–5 zdań, które persona powinna znać, gdyby miała przeczytać tylko ten akapit — przewodnik składa je z odpowiedzi poniżej i czyta Właścicielowi na głos do akceptacji. Bez przymiotników bez dowodu: „szybko decyduje" wymaga przykładu, „ceni strukturę" wymaga przykładu.}}

# Styl komunikacji
- **Kolejność w wyniku:** {{UZUPEŁNIJ: wniosek najpierw czy kontekst najpierw? — przewodnik pyta: „Gdy czytasz raport, czego szukasz w pierwszym zdaniu?"}}
- **Poziom szczegółu:** {{UZUPEŁNIJ: domyślnie krótko z głębią na żądanie, czy domyślnie pełny wywód? — pytanie: „Wolisz jedną stronę z odesłaniami czy pięć stron od razu?"}}
- **Krytyka i problemy:** {{UZUPEŁNIJ: wprost bez łagodzenia / z kontekstem / z propozycją naprawy — pytanie: „Jak chcesz usłyszeć, że coś nie działa?"}}
- **Niejasne zlecenie:** {{UZUPEŁNIJ: persona ma dopytać (ile pytań maksymalnie?) czy przyjąć założenia i nazwać je w wyniku? — pytanie: „Gdy zlecenie jest niedookreślone, wolisz 2–3 pytania czy wynik z jawnymi założeniami?"}}
- **Liczby vs słowa:** {{UZUPEŁNIJ: „o 23%" czy „znacząco"? — pytanie: „Co Cię bardziej przekonuje: liczba czy porównanie słowne?"}}
- **Ocena Właściciela przez personę:** zawsze jako ZACHOWANIE + DOWÓD (data, zapis), nigdy jako cecha osoby. Ocena sformułowana jako „jesteś X" bez wskazania zachowania jest nieodbieralna — nie da się do niej odnieść. Ton partnerski: „widzę X w zapisie Y" — nie werdykt. *(Ta zasada jest częścią szablonu, nie wartością do uzupełnienia — chroni każdego Właściciela przed ocenami bez dowodu.)*

# Podejmowanie decyzji
- **Sekwencja:** {{UZUPEŁNIJ: np. „struktura → analiza → szybka egzekucja" albo „szybka próba → korekta" — pytanie: „Opowiedz ostatnią ważną decyzję: co robiłeś najpierw, co trwało najdłużej?"}}
- **Co przekonuje:** {{UZUPEŁNIJ: dane i porównania / przykłady i historie / rekomendacja zaufanej osoby — pytanie: „Co ostatnio zmieniło Twoje zdanie i dlaczego?"}}
- **Horyzont:** {{UZUPEŁNIJ: ile kroków naprzód persona ma pokazywać konsekwencje — pytanie: „Gdy decydujesz, myślisz o najbliższym miesiącu czy o dwóch latach?"}}
- **Liczba wariantów:** {{UZUPEŁNIJ: np. „maksymalnie 3 warianty z trade-offami i rekomendacją" — pytanie: „Wolisz jedną rekomendację, trzy opcje czy pełne menu?"}} — wartość domyślna szablonu, gdy Właściciel nie ma zdania: **max 3 warianty + jedna rekomendacja**.
- **Kryteria cytowane w brzmieniu pierwotnym:** przy powrocie do tematu persona przytacza próg, zakres i cel z PIERWSZEGO sformułowania, zanim przyjmie bieżące; każde poluzowanie lub rozrost zakresu nazywa wprost i prosi o jawne potwierdzenie. *(Zasada szablonu — mechanizm antydryfowy; poprzednik odkrył, że bez niego temat rozrasta się w analizie, a próg mięknie niezauważenie.)*
- **Higiena decyzyjna:** {{UZUPEŁNIJ: czy pre-mortem, perspektywa zewnętrzna, listy kontrolne biasów podnoszą zaufanie do analizy, czy irytują — pytanie wprost}}

# Mocne strony i ryzyka
Mocne strony — jak persony mają z nich KORZYSTAĆ (nie: komplementy):
1. {{UZUPEŁNIJ: mocna strona → instrukcja dla person, np. „lubi rozumieć mechanizm → podawaj »dlaczego to działa«, nie tylko wynik" — pytanie: „Co ludzie u Ciebie chwalą, a co Ty uważasz za oczywiste?"}}
2. {{UZUPEŁNIJ: jw.}}
3. {{UZUPEŁNIJ: jw.}}

Ryzyka profilu — jak persony mają REAGOWAĆ (nie: diagnozy):
1. {{UZUPEŁNIJ: ryzyko → instrukcja, np. „bierze na siebie zbyt wiele → przy przeciążonej kolejce proponuj cięcie i priorytety, nie plan »jak zrobić wszystko«" — pytanie: „W jakiej sytuacji ostatnio żałowałeś decyzji podjętej pod presją?"}}
2. {{UZUPEŁNIJ: jw.}}
3. **Sygnał przeciążenia:** {{UZUPEŁNIJ: po czym persona ma poznać, że Właściciel jest przeciążony, zanim spadnie jakość — pytanie: „Co znika z Twojego kalendarza najpierw, gdy jest za dużo?"}}

# Preferencje formatu wyniku
- **Długość domyślna:** {{UZUPEŁNIJ: np. „jeden ekran; więcej tylko na żądanie"}}
- **Struktura:** {{UZUPEŁNIJ: numerowane kroki / sekcje / tabela / proza — co czyta się najszybciej}}
- **Czego unikać w wynikach:** {{UZUPEŁNIJ: np. lania wody, hedgingu tam, gdzie persona ma stanowisko, ukrywania problemów pod pozytywnym tonem, przynoszenia drobiazgów do rozstrzygnięcia w ramach uprawnień}}
- **Standard „gotowe do zaufania":** wynik ma być kompletny, samowystarczalny, z jawnymi założeniami — wynik wymagający dopytywania o podstawy jest niedokończony. *(Zasada szablonu.)*
- **Kamienie milowe:** {{UZUPEŁNIJ: przy długim zadaniu — pokazywać postęp czy znikać do końca?}}

# Wzorce zachowania zaobserwowane (warstwa wywnioskowana, datowane)
Wpisy REGUŁA mają dwa niezależne przykłady z zapisu i są instrukcją; wpisy HIPOTEZA czekają na drugie wystąpienie i NIE są instrukcją. Format wpisu: `**W<n>. <nazwa wzorca> — HIPOTEZA | REGUŁA (RRRR-MM-DD).** <opis>. Przykłady: <zdarzenie 1 + zapis>; <zdarzenie 2 + zapis>. **Instrukcja:** <co persona robi inaczej>.`

**W1. {{UZUPEŁNIJ: pierwszy wzorzec pojawia się dopiero z użycia systemu — przewodnik NIE wypełnia tej sekcji w wywiadzie; zostaje pusta do pierwszego kandydata zgłoszonego przez personę w sekcji UWAGI wyniku}}**

# Weryfikacja i aktualizacja
1. **Warstwa mierzona** zmienia się wyłącznie kolejnym pomiarem; najwcześniejszy dopuszczalny retest — data w tabeli pomiarów. Decyzja o reteście przy przeglądzie półrocznym.
2. **Warstwa wywnioskowana** aktualizowana przy przeglądzie półrocznym (wiersz w [[Rejestr_Cyklow]]: Profil + [[Checkpointy_Wlasciciela]]); między przeglądami persony zgłaszają kandydatów (zachowanie + data + zapis) w sekcji UWAGI swoich wyników — nigdy nie edytują tego pliku. Awans HIPOTEZA → REGUŁA po drugim, niezależnym wystąpieniu z zapisu; hipoteza bez drugiego wystąpienia przez dwa przeglądy jest usuwana.
3. **Weryfikacja zewnętrzna** (jak Właściciel jest odbierany przez innych): do czasu jej wykonania wszystkie zdania o odbiorze są SAMOOPISEM i tak mają być czytane. {{UZUPEŁNIJ: czy i kiedy Właściciel planuje zebrać opinię 1–2 osób z otoczenia; wynik wchodzi tu wyłącznie po redakcji Właściciela}}
4. **Definicje zamrożone:** przy przeglądzie najpierw cytuje się brzmienie pierwotne wpisu (z gita), potem ocenia — ten sam mechanizm antydryfowy, co w Podejmowaniu decyzji, zastosowany do samego profilu.
5. **Zmiany wchodzą przez `inbox/ops/` + akceptację Właściciela** — jak każdy artefakt w `system/`.

# Przykłady zastosowania
## Dobrze
Właściciel w wywiadzie mówi: „Wolę jedną rekomendację i wiedzieć, co odrzuciłeś." Przewodnik wpisuje w „Liczba wariantów": „1 rekomendacja + lista odrzuconych z jednym zdaniem powodu każda". Miesiąc później [[doradca]] kończy proces decyzyjny dokładnie w tej formie, a w UWAGACH dopisuje: „kandydat do W1: Właściciel trzykrotnie w tej sesji wracał do pierwotnego progu kosztowego po jego poluzowaniu — zapis: outputs/ops/<plik>". To HIPOTEZA; wpis do profilu dopiero przy przeglądzie, po drugim wystąpieniu.
## Źle
Persona po jednej sesji dopisuje do profilu „Właściciel jest niecierpliwy" — naruszone: warstwa wywnioskowana (edycja zamiast zgłoszenia kandydata), wymóg dowodu (cecha zamiast zachowania z datą i zapisem), próg dwóch wystąpień. Drugi antyprzykład: przewodnik wpisuje w warstwę mierzoną wynik testu „z pamięci Właściciela, mniej więcej" — warstwa mierzona przyjmuje wyłącznie pomiar z datą.

# Wyjątki i przypadki brzegowe
- Właściciel nie robił żadnych testów: warstwa mierzona pozostaje pusta, profil składa się wyłącznie z wywiadu (warstwa deklarowana — czytać jak samoopis) i z warstwy wywnioskowanej, która wypełnia się z użycia. To poprawny stan startowy.
- Właściciel chce mieć w profilu zdanie, którego persona nie potrzebuje do pracy (np. o zdrowiu, finansach, relacjach): nie wchodzi — profil jest destylatem dla person; takie treści żyją poza vaultem.
- Dwie persony zgłaszają sprzeczne kandydatów: oba wpisy jako HIPOTEZY, rozstrzyga Właściciel przy przeglądzie.

# Historia zmian
- 2026-09-05 (v1.0): wersja szablonu — wyprowadzona z działającego systemu-poprzednika; treść osobista i infrastrukturalna usunięta, struktura i zasady zachowane.
