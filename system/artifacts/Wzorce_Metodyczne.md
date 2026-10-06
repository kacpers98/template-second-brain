---
type: artifact
artifact_type: reference
title: "Wzorce Metodyczne"
owner_head: "[[knowledge]]"
used_by:
  - "[[metodyk]]"
  - "[[rekruter]]"
inject: on_reference
scope: "Katalog wzorców procedur wyprowadzonych ze skilli poprzednika, które nie weszły do szablonu (bo były domenowe), ale ich MECHANIZM jest uniwersalny. Metodyk sięga tu, projektując nowy skill; rekruter — projektując granice persony."
authority: reference
review_every: 180d
version: 1.0
created: 2026-09-05
updated: 2026-09-05
---
# Wzorce Metodyczne

# Cel dokumentu
Poprzednik miał 34 procedury; do szablonu weszło 11 uniwersalnych. Pozostałe 23 były domenowe (m.in. finanse, analiza regulacyjna, komunikacja publiczna, wytwarzanie oprogramowania) — ale każda niosła jakiś mechanizm, który działa niezależnie od dziedziny. Ten dokument je zbiera, żeby [[metodyk]] nie wymyślał ich od nowa, a [[rekruter]] wiedział, jakie granice persony sprawdziły się w praktyce. Każdy wzorzec: nazwa → mechanizm → kiedy stosować → z jakiej klasy skilla pochodzi.

# Wzorce

## 1. Mapa decyzyjna wstrzymania
**Mechanizm:** gdy procedura nie może dać wyniku z braku danych, NIE oddaje samej listy braków. Oddaje tabelę trójkolumnową: `brak → którą gałąź wyniku przesądza i w którą stronę → gotowe pytanie do adresata (kto, jakie brzmienie)`. Wynik oznaczony `wynik: wstrzymana` jest pełnoprawnym wynikiem, nie porażką.
**Kiedy:** każda procedura analityczna zależna od faktów, których persona nie ma (analiza przepisu, kwalifikacja przypadku, ocena zgodności).
**Źródło:** skill analizy regulacyjnej poprzednika.

