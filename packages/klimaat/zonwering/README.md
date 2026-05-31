# Klimaat Package - Zonwering

Automatische zonwering op basis van weer, zonpositie en temperatuur.

## Algemeen

### Helpers

**helpers.yaml**
- `input_number.zonwering_buitentemperatuur_threshold` - Min verwachte buitentemperatuur voor zonwering
- `input_number.zonwering_irradiance_threshold` - Min instraling (W/m², DNI-proxy, richtwaarde 900)
- `input_number.zonwering_wind_threshold` - Max windsnelheid (km/h)

### Sensoren

**weer.yaml**
- `sensor.zonwering_instraling` - DNI-benadering: GHI gecorrigeerd voor zonhoogte (`GHI / max(sin(elevatie), sin(10°))`)
  - Geeft betere indicatie van directe straling op verticale vlakken dan GHI
  - Floor op sin(10°): voorkomt explosieve waarden bij lage elevatie (deling door bijna-nul). Onder 10° is de zon te laag om relevant te zijn voor verticale vlakken
- `binary_sensor.zonwering_nodig` - Is zonwering nodig? (zomermaand maart-oktober + instraling >= threshold)
  - Delay on/off: 5 minuten
- `binary_sensor.zonwering_veilig` - Is het weer veilig? (geen regen + wind onder threshold)
  - Delay on: 10 minuten, delay off: 0 (meteen reageren bij onveilig weer)

### Automations

**handmatige_bediening.yaml**
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
- `binary_sensor.zonwering_woonkamer_temperatuur` - Is de temperatuur hoog genoeg?
  - Buitentemperatuur (max knmi/weerstation) >= threshold OF binnentemperatuur >= 21°C
  - Delay on: 5 minuten, delay off: 30 minuten (voorkomt pendelen)
- `automation.zonwering_woonkamer_positie` - Automatische positiecontrole
  - Triggers op: positie sensor, zonwering_nodig, zonwering_veilig, temperatuur sensor, auto mode aan
  - **VEILIGHEID:** Bij onveilig weer ALTIJD retracteren (ook zonder auto mode)
  - Bij auto mode: volg berekende positie als nodig + veilig + temperatuur OK, anders scherm in

**Cover entity:** `cover.woonkamer`

### Kantoor (Rolluik)

**kantoor.yaml**
- `input_boolean.zonwering_kantoor_auto` - Auto mode toggle
- `sensor.zonwering_kantoor_positie` - Berekende positie op basis van:
  - Zon op voorkant: azimuth 227-360°, elevation > 1°
  - Zonwering nodig: 30% (gedeeltelijk dicht)
  - Anders: 100% (open)
- `binary_sensor.zonwering_kantoor_temperatuur` - Is de temperatuur hoog genoeg?
  - Buitentemperatuur (max knmi/weerstation) >= threshold OF binnentemperatuur >= 20°C
  - Delay on: 5 minuten, delay off: 30 minuten (voorkomt pendelen)
- `automation.zonwering_kantoor_positie` - Automatische positiecontrole
  - Triggers op: positie sensor, zonwering_nodig, temperatuur sensor, auto mode aan
  - Bij auto mode: volg berekende positie als nodig + temperatuur OK, anders rolluik open
  - Geen veiligheidscheck (rolluiken zijn windbestendig)

**Cover entity:** `cover.kantoor`

## Nieuwe Kamer Toevoegen

1. Maak `{kamer}.yaml` met:
   - `input_boolean.zonwering_{kamer}_auto`
   - `sensor.zonwering_{kamer}_positie`
   - `binary_sensor.zonwering_{kamer}_temperatuur`
   - `automation.zonwering_{kamer}_positie`
2. Hernoem cover entity naar `cover.{kamer}`
3. Voeg cover toe aan `handmatige_bediening.yaml` trigger
4. Voeg auto boolean toe aan `zonwering_auto_reset` action
