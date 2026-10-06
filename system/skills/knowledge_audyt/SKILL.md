---
name: knowledge_audyt
aliases: ["knowledge_audyt"]              # plik nazywa się SKILL.md — alias pozwala linkować [[knowledge_audyt]] w Obsidianie (lint R8)
description: "Health-check strukturalny vaulta: notatki z tagami spoza puli tags_owned lub bez klastra, osierocone notatki, zepsute wikilinki, nierozwiązane znaczniki [CONTRADICTION], odstępstwa od szablonów systemowych, artefakty po terminie review_every, zaległe źródła captured, propozycje zalegające w inbox/. Opcjonalnie raz na kwartał: TRYB WIERNOŚCI (próbka ingestów zestawiona z oryginałami) i RUBRYKA JAKOŚCI (próbka notatek wiki). Używaj przy zleceniach 'audyt', 'lint', 'health-check vaulta', 'sprawdź spójność', 'czy wiedza jest w porządku' oraz cyklicznie raz w miesiącu. NIE jest tym skillem: naprawianie znalezisk (audyt raportuje i rekomenduje; naprawy to osobne zlecenia po akceptacji raportu), audyt pokrycia wiedzy i portfela źródeł (→ knowledge_audyt_zrodel), audyt zasięgów person (→ knowledge_audyt_dostepow)."
type: skill
skill_type: procedure
used_by:
  - "[[katalizator]]"
depends_on_artifacts:
  - "[[access_map]]"
wymagany_odczyt:                    # ŚCIEŻKI, po jednej linii, z komentarzem KTÓRY KROK tego wymaga
  - clusters/                       # krok 1 i 2: pula tagów z tags_owned, istnienie klastrów
  - moc/                            # krok 2: istnienie warstw wskazywanych w notatkach
  - wiki/                           # kroki 2–6, 8b: taksonomia, sieroty, linki, sprzeczności, szablony, próbka jakości
  - sources/                        # kroki 2, 6, 7b, 8a: taksonomia, szablony, zaległe captured, próbka wierności
  - raw/                            # krok 8a: oryginały do zestawienia (tylko tryb wierności)
  - system/templates/               # krok 1 i 6: wzorce zgodności frontmatterów
  - system/artifacts/               # krok 7a: review_every vs updated
  - system/access_map.md            # krok 1: zasady spójności; NIE porównujesz tu frontmatterów agentów (patrz krok 7)
  - inbox/                          # krok 8: propozycje starsze niż 14 dni
  - outputs/knowledge/              # krok 5 (wiek sprzeczności z logu), krok 9 (raport), log
# Świadomie NIEobecne: system/agents/ — porównanie frontmatterów person z tabelą access_map
# należy do knowledge_audyt_dostepow, którego wykonawca ma ten katalog z tytułu roli.
inputs: "OPCJONALNE: zakres (katalog / warstwa MOC / klaster) — brak = pełny skan. OPCJONALNE: 'tryb wierności' i/lub 'rubryka jakości' (kadencja kwartalna wg [[Rejestr_Cyklow]]) — bez wskazania nie wykonuj kroków 8a/8b. Przy pełnym skanie dużego vaulta zaproponuj podział na 2 przebiegi (wiedza / system) PRZED startem."
output_format: "raport outputs/knowledge/RRRR-MM-DD_audyt.md (kolizja → _02) z ponumerowanymi znaleziskami (waga + pliki + rekomendacja AUTO/RĘCZNA) + wpis w outputs/knowledge/log.md"
version: 1.0
updated: 2026-09-05
---
# Kiedy używać
Zlecenie audytu lub cykliczne uruchomienie — rekomendacja: raz w miesiącu health-check strukturalny (kroki 1–8), raz na kwartał dodatkowo tryb wierności i rubryka jakości (8a, 8b), zgodnie z wierszami w [[Rejestr_Cyklow]].

**NIE jest tym skillem** — testy rozstrzygające:
- *Czy zlecenie brzmi „napraw", „posprzątaj", „usuń sieroty"?* → to osobne zlecenia PO akceptacji raportu. Audyt raportuje i rekomenduje; naprawa w trakcie audytu jest naruszeniem, nawet jeśli jest oczywista.
- *Czy pytanie brzmi „czego nam brakuje w wiedzy i skąd to wziąć"?* → `knowledge_audyt_zrodel` (pokrycie merytoryczne i portfel źródeł). Ten skill pyta „czy vault jest spójny technicznie", nie „czy jest kompletny".
- *Czy pytanie brzmi „czy persona X widzi to, czego wymaga jej skill"?* → `knowledge_audyt_dostepow` u [[rekruter]]. Rozjazd zauważony tu przypadkiem to obserwacja z adnotacją, nie pozycja raportu (krok 7).
- *Czy chodzi o jakość JEDNEJ notatki?* → to praca redakcyjna przez propozycję w inboxie, nie audyt.

