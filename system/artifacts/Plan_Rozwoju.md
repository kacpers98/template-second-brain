---
type: artifact
artifact_type: registry
title: "Plan Rozwoju"
owner_head: "[[knowledge]]"
used_by: []                      # nadać personie, która będzie oceniać szkolenia/kursy (np. przyszły edukator), gdy powstanie
inject: on_reference
scope: "Rejestr szkoleń, kursów, książek i innych inwestycji w rozwój Właściciela wraz z kryterium ich doboru."
authority: reference
review_every: 90d
version: 1.0
created: 2026-09-05
updated: 2026-09-05
---
# Plan Rozwoju

# Cel dokumentu
Jedno miejsce, w którym Właściciel prowadzi listę tego, w co inwestuje swój czas rozwojowy — i, ważniejsze, JAKIM KRYTERIUM ocenia, czy dana pozycja jest tego warta. Kryterium jest ważniejsze od listy: lista się zmienia, kryterium chroni przed kupowaniem kolejnego kursu z impulsu.

# Zasady prowadzenia
1. **Kryterium trzech pytań** — pozycja wchodzi do planu tylko, gdy odpowiedź na wszystkie trzy brzmi „tak":
   - **Oryginał czy interpretacja?** Czy to źródło pierwotne (autor metody, badanie, dokumentacja), czy czyjaś opowieść o nim? Interpretacje wchodzą wyłącznie, gdy oryginał jest niedostępny lub nieproporcjonalnie kosztowny.
   - **Artefakt czy wrażenie?** Czy po zakończeniu zostanie coś, co da się wskazać (notatka źródłowa w `sources/`, procedura, narzędzie, decyzja) — czy tylko poczucie, że „było ciekawie"?
   - **Zasila więcej niż jeden tor?** Czy pozycja pracuje dla co najmniej dwóch obszarów życia lub pracy Właściciela (np. warsztat zawodowy i ten system), czy dla jednego, wąskiego?
2. Każda ukończona pozycja kończy się **notatką źródłową** w `sources/` przez ingest ([[katalizator]]) — inaczej pozycja jest oznaczana jako „bez artefaktu" i liczy się jako sygnał ostrzegawczy przy kolejnym wyborze.
3. Rejestr prowadzi wyłącznie Właściciel. Persony mogą PROPONOWAĆ pozycje w wynikach (sekcja „Uwagi i dalsze kroki"), nigdy dopisywać ich tutaj.
4. Kolumna „Status": planowane → w trakcie → ukończone (z linkiem do notatki źródłowej) → porzucone (z jednym zdaniem dlaczego — porzucenie jest wynikiem, nie wstydem).
5. Przegląd kwartalny: pozycje „planowane" starsze niż dwa kwartały wracają do trzech pytań; jeśli nadal przechodzą — zostają, jeśli nie — są usuwane z adnotacją.

# Tabela
| Pozycja | Forma (książka / kurs / szkolenie / inne) | Trzy pytania (O/A/T) | Status | Artefakt |
| --- | --- | --- | --- | --- |
| {{UZUPEŁNIJ: pierwsza pozycja rozwojowa, którą realnie planujesz w tym kwartale}} | {{UZUPEŁNIJ}} | {{UZUPEŁNIJ: tak/tak/tak — inaczej nie wchodzi}} | planowane | — |

# Kontekst i uzasadnienie
System-poprzednik obserwował, że decyzje rozwojowe podejmowane bez kryterium wracały jako „wrażenia bez artefaktu": kurs ukończony, nic nie zostało w vaulcie, po pół roku nie sposób powiedzieć, co zmienił. Trzy pytania są tanie (odpowiedź zajmuje minutę) i eliminują większość impulsywnych zakupów. Wymóg notatki źródłowej domyka pętlę: rozwój, który nie trafił do bazy wiedzy, nie pracuje dla systemu.

# Przykłady zastosowania
## Dobrze
Podręcznik autora metody (oryginał), po którym powstaje notatka źródłowa z pięcioma tezami i dwiema propozycjami notatek wiki (artefakt), użyteczny w pracy zawodowej i w projektowaniu procedur tego systemu (dwa tory). Wchodzi.
## Źle
Webinar „10 trików" prowadzony przez pośrednika (interpretacja), po którym zostaje wrażenie i zakładka w przeglądarce (brak artefaktu), dotyczący wyłącznie jednego narzędzia (jeden tor). Nie wchodzi — a jeśli już został obejrzany, dostaje status „porzucone: bez artefaktu".

# Wyjątki i przypadki brzegowe
- Pozycja narzucona z zewnątrz (obowiązkowe szkolenie w pracy): wchodzi bez trzech pytań, ale wymóg artefaktu obowiązuje — choćby jednozdaniowa notatka źródłowa „co z tego zostaje".
- Pozycja czysto rozrywkowa: nie należy do tego rejestru i nie musi się tłumaczyć.
- Wszystko inne: decyzja Właściciela.

# Historia zmian
- 2026-09-05 (v1.0): wersja szablonu — wyprowadzona z działającego systemu-poprzednika; treść osobista i infrastrukturalna usunięta, struktura i zasady zachowane.
