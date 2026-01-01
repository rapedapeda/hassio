# Verlichting - Keuken

Deze README beschrijft de setup stappen voor automatische verlichting in de keuken. Volg de stappen om Zigbee2MQTT devices te configureren en Home Assistant groups aan te maken.

## Automatisch aangemaakt door package

**Helpers:**
- `input_boolean.verlichting_keuken_auto` - Auto modus schakelaar
- `input_number.keuken_aanwezigheid_timeout` - Timeout (default: 10 min)
- `input_number.keuken_illuminance_threshold` - Lux drempel (default: 20 lx)

## Handmatig aanmaken

### Zigbee2MQTT

Zorg dat de volgende devices correct benoemd zijn:

| Device Type | Friendly Name | Resulterende Entity |
|-------------|---------------|---------------------|
| Multisensor (PIR + lux) | `keuken_voorkant` | `binary_sensor.keuken_voorkant`<br>`sensor.keuken_voorkant_illuminance` |
| Light(s) | `keuken` | `light.keuken` |

### Home Assistant

#### 1. Sensor Group (Illuminance)

**Settings > Devices & Services > Helpers > Create Helper > Group**

- **Type:** Sensor group
- **Name:** Keuken illuminance
- **Entity ID:** `sensor.keuken_illuminance`
- **Members:**
  - `sensor.keuken_voorkant_illuminance`
- **Type of group:** Last sensor

#### 2. Binary Sensor Group (Occupancy)

**Settings > Devices & Services > Helpers > Create Helper > Group**

- **Type:** Binary sensor group
- **Name:** Keuken occupancy
- **Entity ID:** `binary_sensor.keuken_occupancy`
- **Members:**
  - `binary_sensor.keuken_voorkant`
- **All entities:** OFF

## Controle

Na setup moeten deze entities bestaan:
- ✓ `sensor.keuken_illuminance` (sensor group)
- ✓ `binary_sensor.keuken_occupancy` (binary sensor group)
- ✓ `light.keuken`
- ✓ `input_boolean.verlichting_keuken_auto`
- ✓ `input_number.keuken_aanwezigheid_timeout`
- ✓ `input_number.keuken_illuminance_threshold`
