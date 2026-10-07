# SecondBrain Template

Szkielet osobistego systemu wiedzy i agentów: vault Obsidian, w którym zespół wyspecjalizowanych person AI (uruchamianych przez Claude Code) porządkuje wiedzę, wykonuje powtarzalne czynności i pomaga decydować, nigdy nie zmieniając niczego ważnego bez Twojej zgody.

Szablon został wyprowadzony z działającego systemu, który jedna osoba budowała i używała produkcyjnie od września 2026 (opis: [kacpersliwinski.com/wpisy/secondbrain/](https://kacpersliwinski.com/wpisy/secondbrain/)). Zostały w nim reguły, struktura i siedem uniwersalnych person. Cała wiedza, treści osobiste i narzędzia branżowe zostały usunięte. Swoje obszary i persony budujesz sam, prowadzony przez personę **przewodnik**.

## Co jest w środku

- **Struktura vaulta**: `wiki/`, `clusters/`, `moc/`, `sources/`, `raw/`, `inbox/`, `outputs/`, `system/`. Opis każdego katalogu w `START_TUTAJ.md`.
- **Siedem person** w `system/agents/`: przewodnik (wdrożenie), asystent, doradca, katalizator, metodyk, rekruter (tworzy kolejne persony), zwiadowca (źródła).
- **Model uprawnień** `system/access_map.md`: co dana persona może czytać, a co zmieniać. Egzekwowany technicznie przez `.claude/settings.json`, nie tylko na papierze.
- **Bramka akceptacji**: persony proponują zmiany do `inbox/`, do systemu trafiają po Twoim „akceptuję” (`narzedzia/akceptuj.py`).
- **Lint spójności** `narzedzia/lint.py`: deterministyczna kontrola, czy system nie złamał własnych reguł.
- **Procedury (skille)** w `system/skills/`, szablony notatek w `system/templates/`, artefakty normatywne w `system/artifacts/`.
- **Przewodnik wdrożenia** `system/skills/wdrozenie_krok_po_kroku/` i stan etapów w `outputs/wdrozenie/STAN_WDROZENIA.md`.

## Start

1. Sklonuj repozytorium albo użyj „Use this template” i otwórz folder jako vault w Obsidianie.
2. Zainstaluj wtyczki Dataview i Git (szczegóły w `START_TUTAJ.md`).
3. Uruchom Claude Code w katalogu vaulta. `CLAUDE.md` kieruje pierwszą sesję do przewodnika, który prowadzi wywiad i konfigurację etapami.

Pierwsze 3–5 sesji to konfiguracja: wywiad o Twojej pracy, nazwanie obszarów wiedzy, pierwsze trzy źródła, pierwsza własna persona. Pusty vault nic nie umie. To nie jest asystent gotowy od pierwszej minuty i nie jest automat: wszystko dzieje się w rozmowie, w której jesteś obecny.

## Wymagania

- Obsidian z wtyczkami Dataview i Git
- Claude Code
- Python 3.11 lub nowszy (narzędzia w `narzedzia/`)
- git

## Zasady, które szablon egzekwuje

- Persony nie zapisują poza swoim zasięgiem. Odmowa zapisu to norma działania, nie usterka.
- Nic ważnego nie zmienia się automatycznie: zmiana reguł albo struktury wiedzy najpierw trafia jako propozycja do `inbox/`.
- Każda zmiana zostawia ślad w git: co, kiedy, w jakim kontekście.
- Materiały pracodawcy lub klientów nigdy nie wchodzą do vaulta (`system/artifacts/Granica_Pracy_Zawodowej.md`).
- Wartości sekretów nigdy nie trafiają do plików (`system/artifacts/Rejestr_Sekretow.md`).

## Język

Szablon jest po polsku: nazwy katalogów, person i procedur również. Tłumaczenie na inny język to przeróbka całości, nie pojedynczych plików.

## Licencja

MIT. Możesz używać, zmieniać i rozpowszechniać, także komercyjnie, z zachowaniem noty autorskiej. Treść licencji w pliku `LICENSE`.

## Autor

Kacper Śliwiński, [kacpersliwinski.com](https://kacpersliwinski.com). Pytania i uwagi: issues w tym repozytorium albo e-mail ze strony.
