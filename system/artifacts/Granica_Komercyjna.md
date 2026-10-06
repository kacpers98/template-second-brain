---
type: artifact
artifact_type: policy
title: "Granica Komercyjna"
owner_head: "[[ops]]"
used_by: []
inject: on_reference
scope: "Jedyne źródło prawdy o granicy BENEFICJENTA: praca dla siebie (vault) vs zlecenia dla klientów własnych (katalog poza vaultem). Definiuje jednokierunkowy przepływ wiedzy, prawo wcielania person w sesjach komercyjnych, zakazane kanały, pseudonimizację klientów, ewidencję i backup strefy. Norma nadrzędna dla kontraktu sesji w katalogu pracy."
authority: binding
review_every: 90d
agent_access: true
version: 1.0
created: 2026-09-05
updated: 2026-09-05
---
# Granica Komercyjna

# Cel dokumentu
Druga oś rozdziału w systemie — **BENEFICJENT, nie poufność**: to, co Właściciel robi DLA SIEBIE, zasila vault; to, co robi DLA INNYCH (własni klienci, zlecenia własne), żyje wyłącznie w katalogu poza vaultem — {{UZUPEŁNIJ: ścieżka katalogu pracy, np. ~/Praca/}}. Wiążący dla każdej persony wcielanej w sesji komercyjnej i dla Właściciela. Ten artefakt jest normą nadrzędną dla kontraktu sesji (`CLAUDE.md`) w katalogu pracy: przy sprzeczności artefakt wygrywa, kontrakt poprawić.

**Nie mylić z [[Granica_Pracy_Zawodowej]]** — osie są różne i reguły są różne:

| | [[Granica_Pracy_Zawodowej]] (praca dla Organizacji: etat, kontrakt) | Granica Komercyjna (własni klienci) |
|---|---|---|
| Czyja praca | dla pracodawcy/zleceniodawcy i jego klientów | zlecenia własne Właściciela dla jego klientów |
| Persony vaulta | **ZAKAZANE** — zadania służbowe narzędziami Organizacji | **DOZWOLONE** — wcielane przez wstrzyknięcie definicji |
| Materiały | nie dotykają NICZEGO w systemie | żyją wyłącznie w katalogu pracy, w podfolderze per klient |
| Kto egzekwuje poufność | umowa z Organizacją (kotwice kontraktowe) | Właściciel wobec własnych klientów (umowa/zlecenie z klientem) |
| Wspólny mianownik | jedyny transfer do vaulta: wniosek o WŁASNEJ METODZIE (test przedmiotu + trzy testy zasady 4 [[Granica_Pracy_Zawodowej]]; anonimizacja konieczna, niewystarczająca), ręcznie, przez `inbox/` | tak samo |

