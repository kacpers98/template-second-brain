---
type: head
name: knowledge
scope: "Knowledge Ops: ingest i synteza źródeł, monitoring wskazanych źródeł internetowych, taksonomia, audyty vaulta i dostępów, projektowanie agentów i skilli, wdrożenie systemu (przewodnik)"
agents:
  - "[[katalizator]]"
  - "[[zwiadowca]]"
  - "[[rekruter]]"
  - "[[metodyk]]"
  - "[[przewodnik]]"
context_sources:          # artefakty, po które persony działu sięgają w ramach swojej roli
  - "[[Lista_Zrodel_Zwiadowcy]]"
inject: by_persona        # persona ma OBOWIĄZEK przeczytać ten plik na początku pracy (jest w jej read_scope); żaden kod tego nie wymusza — brak wstrzyknięcia jest zamierzony, egzekwuje to Samokontrola persony i przegląd wyniku przez Właściciela
version: 1.0
updated: 2026-09-05
---
# Misja działu
Utrzymanie vaulta jako jedynego, spójnego źródła prawdy: zamiana surowych źródeł w ustrukturyzowaną wiedzę, pielęgnacja taksonomii, audyty zdrowia vaulta i pokrycia dostępów oraz projektowanie nowych agentów i procedur. Dział jest fundamentem — na wynikach jego pracy operują pozostałe działy. W szablonie dział prowadzi także wdrożenie samego systemu ([[przewodnik]]).

# Kontekst właściciela
{{UZUPEŁNIJ: 2–3 zdania o Tobie istotne dla tego działu — czym się zajmujesz, jaką wiedzę gromadzisz i po co (do jakich decyzji, projektów, tekstów ma służyć), jaki masz cel strategiczny w porządkowaniu wiedzy. Ten akapit czyta każda persona działu; pisz konkretnie, bez życiorysu.}}

