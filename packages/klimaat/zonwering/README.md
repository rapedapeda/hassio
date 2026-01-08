# Klimaat Package - Zonwering

Automatische zonwering op basis van weer, zonpositie en binnentemperatuur.

## Algemeen

### Helpers

**helpers.yaml**
- `input_number.zonwering_buitentemperatuur_threshold` - Min buitentemperatuur voor zonwering
- `input_number.zonwering_binnentemperatuur_threshold` - Min binnentemperatuur per kamer
- `input_number.zonwering_irradiance_threshold` - Min zonnestraling (W/m²)
- `input_number.zonwering_wind_threshold` - Max windsnelheid (km/h)

### Sensoren

**weer.yaml**
- `binary_sensor.zonwering_nodig` - Is zonwering nodig? (zomermaand + buitentemp + irradiance)
  - Delay on/off: 5 minuten
- `binary_sensor.zonwering_veilig` - Is het weer veilig? (geen regen + wind onder threshold)
  - Delay on: 10 minuten, delay off: 0 (meteen reageren bij onveilig weer)

### Automations

**handmatige_override.yaml**
- `automation.zonwering_handmatig_override` - Detecteert handmatige bediening, schakelt auto mode uit
- `automation.zonwering_auto_reset` - Reset alle auto modes elke avond om 22:00

## Per Kamer

### Woonkamer (Zonnescherm)

**woonkamer.yaml**
- `input_boolean.zonwering_woonkamer_auto` - Auto mode toggle
- `sensor.zonwering_woonkamer_positie` - Berekende positie (0-100%) op basis van:
  - Zonhoogte en azimuth (63-200°)
  - Schermafmetingen (200cm hoog, 240cm max lengte)
  - Schermorientatie (123°)
  - Windsnelheid (max 40% bij harde wind)
- `automation.zonwering_woonkamer_positie` - Automatische positiecontrole
  - **VEILIGHEID:** Bij onveilig weer ALTIJD retracteren (ook zonder auto mode)
  - Bij auto mode: volg berekende positie als nodig + veilig + binnentemp OK

**Cover entity:** `cover.woonkamer`

### Kantoor (Rolluik)

**kantoor.yaml**
- `input_boolean.zonwering_kantoor_auto` - Auto mode toggle
- `sensor.zonwering_kantoor_positie` - Berekende positie op basis van:
  - Zon op voorkant: azimuth 227-293°, elevation > 1°
  - Zonwering nodig: 30% (gedeeltelijk dicht)
  - Anders: 100% (open)
- `automation.zonwering_kantoor_positie` - Automatische positiecontrole
  - Bij auto mode: volg berekende positie als nodig + binnentemp OK
  - Geen veiligheidscheck (rolluiken zijn windbestendig)

**Cover entity:** `cover.kantoor`

## Nieuwe Kamer Toevoegen

1. Maak `{kamer}.yaml` met:
   - `input_boolean.zonwering_{kamer}_auto`
   - `sensor.zonwering_{kamer}_positie`
   - `automation.zonwering_{kamer}_positie`
2. Hernoem cover entity naar `cover.{kamer}`
3. Voeg cover toe aan `handmatige_override.yaml` trigger
4. Voeg auto boolean toe aan `zonwering_auto_reset` action
