# Prototyp grafu infrastruktury energetycznej

Pierwszy etap: kontrolowany opis tekstowy -> parser -> walidacja Pydantic -> graf JSON. Nie wymaga jeszcze LLM ani Neo4j. Przykład jest syntetyczny i nie przedstawia fragmentu pandapower case14.

## Uruchomienie

W PowerShell, w katalogu `prototyp`:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m energy_graph przyklad.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Obsługiwane zdania:

```text
Szyna B1 ma napięcie 110 kV.
Szyna B1 jest połączona linią L1 z szyną B2 o długości 10 km.
Do szyny B2 podłączono odbiór O1 o mocy 20 MW.
```

Szyny muszą być zdefiniowane osobnymi zdaniami. Parser odrzuca nieznane zdania, duplikaty identyfikatorów i relacje do nieistniejących szyn. Właściwości liczbowe mają jednostki w nazwach pól (`vn_kv`, `length_km`, `p_mw`).

## Kolejny etap

Podłączyć Neo4j: zapisywać zweryfikowane węzły i relacje z `as_property_graph()` za pomocą parametryzowanych zapytań Cypher. Następnie dodać małe API i formularz. Docelowy moduł LLM zastąpi parser, zachowując ten sam schemat grafu.
