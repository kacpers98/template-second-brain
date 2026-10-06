---
type: artifact
artifact_type: registry
title: "Portfel Inicjatyw"
owner_head: "[[ops]]"
used_by:
  - "[[asystent]]"
  - "[[doradca]]"
  - "[[rekruter]]"
inject: on_reference
scope: "Rejestr pomysłów i inicjatyw Właściciela (projekty, produkty, przedsięwzięcia) ze statusami, następnym krokiem i linkami do analiz — kontekst „nad czym pracujemy""
authority: reference
review_every: 30d
version: 1.0
created: 2026-09-05
updated: 2026-09-05
---
# Portfel Inicjatyw

# Cel dokumentu
Jedno miejsce prawdy o aktywnych i rozważanych inicjatywach Właściciela. Daje personom kontekst „nad czym pracujemy" — każda analiza, specyfikacja, proces decyzyjny czy propozycja nowej persony odnosi się do pozycji z tego rejestru. Wiążący jako kontekst dla [[asystent|asystenta]] (brief tygodniowy: sekcja DECYZJE i PARKING LOT czerpią stąd), [[doradca|doradcy]] (proces decyzyjny cytuje pozycję dosłownie) i [[rekruter|rekrutera]] (nowa persona musi wskazać, którą inicjatywę obsługuje).

# Zasady prowadzenia
1. **Rejestr prowadzi Właściciel.** Persony linkują wyniki analiz w kolumnie „Analizy" WYŁĄCZNIE jako propozycje przez `inbox/ops/`; bezpośrednia edycja tabeli przez personę jest błędem.
2. **Statusy (kolejność jest ścieżką):** `pomysł` → `walidacja` → `specyfikacja` → `prototyp` → `wdrożone` / `odrzucone`. Dodatkowe stany poprzeczne: `UŚPIONA (wyzwalacz: …)` — inicjatywa zatrzymana świadomie, z nazwanym warunkiem wznowienia; pozycja uśpiona nie generuje pracy person, dopóki wyzwalacz nie zadziała. Cofnięcie statusu (np. z `specyfikacja` do `walidacja`) jest dopuszczalne i jest informacją, nie porażką — zapisz powód w kolumnie „Następny krok".
3. **Praca bez inicjatywy = najpierw propozycja wpisu.** Persona, która dostaje zlecenie niedające się przypisać do żadnej pozycji rejestru, NIE rozpoczyna analizy — zwraca propozycję nowego wiersza (nazwa, status `pomysł`, jedno zdanie „po co") i czeka na decyzję Właściciela. Chroni to przed pracą nad rzeczami, których Właściciel nie zdecydował się robić.
4. **Bramki są jawne.** Przejście `walidacja` → `specyfikacja` wymaga nazwanego kryterium („kontynuacja TYLKO gdy …") zapisanego PRZED walidacją; wynik walidacji porównuje się z kryterium, nie z wrażeniem. Sygnał relacyjny („znajomy powiedział, że fajne") nie jest sygnałem popytu.
5. **„Następny krok" to jedno konkretne działanie**, nie opis stanu. Jeżeli nie da się go nazwać — inicjatywa jest uśpiona i tak ma być oznaczona.
6. **Kolumna „Analizy" linkuje do `outputs/`**, nigdy nie streszcza wyników — streszczenie w rejestrze starzeje się szybciej niż plik, do którego linkuje.

# Rejestr

| Inicjatywa | Status | Następny krok | Analizy (linki do outputs/) |
| --- | --- | --- | --- |
| {{UZUPEŁNIJ: nazwa inicjatywy — jedno zdanie: co to jest i dla kogo}} | {{UZUPEŁNIJ: pomysł / walidacja / specyfikacja / prototyp / wdrożone / odrzucone / UŚPIONA (wyzwalacz)}} | {{UZUPEŁNIJ: jedno konkretne działanie}} | {{UZUPEŁNIJ: linki lub „—"}} |

# Kontekst i uzasadnienie
- **Dlaczego rejestr, a nie lista zadań.** Inicjatywa to kierunek, zadanie to krok. Lista zadań Właściciela ([[Rejestr_Cyklow]] zasada 1) niesie kroki; ten rejestr niesie kierunki i ich stan. Mieszanie obu daje listę, na której „napisać ofertę" sąsiaduje z „zbudować produkt".
- **Dlaczego zasada 3.** Poprzednik zauważył, że persony chętnie analizowały wszystko, co dostały — także pomysły rzucone w zleceniu bez decyzji, że warto. Wynikiem były analizy rzeczy, których nikt nie zamierzał robić. Propozycja wpisu jako pierwszy krok kosztuje jedno zdanie i wymusza decyzję.
- **Dlaczego bramki przed walidacją.** Kryterium ustalone po zobaczeniu wyników zawsze pasuje do wyników.
- **Dlaczego stan UŚPIONA.** Usunięcie inicjatywy kasuje kontekst i linki; uśpienie z wyzwalaczem zachowuje je i zdejmuje pozycję z pola pracy person.

# Przykłady zastosowania
## Dobrze
Wiersz: „Kurs online z podstaw ergonomii dla małych warsztatów | walidacja | Rozmowy z 5 właścicielami warsztatów wg scenariusza; bramka: kontynuacja TYLKO gdy ≥3 z 5 deklaruje gotowość zapłaty | outputs/ops/2026-10-02_ergonomia_walidacja.md". Po rozmowach: 2 z 5 → status `UŚPIONA (wyzwalacz: pojawienie się partnera dystrybucyjnego)`, link do notatki z wynikami.
## Źle
[[doradca]] otrzymuje zlecenie „przeanalizuj, czy warto otworzyć drugi punkt usługowy" i od razu prowadzi proces decyzyjny, choć w rejestrze nie ma takiej inicjatywy. Naruszona zasada 3 — poprawnie: propozycja wiersza `pomysł` + jedno zdanie, decyzja Właściciela, dopiero potem analiza. Drugi antyprzykład: w kolumnie „Analizy" trzy akapity streszczenia zamiast linku (zasada 6).

# Wyjątki i przypadki brzegowe
- Inicjatywa rozwoju SAMEGO systemu (nowa persona, refaktor): NIE należy tutaj — [[Rejestr_Cyklow]] zasada 4 (granica twórca/użytkownik); propozycje rozwojowe idą do `inbox/` jako zmiany, nie jako inicjatywy.
- Inicjatywa objęta granicą wobec Organizacji lub klienta ([[Granica_Pracy_Zawodowej]], [[Granica_Komercyjna]]): może mieć wiersz wyłącznie na poziomie, który przechodzi test przedmiotu (np. „własna oferta usługowa"), nigdy z nazwą klienta ani Organizacji.
- Wszystko inne: decyzja Właściciela.

# Historia zmian
- 2026-09-05 (v1.0): wersja szablonu — wyprowadzona z działającego systemu-poprzednika; treść osobista i infrastrukturalna usunięta, struktura i zasady zachowane.
