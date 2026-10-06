---
type: artifact
artifact_type: registry
title: "Checkpointy Właściciela"
owner_head: "[[ops]]"
used_by: []
inject: never
scope: "Metoda półrocznego przeglądu kierunku Właściciela: zamrożone definicje wymiarów, trzy filtry dyskwalifikujące metrykę, zasada „przepływ ≠ zapas ≠ struktura", czego NIE mierzymy, przebieg przeglądu. Czyta wyłącznie Właściciel."
authority: reference
agent_access: false
review_every: 180d
version: 1.0
created: 2026-09-05
updated: 2026-09-05
---
# Checkpointy Właściciela

> **Prywatny rejestr osobisty** (`agent_access: false`, `used_by: []`) — czyta go wyłącznie Właściciel. Włączenie [[asystent|asystenta]] jako wykonawcy części policzalnej (wiersz `used_by` + kolumna Odczyt w [[access_map]] + skill) to możliwa późniejsza decyzja Właściciela, nie stan startowy.

# Cel dokumentu
Obiektywna ocena kierunku, w którym idzie Właściciel — raz na pół roku, z danych zbieranych W TRAKCIE, wg definicji zamrożonych w tym pliku. Odpowiada na poczucie „mało namacalnych rzeczy" liczbami zamiast pamięcią. Ten plik jest METODĄ; wartości i baseline wpisuje Właściciel przy pierwszym przeglądzie.

