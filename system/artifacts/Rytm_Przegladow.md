---
type: artifact
artifact_type: normative
title: "Rytm Przeglądów"
owner_head: "[[ops]]"
used_by:
  - "[[asystent]]"
inject: always
scope: "Wiążący harmonogram, zakres, format i źródła briefów dziennego i tygodniowego oraz zasada ciszy asystenta"
authority: binding
review_every: 90d
version: 1.0
created: 2026-09-05
updated: 2026-09-05
---
# Rytm Przeglądów

# Cel dokumentu
Definiuje, kiedy i w jakiej formie [[asystent]] raportuje — żeby „daj znać o najważniejszym" było powtarzalnym standardem, nie improwizacją. Wiążący dla asystenta i dla skilla `ops_brief`, który jest procedurą wykonawczą tej normy (przy sprzeczności wygrywa ten artefakt; skill poprawić).

# Zasady wiążące
1. **Brief dzienny**: dni robocze, {{UZUPEŁNIJ: godzina, np. 7:30}} — wykonywany w sesji, w której Właściciel jest obecny (Właściciel otwiera sesję i zleca brief; tryb cykliczny bez człowieka to możliwe rozszerzenie, nie stan startowy). Układ sekcyjny w stałej kolejności: `## DZIŚ`, `## ZA CHWILĘ`, `## TŁO`. Zakres: terminy dziś/jutro, pozycje zaległe, blokery, maksymalnie 1 decyzja czekająca. Limit: maksymalnie **5 POZYCJI merytorycznych łącznie** we wszystkich sekcjach (nagłówki sekcji, puste linie i końcowa linia „Źródła:" do limitu się nie liczą). Gdy kwalifikuje się więcej niż 5 pozycji — brief pokazuje 5 o najwyższym priorytecie (kolejność cięcia: najpierw znika z TŁO, potem z ZA CHWILĘ, DZIŚ tnie się jako ostatnie), a nadmiar sygnalizuje JEDNĄ zbiorczą linią z licznikiem (np. „+4 dalsze zaległe"); **ciche skrócenie listy jest zabronione**. Sekcja bez zawartości jest POMIJANA, nigdy wypełniana słowem „brak". Jeśli nie ma nic pilnego — jedna sekcja `## DZIŚ` z linią „czysto", nie sztuczna treść.
2. **Brief tygodniowy** (przegląd tygodnia): {{UZUPEŁNIJ: dzień i godzina, np. niedziela 18:00 — domknięcie tygodnia + plan przed poniedziałkiem; świadoma alternatywa: piątek po południu}} — zmiana terminu wymaga edycji tej zasady. Zakres w stałej kolejności: `## TOP-3` na nadchodzący tydzień → `## ZAGROŻONE` (terminy zagrożone) → `## DECYZJE` (czekające) → `## PARKING LOT` (skrót) → `## DELTA` (względem poprzedniego briefu tygodniowego) → **(opcjonalnie, na końcu) `## TŁO`**: plan tygodnia z kalendarza i zbiorcze liczniki spraw poza horyzontem tygodnia. Sekcja bez zawartości jest pomijana; sekcja TŁO nigdy nie wypycha treści z pięciu sekcji wcześniejszych. Brief tygodniowy mieści się na jednym ekranie (twardy limit).
3. **Format i źródła.** Treść briefu żyje WYŁĄCZNIE w sekcjach oznaczonych nagłówkiem markdown drugiego poziomu; nazwy i kolejność sekcji wynikają z zasady 1 (dzienny) i zasady 2 (tygodniowy). Każda pozycja to jeden punkt „- " w JEDNEJ linii, bez zdań podrzędnych o pochodzeniu danych; terminy podawane WZGLĘDNIE względem daty briefu („za 3 dni (pon 24.08)"), nie samą datą ISO.
   **Źródła — lista ZAMKNIĘTA**: (a) [[Rejestr_Cyklow]] (tabela *Cykle*); (b) projekcje JEDNOKIERUNKOWE wklejone przez Właściciela w treść zlecenia: bieżące zadania z listy zadań Właściciela (np. Google Tasks, Todoist, papier) — {{UZUPEŁNIJ: nazwa Twojej listy zadań}} — oraz wydarzenia z kalendarza na horyzont trybu. Brief NIGDY nie tworzy własnej wersji prawdy: nie wymyśla pozycji, nie zmienia stanu w żadnym ze źródeł i nie jest dla nich kanałem zwrotnym. Gdy Właściciel nie wkleił któregoś wejścia — brief mówi to JEDNĄ linią statusową („lista zadań: nie przekazana w zleceniu"), nie zgaduje. Wejście spoza tej listy wymaga zmiany tej zasady.
   **Ślad proweniencji** (z której tabeli/źródła, na jakiej zasadzie, co jest projekcją jednokierunkową) idzie w JEDNEJ linii na końcu pliku, zaczynającej się od „Źródła:" — nigdy wewnątrz punktów. Wikilinki żyją w tej linii i we frontmatterze; wewnątrz punktów ich nie ma, bo każdy kanał dostarczenia inny niż Obsidian wycina je do martwej etykiety, a przy pozycjach spoza rejestru byłyby dodatkowo nieprawdziwe.
4. **Kanał dostarczenia — plik kanoniczny i projekcja.** Wersją KANONICZNĄ bieżącego briefu jest plik w `outputs/ops/` — `brief_ostatni_[tryb].md` (`dzienny` | `tygodniowy`), NADPISYWANY przy każdym przebiegu (bez archiwum datowanych plików; plik pełni rolę pamięci OSTATNIEGO stanu dla delty i wykrycia przerwy, historię trzyma git). Każde inne dostarczenie (odczyt w czacie, kopia do komunikatora, mail) jest PROJEKCJĄ tego pliku. Kanałowi WOLNO zmienić warstwę **prezentacji**: emoji i wyróżnienia przy nazwach sekcji, wcięcia i odstępy, zamianę nagłówka pliku na linię z datą, wycięcie wikilinków do czystej etykiety. Kanałowi NIE WOLNO zmienić **treści pozycji, ich kolejności, zestawu sekcji ani zestawu źródeł**. Przy rozbieżności między plikiem a projekcją rozstrzyga plik. Zmiana samej warstwy prezentacji nie wymaga zmiany tej zasady ani skilla `ops_brief` — pod warunkiem, że plik kanoniczny pozostaje bez zmian. Nazwa sekcji nieznana kanałowi nie jest błędem: kanał renderuje ją neutralnie.
5. **Zasada ciszy**: poza rytmem asystent odzywa się WYŁĄCZNIE, gdy zagrożony jest termin zewnętrzny (wobec osób trzecich) w horyzoncie <24h. Zobowiązanie zewnętrzne rozpoznaje się po prefiksie `[Z]` w tytule zadania (konwencja: zasada 3 [[Rejestr_Cyklow]]); pozycja bez prefiksu jest wewnętrzna i ciszy nie przerywa. Wszystko inne czeka do najbliższego briefu. Rytmem w rozumieniu tej zasady są przebiegi z zasad 1 i 2.
6. **Retencja**: jedynymi plikami briefów są nadpisywane `brief_ostatni_[tryb].md` (zasada 4); pełna historia wyłącznie w gicie. Datowane kopie briefów nie powstają.

# Kontekst i uzasadnienie
- **„5 pozycji", nie „5 linii"**: miara w liniach zależy od szerokości ekranu i kanału; miara w pozycjach jest niezależna od prezentacji. Licznik nadmiaru istnieje po to, żeby limit nie stał się cichą utratą informacji — Właściciel widzi, że coś zostało ucięte, i może zlecić pełną listę.
- **Zamknięta lista źródeł**: brief, który sam szuka wejść, zaczyna tworzyć własną wersję prawdy. Wejścia wklejane przez Właściciela w zlecenie są jednokierunkową projekcją — brief nie może niczego w nich zmienić, bo fizycznie nie ma do nich dostępu.
- **Plik kanoniczny nadpisywany**: archiwum datowanych briefów u poprzednika rozrosło się w śmieci, a przy awarii dostarczono nieaktualny plik. Jeden plik + git = delta i historia bez sprzątania.
- **Rozdział prezentacja/treść (zasada 4)**: bez niego każda zmiana wyglądu w kanale uruchamiała blokadę normatywną. Z nim norma pilnuje tego, co znaczy, a kanał — tego, jak wygląda.

# Przykłady zastosowania
## Dobrze
```
# Brief dzienny — wt 08.09
## DZIŚ
- [Z] odesłać podpisaną umowę do kontrahenta — dziś do 16:00
- opłacić fakturę za hosting — dziś
## ZA CHWILĘ
- przegląd faktur dostawców — jutro
- spotkanie z księgową — za 2 dni (czw 10.09)
## TŁO
- decyzja czekająca: czy przedłużać abonament narzędzia X (termin za 9 dni)
+3 dalsze zaległe
Źródła: Rejestr_Cyklow (Cykle); lista zadań i kalendarz — projekcje jednokierunkowe z treści zlecenia.
```
## Źle
Brief dzienny z 9 pozycjami „bo wszystkie są ważne", sekcją `## TŁO` zawierającą „brak" oraz zdaniem „według Twojej listy zadań z Google Tasks masz też…" wewnątrz punktu. Naruszone: zasada 1 (limit 5 bez licznika nadmiaru), zasada 3 (sekcja pusta wypełniona „brak"; proweniencja wewnątrz punktu zamiast w linii „Źródła:").

# Wyjątki i przypadki brzegowe
- Urlop/przerwa zgłoszona przez Właściciela: briefy zawieszone, po powrocie pierwszy brief = skondensowane podsumowanie okresu zamiast zaległych sztuk.
- Dzień bez sesji (Właściciel nie otworzył Claude Code): brief nie powstaje; przy najbliższym zleceniu brief zawiera adnotację o przerwie („poprzedni brief: 3 dni temu") — bez nadrabiania wstecz wielu sztuk.
- Właściciel prosi o „pełną listę bez limitu": to osobne zlecenie, nie brief — wynik idzie do innego pliku w `outputs/ops/`, plik kanoniczny briefu pozostaje w limicie.

# Historia zmian
- 2026-09-05 (v1.0): wersja szablonu — wyprowadzona z działającego systemu-poprzednika; treść osobista i infrastrukturalna usunięta, struktura i zasady zachowane.
