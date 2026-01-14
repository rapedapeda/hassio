# Klimaat Package - Ventilatie

Automatische ventilatie op basis van luchtkwaliteit, temperatuur en aanwezigheid.

## Functies

### Functie 1: Away modus
**Ventilatie uit als niemand thuis**
- ALTIJD actief (ook zonder auto mode)
- Bij `alarm_control_panel.huis` = armed_away → fan uit
- Anders → fan aan (percentage bepaald door andere functies)

### Functie 2: Boost luchtkwaliteit
**Verhoogde ventilatie bij slechte luchtkwaliteit**
- Actief als `ventilatie_auto` = on
- CO2 > 1000 ppm OF humidity badkamer te hoog → 66%
- Anders → 33%

### Functie 3: Nachtkoeling
**Extra ventilatie op warme zomernachten**
- Actief als `ventilatie_auto` = on
- Bovenverdieping > 21°C EN bypass aan (buiten kouder) → 100%
- Anders → 33%

### Functie 4: Auto reset
**Dagelijkse reset van auto mode**
- Elke ochtend om 6:00 → `ventilatie_auto` = on

## Sensor Groups (aanmaken via GUI)

**Settings → Devices & Services → Helpers → Create Helper → Group (Sensor)**

1. **`sensor.co2_sensoren`** (Aggregation: Max)
   - Alle CO2 sensoren toevoegen

2. **`sensor.temperatuur_huis`** (Aggregation: Mean)
   - Alle temperatuursensoren toevoegen

3. **`sensor.temperatuur_bovenverdieping`** (Aggregation: Max)
   - Slaapkamer, kinderkamer, overloopeerste toevoegen

4. **`binary_sensor.ventilatie_nachtkoeling_nodig`** (Threshold sensor)
   - entity_id voor de threshold: sensor.temperatuur_bovenverdieping

## Bestanden

**fan.yaml** - Template fan entity `fan.wtw`
**helpers.yaml** - `input_boolean.ventilatie_auto` + cooling threshold
**sensoren.yaml** - Binary sensors (CO2, humidity, bypass, nachtkoeling temp)
**away_modus.yaml** - Functie 1
**boost_luchtkwaliteit.yaml** - Functie 2 (gecombineerd aan/uit)
**nachtkoeling.yaml** - Functie 3
**auto_reset.yaml** - Functie 4

## Handmatig Mode

`ventilatie_auto` = off → Handmatige controle via:
- `fan.wtw` entity percentage
- Fysieke knoppen bij WTW zelf
- Away modus blijft actief
