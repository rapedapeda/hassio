# Energie Package

Automatisch energiebeheer op basis van dynamische stroomprijzen en batterijstatus.
Doel: maximaal zelfverbruik + laden bij goedkope stroom, ontladen bij dure stroom.

## Werking

De batterijbeslisser draait elk uur (bij prijsupdate) en kiest een modus op basis van prioriteit:

| Prioriteit | Conditie | Batterijmodus |
|-----------|----------|---------------|
| 1 | `energie_auto = off` | Automatic (niet ingrijpen) |
| 2 | Prijs duur + SOC > min + 5% | Force Discharge |
| 3 | Prijs goedkoop + SOC < max - 5% | Force Charge |
| Standaard | Geen extreme prijs | Automatic |

**Goedkoop/duur** is relatief: op basis van de positie in de dagrangschikking (EnergyZero
`hours_priced_equal_or_lower`). Instelbaar via `energie_laden_uren` en `energie_ontladen_uren`.

## Vereiste integraties

| Integratie | Doel | Status |
|-----------|------|--------|
| [EnergyZero](https://github.com/bajansen/home-assistant-energyzero) | Dynamische stroomprijzen | ✓ Actief |
| [Home Battery Simulation](https://github.com/selfhacked-nl/ha-home-battery-simulation) | Marstek Venus E simulatie | ✓ Actief |
| Solcast | Zonne-energieforecast | TODO |

## TODO: Solcast

Na installatie van Solcast uitbreiden met:
- `binary_sensor.energie_laden_zinvol`: niet laden van net als zon verwacht de batterij vult
- `binary_sensor.energie_ontladen_zinvol`: ruimer ontladen als zon morgen de batterij aanvult
- Nachtelijke pre-discharge: SOC verlagen vóór zonsopgang als solar forecast > batterijcapaciteit

Solcast entiteiten (na installatie):
- `sensor.solcast_pv_forecast_forecast_today` (kWh)
- `sensor.solcast_pv_forecast_forecast_tomorrow` (kWh)

## Marstek batterijmodus

Verifieer de exacte optienamen via **Ontwikkeltools → Staten**:
`select.marstek_venus_e_5_12kwh_3nd_gen_battery_mode`

Huidige aannames: `Automatic`, `Force Charge`, `Force Discharge`

## Bestanden

| Bestand | Inhoud |
|---------|--------|
| `helpers.yaml` | `input_boolean.energie_auto` + drempelwaarden uren |
| `sensoren.yaml` | Binary sensors voor prijs en beslissing |
| `batterij.yaml` | Centrale automation |
