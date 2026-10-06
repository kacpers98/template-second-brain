---
type: system
title: "Kokpit operatora"
cssclasses:
  - kokpit
---
# Kokpit

> Pierwszy raz tutaj? Otwórz [[START_TUTAJ]]. Jeśli tabele poniżej wyglądają jak surowy kod — brakuje wtyczki Dataview (START_TUTAJ, krok 2).

## 🧭 Wdrożenie
*Sekcja żyje do etapu 7. Potem możesz ją usunąć — albo zostawić jako przypomnienie, skąd system się wziął.*
```dataview
TABLE WITHOUT ID file.link AS "Stan wdrożenia", etap AS "Etap", dateformat(file.mtime, "dd.MM HH:mm") AS "Ostatnia zmiana"
FROM "outputs/wdrozenie"
WHERE file.name = "STAN_WDROZENIA"
```

## 📥 Inbox — czeka na Twoją akceptację
*Pusta tabela = czysty stan umysłu. Najdłużej czekające na górze. Akceptujesz słowami w sesji Claude Code: „akceptuję <nazwa>".*
```dataview
TABLE WITHOUT ID file.link AS "Propozycja", dateformat(file.mtime, "dd.MM HH:mm") AS "Czeka od"
FROM "inbox"
WHERE file.name != ".gitkeep" AND !contains(file.path, "archive")
SORT file.mtime ASC
```

## 📤 Świeże wyniki (7 dni)
```dataview
TABLE WITHOUT ID file.link AS "Wynik", agent AS "Persona", dateformat(file.mtime, "dd.MM HH:mm") AS "Kiedy"
FROM "outputs"
WHERE file.mtime >= date(today) - dur(7 days) AND file.name != "log" AND file.name != "STAN_WDROZENIA" AND !startswith(file.name, "brief_ostatni")
SORT file.mtime DESC
LIMIT 15
```

## ✅ Zadania i kalendarz
*Zadania jednorazowe żyją POZA vaultem — na Twojej liście zadań ({{UZUPEŁNIJ: nazwa narzędzia, np. Google Tasks / Todoist / kartka}}). Do vaulta wracają wyłącznie jako projekcje w briefach (`outputs/ops/`). Rytmy systemu: [[system/artifacts/Rejestr_Cyklow|Rejestr Cyklów]].*

## 📋 Puls systemu
*Świeża data logu routera = system jest używany. Stęchlizna dłuższa niż tydzień = wróć do pytania „po co mi to" (Lekcje_Poprzednika, miernik „używanie").*
```dataview
TABLE WITHOUT ID file.link AS "Log routera", entry_count AS "Zleceń", dateformat(file.mtime, "dd.MM HH:mm") AS "Ostatnia zmiana"
FROM "outputs/router"
WHERE file.name = "log"
```

## 🔗 Szybkie skoki
**Rytmy:** [[outputs/ops/brief_ostatni_dzienny|Brief dzienny]] · [[outputs/ops/brief_ostatni_tygodniowy|Brief tygodniowy]] *(pliki powstaną przy pierwszym briefie)*
**Normy:** [[system/artifacts/Rejestr_Cyklow|Cykle]] · [[system/artifacts/Profil_Wlasciciela|Profil Właściciela]] · [[system/artifacts/Lista_Zrodel_Zwiadowcy|Źródła]] · [[system/access_map|Księga dostępów]] · [[system/sciaga_wywolan|Ściąga wywołań]]
**Wdrożenie:** [[system/artifacts/Lekcje_Poprzednika|Lekcje poprzednika]] · [[outputs/wdrozenie/STAN_WDROZENIA|Stan wdrożenia]]
**Ewidencja:** [[outputs/router/log|Log routera]] · [[outputs/knowledge/log|Log wiedzy]]