# Zasady wiążące
1. **Miejsce.** Każda sesja komercyjna startuje z katalogu pracy (kontrakt sesji i polityka uprawnień ładują się stamtąd — sesja uruchomiona skądinąd nie ma egzekucji i jest błędem proceduralnym). Materiały klienta w podfolderze per klient, nazwanym KODEM klienta (zasada 8), nie nazwą.
2. **Wiedza płynie w JEDNĄ stronę.** Sesja komercyjna czyta vault (`wiki/`, `sources/`, `moc/`, `clusters/`, `system/`) WYŁĄCZNIE narzędziem odczytu plików — nigdy poleceniami systemowymi, które mogłyby połączyć odczyt z zapisem. Wolno wcielać persony i skille przez wstrzyknięcie pełnej definicji (jak w [[router]]); zasięgi odczytu person stosują się odpowiednio. **Nawigacja bez listowania:** kontrakt sesji wymienia kanoniczne punkty wejścia do vaulta (`KOKPIT.md`, `system/sciaga_wywolan.md`, [[access_map]]), z których linkami dociera się do każdego pliku.
3. **Kolizja persona ↔ kontrakt — rozstrzygnięcie stałe.** Wcielona persona przynosi własne reguły zapisu (write_access, frontmattery, kanały propozycji do artefaktów vaulta) — one w sesji komercyjnej NIE OBOWIĄZUJĄ. **Kontrakt wygrywa co do MIEJSCA i FORMY zapisu, persona co do METODY.** Kroki skilli kierujące wynik do vaulta są bezprzedmiotowe i pomijane bez pytania. Bez tej reguły posłuszna sesja mogłaby wpisać dane klienta do artefaktu vaulta, wykonując skill co do litery.
4. **Zapis vaulta w sesji komercyjnej NIE ISTNIEJE.** Żaden wyjątek nie obowiązuje — także wyjątek linkowania zwrotnego w `wiki/` (on dotyczy ingestu wiedzy własnej, nie pracy dla klienta). Zapis wyłącznie w katalogu pracy.
5. **Transfer do vaulta: wyłącznie ręczny, po testach.** Sesja kończy wynik listą „kandydaci do vaulta"; Właściciel sam przenosi wybrane pozycje przez `inbox/` (przeniesienie = podpis). Test jak w [[Granica_Pracy_Zawodowej]] zasada 4: przedmiot (czyje to twierdzenie), identyfikacja (nikogo nie da się rozpoznać), zbiór.
6. **Zakazane kanały.** Dane klienta nigdy w: vaultcie, synchronizacji chmurowej vaulta, repozytorium vaulta, few-shotach i przykładach person, ORAZ w treści zleceń kierowanych do jakiegokolwiek przebiegu, który pisze do vaulta lub loguje treść zleceń w vaultcie (np. `outputs/router/log.md`). Jedyny tryb pracy komercyjnej to sesja interaktywna w katalogu pracy.
7. **Ewidencja.** Po każdym przebiegu jedna linia w logu komercyjnym w katalogu pracy: `| data | kod klienta | zlecenie (1 linia) | wynik (ścieżka) |` — a po niej commit repozytorium strefy (sekcja Backup). Log jest jedynym miejscem, w którym po miesiącach da się odtworzyć, co i dla kogo powstało.
8. **Pseudonimizacja klientów.** Klient występuje w logu, nazwach folderów i treści zleceń pod KODEM (np. `K-01`, `K-02`); mapowanie kod → klient żyje wyłącznie poza systemem (umowa, menedżer haseł, notatka poza vaultem) — {{UZUPEŁNIJ: gdzie trzymasz mapowanie kodów}}. Kod nie jest anonimizacją (Właściciel wie, kto to) — jest zabezpieczeniem przed przypadkowym wyniesieniem nazwy klienta do vaulta razem z wnioskiem o metodzie.
9. **Styk z granicą wobec Organizacji.** Materiały pracodawcy/zleceniodawcy nie wchodzą nawet do sesji komercyjnych z personami — [[Granica_Pracy_Zawodowej]] zasada 2 obowiązuje bez względu na katalog. Katalog pracy może zawierać podfolder roboczy Organizacji, ale sesje z personami go nie dotykają.

# Egzekucja — wzorzec trzech warstw (w katalogu pracy, poza vaultem)
Granica nie opiera się na dobrej woli sesji. Wzorzec do odtworzenia przez [[przewodnik|przewodnika]] przy powołaniu strefy komercyjnej (kod i konfiguracja powstają wtedy, nie tutaj):

1. **Kontrakt tekstowy sesji** (`CLAUDE.md` w katalogu pracy): vault wyłącznie do odczytu; zakaz wnoszenia danych klienta do vaulta; obowiązek pseudonimizacji; lista „kandydaci do vaulta"; log komercyjny; kanoniczne punkty wejścia; reguła kolizji persona ↔ kontrakt. Ten artefakt jest jego normą nadrzędną.
2. **Polityka uprawnień** (`.claude/settings.json` w katalogu pracy): `deny` dla zapisu i edycji na ścieżkę vaulta — w każdej formie zapisu ścieżki, jaką narzędzie może przyjąć (bezwzględna, względna, ze skrótem katalogu domowego). Warstwa uprawnień normalizuje ścieżki względne — obejście przez `..` nie działa.
3. **Mechaniczna blokada na poziomie narzędzi — OPCJONALNA, poza zakresem etapów 0–7** (hook uruchamiany przed poleceniami systemowymi, fail-closed; w szablonie NIE ma tego mechanizmu — warstwy 1–2 wystarczają na start, warstwę 3 buduje się dopiero, gdy strefa komercyjna realnie istnieje, jako osobny projekt z pomocą przewodnika lub osoby technicznej): każde polecenie łączące odwołanie do vaulta z operatorem zapisu kończy się odmową. Cena szczelności: hook odrzuca także polecenia, które wyglądają jak zapis, a nim nie są — stąd twarda reguła „vault wyłącznie narzędziem odczytu plików" (zasada 2). To ograniczenie jest ceną szczelności, nie usterką.

Warstwa 2 jest mechaniczna (polityka narzędzia), warstwa 1 — proceduralna, warstwa 3 — opcjonalna i mechaniczna. Po wdrożeniu strefę testuje się kilkoma wektorami zapisu do vaulta (zapis bezpośredni, kopia, przeniesienie, przekierowanie wyjścia, operacje zapisujące systemu kontroli wersji) — wszystkie muszą zostać zablokowane, a wynik testu zapisany w logu komercyjnym.

