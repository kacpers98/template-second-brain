---
type: artifact
artifact_type: registry
title: "Rejestr Sekretów"
owner_head: "[[knowledge]]"
used_by: []
inject: never
scope: "Rejestr NAZW sekretów i warstw niewersjonowanych: gdzie żyje każda pozycja, skąd ją odtworzyć, kadencja rotacji. NIGDY wartości. Czyta wyłącznie Właściciel."
authority: reference
agent_access: false
review_every: 90d
version: 1.0
created: 2026-09-05
updated: 2026-09-05
---
# Rejestr Sekretów

# Cel dokumentu
Rejestr **nazw** sekretów systemu i miejsc, w których żyją — po to, żeby po awarii dysku, utracie konta lub zmianie komputera było CO odtwarzać, zamiast opierać się na pamięci. W stanie startowym szablonu (Obsidian + git + Claude Code) sekretów jest niewiele — typowo dostęp do zdalnego repozytorium git i konto dostawcy modelu; rejestr rośnie wraz z każdym rozszerzeniem stacku ([[Stack_Technologiczny]], sekcja „Możliwe rozszerzenia").

**ŻELAZNA ZASADA — jedyna, której naruszenie unieważnia cały dokument:** ten plik NIGDY nie zawiera wartości sekretu. Ani w całości, ani we fragmencie, ani „na chwilę do testu", ani w komentarzu, ani w historii zmian. Wyłącznie: nazwa, miejsce życia, ścieżka odtworzenia, kadencja rotacji. Plik ma `agent_access: false` — jest niewidoczny dla WSZYSTKICH person niezależnie od ich zasięgu odczytu ([[access_map]]) — ale to zabezpieczenie drugiej linii, nie licencja na wpisywanie tu czegokolwiek wrażliwego. Vault jest w gicie; jeżeli ma zdalne repozytorium, każda wartość wpisana tu „na chwilę" zostaje w historii na zawsze.

# Zasady prowadzenia
1. **Zero wartości sekretów w tym pliku** (patrz wyżej). Zero także w opisach commitów, w `outputs/`, w logach routera i w treści zleceń dla person. Wartość, która trafiła do czatu z personą, jest wartością ujawnioną — podlega rotacji, nie „usunięciu z historii".
2. **Każdy NOWY sekret dostaje wiersz w tabeli w tym samym kroku**, w którym powstaje (klucz wygenerowany w panelu dostawcy, token wklejony do pliku środowiskowego) — nie „przy najbliższej okazji". Propozycja rozszerzenia stacku bez wiersza w tym rejestrze jest niekompletna ([[Stack_Technologiczny]] zasada 2).
3. **Wartości odtwarzasz wyłącznie z panelu dostawcy albo z menedżera haseł** — NIGDY z kopii pliku środowiskowego wysłanej mailem lub komunikatorem, z historii terminala ani z załącznika w czacie.
4. **Kopia wartości KAŻDEJ pozycji w menedżerze haseł pod nazwą IDENTYCZNĄ z kolumną „Nazwa".** Podział ról: menedżer haseł trzyma wartości, ten plik mówi, gdzie żyją operacyjnie i jak je odtworzyć. Procedura po awarii = ten rejestr + menedżer haseł, zero przekopywania paneli. Menedżer haseł Właściciela: {{UZUPEŁNIJ: nazwa menedżera haseł}}.
5. **Kolumna „Rotacja" jest JEDYNYM źródłem prawdy o kadencji.** Ewentualny wiersz „Rotacja sekretów" w [[Rejestr_Cyklow]] wyłącznie przypomina i odsyła tutaj. Zmiana kadencji = zmiana komórki tutaj + wpis w Historii zmian.

# Sekrety
Kolumny: **Nazwa** (nazwa zmiennej lub pozycji — jak w menedżerze haseł) · **Gdzie żyje** (plik, panel, urządzenie — operacyjne miejsce użycia) · **Skąd odtworzyć** (panel dostawcy / menedżer haseł / „nie do odtworzenia — wygenerować nową") · **Rotacja** (kadencja kalendarzowa albo „zdarzeniowa").

| Nazwa | Gdzie żyje | Skąd odtworzyć | Rotacja |
| --- | --- | --- | --- |
| {{UZUPEŁNIJ: NAZWA_ZMIENNEJ}} | gdzie żyje | skąd odtworzyć | rotacja |

# Warstwy, które NIE odtworzą się z repozytorium
Nie są sekretami, ale mają dokładnie tę samą właściwość: znikają razem z maszyną i nikt o nich nie pamięta w trakcie awarii. Każda taka warstwa dostaje tu wiersz z instrukcją odtworzenia (bez wartości).

| Warstwa | Dlaczego poza gitem | Jak odtworzyć |
| --- | --- | --- |
| Lokalne ustawienia sesji Claude Code (np. `.claude/settings.local.json`, jeśli powstanie) | w `.gitignore` — zawierają uprawnienia i ustawienia specyficzne dla maszyny | {{UZUPEŁNIJ: stan minimalny do przywrócenia po odtworzeniu środowiska}} |
| Pliki środowiskowe (`.env` lub równoważne) przy każdym rozszerzeniu stacku | świadomie poza gitem — niosą wartości | wyłącznie z tego rejestru + menedżera haseł / paneli dostawców |
| Sesje logowania w przeglądarce (np. do źródeł subskrypcyjnych) | żyją w przeglądarce, nie w plikach | ponowne logowanie ręczne przez Właściciela; automatyzacja logowania z uwierzytelnianiem dwuskładnikowym jest świadomie NIEDOPUSZCZONA (dwuskładnikowość istnieje po to, żeby automat się nie logował) |

# Kadencje rotacji — zasada
Dwie klasy pozycji, żeby kolumna „Rotacja" nie była wypełniana „do ustalenia":
- **Kalendarzowa** — dla kluczy API i tokenów dostępu do usług: jedna wspólna kadencja dla wszystkich pozycji tej klasy — {{UZUPEŁNIJ: kadencja, np. 180 dni}}; licznik od daty ostatniej rotacji. Jedna kadencja zamiast wielu, bo wiele kadencji oznacza wiele terminów do pilnowania i żadnego pilnowanego.
- **Zdarzeniowa** — dla pozycji, których rotacja jest kosztowna lub wymuszana przez zdarzenie (klucze prywatne, hasła baz danych, tokeny urządzeń): rotacja przy podejrzeniu wycieku, przy odtwarzaniu maszyny i przy każdej wartości, która pojawiła się w czacie, logu lub wiadomości.
- Pozycja, która NIE jest sekretem (identyfikator, adres, nazwa folderu), ale jest potrzebna do odtworzenia systemu, dostaje wiersz z rotacją „nie dotyczy" — dla kompletności skanu.

# Kontekst i uzasadnienie
Poprzednik budował ten rejestr po fakcie — gdy okazało się, że odwołania do „rotacji sekretów" w innych normach wskazywały w pustkę, a jedna z wartości trafiła do zewnętrznej rozmowy przez wklejenie alertu, który niósł ją w treści (szczegóły: [[Lekcje_Poprzednika]], część II). Trzy lekcje weszły do zasad: wartość w czacie = wartość ujawniona (zasada 1); wiersz w tym samym kroku co sekret (zasada 2) — „przy okazji" nie nastąpiło ani razu; jedna kadencja dla całej klasy (sekcja Kadencje) — rozjazd dwóch norm o częstotliwości rotacji został rozstrzygnięty dopiero wtedy, gdy jedna kolumna została ogłoszona jedynym źródłem prawdy.

# Przykłady zastosowania
## Dobrze
Właściciel decyduje o zdalnym prywatnym repozytorium git dla vaulta. W tym samym kroku, w którym generuje klucz dostępu, dopisuje wiersz: nazwa klucza · „konfiguracja git na tym komputerze" · „panel dostawcy repozytorium → klucze dostępu; kopia w menedżerze haseł pod tą samą nazwą" · „zdarzeniowa (przy zmianie komputera lub podejrzeniu wycieku)". Wartość klucza nie pojawia się nigdzie w vaultcie.
## Źle
Persona [[przewodnik]] przy konfiguracji rozszerzenia prosi: „wklej token, sprawdzę, czy działa" — a Właściciel wkleja go do czatu. Naruszona zasada 1 (wartość w czacie = ujawniona → rotacja) oraz duch `agent_access: false` (żadna persona nie potrzebuje wartości; potrzebuje wyłącznie nazwy i miejsca). Poprawnie: przewodnik podaje gotową komendę, którą Właściciel uruchamia sam, a token wkleja bezpośrednio do pliku środowiskowego poza vaultem.

# Wyjątki i przypadki brzegowe
- Sekret współdzielony z inną osobą (np. wspólne konto): wiersz tutaj + adnotacja „współdzielony" — rotacja wymaga uzgodnienia, więc zawsze zdarzeniowa.
- Sekret, którego nie da się odtworzyć (klucz prywatny wydawany jednorazowo): w kolumnie „Skąd odtworzyć" wpisz wprost „NIE DA SIĘ — wygenerować nowy + kroki ponownej rejestracji"; to nie jest luka, to informacja krytyczna.
- Wszystko inne: decyzja Właściciela. Persony nie czytają tego pliku i nie proponują do niego zmian.

# Historia zmian
- 2026-09-05 (v1.0): wersja szablonu — wyprowadzona z działającego systemu-poprzednika; treść osobista i infrastrukturalna usunięta, struktura i zasady zachowane.
