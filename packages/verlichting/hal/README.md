# Verlichting - Hal

## Helpers
- `input_boolean.verlichting_hal_auto` - Auto modus schakelaar
- `input_number.hal_aanwezigheid_timeout` - Timeout (1 min)
- `input_number.hal_illuminance_threshold` - Lux drempel (10 lx)

## GUI Groups Vereist
- `binary_sensor.hal_occupancy` - Occupancy group met:
  - `binary_sensor.hal_occupancy` (PIR, Zigbee2MQTT device: `hal`)
  - `binary_sensor.voordeur`

## Sensoren Vereist
- `sensor.hal_illuminance` (Zigbee2MQTT device: `hal`)
- `light.hal`