# Zasady wiążące
1. **Przepływ ≠ zapas ≠ struktura.** Nie mierzymy przepływu (ile zrobiłem) — metryka przepływu nagradza przeciążenie, czyli u większości ludzi budujących taki system tryb awarii. Mierzymy zapas (co mam) i strukturę (na ilu pojedynczych „tak" to wisi). Rok ubogi w przepływ może być najlepszym rokiem strukturalnie — zestaw bez wymiaru strukturalnego takie lata zaniża.
2. **Trzy filtry dyskwalifikujące metrykę:** (a) musi być policzalna z istniejącego zapisu, nie oceniana z pamięci; (b) musi być zbierana w trakcie, nie odtwarzana przy przeglądzie; (c) jej definicja jest ZAMROŻONA tutaj i cytowana dosłownie PRZED spojrzeniem na dane. Metryka, która nie przechodzi któregoś filtru, nie wchodzi — nawet jeśli jest ciekawa.
3. **Kadencja: półroczna**, spięta z przeglądem [[Profil_Wlasciciela]] (`review_every: 180d`) w jeden wiersz [[Rejestr_Cyklow]]. Daty: {{UZUPEŁNIJ: dwie daty w roku — wskazówka: nieokrągłe, związane z dostępnością danych (np. dzień po miesięcznym zestawieniu), poza Nowym Rokiem i urodzinami, żeby przegląd nie mieszał się z postanowieniami}}; pierwszy przegląd: {{UZUPEŁNIJ: data}}. Pokusa rozmiękczenia definicji przy drugim punkcie w roku jest rozbrajana przez zasadę 2c.
4. **Definicje zmienia się wyłącznie przy przeglądzie, jawnie, z wpisem w Historii zmian** — i dopiero PO ocenie wg starej definicji. Porównanie rok do roku dwóch różnych miar nie jest postępem.
5. **Przegląd przychodzi policzony.** Wymiary z zapisu ciągłego liczy się z ich źródeł; wymiary zdarzeniowe — z linii dziennika (zasada 6). Przegląd, który wymaga od Właściciela zebrania danych od zera, jest wersją zadeklarowaną — a deklaracje bez mechanizmu nie są wykonywane.
6. **Zapis zdarzeniowy idzie do jednego dziennika** — {{UZUPEŁNIJ: gdzie prowadzisz krótki dziennik dzienny (plik poza vaultem, notatnik, kalendarz) — jedno miejsce, jedno przypomnienie}} — jako jedna opcjonalna linia wpisu dnia: `- checkpoint: <wymiar> — <zdarzenie>`. Zero nowych nawyków; przegląd wyszukuje linie `checkpoint:` z sześciu miesięcy.

# Wymiary — definicje ZAMROŻONE
Poniższe nazwy są PRZYKŁADOWYM zestawem siedmiu wymiarów, który u poprzednika przeszedł trzy filtry. Właściciel przy pierwszym przeglądzie zostawia, zmienia lub skreśla — a potem zamraża. Kolumna „Metryka" jest tym, co cytuje się dosłownie przed oceną.

| # | Wymiar (przykładowa nazwa) | Co naprawdę mierzy | Metryka (definicja dosłowna) | Źródło | Rozdzielczość |
| --- | --- | --- | --- | --- | --- |
| 1 | Ekspozycja strukturalna | ile rzeczy wisi na jednym „tak" | liczba DOMEN życia/pracy zależnych od dokładnie jednego człowieka, jednego źródła dochodu lub jednej instytucji (każda domena liczona raz, stan na dzień przeglądu) | ręcznie przy przeglądzie + linie `checkpoint: ekspozycja` przy zmianach w trakcie | półrocznie |
| 2 | Mandat i sprawczość | czy działa z pozycji, czy obok niej | (a) odsetek pozycji [[Portfel_Inicjatyw]] o statusie aktywnym, w których Właściciel ma budżet/decyzję/własność; (b) licznik propozycji zgłoszonych na zewnątrz: zgłoszone / rozważone merytorycznie / wdrożone | Portfel + linie `checkpoint: sygnał` | półrocznie |
| 3 | Konwersja zapasu w wynik | „mało namacalnych rzeczy" | liczba rzeczy WYPUSZCZONYCH NA ZEWNĄTRZ w półroczu: publikacja, wdrożenie u kogoś, wystąpienie, produkt z użytkownikiem. Nie liczą się: przeczytane, napisane do szuflady, notatki, commity | statusy Portfela + `outputs/` + git + linie `checkpoint: konwersja` | półrocznie |
| 4 | Zapas finansowy | jedyna koncentracja, której nie da się rozbroić deklaracją | STAN, nie przychód: {{UZUPEŁNIJ: definicja dosłowna, np. poduszka w miesiącach kosztów = saldo płynne / średni koszt miesięczny}} | {{UZUPEŁNIJ: skąd liczysz — poza vaultem}} | miesięcznie → odczyt przy przeglądzie |
| 5 | Uwaga i obciążenie | ile torów jednocześnie | (a) liczba równoległych torów AKTYWNYCH (baseline: {{UZUPEŁNIJ}}); (b) agregat dziennika: mediana obciążenia dnia (1–10) z półrocza | dziennik (zasada 6) | codziennie → agregat półroczny |
| 6 | Sygnał zewnętrzny | czytelność Właściciela dla innych — jedyne, czego samooceną nie zmierzy | liczba osób, które SAME się zgłosiły: poprosiły o coś, zaprosiły, zaproponowały współpracę (jedna osoba = 1, niezależnie od liczby kontaktów) | linie `checkpoint: sygnał` | zdarzeniowo → suma półroczna |
| 7 | Fundament osobisty | zadeklarowana podstawa (zdrowie, regeneracja) | ciągłości BINARNE utrzymane w półroczu (tak/nie per ciągłość zdefiniowana przez Właściciela POZA tym plikiem) — tu wyłącznie licznik, nigdy treść | {{UZUPEŁNIJ: kalendarz / aplikacja — poza vaultem}} | półrocznie |

Wymiary 1, 3 i 6 wymagają jednej linii w dzienniku przy zdarzeniu — i to są dokładnie te, których z wewnątrz nie widać.

# Czego NIE mierzymy (zamrożone)
Liczba zamkniętych zadań, liczba działań, liczba notatek w vaultcie, liczba certyfikatów, liczba zmian w systemie. Pierwsze dwa nagradzają przeciążenie, trzecia jest metryką próżności (wejście, nie wyjście), czwarta mierzy konsumpcję, nie kompetencję, piąta myli ruch z kierunkiem. **Wyjątek:** subiektywne poczucie sprawczości/spełnienia — dopuszczone WYŁĄCZNIE jako agregat codziennego dziennika (dane podłużne), nigdy jako ocena retrospektywna z dnia przeglądu.

# Stan wyjściowy (baseline)
| Wymiar | Wartość | Data | Uwaga |
| --- | --- | --- | --- |
| {{UZUPEŁNIJ: numer i nazwa wymiaru}} | {{UZUPEŁNIJ: pierwszy pomiar}} | {{UZUPEŁNIJ: data}} | {{UZUPEŁNIJ: definicja użyta przy pomiarze — dosłownie}} |

# Przebieg przeglądu (checklist)
1. Zacytuj dosłownie definicje z tabeli w wersji obowiązującej w POPRZEDNIM przeglądzie (z gita) — zanim spojrzysz na dane.
2. Policz wymiary z zapisu ciągłego ze źródeł; zdarzeniowe z Portfela i linii `checkpoint:`; ekspozycję ręcznie.
3. Zapisz wynik jako tabelę w `outputs/ops/checkpointy_RRRR-MM.md` (jeden plik na przegląd — tu archiwum JEST celem, inaczej nie ma z czym porównać).
4. Dopiero potem: przegląd warstwy wywnioskowanej [[Profil_Wlasciciela]] (hipotezy → reguły / usunięcie) i decyzja o reteście warstwy mierzonej.
5. Ewentualna zmiana definicji — na koniec, z wpisem w Historii zmian i nowym numerem wersji.

# Kontekst i uzasadnienie
Poprzednik zaprojektował ten mechanizm po obserwacji, że pół roku intensywnej pracy zostawiło poczucie „nic namacalnego" — mimo że zapis (git, outputs) mówił co innego. Wniosek: pamięć ocenia przepływ i emocje, zapis pokazuje zapas i strukturę. Stąd trzy filtry (bez zapisu nie ma metryki), zamrożenie definicji (żeby przegląd nie dopasowywał miary do nastroju) i wymiar strukturalny (żeby rok bez „wyników", w którym rozbrojono dwie zależności od jednej osoby, był widoczny jako dobry rok).