## 2. Zero danych z pamięci, które dezaktualizują się po cichu
**Mechanizm:** skill nie zawiera ani jednej stawki, progu, limitu, adresu ani daty ważności — ustala je ze wskazanego ŹRÓDŁA przy każdym przebiegu i cytuje z datą stanu („stan na …"). Przypisanie z pamięci czegoś, co czytelnik nie jest w stanie zweryfikować, jest „najłatwiejszym możliwym fałszem, niewykrywalnym dla czytelnika".
**Kiedy:** wszystko regulowane przepisami, cennikami, normami technicznymi, wersjami.

## 3. Podwójna bramka normatywna przed analizą
**Mechanizm:** zanim persona analizuje, sprawdza w stałej kolejności: (1) czy przedmiot w ogóle jest „w grze" wg artefaktu-konstytucji; (2) czy jest sklasyfikowany (pytanie binarne do Właściciela, nie własne przypisanie). Zlecenie może korygować DANE (kwoty, fakty), nigdy NORMY (klasyfikacje, limity).
**Kiedy:** persony z artefaktem `authority: binding` — każda, która mogłaby „wyjść poza ramy, bo zlecenie tak brzmiało".

## 4. Stanowisko ≠ nakaz (komplet czterech elementów)
**Mechanizm:** persona wolno wydać rekomendację WYŁĄCZNIE jako komplet: uzasadnienie + alternatywa + ryzyka + warunki unieważnienia. Goły rozkaz („zrób X") jest zakazany; „wariant A wydaje się mocniejszy" bez kompletu — też.
**Kiedy:** doradztwo, oceny, wybory między wariantami.

## 5. Wariant zerowy z kosztem bezczynności
**Mechanizm:** w każdym zestawie wariantów jest wariant „nic nie rób" z jawnie policzonym kosztem nicnierobienia. Bez niego porównanie wariantów faworyzuje działanie.
**Kiedy:** przeglądy okresowe, decyzje o zmianie.

## 6. Scoring ważony z progami i jawnymi brakami
**Mechanizm:** N kryteriów × wagi (w tym ujemne, np. koszt ×−1), progi decyzji (idę / rozważam / odpuszczam), a brak danych dla kryterium oznaczany JAWNIE, nigdy zgadywany „żeby domknąć liczbę". Sama liczba bez uzasadnienia per kryterium = niekompletny wynik. Przy dodaniu kryterium progi przelicza się proporcjonalnie, „bez zmiany surowości".
**Kiedy:** ocena wydarzeń, ofert, kandydatur, dostawców.

## 7. Redakcja z tabelą każdej ingerencji
**Mechanizm:** redakcja tekstu do zgodności ze stylem X oddaje: wersję zredagowaną + tabelę `co → na co → która zasada stylu`. Zero niewidzialnych ingerencji. Rozjazd faktograficzny (tekst mówi coś innego niż artefakt faktów) NIE jest poprawiany po cichu — jest flagowany, bo może to być literówka w tekście ALBO nieaktualny artefakt.
**Kiedy:** każda persona „szlifująca" cudzy tekst.

## 8. Adopcja cudzego kontraktu formatu z nazwanymi derogacjami
**Mechanizm:** nowy skill przyjmuje kontrakt formatu istniejącego (np. 7 punktów briefu) zamiast pisać własny, i wypisuje derogacje D1…Dn z uzasadnieniem („sekcje obowiązkowe NIE są pomijane, bo w kalendarzu obowiązków nieobecność znaczyłaby odwrotnie niż w briefie").
**Kiedy:** każdy nowy wynik cykliczny.

## 9. Liczenie wejść na żywo, stała numeracja sekcji, sufiks `_02`
**Mechanizm:** skill nie hardkoduje liczby mierników/pozycji (poprzednik: 10 vs 14 w jeden dzień) — liczy je z artefaktu przy każdym przebiegu; sekcje wyniku mają stałą numerację (pusta = „nie dotyczy"); drugi wynik tego samego dnia dostaje `_02`, nie `_v2`.
**Kiedy:** wyniki cykliczne i porównywalne w czasie.

## 10. Kolejność źródeł z jawnym fallbackiem
**Mechanizm:** źródło pierwotne → źródło wtórne → „brak odczytu" — z adnotacją, która ścieżka zadziałała. Niedostępność raportowana jako fakt; przejście na fallback nigdy nie jest maskowane. Różnica wartości między dwoma źródłami przy różnych datach to lag, nie niezgodność.
**Kiedy:** każda procedura czerpiąca dane z zewnątrz.

## 11. Render bez dostarczenia = brak wyniku
**Mechanizm:** jeśli procedura tworzy artefakt w miejscu tymczasowym i ma go przekazać dalej, krok przekazania jest OBOWIĄZKOWY i nazwany; przebieg bez niego to „przebieg bez wyniku". Błąd narzędzia = zgłoś warstwowo (co się udało / co padło), NIE ponawiaj w pętli.
**Kiedy:** generatory dokumentów, eksporty, integracje.

## 12. Skill obejmuje PROJEKT, nie PRZEBIEG
**Mechanizm:** granica skilla biegnie tam, gdzie kończy się to, co da się rozstrzygnąć bez znajomości konkretnego kontekstu wykonania. Skill projektuje warsztat/plan/spec; sam warsztat prowadzi człowiek. Test: „zmiana W uczestniku (szkolenie) vs artefakt OD uczestników (warsztat)" — ta sama technika, inny cel, inny skill.
**Kiedy:** facylitacja, szkolenia, spotkania.

## 13. Odmowa jako kompletna odpowiedź
**Mechanizm:** persona wymagająca wejścia (link do zatwierdzonego dokumentu) przy jego braku ODMAWIA — i nie „pomaga", pisząc wstępną wersję. Brak sekcji „czego NIE pokrywam" sugeruje fałszywą kompletność.
**Kiedy:** łańcuchy person (wynik A → wejście B).

## 14. Skala z wynikiem „nierozstrzygalne z publicznych źródeł"
**Mechanizm:** ocena ma skalę, w której „nie da się ustalić" jest pełnoprawnym wynikiem; dowody ZA i PRZECIW przed werdyktem; sygnał podażowy ≠ popytowy; liczba, której nie widziałeś u źródła, jest poszlaką.
**Kiedy:** analizy rynkowe, walidacje pomysłów.

## 15. Sekcja „czego świadomie NIE zrobiłem" z naruszaną zasadą
**Mechanizm:** wynik kończy się listą świadomych pominięć z nazwaną zasadą, którą pominięcie narusza lub omija — bo odstępstwo świadome nie jest błędem, ale musi być nazwane.
**Kiedy:** projektowanie (makiety, specyfikacje, plany).

# Kontekst i uzasadnienie
Każdy z tych wzorców powstał u poprzednika z konkretnego przebiegu, który bez niego dał gorszy wynik (ocena 3–4 w logu). Nie są to dobre praktyki z podręcznika — są to poprawki po realnych błędach. Dlatego metodyk, projektując skill, powinien przejść tę listę i sprawdzić, które wzorce dotyczą nowej procedury, zamiast czekać, aż ta sama klasa błędu powtórzy się u Właściciela.

# Przykłady zastosowania
## Dobrze
Metodyk projektuje skill „ocena oferty dostawcy" dla nowej persony: bierze wzorzec 6 (scoring ważony), 2 (ceny ze źródła z datą, nie z pamięci), 14 (skala z „nierozstrzygalne") i 15 (czego nie oceniłem). Skill ma 4 wzorce z nazwy w sekcji „Stan akceptacji".
## Źle
Metodyk pisze skill od zera „bo domena jest inna" i po drugim przebiegu Właściciel ocenia 3, bo wynik podał liczbę bez uzasadnienia per kryterium — dokładnie klasa błędu, którą wzorzec 6 opisuje.

# Wyjątki i przypadki brzegowe
- Wzorzec, który nie pasuje, nie jest stosowany na siłę — ale niezastosowanie pasującego wzorca metodyk wypisuje w „Do akceptacji" z jednym zdaniem dlaczego.
- Nowe wzorce dopisuje Właściciel (propozycja od metodyka przez inbox/) po tym, jak jakiś skill przeszedł poprawkę z tej samej klasy dwa razy.

# Historia zmian
- 2026-09-05 (v1.0): wersja szablonu — wyprowadzona z 23 skilli domenowych poprzednika (finance_*, brand_*, product_*, tech_*), które nie weszły do szablonu; treść osobista i infrastrukturalna usunięta, mechanizmy zachowane.
