# Klimaat Package - Verwarming

Automatische verwarming op basis van schedules, aanwezigheid en beweging.

## Setup

### Automatisch aangemaakt (via package)

**helpers.yaml**
- `input_boolean.verwarming_woonkamer_auto` - Auto mode woonkamer
- `input_boolean.verwarming_hal_auto` - Auto mode hal
- `input_boolean.verwarming_kantoor_auto` - Auto mode kantoor

### Handmatig aanmaken (via GUI)

#### 1. Schedule Helpers

**Settings → Devices & Services → Helpers → Create Helper → Schedule**

Voor elke kamer met schedule-based verwarming:

1. Maak `schedule.verwarming_{kamer}`
2. Stel tijdsblokken in (ma-zo)
3. Voeg custom data toe per block:
   ```yaml
   temperature: 20
   ```

**Huidige setup:**
- `schedule.verwarming_woonkamer` (ma-vr 17:00-21:30, za-zo 07:30-21:30, temp: 20)
- `schedule.verwarming_hal` (zelfde tijden als woonkamer, temp: 18)

#### 2. Labels

**Settings → Devices & Services → Entities → {entity} → Settings → Labels**

Label de volgende entities met **"Verwarming"**:
- `climate.woonkamer`
- `climate.hal`
- `climate.kantoor`
- `schedule.verwarming_woonkamer`
- `schedule.verwarming_hal`

## Functies

### Functie 1: Schema
**Schedule-based verwarming per kamer**
- Actief als `verwarming_{kamer}_auto` = on
- Volgt `schedule.verwarming_{kamer}` temperatuur
- Handmatige override blijft actief tot volgende schedule change
- Alleen triggers op schedule changes (niet op climate changes)

### Functie 2: Occupancy based heating
**Verwarming bij beweging voor kamers zonder schedule**
- Actief als `verwarming_{kamer}_auto` = on
- Beweging detected → 19°C
- Geen beweging 30 min → uit
- Gebruikt `binary_sensor.{kamer}_beweging`

### Functie 3: Away override
**Eco mode bij afwezigheid**
- Na 1u `armed_away` + actieve schedule → -2°C (eco mode)
- Na 4u `armed_away` → alle verwarming uit
- Bij thuiskomst → herstel schedule temperaturen

### Functie 4: Slim aan
**Automatische verwarming op niet-schedule dagen**
- Check om 08:00 of iemand thuis (`disarmed`)
- Als schedule niet actief → zet aan op schedule temperatuur
- Haalt temperatuur uit eerste block van schedule (via `schedule.get_schedule`)

### Functie 5: Dagelijkse reset
**Robuuste fallback voor sensor failures**
- Elke nacht om 03:00
- Zet verwarming uit als schedule niet actief
- Kantoor altijd uit (geen schedule)

## Bestanden

**helpers.yaml** - Auto mode toggles per kamer
**schema.yaml** - Functie 1 (schedule-based)
**occupancy_based_heating.yaml** - Functie 2 (beweging)
**away_override.yaml** - Functie 3 (eco + uit)
**slim_aan.yaml** - Functie 4 (08:00 check)
**dagelijkse_reset.yaml** - Functie 5 (03:00 fallback)

## Handmatig Mode

`verwarming_{kamer}_auto` = off → Handmatige controle via:
- `climate.{kamer}` entity (temperature + hvac_mode)
- Fysieke thermostaat
- Lovelace climate card

Handmatige changes tijdens auto mode blijven actief tot volgende schedule change.

## Nieuwe Kamer Toevoegen

### Met schedule:
1. Maak `schedule.verwarming_{kamer}` via GUI (zie Setup)
2. Label schedule met "Verwarming"
3. Voeg `input_boolean.verwarming_{kamer}_auto` toe aan helpers.yaml
4. Label `climate.{kamer}` met "Verwarming"
5. Reload package
6. Klaar! Alle automations gebruiken dynamische entity discovery

### Zonder schedule (occupancy-based):
1. Voeg `input_boolean.verwarming_{kamer}_auto` toe aan helpers.yaml
2. Label `climate.{kamer}` met "Verwarming"
3. Zorg dat `binary_sensor.{kamer}_beweging` bestaat
4. Reload package
5. Klaar! occupancy_based_heating.yaml pakt automatisch op
