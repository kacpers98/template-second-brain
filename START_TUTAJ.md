---
type: system
title: "Start tutaj"
---
# Start tutaj

## Czym to jest — i czym nie jest

To jest **szkielet osobistego systemu wiedzy i agentów**: folder notatek (Obsidian), w którym zespół wyspecjalizowanych „person" AI (uruchamianych przez Claude Code) pomaga Ci porządkować wiedzę fachową, wykonywać powtarzalne czynności i podejmować decyzje — **nigdy nie zmieniając niczego ważnego bez Twojej zgody**. Wszystko, co persony proponują, ląduje w skrzynce `inbox`, a do systemu trafia dopiero, gdy powiesz „akceptuję".

Szkielet został wyprowadzony z działającego systemu, który jedna osoba budowała i używała przez kilka miesięcy w zupełnie innej branży niż Twoja. Z tamtego systemu zostały tu **reguły, struktura i sześć uniwersalnych person** — cała wiedza, treści osobiste i narzędzia branżowe zostały usunięte. Twoją wiedzę i Twoje persony zbudujesz sam, prowadzony przez siódmą personę: **przewodnika**.

**Czym to NIE jest:** nie jest gotowym asystentem, który działa od pierwszej minuty. Pusty vault nic nie umie. Pierwsze 3–5 sesji z przewodnikiem to konfiguracja (wywiad o Twojej pracy, nazwanie obszarów wiedzy, pierwsze 3 źródła, pierwsza własna persona). Nie jest też automatem — wszystko dzieje się w rozmowie, w której jesteś obecny. Automatyzacje to osobna decyzja na później.

## Trzy kroki do pierwszej rozmowy

**Krok 1 — Obsidian.** Masz ten folder otwarty jako vault w Obsidianie (jeśli czytasz to w Obsidianie — masz). Otwórz plik `KOKPIT.md` — to Twój pulpit.

**Krok 2 — Dwie wtyczki.** Jeśli w KOKPICIE zamiast tabel widzisz ramki z surowym tekstem, brakuje wtyczki. Ustawienia (koło zębate) → *Wtyczki społeczności* → *Wyłącz tryb ograniczony* → *Przeglądaj* → wyszukaj **Dataview** → *Zainstaluj* → *Włącz*. To samo dla **Git** (nazwa: „Git" lub „Obsidian Git"). Wróć do KOKPITU — tabele powinny się pojawić.

**Krok 3 — Claude Code.** Otwórz terminal w tym folderze i uruchom `claude` (jeśli masz już otwarte Claude Code w tym folderze — masz). Napisz pierwszą wiadomość:

> **zacznijmy**

Odezwie się przewodnik. Powie, na którym etapie jesteście (na początku: 0), zada jedno pytanie i poprowadzi dalej. Odpowiadasz zwykłym językiem. Gdy zaproponuje zmianę w systemie, zobaczysz ją najpierw opisaną po ludzku, a potem Claude Code zapyta o zgodę na komendę — Twoje „tak" jest podpisem.

## Co się będzie działo (8 etapów, w tej kolejności — kolejność nie jest przypadkowa)

0. Kontrola środowiska (wtyczki, historia zmian, kopia zapasowa) · 1. Wywiad o Twojej pracy · 2. Twój profil i granice (co poufne) · 3. Mapa obszarów wiedzy (najważniejszy etap) · 4. Pierwsze 3 źródła · 5. Pierwsza własna persona · 6. Rytmy (przegląd tygodniowy) · 7. Przekazanie do użytku.

Przewodnik nie przepuści Cię dalej, dopóki etap nie jest domknięty — i ostrzeże, gdy będziesz chciał zrobić coś, co u poprzednika okazało się ślepą uliczką (np. założyć od razu dziesięć obszarów wiedzy, wgrać trzydzieści książek „na zapas", automatyzować przed używaniem). Możesz go nie posłuchać — zapisze to jako Twoją świadomą decyzję.

## Gdzie co jest (na później — nie musisz tego czytać teraz)

- `KOKPIT.md` — pulpit: co czeka na akceptację, świeże wyniki, stan wdrożenia.
- `system/` — reguły (kto co może: `access_map.md`), persony (`agents/`), procedury (`skills/`), normy i rejestry (`artifacts/`), szablony. Tu agenci NIE piszą — tylko proponują.
- `moc/`, `clusters/` — mapa Twoich obszarów wiedzy (warstwy → klastry → tagi). Powstaje w etapie 3.
- `wiki/`, `sources/` — Twoja wiedza: notatki i notatki źródłowe. Powstają od etapu 4.
- `raw/` — tu wrzucasz pliki do przetworzenia (PDF, teksty). Agenci ich nie zmieniają.
- `inbox/` — propozycje czekające na Twoje „akceptuję".
- `outputs/` — wyniki pracy person i logi (co kto zrobił, z Twoją oceną 1–5).
- `narzedzia/` — dwa skrypty, które przewodnik uruchamia za Ciebie (akceptacja, kontrola spójności).
- `system/artifacts/Lekcje_Poprzednika.md` — jeśli chcesz wiedzieć, skąd wzięły się te reguły.

## Zasady, których szablon nie pozwoli Ci złamać (i dlaczego)

Agenci nie piszą do Twojej wiedzy ani do reguł systemu — tylko proponują (żeby nic nie zmieniło się bez Ciebie). Nic nie wychodzi poza ten folder (w szablonie nie ma narzędzi wysyłających cokolwiek — to celowe). Dane klientów, pracodawcy, pacjentów, Twoje zdrowie i finanse z kwotami NIE wchodzą do vaulta (bo vault czytają agenci). Historia każdej zmiany jest w gicie (żeby nic nie ginęło).

## Licencja

MIT (plik `LICENSE`). Możesz używać, zmieniać i rozpowszechniać, także komercyjnie, z zachowaniem noty autorskiej.