# Backup strefy
Katalog pracy to cała warstwa egzekucji granicy — utrata dysku bez kopii oznacza odtwarzanie kontraktu z pamięci. Model dwuwarstwowy:
1. **Warstwa governance = prywatne repozytorium git** katalogu pracy z `.gitignore` w trybie BIAŁEJ LISTY: wersjonowane są wyłącznie `CLAUDE.md`, `.claude/settings.json`, log komercyjny (i skrypt hooka, jeśli powstał). Utrata dysku = klon repozytorium + gotowa egzekucja w minutę. Commit po każdym przebiegu (zasada 7). Zdalne repozytorium: {{UZUPEŁNIJ: czy i gdzie — wyłącznie prywatne}}.
2. **Dane klienckie — ŚWIADOMIE poza gitem** (poufność wobec klienta: nie wchodzą do żadnego zdalnego repozytorium). Kopia wg decyzji per klient do archiwum poza vaultem; brak kopii = akceptowane ryzyko odtworzenia od klienta — {{UZUPEŁNIJ: decyzja o kopii danych klienckich}}.

# Kontekst i uzasadnienie
- **Dlaczego oś beneficjenta, nie poufności.** Poufność jest kwestią umowy z klientem i bywa różna. Beneficjent jest binarny: albo pracuję dla siebie, albo dla kogoś. Binarna oś daje mechaniczną regułę miejsca; poufność dałaby regułę uznaniową.
- **Dlaczego persony są dozwolone (inaczej niż wobec Organizacji).** Właściciel jest stroną umowy z własnym klientem i sam decyduje o narzędziach; wobec Organizacji decyduje jej umowa. Wspólny mianownik obu granic to kierunek: do vaulta wchodzi wyłącznie metoda.
- **Dlaczego reguła kolizji.** Poprzednik zauważył, że persona wcielona w sesji komercyjnej wykonała krok skilla „zapisz wynik do artefaktu vaulta" — sesja sama się zatrzymała, ale norma milczała. Milczenie normy w takim miejscu to luka, którą następna sesja wypełni posłuszeństwem.
- **Dlaczego biała lista w gitignore.** Domyślne „wersjonuj wszystko poza wyjątkami" przy danych klienckich odwraca ciężar dowodu: jeden nowy folder bez wpisu w ignore trafia do zdalnego repozytorium. Biała lista odwraca to z powrotem.

# Przykłady zastosowania
## Dobrze
Właściciel otwiera sesję w katalogu pracy, w podfolderze `K-03/`, i wciela [[doradca|doradcę]] do procesu decyzyjnego dla klienta. Persona czyta z vaulta notatkę o metodzie ważenia kryteriów (narzędziem odczytu), wynik zapisuje w `K-03/decyzja_dostawca.md`, krok skilla „zapisz propozycję do `inbox/ops/`" pomija (zasada 3). Wynik kończy się listą „kandydaci do vaulta": jedno zdanie o własnej metodzie. Linia w logu komercyjnym, commit strefy. Właściciel po karencji przepisuje zdanie ręcznie do `inbox/knowledge/`.
## Źle
Właściciel z lenistwa uruchamia sesję w katalogu vaulta i wkleja materiały klienta „bo tu mam persony pod ręką". Naruszone: zasada 1 (miejsce), zasada 6 (dane klienta w zleceniu logowanym w vaultcie) — a kanoniczny log routera właśnie utrwalił nazwę klienta w historii gita. Drugi antyprzykład: folder `Firma_Nowak_sp_z_oo/` w katalogu pracy — naruszona zasada 8 (nazwa zamiast kodu).

# Wyjątki i przypadki brzegowe
- Klient wymaga, żeby praca odbywała się w JEGO narzędziach i środowisku: wtedy klient zachowuje się jak Organizacja — stosuje się [[Granica_Pracy_Zawodowej]] w całości, łącznie z zakazem person.
- Wniosek o metodzie, który przechodzi testy, ale zawiera kod klienta (`K-03`): kod usunąć przed przeniesieniem — kod jest pseudonimem, nie anonimizacją.
- Właściciel nie prowadzi zleceń własnych: artefakt pozostaje wiążący jako zasada gotowości; strefa może nie istnieć.
- Wszystko inne: decyzja Właściciela.

# Historia zmian
- 2026-09-05 (v1.0): wersja szablonu — wyprowadzona z działającego systemu-poprzednika; treść osobista i infrastrukturalna usunięta, struktura i zasady zachowane.