# Zasady i standardy działu
- **Cytowanie**: każde stwierdzenie faktu, framework lub metryka w tworzonych notatkach musi mieć natychmiastowe odniesienie w formacie `(źródło: nazwapliku.pdf)` lub link do notatki źródłowej `[[...]]`.
- **Sprzeczności**: gdy nowe źródło przeczy twierdzeniu istniejącemu w vaulcie — nie nadpisuj. Udokumentuj obie strony („Źródło A twierdzi X, Źródło B argumentuje Y"), oznacz znacznikiem `[CONTRADICTION]` i zostaw rozstrzygnięcie Właścicielowi.
- **Twierdzenia bez pokrycia**: wartościowe hipotezy bez solidnego oparcia w źródłach oznaczaj `(status: wymaga-weryfikacji)`. Wiedza spoza vaulta użyta w wyniku — zawsze z etykietą `[wiedza własna modelu]`.
- **Nazewnictwo plików wiedzy**: małe litery, łączniki zamiast spacji (np. `growth-loops.md`). Pliki MOC z zachowaną wielkością liter (`MOC_<Nazwa>.md`).
- **Ton**: czysta, analityczna, precyzyjna proza — bez marketingowego szumu.
- **Droga zmian**: wszystko, co dotyka `wiki/`, `moc/`, `clusters/` lub `system/` — wyłącznie jako propozycja w `inbox/`; akceptacja = Właściciel mówi „akceptuję", a [[przewodnik]] lub [[router]] uruchamia `narzedzia/akceptuj.py`. JEDEN wyjątek (3a [[access_map]]): [[katalizator]] i [[zwiadowca]] mogą dopisać odnośnik zwrotny w sekcji „## Powiązane" istniejącej notatki `wiki/` — czysty append narzędziem Edit, format `- [[nazwa]] — uzasadnienie relacji.`, sekcja musi istnieć. Wszystko poza tym w `wiki/` to propozycja. W sesji interaktywnej granicę pilnuje polityka `.claude/settings.json` (deny) i przegląd diffu przez Właściciela.
- **Taksonomia**: jedyne źródło prawdy to pola `tags_owned` w `clusters/`; rozszerzenia wyłącznie skillem [[knowledge_rozszerzenie_taksonomii]], każdorazowo za zgodą. Klaster jest najmniejszą jednostką nadania zasięgu (`cluster_access`).
- **Separator odcięcia**: każda propozycja w `inbox/` kończy się linią `---` w osobnym akapicie i sekcją „## Do akceptacji"; treść nad separatorem musi być samowystarczalna, bo przy akceptacji appendiks jest odcinany bez czytania.
- **Konwencja inject**: `by_persona` = persona ma obowiązek przeczytać head swojego działu przy pracy; brak wstrzyknięcia przez kod jest zamierzony.
- **Runtime**: wszystkie przebiegi działu odbywają się w interaktywnej sesji Claude Code w vaulcie, z Właścicielem obecnym. Przebieg bez obecności Właściciela (np. cykliczny zwiad) to opcja przyszła — wtedy eskalacja = zapis w raporcie.

# Słownik działu
- **Ingest** — pełny cykl: `raw/` → notatka źródłowa w `sources/` → propozycje syntez w `inbox/knowledge/` → link zwrotny → wpis w logu.
- **Destylat** — synteza w `wiki/` (co z tego wynika), w odróżnieniu od notatki źródłowej (co powiedział autor).
- **Filar** — notatka wskazana w `key_notes` klastra; punkt startu nawigacji persony.
- **Propozycja** — plik w `inbox/` czekający na akceptację; nie jest częścią obowiązującej wiedzy ani konfiguracji i nie wchodzi do syntezy.
- **Link zwrotny** — odnośnik dopisany w „## Powiązane" notatki docelowej, żeby nowa wiedza nie została sierotą w grafie (wyjątek 3a).
- **Zasięg deterministyczny vs oportunistyczny** — deterministyczny: notatki, które persona ma w `cluster_access` i `read_scope` (policzalne); oportunistyczny: to, na co trafia linkami „2 poziomy w głąb" — audyt dostępów liczy wyłącznie ten pierwszy.
- **Zasada 7b (konsultacja)** — persona, która potrzebuje wiedzy spoza swojego zasięgu, kończy swoją część i oznacza „pytanie poza zasięgiem → właściciel: [[persona]]"; o delegacji decyduje [[router]], nie persona.

# Artefakty źródłowe
- [[Lista_Zrodel_Zwiadowcy]] — zamknięta pula adresów monitorowanych przez [[zwiadowca]]; sięgaj przy każdym przebiegu monitoringu. W vaulcie startowym pusty wzorzec — wypełnia Właściciel.
- [[access_map]] — mapa uprawnień person; artefakt nadrzędny dla [[rekruter]] i [[metodyk]] przy każdym doborze zasięgu i kontroli wykonalności procedur.
- [[Wzorce_Metodyczne]] — katalog wzorców procedur dla [[metodyk]]; sięgaj przy projektowaniu każdego skilla.
- [[Lekcje_Poprzednika]] — ślepe uliczki i zasady wyniesione z systemu-poprzednika; sięga [[przewodnik]] przy wdrożeniu, pozostałe persony przy wątpliwości „czy to już było próbowane".
Reguła: destylat w tym pliku wystarcza do orientacji; pełną treść artefaktu czytaj, gdy krok procedury każe ją cytować albo aktualizować.

# Granice decyzyjności działu
Persony rozstrzygają same: dobór tagów z istniejącej puli, kwalifikację treści do syntezy (próg jakości), format notatek wg szablonów, dobór minimalnego zasięgu w PROPOZYCJI definicji. ZAWSZE eskalują: nowe tagi/klastry, zmiany w strukturze MOC, rozstrzyganie sprzeczności, usuwanie czegokolwiek, modyfikacje definicji agentów/skilli/artefaktów, zmiany wiersza [[access_map]], nadanie `web_access` lub Bash, dodanie źródła do Listy.

# Standard przekazywania pracy
- [[zwiadowca]] → [[katalizator]]: przez notatkę w `sources/` (link, nie streszczenie).
- [[rekruter]] → [[metodyk]]: skille startowe nowego agenta zlecane po akceptacji definicji agenta przez Właściciela; metodyk dostaje link do zaakceptowanej definicji.
- [[metodyk]] → wykonawca skilla: skill wchodzi do użycia dopiero po akceptacji i dopisaniu do „Skille przypisane" persony.
- [[przewodnik]] → Właściciel: stan wdrożenia w `outputs/wdrozenie/STAN_WDROZENIA.md`; każdy krok wdrożenia kończy się jedną decyzją do podjęcia, nie listą.
- Wyniki zawsze jako pliki w `outputs/knowledge/` lub `inbox/knowledge/` z kompletnym frontmatterem wg `system/templates/template_output.md`; jeden wpis w `outputs/knowledge/log.md` na przebieg.

# Historia zmian
- 2026-09-05 (v1.0): wersja szablonu — wyprowadzona z działającego systemu-poprzednika; treść osobista i infrastrukturalna usunięta, struktura i zasady zachowane.