# Wymagane wejście
Zakres audytu. Brak wskazania = pełny skan. Przy pełnym skanie dużego vaulta (orientacyjnie: setki notatek) zaproponuj podział na 2 przebiegi (wiedza / system), zanim zaczniesz — jeden przebieg, który się nie mieści, daje raport urwany po cichu. Tryb wierności i rubryka jakości uruchamiają się WYŁĄCZNIE, gdy zlecenie je wywołuje (przebieg kwartalny). Wszystko liczysz na żywo z plików — liczba klastrów, tagów, notatek nie jest znana z góry.

# Podstawa metodyczna (Grounding)
`brak — podstawa normatywna, nie epistemiczna: [[access_map]] (zasady spójności, pary norma–definicja) oraz szablony systemowe w system/templates/ (template_wiki / template_skill / template_agent / template_source / template_artifact jako wzorce zgodności)`. Health-check strukturalny egzekwuje normy systemu, nie metodę z literatury; rubryka jakości ocenia próbkę wg kryteriów zdefiniowanych w tym skillu jako norma systemu.

# Procedura
1. **Zbuduj referencje:** pula tagów z `tags_owned` wszystkich klastrów; lista klastrów i warstw MOC; lista szablonów z `system/templates/` z ich wymaganymi polami; zasady spójności z [[access_map]].
2. **Taksonomia:** Grep frontmatterów `wiki/` i `sources/` — wykaż notatki z tagami spoza puli, bez wskazania klastra/warstwy, lub z klastrem nieistniejącym. Tag „oczekujący na akceptację" (adnotacja z `knowledge_rozszerzenie_taksonomii`) zgłaszasz osobno, jako zaległość inboxa, nie jako naruszenie.
3. **Sieroty:** notatki `wiki/` bez ani jednego linku przychodzącego (Grep nazwy notatki w podwójnych nawiasach kwadratowych po całym vaulcie, z pominięciem samej notatki).
4. **Zepsute linki:** wikilinki prowadzące do nieistniejących plików. Cel `inbox/knowledge/prop_X.md` traktuj jako rozwiązywalny (propozycja w locie), ale zgłoś osobno, jeśli leży w inboxie dłużej niż 14 dni.
5. **Sprzeczności:** wszystkie aktywne znaczniki `[CONTRADICTION]` + wiek każdego (data wpisu w `outputs/knowledge/log.md`, jeśli ustalalna).
6. **Zgodność z szablonami:** notatki bez wymaganych pól frontmatteru dla swojego `type` (porównanie z szablonem danego typu).
7. **Spójność systemu:** (a) artefakty w `system/artifacts/`, którym minęło `review_every` od `updated`; (b) wpisy `sources/` ze `status: captured` starsze niż 30 dni (zaległości ingestu).
   **Czego tu NIE robisz:** porównania frontmatterów person z tabelą [[access_map]]. Wykonawca tego skilla nie ma `system/agents/` w zasięgu, a to samo zestawienie żyje w `knowledge_audyt_dostepow`, którego wykonawca ma ten katalog z tytułu roli. Jeśli w trakcie audytu wiedzy zauważysz rozjazd frontmatter↔mapa przypadkiem (np. czytając artefakt), odnotuj go jako obserwację z adnotacją „poza zakresem tego skilla, do audytu dostępów", nie jako pozycję raportu.
