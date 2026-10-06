---
type: log
title: Log delegacji routera
owner: "[[router]]"
scope: "Rejestr wszystkich zleceń: routing, wyniki, jakość. Podstawa przeglądów person, few-shotów i poprawek pól description."
append_only: true
entry_count: 0
last_entry:            # puste do pierwszego wpisu
version: 1.0
created: 2026-09-05
updated: 2026-09-05
---
# Instrukcja wpisu (dla routera)
Dopisuj na końcu pliku, wg wzoru poniżej. Pola `ocena`, `poprawka` i `wnioski` zostawiaj puste — wypełnia je Właściciel przy przeglądzie (przypomnij mu o tym po ważniejszych przebiegach: to jedyne paliwo dla przeglądów person i few-shotów). Nie modyfikuj wpisów historycznych (append_only). Po dopisaniu zaktualizuj `entry_count` i `last_entry` we frontmatterze. Dopisuj narzędziem Edit z kotwicą na końcu pliku, nie przepisuj całego pliku.

Rotacja: gdy plik przekroczy ~200 wpisów, Właściciel (lub przewodnik na jego polecenie) przenosi wpisy sprzed bieżącego kwartału do `log_RRRRQn.md` obok; liczniki biegną dalej bez resetu.

# Wzór wpisu
## [ID: RRRR-MM-DD-NNN]  ← wzór, nie wpis
- **zlecenie:** [skrót 1 zdanie — pełną treść zlecenia dostaje persona, w logu wystarczy skrót]
- **routing:** [persona lub łańcuch, np. zwiadowca → katalizator; droga: wcielenie | delegacja]
- **pewność routingu:** wysoka | średnia | niska (+ 1 zdanie, jeśli nie wysoka: między kim się wahałeś i dlaczego tak wybrałeś)
- **wyniki:** [[outputs/dział/RRRR-MM-DD_persona-skrót]]
- **uwagi routera:** [problemy: brak wiedzy w vaultcie, persona poza dostępami, odmowa polityki zapisu, konieczność dopytania; „brak" jeśli czysto]
- **czas:** [wypełnia Właściciel, NIE router: „-" jeśli nie mierzono]
- **ocena (Właściciel):** ⬜ 1–5
- **poprawka (Właściciel):** ⬜ min [łączny czas Twojej pracy nad wynikiem PO przebiegu; 0 = użyty bez zmian; puste ⬜ = jeszcze nieocenione]
- **wnioski (Właściciel):** [co poprawić: description? definicja persony? luka w wiki?]

---

# Wpisy

