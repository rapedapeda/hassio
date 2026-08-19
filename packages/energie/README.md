# Energie Package

Automatisch energiebeheer op basis van dynamische stroomprijzen en batterijstatus.
Doel: maximaal zelfverbruik + laden bij goedkope stroom, ontladen bij dure stroom.

## Werking

De batterijbeslisser draait elk uur (bij prijsupdate) en kiest een modus op basis van prioriteit:

| Prioriteit | Conditie | Batterijmodus |
|-----------|----------|---------------|
| 1 | `energie_auto = off` | Default mode (niet ingrijpen) |
| 2 | Prijs duur + SOC > min + 5% | Force discharge |
| 3 | 's Nachts + SOC > 60% + morgen ≥ 3.8 kWh zon | Discharge only (ruimte maken) |
| 4 | Prijs goedkoop + ruimte in batterij + zon vandaag vult niet | Force charge |
| Standaard | Geen actie vereist | Default mode |

**Goedkoop/duur** is relatief: op basis van de positie in de dagrangschikking (EnergyZero
`hours_priced_equal_or_lower`). Instelbaar via `energie_laden_uren` en `energie_ontladen_uren`.

**Laden van net** triggert niet als Forecast.Solar aangeeft dat de resterende opwek vandaag
de vrije batterijruimte al vult — in dat geval is grid-laden verspilling.

## Vereiste integraties

| Integratie | Doel | Status |
|-----------|------|--------|
| [EnergyZero](https://github.com/bajansen/home-assistant-energyzero) | Dynamische stroomprijzen | ✓ Actief |
| [Home Battery Simulation](https://github.com/selfhacked-nl/ha-home-battery-simulation) | Marstek Venus E simulatie | ✓ Actief |
| Forecast.Solar | Zonne-energieforecast | ✓ Actief |

## Marstek batterijmodi

`select.marstek_venus_e_5_12kwh_3nd_gen_battery_mode` opties:

| Optie | Gebruik |
|-------|---------|
| `Default mode` | Normaal: laden van zon, ontladen naar huis |
| `Force charge` | Laden van net (goedkope uren) |
| `Force discharge` | Ontladen naar huis (dure uren) |
| `Charge only` | Alleen laden, niet ontladen (bewaar voor zon) |
| `Discharge only` | Alleen ontladen, niet laden (leegtrekken voor zon) |
| `Pause battery` | Batterij volledig inactief |

## Bestanden

| Bestand | Inhoud |
|---------|--------|
| `helpers.yaml` | `input_boolean.energie_auto` + drempelwaarden uren |
| `sensoren.yaml` | Binary sensors voor prijs, solar en beslissing |
| `batterij.yaml` | Centrale automation |
