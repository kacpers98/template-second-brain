---
name: knowledge_rozszerzenie_taksonomii
aliases: ["knowledge_rozszerzenie_taksonomii"]              # plik nazywa się SKILL.md — alias pozwala linkować [[knowledge_rozszerzenie_taksonomii]] w Obsidianie (lint R8)
description: "Procedura bezpiecznego rozszerzania taksonomii, gdy żaden istniejący tag ani klaster nie pasuje do treści bez naciągania: zatrzymanie bieżącego ingestu, dowód próby dopasowania, propozycja minimalnej zmiany (tag > klaster > eskalacja MOC), po zgodzie komplet diffów w inbox/knowledge/ z prefiksem tax_. Używaj WYŁĄCZNIE jako odgałęzienie z knowledge_ingest (krok 0 lub 2) albo na wprost zlecenie Właściciela 'dodaj tag', 'dodaj klaster', 'rozszerz taksonomię'. NIE jest tym skillem: dopasowanie tagu 'prawie pasującego' (wybierz istniejący i odnotuj wątpliwość w propozycji ingestu), zmiana struktury MOC-ów (decyzja Właściciela poza zakresem agentów), retagowanie istniejących notatek (osobne zlecenie)."
type: skill
skill_type: procedure
used_by:
  - "[[katalizator]]"
  - "[[zwiadowca]]"
depends_on_artifacts: []
wymagany_odczyt:                    # ŚCIEŻKI, po jednej linii, z komentarzem KTÓRY KROK tego wymaga
  - clusters/                       # krok 2 i 3: zakresy klastrów, pola tags_owned, sekcja „Definicje tagów"
  - moc/                            # krok 2b: czy temat mieści się w istniejącej warstwie (wariant nowego klastra)
  - system/templates/               # krok 4: template_cluster.md dla wariantu (b)
  - outputs/knowledge/log.md        # krok 6: kotwica na końcu logu
# Świadomie NIEobecne: wiki/ — sekcja „Wpływ" (kandydaci do retagowania) buduje się z Grep po
# frontmatterach wiki/, ale jest warunkowa („brak kandydatów" to poprawna wartość), więc nie
# blokuje procedury; wykonawcy tego skilla i tak mają wiki/ z tytułu roli.
inputs: "TWARDE: (1) treść/źródło, dla której brak dopasowania; (2) DOWÓD PRÓBY: 2–3 najbliższe istniejące tagi + jedno zdanie per tag, dlaczego jest naciągnięciem. Bez dowodu procedura nie startuje. OPCJONALNE: wprost zlecenie Właściciela z gotową nazwą tagu/klastra (nadal przechodzi przez krok 2 i 3)."
output_format: "propozycja na czacie → po zgodzie Właściciela: inbox/knowledge/tax_diff_[klaster].md (wariant a) albo inbox/knowledge/tax_nowy_klaster_[nazwa].md + tax_diff_[moc].md (wariant b) + wpis w outputs/knowledge/log.md"
version: 1.0
updated: 2026-09-05
---
# Kiedy używać
Krok 0 `knowledge_ingest` wykazał brak klastra dla źródła, krok 2 wykazał brak tagu bez naciągania, albo Właściciel wprost zleca zmianę taksonomii. W świeżym vaulcie (dwa klastry przykładowe: [[Wydajność i Skupienie]], [[Przywództwo i Decyzje]]) ten skill będzie uruchamiany często — to zamierzony sposób, w jaki taksonomia rośnie z treści, którą Właściciel realnie wprowadza.

**NIE jest tym skillem** — testy rozstrzygające:
- *Czy istniejący tag pokrywa treść, tylko brzmi trochę inaczej niż byś to nazwał?* → to dopasowanie „prawie pasujące": wybierz istniejący tag i odnotuj wątpliwość w propozycji ingestu. Rozszerzasz taksonomię, gdy istniejący tag byłby FAŁSZEM o treści, nie gdy jest niezgrabny.
- *Czy zmiana dotyczy warstwy MOC (nowa warstwa, scalenie warstw, zmiana pytań warstwy)?* → poza zakresem agentów; zgłaszasz jako decyzję strukturalną, nie proponujesz diffu.
- *Czy chodzi o nadanie NOWEGO tagu ISTNIEJĄCYM notatkom?* → retagowanie to osobne zlecenie po akceptacji tagu; tu tylko wypisujesz kandydatów w sekcji „Wpływ".
- *Czy Właściciel chce po prostu przetworzyć źródło?* → `knowledge_ingest`; ten skill jest jego odgałęzieniem, nie zamiennikiem.

