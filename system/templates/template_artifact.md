---
type: artifact
artifact_type: normative        # normative (zasady) | registry (tabela prowadzona) | profile (kontekst osoby) | policy (granica)
title: Nazwa_Artefaktu
owner_head: "[[ops]]"            # dział-właściciel: knowledge | ops | <Twój dział>
used_by:
  - "[[asystent]]"           # persony, które czytają ten artefakt — lustro kolumny Odczyt w access_map (lint R2)
inject: on_reference            # always (tylko dla 1–2 artefaktów w systemie — koszt kontekstu) | on_reference | never
scope: "Jedno zdanie: co ten dokument rozstrzyga"
authority: binding
review_every: 90d               # 30d | 90d | 180d | 365d
agent_access: true              # false = niewidoczny dla WSZYSTKICH person (dane wrażliwe)
version: 1.0
created: RRRR-MM-DD
updated: RRRR-MM-DD
---
# Cel dokumentu
[1–2 zdania: co ten artefakt rozstrzyga i dla kogo jest wiążący.]

# Zasady wiążące
[Ponumerowana lista żelaznych reguł — to sekcja, której naruszenie = błąd agenta.
Numeracja celowo: agent może się odwołać "zgodnie z zasadą 3".]
1. ...
2. ...

# Kontekst i uzasadnienie
[Dlaczego te zasady są takie, jakie są — pomaga agentowi rozstrzygać
przypadki brzegowe w duchu dokumentu, nie tylko literalnie.]

# Przykłady zastosowania
## Dobrze
[konkretny przykład zgodny z zasadami]
## Źle
[antyprzykład + która zasada jest naruszona]

# Wyjątki i przypadki brzegowe
[Kiedy zasady można nagiąć i kto o tym decyduje — domyślnie: eskalacja do mnie.]

# Historia zmian
- RRRR-MM-DD (v1.0): [co i dlaczego zmieniono — każdy wpis: data (wersja): co + DLACZEGO]