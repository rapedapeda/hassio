# Klimaat Package - Ventilatie

Automatische ventilatie op basis van luchtkwaliteit, temperatuur en aanwezigheid.

## Werking

Één centrale automation evalueert bij elke relevante state change de ventilatiestand op basis van prioriteit:

| Prioriteit | Conditie | Stand | Auto vereist |
|-----------|----------|-------|-------------|
| 1 | Niemand thuis (`alarm = armed_away`) | Uit | Nee |
| 2 | Nachtkoeling nodig + bypass open | 100% | Ja |
| 3 | Luchtkwaliteit slecht (CO₂ of vochtigheid) | 66% | Ja |
| 4 | Anders (basisstand, ook bij thuiskomst) | 33% | Nee |

`ventilatie_auto = off` schakelt de automatische aanpassing uit (prioriteit 2 en 3 vallen weg), maar de basisstand van 33% blijft actief. Away modus blijft altijd actief.

## Sensor Groups (aanmaken via GUI)

**Settings → Devices & Services → Helpers → Create Helper → Group (Sensor)**

1. **`sensor.co2_sensoren`** (Aggregation: Max)
   - Alle CO₂-sensoren toevoegen

2. **`sensor.temperatuur_huis`** (Aggregation: Mean)
   - Alle temperatuursensoren toevoegen

3. **`sensor.temperatuur_bovenverdieping`** (Aggregation: Max)
   - Slaapkamer, kinderkamer, overloop toevoegen

4. **`binary_sensor.ventilatie_nachtkoeling_nodig`** (Threshold sensor)
   - Entity: `sensor.temperatuur_bovenverdieping`
   - Drempel instellen via `input_number.ventilatie_cooling_threshold` (standaard 21°C)

5. **`binary_sensor.ventilatie_luchtkwaliteit_slecht`** (Binary sensor group, OR logica)
   - `binary_sensor.ventilatie_co2` toevoegen
   - `binary_sensor.ventilatie_humidity` toevoegen

## Bestanden

| Bestand | Inhoud |
|---------|--------|
| `fan.yaml` | Template fan `fan.wtw` + `script.set_ventilatie_stand` |
| `helpers.yaml` | `input_boolean.ventilatie_auto` + cooling threshold |
| `sensoren.yaml` | Binary sensors (CO₂, vochtigheid, bypass) |
| `ventilatie.yaml` | Centrale automation (prioriteit 1–4) |
| `auto_reset.yaml` | Dagelijkse reset van auto mode om 06:00 |

## Handmatige modus

`ventilatie_auto = off` → prioriteit 2 en 3 zijn niet actief. De fan staat op 33% tenzij handmatig aangepast via:
- `fan.wtw` entity percentage
- Fysieke knoppen bij de WTW
- Away modus blijft actief
