# Verlichting - Woonkamer

Deze README beschrijft de setup stappen voor automatische verlichting in de woonkamer. Volg de stappen om Zigbee2MQTT devices te configureren en Home Assistant groups aan te maken.

## Automatisch aangemaakt door package

**Helpers:**
- `input_boolean.verlichting_woonkamer_auto` - Auto modus schakelaar
- `input_number.woonkamer_aanwezigheid_timeout` - Timeout (default: 10 min)
- `input_number.woonkamer_illuminance_threshold` - Lux drempel (default: 20 lx)

**Template Sensors:**
- `binary_sensor.woonkamer_occupancy` - Combineert PIR (kan initiëren) en mmWave (kan alleen verlengen). Template ipv group vanwege complexe logica met `this.state` check voor mmWave.

## Handmatig aanmaken

### Zigbee2MQTT

Zorg dat de volgende devices correct benoemd zijn:

| Device Type | Friendly Name | Resulterende Entity |
|-------------|---------------|---------------------|
| Multisensor (PIR + lux) | `woonkamer_eettafel` | `binary_sensor.beweging_eetkamer_occupancy`<br>`sensor.woonkamer_eettafel_illuminance` |
| mmWave sensor | `woonkamer_mmwave` | `binary_sensor.beweging_woonkamer_mmwave` |
| Light(s) | `woonkamer` | `light.woonkamer` |

### Home Assistant

#### 1. Sensor Group (Illuminance)

**Settings > Devices & Services > Helpers > Create Helper > Group**

- **Type:** Sensor group
- **Name:** Woonkamer illuminance
- **Entity ID:** `sensor.woonkamer_illuminance`
- **Members:**
  - `sensor.woonkamer_eettafel_illuminance`
- **Type of group:** Last sensor

## Controle

Na setup moeten deze entities bestaan:
- ✓ `sensor.woonkamer_illuminance` (sensor group)
- ✓ `binary_sensor.woonkamer_occupancy` (template sensor, package)
- ✓ `light.woonkamer`
- ✓ `input_boolean.verlichting_woonkamer_auto`
- ✓ `input_number.woonkamer_aanwezigheid_timeout`
- ✓ `input_number.woonkamer_illuminance_threshold`