8. **Higiena inboxa:** propozycje w `inbox/` starsze niż 14 dni — lista do decyzji Właściciela (akceptacja / odrzucenie), z podziałem na strefy (`knowledge`, `agents`, `skills`, `ops`, `tech`).
8a. **TRYB WIERNOŚCI (wyłącznie gdy zlecenie go wywołuje; kadencja kwartalna — wiersz w [[Rejestr_Cyklow]]).** Kontrola, czy ingest nie tnie źródeł mocniej, niż deklaruje — przeciw propagacji błędu pierwotnego:
   a. Wylosuj 3–5 notatek z `sources/` o `status: processed`, zaktualizowanych w ostatnim kwartale (przy mniejszej liczbie — wszystkie).
   b. Dla każdej sprawdź sekcję „## Granice kompresji": BRAK lub boilerplate = znalezisko (waga średnia) niezależnie od dalszych kroków.
   c. Zestaw notatkę z ORYGINAŁEM: jeśli plik leży w `raw/` — czytasz sam; jeśli nie — wypisz w raporcie listę potrzebnych źródeł (tytuł + strony cytowane w notatce) i poproś Właściciela o wgranie plików do `raw/` na czas przebiegu albo wklejenie wskazanych fragmentów. Pozycji bez oryginału NIE oceniasz — oznaczasz „niezweryfikowana w tym przebiegu", nigdy nie zgadujesz.
   d. Werdykt per notatka, każdy z cytatem oryginału obok twierdzenia notatki: **WIERNA** / **PRZYCIĘTA BEZPIECZNIE** (pominięcia istnieją, ale są zadeklarowane w Granicach kompresji i nie zmieniają sensu) / **ZNIEKSZTAŁCONA** (teza notatki mocniejsza lub inna niż w oryginale, pominięcie zmienia sens, cytat lub paginacja niezgodne z egzemplarzem).
   e. Dla każdej ZNIEKSZTAŁCONEJ: propozycja sprostowania przez `inbox/knowledge/` (nigdy bezpośrednia edycja) + KONTROLA PROPAGACJI — Grep stron z `distilled_to` i linków tej notatki; strony wiki wyprowadzone ze zniekształconego fragmentu wypisz w raporcie jako dotknięte, z rekomendacją przeglądu.
8b. **RUBRYKA JAKOŚCI (wyłącznie w przebiegu kwartalnym, razem z trybem wierności).** Health-check mierzy spójność strukturalną; ta rubryka jako jedyna ocenia JAKOŚĆ treści:
   a. Próbka: 10 losowych notatek `wiki/` (albo wszystkie, gdy jest ich mniej) + wszystkie z polem `quality` na poziomie 2 lub niższym + notatki bez ani jednego linku przychodzącego spoza własnego klastra.
   b. Trzy kryteria per notatka, każde OK/uwaga z jednym zdaniem: (1) AKTUALNOŚĆ względem korpusu — czy nowsze notatki lub źródła nie unieważniły albo nie zawęziły jej twierdzeń (Grep po kluczowych pojęciach); (2) ZGODNOŚĆ `summary` z treścią — czy streszczenie obiecuje to, co strona faktycznie zawiera; (3) UŻYCIE — czy cokolwiek na nią wskazuje, a jeśli nic — czy to problem strony, czy naturalna pozycja referencyjna.
   c. Wynik: osobna sekcja raportu z kandydatami do POPRAWY (co konkretnie), SCALENIA (z którą stroną i czemu) albo ARCHIWIZACJI — wyłącznie rekomendacje; decyzje i wykonanie po stronie Właściciela (propozycje przez `inbox/knowledge/` jak zwykle).
   d. Rubryka NICZEGO nie poprawia w locie i nie zmienia pól `quality` — to wejście do decyzji, nie egzekucja.
9. **Zbuduj raport** wg szablonu wyniku i zapisz do `outputs/knowledge/`. W przebiegu kwartalnym raport zawiera sekcje 5 („Tryb wierności") i 6 („Rubryka jakości"); w przebiegu miesięcznym wpisz w nich „nie dotyczy — przebieg miesięczny", nie usuwaj ich i nie przesuwaj numeracji.
10. **Dopisz wpis do `outputs/knowledge/log.md`** wyłącznie narzędziem Edit z kotwicą na końcu pliku (technika jak w kroku 7 `knowledge_ingest`): `## [RRRR-MM-DD] audyt | zakres | X znalezisk (K krytycznych / S średnich / M kosmetycznych)`.

