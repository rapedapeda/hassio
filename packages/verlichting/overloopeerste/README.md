# Verlichting - Overloop Eerste

Deze README beschrijft de setup stappen voor automatische verlichting op de overloop eerste. Volg de stappen om Zigbee2MQTT devices te configureren en Home Assistant groups aan te maken.

## Automatisch aangemaakt door package

**Helpers:**
- `input_boolean.verlichting_overloopeerste_auto` - Auto modus schakelaar
- `input_number.overloopeerste_aanwezigheid_timeout` - Timeout (default: 1 min)
- `input_number.overloopeerste_illuminance_threshold` - Lux drempel (default: 50 lx)

## Handmatig aanmaken

### Zigbee2MQTT

Zorg dat de volgende devices correct benoemd zijn:

| Device Type | Friendly Name | Resulterende Entity |
|-------------|---------------|---------------------|
| PIR/Multisensor(s) | `overloopeerste_*` | `binary_sensor.overloopeerste_*_occupancy`<br>`sensor.overloopeerste_*_illuminance` |
| Light(s) | `overloopeerste` | `light.overloopeerste` |

### Home Assistant

#### 1. Sensor Group (Illuminance)

**Settings > Devices & Services > Helpers > Create Helper > Group**

- **Type:** Sensor group
- **Name:** Overloop eerste illuminance
- **Entity ID:** `sensor.overloopeerste_illuminance`
- **Members:**
  - Alle illuminance sensoren van overloopeerste
- **Type of group:** Last sensor

#### 2. Binary Sensor Group (Occupancy)

**Settings > Devices & Services > Helpers > Create Helper > Group**

- **Type:** Binary sensor group
- **Name:** Overloop eerste occupancy
- **Entity ID:** `binary_sensor.overloopeerste_occupancy`
- **Members:**
  - Alle occupancy/motion sensoren van overloopeerste
- **All entities:** OFF

## Controle

Na setup moeten deze entities bestaan:
- ✓ `sensor.overloopeerste_illuminance` (sensor group)
- ✓ `binary_sensor.overloopeerste_occupancy` (binary sensor group)
- ✓ `light.overloopeerste`
- ✓ `input_boolean.verlichting_overloopeerste_auto`
- ✓ `input_number.overloopeerste_aanwezigheid_timeout`
- ✓ `input_number.overloopeerste_illuminance_threshold`
