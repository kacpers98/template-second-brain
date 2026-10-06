---
type: artifact
artifact_type: policy
title: "Granica Pracy Zawodowej"
owner_head: "[[ops]]"
used_by: []
inject: on_reference
scope: "Jedyne źródło prawdy o granicy między trwałym vaultem prywatnym a pracą wykonywaną dla pracodawcy lub zleceniodawcy (etat, kontrakt). Definiuje, co NIGDY nie wchodzi do vaulta, jedyny dozwolony kanał transferu wniosków oraz wzorzec egzekucji po stronie katalogu pracy."
authority: binding
review_every: 90d
agent_access: true
version: 1.0
created: 2026-09-05
updated: 2026-09-05
---
# Granica Pracy Zawodowej

# Cel dokumentu
Vault jest trwałą własnością prywatną Właściciela — wiedza, taksonomia i artefakty budowane na lata. Praca dla pracodawcy lub zleceniodawcy (dalej: „Organizacja") żyje WYŁĄCZNIE w katalogu poza vaultem (np. `~/Praca/`), z własnym kontraktem sesji i własną egzekucją. Granica jest asymetryczna: wiedza prywatna może zasilać pracę (odczyt `wiki/` z katalogu pracy jest dozwolony), praca nie może zasilać vaulta niczym poza wnioskami o WŁASNEJ METODZIE Właściciela, które przechodzą trzy testy z zasady 4. Wiążący dla każdej persony i dla Właściciela; `agent_access: true`, bo każda persona musi umieć rozpoznać materiał, którego nie wolno jej przetwarzać.

# Zasady wiążące
1. **Do vaulta NIGDY nie wchodzą:** dane, nazwy, procesy, dokumenty, kod ani jakiekolwiek materiały Organizacji i jej klientów — żadnym kanałem: ani jako pliki w `raw/`, ani jako źródła ingestu, ani jako treść zleceń, ani jako fragmenty wklejone do artefaktów, notatek czy przykładów.
2. **Żadna persona nie otrzymuje materiałów pracy.** Persona, która w zleceniu dostanie materiał o znamionach służbowych (nazwy klientów lub Organizacji, dane projektowe, treści objęte poufnością), PRZERYWA wykonanie tego fragmentu i zgłasza granicę w wyniku — zamiast przetwarzać. To ta sama klasa zachowania co odmowa zapisu poza zasięgiem: odmowa strażnika to norma działająca, nie usterka.
3. **Wsparcie w zadaniach służbowych** wykonuje się narzędziami Organizacji i w katalogu pracy — nie personami vaulta. Jeżeli Organizacja dopuszcza użycie własnych narzędzi AI, sesja i tak startuje z katalogu pracy, nie z vaulta (patrz [[Granica_Komercyjna]], zasada 1 — mechanizm miejsca jest wspólny).
4. **Jedyny dozwolony transfer praca → vault: wniosek o WŁASNEJ METODZIE.** Nie „wniosek zanonimizowany" — **anonimizacja jest warunkiem koniecznym, nie wystarczającym**. Wniosek przechodzi wyłącznie po zdaniu trzech testów łącznie:
   - **Test przedmiotu (oś pierwsza, rozstrzygający).** Wniosek musi być twierdzeniem o tym, **jak pracuje Właściciel** — nie twierdzeniem o Organizacji, jej kliencie, produkcie, procesie, systemie, zabezpieczeniu, planie ani danych. *Test operacyjny:* usuń z wniosku wszystkie okoliczności pochodzące ze zlecenia służbowego. Jeżeli po tym usunięciu wniosek **nadal jest prawdziwy i użyteczny** — jest twierdzeniem o metodzie i przechodzi. Jeżeli **traci sens albo staje się banałem** — był twierdzeniem o Organizacji i NIE przechodzi, choćby był w pełni zanonimizowany.
   - **Test identyfikacji (oś druga, warunek konieczny).** Zdanie mogłoby paść publicznie bez możliwości identyfikacji Organizacji, jej klienta ani osoby. **Sam w sobie nie przesądza niczego** — wniosek zanonimizowany, który nie przeszedł testu przedmiotu, jest odrzucany.
   - **Test zbioru (oś trzecia).** Przed zapisem sprawdź, czy nowy wniosek **w zestawieniu z już zapisanymi** nie odtwarza sposobu działania Organizacji. Test stosuje się do zbioru, nie do pojedynczego wpisu — przepisy o ochronie tajemnicy przedsiębiorstwa chronią informacje także w ich szczególnym zestawieniu, a zbiór, który jako całość nabiera charakteru tajemnicy, może uruchamiać obowiązki bez terminu końcowego.
   
   **Zakaz kategorialny.** Niezależnie od wyniku trzech testów do vaulta NIE wchodzą wnioski dotyczące: **procesów, architektury, struktury organizacyjnej, zabezpieczeń, planów, danych finansowych i handlowych oraz klientów i użytkowników Organizacji.** Katalog należy odwzorować z wyliczenia w klauzuli poufności — {{UZUPEŁNIJ: § Twojej umowy / regulaminu, który wylicza informacje poufne}}.
   
   **Karencja.** Wniosek trafia do `inbox/knowledge/` nie wcześniej niż {{UZUPEŁNIJ: karencja, np. 30 dni}} po zdarzeniu, które go wywołał. Wniosek zapisany w tygodniu zdarzenia jest łatwiej powiązywalny z konkretnym zleceniem niż ten sam wniosek po kwartale.
   
   **Utrwalenie uzasadnienia.** Wpis na liście „kandydaci do vaulta" w logu katalogu pracy zawiera: datę zdarzenia, datę przeniesienia i **jednozdaniowe uzasadnienie przejścia testu przedmiotu**. To uzasadnienie jest jedynym dowodem należytej staranności w ewentualnym sporze; odtworzenie go z pamięci po latach jest niewykonalne.
   
   **Kotwica kontraktowa.** Każdy przeniesiony wniosek musi dać się zakwalifikować jako element dorobku własnego Właściciela — rezultat pracy twórczej powstający **niezależnie od wykonywania konkretnych zadań** na rzecz Organizacji. Podstawa: {{UZUPEŁNIJ: § Twojej umowy / regulaminu o dorobku własnym lub prawach do rezultatów}}. Wniosek, którego nie da się tak zakwalifikować, nie przechodzi.
   
   **Kanał:** wpis w logu katalogu pracy → Właściciel **ręcznie przepisuje** wniosek do `inbox/knowledge/` → przeniesienie do `wiki/` = akt podpisu („akceptuję" w czacie → `narzedzia/akceptuj.py`). Innych kanałów nie ma. Wymóg ręcznego przepisania jest zabezpieczeniem przed przeklejeniem materiału źródłowego.
5. **Czego granica NIE obejmuje:** **umiejętności** nabytych w pracy — umiejętność nie jest informacją, a klauzule poufności chronią informacje — oraz notatek z publicznych źródeł branżowych i wiedzy uzyskanej zgodnie z prawem z innego źródła. Te wchodzą normalną ścieżką ingestu. Rozróżnienie wiążące: *„nauczyłem się prowadzić warsztat inaczej"* → umiejętność, poza zakresem; *„u tego klienta warsztat wymagał trzech rund, bo X"* → informacja o Organizacji, w zakresie — także bez nazwy klienta. Sformułowanie „wiedza ogólna nabyta w pracy" jest celowo NIEUŻYWANE: ma komponent informacyjny, którego typowa umowa nie wyłącza — sprawdź własną: {{UZUPEŁNIJ: czy Twoja umowa zawiera wyłączenie wiedzy ogólnej}}.
6. **Vault jest narzędziem AI.** Persony czytają `wiki/` modelami zewnętrznych dostawców — wprowadzenie treści do vaulta jest wprowadzeniem jej do narzędzia opartego na sztucznej inteligencji, co wiele umów reguluje osobno ({{UZUPEŁNIJ: § Twojej umowy / regulaminu o narzędziach AI, jeśli istnieje}}). Konsekwencja operacyjna: **testy z zasady 4 przechodzi się PRZED zapisem, nigdy po.** Nie ma stanu „tymczasowo w vaulcie, do oceny później" — zapis jest zdarzeniem nieodwracalnym w sensie kontraktowym.
7. **Kierunek odwrotny (vault → praca) też ma reżim.** Asymetria z Celu dokumentu obowiązuje, ale nie jest darmowa: element własny wbudowany w rezultat oddawany Organizacji tak, że jest niezbędny do korzystania z rezultatu, może zostać objęty licencją na rzecz Organizacji — {{UZUPEŁNIJ: § Twojej umowy o prawach do rezultatów i elementów własnych}}. Dlatego:
   - **Elementy systemu (prompty, definicje person, skille, szablony, architektura vaulta) są narzędziem OSOBISTYM i NIGDY nie stają się komponentem oddawanego rezultatu.** Rezultat jest zawsze produktem przetworzonym samodzielnie, bez osadzonych elementów systemu.
   - **Test rozdzielności — przed każdym oddaniem rezultatu:** *usuń z rezultatu swój element; czy Organizacja nadal może z niego w pełni korzystać?* TAK → narzędzie produkcji, oddajesz normalnie. NIE → element jest niezbędny; zatrzymujesz się i wybierasz świadomie: przeprojektowanie rezultatu albo uzgodnienie osobnych warunków.
   - **Rejestr wbudowań** w katalogu pracy: data · rezultat · wbudowany element · dlaczego był niezbędny · wybrana ścieżka. Bez rejestru nie da się po latach odtworzyć, które elementy własne są już licencjonowane.
   - **Zasada rozstrzygania wątpliwości:** przy niepewności przyjmuje się, że element JEST niezbędny. Koszt fałszywego alarmu to jedno pytanie i jeden wpis; koszt przeoczenia jest nieodwracalny.

# Egzekucja (strona katalogu pracy)
Granica po stronie pracy nie opiera się na dobrej woli — jest wymuszona wzorcem trzech warstw w katalogu pracy, opisanym w [[Granica_Komercyjna]] (kontrakt tekstowy sesji → polityka `deny` dla zapisu do vaulta → mechaniczna blokada zapisu na poziomie narzędzi). Katalog pracy wymaga dodatkowo warstwy PROCEDURALNEJ dla zasady 7 (lista czerwonych flag wymuszających test rozdzielności) — ta warstwa nie jest mechaniczna i opiera się na dyscyplinie; trzeba o tym wiedzieć.

# Kontekst i uzasadnienie
- **Dlaczego test przedmiotu, a nie test anonimizacji.** Poprzednik zaczął od reguły „wniosek zanonimizowany może wejść" i odkrył, że w pełni zanonimizowane zdanie o tym, *jak działa proces u klienta*, nadal jest informacją o kliencie — anonimizacja usuwa etykietę, nie treść. Test przedmiotu pyta o coś innego: czyje to twierdzenie. To rozstrzyga większość przypadków jednym pytaniem.
- **Dlaczego zbiór, nie wpis.** Dziesięć pojedynczo niewinnych wniosków może razem odtworzyć sposób działania Organizacji. Bez testu zbioru granica jest szczelna tylko dla pierwszego wpisu.
- **Dlaczego ręczne przepisanie.** Każdy kanał automatyczny (skrypt, kopiuj-wklej, synchronizacja) prędzej czy później przeniesie fragment materiału źródłowego razem z wnioskiem. Ręczne przepisanie jest wolne celowo.
- **Dlaczego „przed zapisem, nigdy po".** Zapis do vaulta jest w sensie kontraktowym nieodwracalny (historia w gicie, odczyt przez modele). Stan „tymczasowo, do oceny" nie istnieje.

# Przykłady zastosowania
## Dobrze
Właściciel po projekcie dla Organizacji notuje w logu katalogu pracy: „Przy planowaniu warsztatu zacząłem od spisania ścieżek wyjątków, zanim ustaliłem ścieżkę główną — skraca rundy uzgodnień." Test przedmiotu: po usunięciu okoliczności projektu zdanie nadal jest prawdziwe i użyteczne → twierdzenie o metodzie. Test identyfikacji: nikogo nie da się rozpoznać. Test zbioru: w `wiki/` nie ma wpisów, z którymi to zdanie odtwarzałoby proces Organizacji. Po karencji Właściciel przepisuje wniosek ręcznie do `inbox/knowledge/` z jednozdaniowym uzasadnieniem i akceptuje.
## Źle
Wniosek: „W organizacjach tej branży proces akceptacji ma zwykle trzy rundy, bo kontrola limitu jest oddzielona od zatwierdzenia" — w pełni zanonimizowany, bez nazw. Po usunięciu okoliczności ze zlecenia zdanie staje się banałem albo traci sens → NIE przechodzi testu przedmiotu (zasada 4), dodatkowo dotyczy procesów Organizacji (zakaz kategorialny). Drugi antyprzykład: persona [[doradca]] otrzymuje w zleceniu fragment wewnętrznej prezentacji Organizacji „do analizy ryzyk" i analizuje go — naruszona zasada 2 (powinna przerwać i zgłosić granicę).

# Wyjątki i przypadki brzegowe
- Materiał publiczny Organizacji (strona www, publiczny raport, oferta): wchodzi jak każde publiczne źródło branżowe (zasada 5) — ale wyłącznie w wersji publicznej, nie w wersji roboczej, do której Właściciel ma dostęp z racji pracy.
- Zmiana pracodawcy/zleceniodawcy: zasady nie zmieniają się; aktualizacji wymagają wyłącznie kotwice kontraktowe ({{UZUPEŁNIJ}}) — przegląd tego artefaktu jest obowiązkowym krokiem przy każdej nowej umowie.
- Właściciel nie ma obecnie żadnej pracy dla Organizacji: artefakt pozostaje wiążący (chroni przed „tylko ten jeden raz" przy pierwszym zleceniu), ale katalog pracy może nie istnieć.
- Wszystko inne: decyzja Właściciela, przy realnych wątpliwościach prawnych — konsultacja z prawnikiem, nie z personą.

# Historia zmian
- 2026-09-05 (v1.0): wersja szablonu — wyprowadzona z działającego systemu-poprzednika; treść osobista i infrastrukturalna usunięta, struktura i zasady zachowane.