# Przykłady zastosowania
## Dobrze
W trakcie półrocza Właściciel dopisuje do dziennika trzy linie `checkpoint: sygnał — znajoma z branży poprosiła o konsultację`, `checkpoint: konwersja — artykuł opublikowany w piśmie branżowym`, `checkpoint: ekspozycja — drugi dostawca podpisany, zależność od jednego zniknęła`. Przy przeglądzie cytuje definicje, liczy, zapisuje tabelę, dopiero potem ocenia.
## Źle
Przy przeglądzie Właściciel ocenia „z głowy", że „sygnałów było sporo", a wymiar 3 liczy jako „napisałem dużo notatek". Naruszone: zasada 2a (z pamięci, nie z zapisu), definicja wymiaru 3 (notatki się nie liczą), „Czego NIE mierzymy".

# Wyjątki i przypadki brzegowe
- Brak dziennika przez część półrocza: wymiary zdarzeniowe raportuje się jako „dane niepełne od–do", nie odtwarza z pamięci.
- Wymiar, którego źródło zniknęło (np. zmiana aplikacji): pomiar „brak danych" + decyzja o nowym źródle przy przeglądzie; definicja bez zmian.
- Pokusa dodania ósmego wymiaru: dopuszczalna wyłącznie po trzech filtrach i z wpisem w Historii zmian; wymiar bez zapisu nie wchodzi.

# Historia zmian
- 2026-09-05 (v1.0): wersja szablonu — wyprowadzona z działającego systemu-poprzednika; treść osobista i infrastrukturalna usunięta, struktura i zasady zachowane.