# Wymagane wejście
- **Treść/źródło powodujące lukę** — ścieżka albo wskazanie fragmentu.
- **Dowód próby:** 2–3 najbliższe istniejące tagi + 1 zdanie per tag, dlaczego każdy jest naciągnięciem. Bez tego dowodu nie proponuj rozszerzenia — dowód chroni pulę przed rozrostem z wygody.
- Pulę tagów i zakresy klastrów czytasz na żywo z `clusters/`, nie z pamięci o poprzednim ingeście.

# Podstawa metodyczna (Grounding)
- {{UZUPEŁNIJ: notatka o oddolnym wzroście taksonomii z treści}} → krok 2 i 3 — taksonomia rośnie ODDOLNIE z treści, która jej nie mieści; uzasadnia zatrzymanie pracy zamiast naciągania istniejącego tagu i preferencję najmniejszej zmiany. Vault startowy nie zawiera tej notatki; do czasu ingestu krok wykonuj z oznaczeniem `[wiedza własna modelu]`.

Podstawa normatywna trybu zmiany (propozycja → podpis Właściciela): [[access_map]] oraz `template_cluster.md` / `template_wiki.md` (pola frontmatteru, sekcja „Definicje tagów" klastra).

# Procedura
1. **ZATRZYMAJ bieżący ingest.** Nie taguj „na razie czymkolwiek" — tag tymczasowy staje się trwały w chwili akceptacji propozycji ingestu.
2. **Ustal minimalny zakres zmiany**, w kolejności preferencji:
   (a) **nowy tag w ISTNIEJĄCYM klastrze** — rozwiązanie domyślne;
   (b) **nowy klaster w istniejącym MOC** — tylko gdy temat wykracza poza zakresy WSZYSTKICH klastrów tej warstwy (sprawdź pola `summary` i `tags_owned` każdego klastra w `clusters/` oraz pytania warstwy w `moc/`);
   (c) **zmiana na poziomie MOC** — nie proponujesz; zgłaszasz Właścicielowi jako decyzję strukturalną jednym akapitem i kończysz ten skill (ingest wraca z najbliższym istniejącym tagiem, krok 5).
   Grounding: {{UZUPEŁNIJ: notatka o oddolnym wzroście taksonomii z treści}}.
3. **Przedstaw na czacie propozycję:** nazwa tagu (konwencja jak w puli — sprawdź istniejące `tags_owned`: ten sam język, ten sam styl zapisu, np. `snake_case`), klaster docelowy, definicja tagu (1 zdanie wg formatu sekcji „Definicje tagów" tego klastra), uzasadnienie luki (dowód z wejścia), 2–3 przykłady przyszłych treści, które ten tag obejmie. **Czekaj na decyzję Właściciela.**
4. **Po zgodzie przygotuj do `inbox/knowledge/` komplet (prefiks `tax_`):**
   - wariant (a): `tax_diff_[klaster].md` — dosłowny diff frontmatteru (`tags_owned`) i sekcji „Definicje tagów" klastra (przed/po);
   - wariant (b): `tax_nowy_klaster_[nazwa].md` — pełny plik klastra wg `template_cluster.md` + `tax_diff_[moc].md` z wpisem do sekcji „Mapa klastrów" właściwego MOC-a.
   Pliki leżą wyłącznie w `inbox/knowledge/` — obowiązuje żelazna zasada miejsca z `knowledge_ingest` (krok 6): zero komend przenoszących w podsumowaniu. Akceptacja: Właściciel mówi „akceptuję", a przewodnik lub router uruchamia `python3 narzedzia/akceptuj.py --vault . inbox/knowledge/tax_*.md` — przeniesienie do `clusters/` lub `moc/` jest podpisem i wykonuje je Właściciel albo przewodnik na jego polecenie, nigdy wykonawca tego skilla.
5. **Po odmowie:** wróć do ingestu z najbliższym istniejącym tagiem i odnotuj w propozycji ingestu adnotację `taksonomia: wymaga-weryfikacji` z jednym zdaniem, czego zabrakło.
6. **Dopisz wpis do `outputs/knowledge/log.md`** wyłącznie narzędziem Edit z kotwicą na końcu pliku (technika jak w kroku 7 `knowledge_ingest`): `## [RRRR-MM-DD] taxonomy | propozycja #tag (klaster) | zgoda/odmowa/eskalacja-MOC`.
7. **Wróć do przerwanego `knowledge_ingest` (krok 2)** z zaktualizowaną pulą — pamiętając, że pula formalnie rośnie dopiero po akceptacji diffów przez Właściciela; do tego czasu taguj propozycje warunkowo z adnotacją „tag oczekuje na akceptację: inbox/knowledge/tax_diff_[klaster].md". Zgoda dotyczy TEGO przypadku — żadnego drugiego tagu „przy okazji".

# Szablon wyniku
**Plik `tax_diff_*.md`:** frontmatter wg `template_output.md` (`type: output`, `agent`, `task: taxonomy`, `date`, `head: "[[knowledge]]"`) + sekcje w stałej numeracji:
```
## 1. Diff (dosłowne PRZED / PO dla frontmatteru tags_owned i sekcji „Definicje tagów")
## 2. Uzasadnienie (dowód próby: najbliższe tagi + dlaczego naciągnięcie; przykłady przyszłych treści)
## 3. Wpływ (istniejące notatki wiki/, które mogłyby dostać nowy tag — lista do ewentualnego retagowania jako OSOBNE zlecenie; „brak istniejących kandydatów" to poprawna wartość)
```
**Plik `tax_nowy_klaster_*.md`:** pełna treść klastra wg `template_cluster.md` (tak, żeby akceptacja była przeniesieniem bez redakcji) + na końcu sekcja „## Uzasadnienie propozycji" (dlaczego żaden istniejący klaster warstwy nie mieści tematu).

# Checklist przed oddaniem
- [ ] Dowód próby dopasowania obecny (bez niego procedura nie startuje).
- [ ] Wybrany najmniejszy wystarczający zakres zmiany (tag przed klastrem; MOC tylko jako eskalacja, nie diff).
- [ ] Zgoda dotyczy TEGO przypadku — żadnego „przy okazji" drugiego tagu.
- [ ] Zero bezpośrednich zmian w `clusters/`, `moc/`, `system/` — wyłącznie diffy w `inbox/knowledge/` z prefiksem `tax_`; zero komend przenoszących w podsumowaniu.
- [ ] Nazwa tagu zgodna konwencyjnie z istniejącą pulą (sprawdzona na żywo, nie założona).
- [ ] Sekcja „Wpływ" wypełniona (choćby: „brak istniejących kandydatów").
- [ ] Wpis w logu przez Edit z kotwicą.
- [ ] Zgodność z [[access_map]] (tryb zmiany przez inbox + akceptację).
- [ ] Sekcja „Podstawa metodyczna" obecna; pozycja `{{UZUPEŁNIJ}}` nierozwiązana oznaczona jako `[wiedza własna modelu]`.

# Wzorcowy przykład
[uzupełnić pierwszym zaakceptowanym wynikiem — few-shot musi cytować realny, oceniony przebieg z outputs/router/log.md]

Oczekiwany kształt: dowód próby (3 tagi z uzasadnieniem odrzucenia) → propozycja na czacie → cytat sekcji „1. Diff" z zaakceptowanego `tax_diff_*.md` → jak ingest oznaczył tag warunkowo przed akceptacją.

# Stan akceptacji
Rozstrzygnięcia przyjęte z doświadczenia poprzednika (bezosobowo; szczegóły w [[Lekcje_Poprzednika]]):
- **Bez dowodu próby nie ma propozycji.** Pula tagów rośnie z wygody szybciej niż z potrzeby; wymóg wskazania 2–3 najbliższych tagów i powodu odrzucenia każdego zatrzymał większość „nowych" tagów, które były synonimami istniejących.
- **Zgoda dotyczy jednego przypadku.** Próba dopisania drugiego tagu „skoro już zmieniamy klaster" była odrzucona jako obejście podpisu — każda zmiana taksonomii ma własny diff i własną akceptację.
- **Pula rośnie dopiero po akceptacji, nie po propozycji.** Propozycje ingestu tagowane nowym tagiem przed przeniesieniem diffu oznacza się warunkowo z adnotacją; inaczej odrzucenie tagu zostawia notatki z tagiem spoza puli, których `knowledge_audyt` zgłosi jako naruszenie.
- **Numeracja kroków musi być ciągła.** W wersji poprzednika kroki po zgodzie miały zdublowaną numerację (1-2-3-4-1-2-3), co utrudniało odwołania z innych skilli („wróć do kroku 2") — w szablonie naprawione na 1–7.

# Historia zmian
- 2026-09-05 (v1.0): wersja szablonu — wyprowadzona z działającego systemu-poprzednika; treść osobista i infrastrukturalna usunięta, struktura i zasady zachowane.
