# Verlichting - Kantoor

Deze README beschrijft de setup stappen voor automatische verlichting in het kantoor. Volg de stappen om Zigbee2MQTT devices te configureren en Home Assistant groups aan te maken.

## Automatisch aangemaakt door package

**Helpers:**
- `input_boolean.verlichting_kantoor_auto` - Auto modus schakelaar
- `input_number.kantoor_aanwezigheid_timeout` - Timeout (default: 10 min)
- `input_number.kantoor_illuminance_threshold` - Lux drempel (default: 35 lx)

## Handmatig aanmaken

### Zigbee2MQTT

Zorg dat de volgende devices correct benoemd zijn:

| Device Type | Friendly Name | Resulterende Entity |
|-------------|---------------|---------------------|
| Multisensor (PIR + lux) | `kantoor_multisensor` | `binary_sensor.kantoor_multisensor_occupancy`<br>`sensor.kantoor_multisensor_illuminance` |
| Light(s) | `kantoor` | `light.kantoor` |

### Home Assistant

#### 1. Sensor Group (Illuminance)

**Settings > Devices & Services > Helpers > Create Helper > Group**

- **Type:** Sensor group
- **Name:** Kantoor illuminance
- **Entity ID:** `sensor.kantoor_illuminance`
- **Members:**
  - `sensor.kantoor_multisensor_illuminance`
- **Type of group:** Last sensor

#### 2. Binary Sensor Group (Occupancy)

**Settings > Devices & Services > Helpers > Create Helper > Group**

- **Type:** Binary sensor group
- **Name:** Kantoor occupancy
- **Entity ID:** `binary_sensor.kantoor_occupancy`
- **Members:**
  - `binary_sensor.kantoor_multisensor_occupancy`
- **All entities:** OFF

## Controle

Na setup moeten deze entities bestaan:
- ✓ `sensor.kantoor_illuminance` (sensor group)
- ✓ `binary_sensor.kantoor_occupancy` (binary sensor group)
- ✓ `light.kantoor`
- ✓ `input_boolean.verlichting_kantoor_auto`
- ✓ `input_number.kantoor_aanwezigheid_timeout`
- ✓ `input_number.kantoor_illuminance_threshold`
