---
type: artifact
artifact_type: registry
title: "Lista Źródeł Zwiadowcy"
owner_head: "[[knowledge]]"
used_by:
  - "[[zwiadowca]]"
inject: on_reference
scope: "Zamknięta pula adresów monitorowanych cyklicznie przez zwiadowcę — jedyne miejsca, które zwiadowca odwiedza w sieci"
authority: binding
review_every: 30d
version: 1.0
created: 2026-09-05
updated: 2026-09-05
---
# Lista Źródeł Zwiadowcy

# Cel dokumentu
Jedyna dozwolona pula adresów, które [[zwiadowca]] odwiedza. Dostęp zwiadowcy do sieci służy wyłącznie monitoringowi tej listy — eksploracja poza nią jest zabroniona (research otwarty to osobne zlecenie Właściciela, nie zwiad). Wiążący dla zwiadowcy i dla skilli `knowledge_przebieg_zwiadu` (przebieg) i `knowledge_audyt_zrodel` (audyt kwartalny).

# Zasady prowadzenia
1. **Pula zamknięta.** Nowe źródło dopisuje wyłącznie Właściciel (przez `inbox/knowledge/` + akceptacja albo ręcznie). Zwiadowca zgłasza kandydatów w raporcie przebiegu — nigdy nie dopisuje ich sam, nawet gdy trafił na nie „po drodze".
2. **Zwiadowca modyfikuje wyłącznie kolumnę `last_checked`** — to jego jedyna dozwolona zmiana w tym pliku (wyjątek od reguły „`system/` tylko przez inbox", nadany w [[access_map]]; w sesji interaktywnej egzekwowany przeglądem diffu przez Właściciela). Zmiana czegokolwiek innego w tym pliku przez zwiadowcę jest błędem.
3. **Źródło martwe lub przeniesione** → zwiadowca oznacza w raporcie jako „do usunięcia?" z dowodem (kod odpowiedzi, brak nowych pozycji przez N przebiegów); decyduje Właściciel. Usunięcie zwalnia miejsce dla kandydata.
4. **Częstotliwość = MINIMALNY odstęp między odwiedzinami.** Przebieg sprawdza wyłącznie pozycje, którym minął termin (`last_checked` + częstotliwość < dziś). Częstotliwość jest limitem kosztu, nie obietnicą — przebieg, w którym nic nie „dojrzało", kończy się raportem „0 pozycji do sprawdzenia" i to jest wynik poprawny.
5. **Paywall = niedostępne.** Źródło za paywallem, do którego zwiadowca nie ma legalnego dostępu z poziomu sesji, jest poza cyklem — zero obejść, zero prób logowania. Jeżeli Właściciel ma opłacony dostęp, przegląda takie źródło RĘCZNIE i sam decyduje o ingeście; w kolumnie „Częstotliwość" wpisuje się „POZA CYKLEM — przegląd ręczny Właściciela".
6. **Adnotacja `rozpoznanie:`** w kolumnie „Zakres tematyczny" wskazuje konkretne strony-listingi (ścieżki względne wobec adresu źródła), od których zaczyna się przebieg dla danej pozycji — zamiast strony głównej. Zwiadowca czyta je najpierw (WebFetch), zbiera z nich adresy i daty, deduplikuje po adresie, a dopiero potem pobiera treść. Brak adnotacji = rozpoznanie ze strony głównej. Kategorie NIEWYMIENIONE w adnotacji są poza cyklem. Adnotacja służy też do OMINIĘCIA warstwy renderowania (np. gdy strony HTML są niedostępne dla narzędzia, a kanał RSS działa) — bez zmiany skilla.
7. **Sekcje wg warstw MOC.** Tabela jest podzielona na sekcje odpowiadające warstwom wiedzy z `moc/` — po to, żeby audyt kwartalny widział, która warstwa nie ma ŻADNEGO źródła w cyklu (luka pokrycia), a która ma ich za dużo względem tagów, które zasila. Tagi w kolumnie „Zakres tematyczny" muszą istnieć w `tags_owned` klastrów — tag spoza taksonomii jest błędem wykrywanym przez lint.
8. **Retencja raportów przebiegu** (`outputs/knowledge/RRRR-MM-DD_zwiad.md`): raport żyje do najbliższego kwartalnego audytu źródeł, który jest jego jedynym czytelnikiem poza dniem publikacji; po audycie raporty z minionego kwartału trafiają do `_to_delete/`. Syntezy i notatki źródłowe z przebiegu żyją niezależnie w `wiki/` i `sources/`.

# Rejestr
Kolumny: **Źródło (URL)** · **Częstotliwość** (minimalny odstęp) · **Zakres tematyczny** (tagi z taksonomii + ewentualne adnotacje `rozpoznanie:` i uwagi o charakterze źródła, np. „eseje z tezą — interes autora w narracji") · **last_checked** (data ostatniego odwiedzenia; „(nigdy)" dla nowej pozycji).

Sekcje odpowiadają warstwom z `moc/` — nazwy zastąp własnymi po przemianowaniu warstw. Pusta sekcja jest INFORMACJĄ (luka pokrycia), nie błędem — nie usuwaj jej.

### {{UZUPEŁNIJ: nazwa warstwy MOC 1}}

| Źródło (URL) | Częstotliwość | Zakres tematyczny | last_checked |
| --- | --- | --- | --- |
| https://example.org/blog | co 30 dni | {{UZUPEŁNIJ}} | — |

### {{UZUPEŁNIJ: nazwa warstwy MOC 2}}

| Źródło (URL) | Częstotliwość | Zakres tematyczny | last_checked |
| --- | --- | --- | --- |
| | | | |

### {{UZUPEŁNIJ: nazwa warstwy MOC 3}}

| Źródło (URL) | Częstotliwość | Zakres tematyczny | last_checked |
| --- | --- | --- | --- |
| | | | |

### {{UZUPEŁNIJ: nazwa warstwy MOC 4}}

| Źródło (URL) | Częstotliwość | Zakres tematyczny | last_checked |
| --- | --- | --- | --- |
| | | | |

### {{UZUPEŁNIJ: nazwa warstwy MOC 5}}

| Źródło (URL) | Częstotliwość | Zakres tematyczny | last_checked |
| --- | --- | --- | --- |
| | | | |

*(Wiersz przykładowy w pierwszej sekcji jest fikcyjny — do zastąpienia pierwszym realnym źródłem Właściciela.)*

# Kontekst i uzasadnienie
- **Dlaczego pula zamknięta.** Zwiadowca z otwartym dostępem do sieci zaczyna „szukać ciekawych rzeczy" i dostarcza szum, którego nikt nie zamawiał; poprzednik doświadczył tego z automatem kreatywnym bez deduplikacji ([[Lekcje_Poprzednika]]). Lista zamknięta zamienia zwiad w monitoring: przewidywalny koszt, przewidywalny strumień.
- **Dlaczego zwiadowca zmienia tylko `last_checked`.** To jedyna informacja, którą zwiadowca zna lepiej niż Właściciel. Reszta tabeli to decyzje Właściciela o tym, co chce czytać.
- **Dlaczego częstotliwość jest minimum, nie harmonogramem.** Harmonogram wymaga automatu; minimum działa też wtedy, gdy Właściciel otwiera sesję nieregularnie — przebieg po dwóch tygodniach przerwy sprawdza wszystko, co dojrzało, bez nadrabiania sztuk.
- **Dlaczego sekcje wg warstw.** Bez nich audyt widział listę adresów, nie mapę pokrycia; luka „warstwa bez żadnego źródła" była niewidoczna przez kwartał.
- **Dlaczego paywall = poza cyklem.** Obejście paywallu jest naruszeniem warunków źródła; automatyzacja logowania kontem Właściciela wymaga trzymania sesji/hasła w systemie ([[Rejestr_Sekretow]]) i jest ROZSZERZENIEM stacku, nie stanem startowym ([[Stack_Technologiczny]], zasada 6).

# Przykłady zastosowania
## Dobrze
Przebieg zwiadu: 3 pozycje dojrzały, zwiadowca czyta ich strony rozpoznania, znajduje 5 nowych wpisów, po deduplikacji zostają 4, z których 2 przechodzą próg wartości i idą jako propozycje do `inbox/knowledge/`. W pliku listy zmienia się wyłącznie `last_checked` trzech wierszy. Raport zawiera sekcję „Kandydaci do listy: 1 — blog autora cytowanego w dwóch pobranych wpisach; decyzja Właściciela".
## Źle
Zwiadowca, widząc że źródło przekierowuje na nowy adres, sam poprawia URL w tabeli i dopisuje dwa „ciekawe" blogi znalezione po drodze. Naruszone: zasada 1 (pula zamknięta), zasada 2 (zmiana poza `last_checked`), zasada 3 (przeniesienie zgłasza się w raporcie, decyduje Właściciel).

# Wyjątki i przypadki brzegowe
- Źródło typu podcast/wideo bez transkryptów: kilka przebiegów bez syntez nie oznacza braku wartości, tylko brak dostępnej treści — przenieść „POZA CYKLEM — przegląd ręczny", nie usuwać.
- Źródło bez dat publikacji (nowość nierozstrzygalna): poza cyklem, przegląd ręczny.
- Ten sam autor w dwóch kanałach (np. blog na liście + newsletter, który Właściciel czyta osobno): duplikat jest oczekiwany — lista obejmuje wyłącznie kanał, który odwiedza zwiadowca.
- Wszystko inne: decyzja Właściciela przy audycie kwartalnym.

# Historia zmian
- 2026-09-05 (v1.0): wersja szablonu — wyprowadzona z działającego systemu-poprzednika; treść osobista i infrastrukturalna usunięta, struktura i zasady zachowane.
