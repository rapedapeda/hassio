# Verlichting - Hal

Deze README beschrijft de setup stappen voor automatische verlichting in de hal. Volg de stappen om Zigbee2MQTT devices te configureren en Home Assistant groups aan te maken.

## Automatisch aangemaakt door package

**Helpers:**
- `input_boolean.verlichting_hal_auto` - Auto modus schakelaar
- `input_number.hal_aanwezigheid_timeout` - Timeout (default: 1 min)
- `input_number.hal_illuminance_threshold` - Lux drempel (default: 10 lx)

## Handmatig aanmaken

### Zigbee2MQTT

Zorg dat de volgende devices correct benoemd zijn:

| Device Type | Friendly Name | Resulterende Entity |
|-------------|---------------|---------------------|
| Multisensor (PIR + lux) | `hal_voorkant` | `binary_sensor.hal_voorkant`<br>`sensor.hal_voorkant_illuminance` |
| Deur sensor | `hal_voordeur` | `binary_sensor.hal_voordeur` |
| Light(s) | `hal` | `light.hal` |

### Home Assistant

#### 1. Sensor Group (Illuminance)

**Settings > Devices & Services > Helpers > Create Helper > Group**

- **Type:** Sensor group
- **Name:** Hal illuminance
- **Entity ID:** `sensor.hal_illuminance`
- **Members:**
  - `sensor.hal_voorkant_illuminance`
- **Type of group:** Last sensor

#### 2. Binary Sensor Group (Occupancy)

**Settings > Devices & Services > Helpers > Create Helper > Group**

- **Type:** Binary sensor group
- **Name:** Hal occupancy
- **Entity ID:** `binary_sensor.hal_occupancy`
- **Members:**
  - `binary_sensor.hal_voorkant`
  - `binary_sensor.hal_voordeur`
- **All entities:** OFF

## Controle

Na setup moeten deze entities bestaan:
- ✓ `sensor.hal_illuminance` (sensor group)
- ✓ `binary_sensor.hal_occupancy` (binary sensor group)
- ✓ `light.hal`
- ✓ `input_boolean.verlichting_hal_auto`
- ✓ `input_number.hal_aanwezigheid_timeout`
- ✓ `input_number.hal_illuminance_threshold`
