---
name: dzial_czynnosc
description: "TEKST ROUTINGOWY (300–900 znaków): jaką procedurę wykonuje i przy jakich zleceniach ją uruchamiać („Używaj przy KAŻDYM zleceniu typu …") oraz czym NIE jest („NIE jest tym skillem: …")."
# --- pola własne ---
type: skill
skill_type: procedure               # procedure | template | script
used_by:
  - "[[persona]]"
depends_on_artifacts:               # skill = procedura; WIEDZA i NORMY żyją w artefaktach (lint R1: para z zasięgiem persony)
  - "[[Nazwa_Artefaktu]]"
wymagany_odczyt:                    # POLE OBOWIĄZKOWE. ŚCIEŻKI (nie artefakty), których procedura wymaga do ODCZYTU
  - outputs/ops/                    # — po jednej linii, z komentarzem wskazującym KROK, który tego wymaga.
# Dlaczego to pole istnieje: ścieżki żyjące wyłącznie w prozie kroków nikt nie porównuje z kolumną
# „Odczyt (poza wiki/)" w access_map — u poprzednika to była najczęstsza klasa defektu: skill niewykonalny
# w literze normy przy czystym lincie. Pilnuje tego reguła R13 (ścieżki skilla ↔ zasięg persony z used_by).
# Konwencja: moc/ i clusters/ są czytelne dla każdej persony (zasada 4) i nie wymagają nadania; zasięg wiki/
# niesie cluster_access. Ścieżka WARUNKOWA (krok wykonalny bez niej) NIE wchodzi do pola — opisz ją komentarzem.
inputs: "co procedura dostaje na wejściu — TWARDE / warunkowe / opcjonalne"
output_format: "ścieżka wyniku + numeracja sekcji + czy plik jest nadpisywany"
version: 1.0
updated: RRRR-MM-DD
---
# Kiedy używać
[Doprecyzowanie description: typy zleceń, które uruchamiają tę procedurę.]
**NIE jest tym skillem:** [pokrewne przypadki z TESTEM ROZRÓŻNIAJĄCYM, symetrycznie po obu stronach granicy — granica opisana jednostronnie działa tylko dla tego, kto ją czyta.]

# Wymagane wejście
[Czego procedura potrzebuje na starcie (twarde / warunkowe / opcjonalne); co zrobić, gdy czegoś brakuje — domyślnie: dopytać, nie zgadywać. Wejścia czytane na żywo, nie z pamięci.]

# Podstawa metodyczna (Grounding)
[SEKCJA OBOWIĄZKOWA jako SLOT — nie usuwaj jej. Wolno w niej wpisać „brak", nie wolno jej pominąć.]
Indeks notatek `wiki/`, na których stoi METODA stosowana przez tę procedurę — nie temat, którego dotyczy. Test rozstrzygający: czy notatka mówi, JAK wykonać krok, czy O CZYM ten krok będzie.

Format — jedna linia na pozycję, trzy elementy obowiązkowe:
```
- [[nazwa-notatki]] → krok N — [co ta notatka wnosi DO TEGO KROKU]
```
Ta sama pozycja powtarza się przy właściwym kroku jako `Grounding: [[nazwa]]`.

Trzy dopuszczalne postacie „brak" (samo słowo „brak" jest niekompletne):
1. `brak — procedura mechaniczna` (walidacja formatu, przeniesienie pliku — metoda nie ma wariantów).
2. `brak — podstawa normatywna, nie epistemiczna: [[Artefakt]]` (procedura stosuje decyzję Właściciela albo normę systemu, nie metodę z literatury).
3. `brak — LUKA WIEDZY: metoda ma literaturę, vault jej nie ma` + jedno zdanie, czego brakuje. Ta wartość jest jednocześnie ZGŁOSZENIEM kandydata do ingestu dla [[katalizator]].

TEST JAKOŚCI — pozycja wypełniona byle czym jest gorsza od jej braku. Pozycja przechodzi, gdy przechodzi WSZYSTKIE TRZY: (1) **test nazwy pliku** — jeśli uzasadnienie dałoby się napisać z samej nazwy notatki, notatka nie została przeczytana; (2) **test podmiany** — jeśli uzasadnienie pozostaje prawdziwe po podmianie notatki na inną z tego samego klastra, pozycja opisuje TEMAT, nie METODĘ; (3) **test usunięcia** — powiedz, co konkretnie w WYNIKU byłoby inne, gdyby wykonawca tej notatki nie przeczytał; „nic" = pozycja do usunięcia.

Granica odpowiedzialności: [[metodyk]] nie ma `wiki/` w zasięgu, więc NIE może zweryfikować, czy notatka istnieje ani co mówi. Pozycję niezweryfikowaną wpisuje jako `- [[nazwa]] → krok N — KANDYDAT, uzasadnienie do potwierdzenia przez [[katalizator]]` i wypisuje w „Do akceptacji". W vaultcie startowym większość pozycji to `{{UZUPEŁNIJ: notatka o …}}` — do czasu ingestu krok wykonuje się z oznaczeniem [wiedza własna modelu].

# Procedura
0. [wybór ścieżki/trybu, jeśli skill ma warianty]
1. [krok — konkretny, wykonywalny; przy krokach warunkowych: „jeśli X → krok 5, jeśli nie → krok 6"]
2. [krok stojący na notatce niesie ją inline: `Grounding: [[nazwa]]`]
3. ...
Zasady stałe: brak danych = zapis „brak danych" (zero szacowania z trendu); wstrzymanie / „czysto" / przebieg zerowy to pełnoprawne wyniki — nie wymyślaj pracy, żeby wynik wyglądał na pełny; ciche skrócenie zabronione, skrócenie z licznikiem („+N dalsze") dozwolone; skill nie przechowuje danych, które dezaktualizują się po cichu (progi, stawki, limity) — ustala je ze źródła przy każdym przebiegu.

# Szablon wyniku
[Dosłowna struktura outputu: frontmatter wg [[template_output]], sekcje o STAŁEJ numeracji — sekcja pusta = „nie dotyczy", nie usuwaj i nie przesuwaj numeracji. Nazwa pliku: `RRRR-MM-DD_<persona>-<skrót>.md`; kolizja → sufiks `_02` (nie `_v2`). Wyniki cykliczne: jeden plik kanoniczny nadpisywany, historię trzyma git.]

# Checklist przed oddaniem
- [ ] [kontrola 1 — specyficzna, weryfikowalna; kontrola wymagająca WYWOŁANIA NARZĘDZIA nie może być haczykiem do odhaczenia — ma osobny krok z liczbą]
- [ ] [kontrola 2]
- [ ] Zgodność z [[artefakt z depends_on_artifacts]]
- [ ] Sekcja „Podstawa metodyczna" obecna i niepusta (pozycje w formacie albo jedna z trzech postaci „brak" z dopiskiem); pozycje niezweryfikowane oznaczone jako KANDYDAT.

# Wzorcowy przykład
[uzupełnić pierwszym zaakceptowanym wynikiem — few-shot musi cytować realny, oceniony przebieg z outputs/router/log.md]
Każde twierdzenie o zachowaniu w tym przykładzie musi mieć pokrycie w treści cytowanego wyniku, a cytowany przebieg musi mieć wpis z oceną w logu — jeśli nie ma, oznacz to jawnie.

# Stan akceptacji
[Powstaje z sekcji „## Do akceptacji" przy podpisie (skille się KONWERTUJE, nie odcina — bo skill nie ma osobnej Historii, w której ślad decyzji mógłby zostać). Wpisy od najnowszego: rozstrzygnięcie WDROŻONE / OTWARTE + jedno zdanie dlaczego.]

# Historia zmian
- RRRR-MM-DD (v1.0): [co + POWÓD + który przebieg to wymusił]

---
## Do akceptacji
[Sekcja istnieje WYŁĄCZNIE w propozycji w inbox/skills/. Warianty do decyzji Właściciela (A/B z konsekwencjami), pozycje KANDYDAT z Groundingu, DECYZJE OTWARTE oznaczone tak, „żeby nie dały się przeczytać jako rozstrzygnięcie". Separator `---` nad tym nagłówkiem jest MECHANIZMEM: akceptuj.py konwertuje tę sekcję na „Stan akceptacji" — instrukcja prozą nie wystarczy, bo przeniesienie pliku to operacja bez czytania.]