# Szablon wyniku
Plik: `outputs/knowledge/RRRR-MM-DD_audyt.md` (kolizja w tym samym dniu → sufiks `_02`).
Frontmatter wg `template_output.md`: `type: output`, `agent: katalizator`, `task: audyt`, `date`, `head: "[[knowledge]]"`, `linked_sources: []`, `status`, dodatkowo `scope: <zakres>`.
Sekcje w stałej numeracji (sekcja pusta = „nie dotyczy", nie usuwaj i nie przesuwaj numeracji):
```
# Raport audytu — [RRRR-MM-DD]
## 1. Podsumowanie (3 zdania + liczby: X naruszeń taksonomii, Y sierot, Z zepsutych linków, W sprzeczności, V zaległości)
## 2. Znaleziska
ponumerowana lista; każda pozycja: waga (krytyczna / średnia / kosmetyczna), opis, dotknięte pliki (ścieżki), rekomendacja: AUTO (mogę naprawić po akceptacji, jednym zleceniem) / RĘCZNA (wymaga decyzji Właściciela)
## 3. Obserwacje poza zakresem (np. rozjazd frontmatter↔mapa „do audytu dostępów") — albo „brak"
## 4. Proponowana kolejność napraw (krytyczne najpierw; pozycje AUTO zgrupowane w jedno zlecenie)
## 5. Tryb wierności (tylko kwartalnie: tabela notatka → werdykt → cytat oryginału → propagacja) — albo „nie dotyczy"
## 6. Rubryka jakości (tylko kwartalnie: tabela notatka → 3 kryteria → rekomendacja) — albo „nie dotyczy"
```

# Checklist przed oddaniem
- [ ] Każde znalezisko ma wagę, ścieżki plików i rekomendację AUTO/RĘCZNA.
- [ ] Zero napraw wykonanych w trakcie audytu — tylko raport (także wtedy, gdy naprawa była jednolinijkowa).
- [ ] Referencje (pula tagów, lista klastrów, szablony) zbudowane na żywo w tym przebiegu, nie z pamięci.
- [ ] Porównanie frontmatterów person z [[access_map]] NIE wykonane tu; rozjazd zauważony przypadkiem trafił do sekcji 3 jako obserwacja.
- [ ] (tryb wierności) Każdy werdykt ma cytat oryginału; pozycje bez oryginału oznaczone „niezweryfikowana", nie ocenione zgadywaniem; zniekształcenia mają propozycję sprostowania i listę stron dotkniętych propagacją.
- [ ] (rubryka jakości) Zero zmian pól `quality` i zero poprawek w locie.
- [ ] Sekcje 5 i 6 obecne także w przebiegu miesięcznym (jako „nie dotyczy"), numeracja stała.
- [ ] Log zaktualizowany przez Edit z kotwicą.
- [ ] Zgodność z [[access_map]] (zakres odczytu wykonawcy nieprzekroczony).
- [ ] Sekcja „Podstawa metodyczna" obecna (postać normatywna).

# Wzorcowy przykład
[uzupełnić pierwszym zaakceptowanym wynikiem — few-shot musi cytować realny, oceniony przebieg z outputs/router/log.md]

Oczekiwany kształt: 3 pozycje znalezisk z pierwszego audytu, po jednej dla każdej wagi, każda z pełną trójką waga/pliki/rekomendacja; plus jeden przykład obserwacji „poza zakresem", żeby pokazać różnicę między pozycją raportu a adnotacją.

# Stan akceptacji
Rozstrzygnięcia przyjęte z doświadczenia poprzednika (bezosobowo; szczegóły w [[Lekcje_Poprzednika]]):
- **Audyt raportuje, nie naprawia.** Naprawa w locie, nawet trywialna, miesza role: ten sam przebieg staje się sędzią i wykonawcą, a Właściciel traci punkt, w którym decyduje.
- **Pozycja niewykonalna w granicach wykonawcy została przeniesiona do skilla, którego wykonawca ma dostęp z tytułu roli.** Porównanie frontmatterów person z mapą wymagało odczytu `system/agents/`, którego katalizator nie ma; rozważono i odrzucono nadanie dostępu (konfiguracja całego systemu przyznawana dla jednej pozycji lintu). Zasada ogólna: nie każda twarda zależność skilla musi trafić do zasięgu — tańszą naprawą bywa przepisanie kroku.
- **Rozjazd zauważony przypadkiem to obserwacja z adnotacją, nie pozycja raportu.** Inaczej audyt „po cichu" rozszerza własny zakres i zaczyna orzekać o rzeczach, których nie zbadał systematycznie.
- **Tryb wierności jako kwartalna opcja, nie stały krok.** Zestawianie notatek z oryginałami jest drogie i wymaga materiału od Właściciela; jako kontrola co miesiąc zamieniłoby się w rytuał. Kwartalna próbka 3–5 notatek plus sekcja „Granice kompresji" po stronie ingestu wystarczają, żeby ciche cięcie było wykrywalne.
- **Stała numeracja sekcji raportu.** Sekcje kwartalne obecne również w raporcie miesięcznym jako „nie dotyczy" — dzięki temu porównanie raportów w czasie nie wymaga zgadywania, czy sekcji nie było, czy nie była potrzebna.

# Historia zmian
- 2026-09-05 (v1.0): wersja szablonu — wyprowadzona z działającego systemu-poprzednika; treść osobista i infrastrukturalna usunięta, struktura i zasady zachowane.
