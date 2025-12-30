# Verlichting - Woonkamer

## Helpers
- `input_boolean.verlichting_woonkamer_auto` - Auto modus schakelaar
- `input_number.woonkamer_aanwezigheid_timeout` - Timeout (10 min)
- `input_number.woonkamer_illuminance_threshold` - Lux drempel (20 lx)

## Template Sensors
- `sensor.woonkamer_illuminance` - Wijst naar `sensor.woonkamer_eettafel_illuminance` (primary sensor, centrale positie)

## GUI Groups Vereist
- `binary_sensor.woonkamer_occupancy` - Occupancy group met:
  - Alle PIR sensoren in woonkamer
- `binary_sensor.woonkamer_occupancy_verlengen` - Voor timeout met:
  - Alle PIR sensoren
  - `binary_sensor.beweging_woonkamer_mmwave`

## Sensoren Vereist
- `sensor.woonkamer_eettafel_illuminance` (Zigbee2MQTT device: `woonkamer_eettafel`)
- PIR sensoren (in occupancy group)
- `binary_sensor.beweging_woonkamer_mmwave`
- `light.woonkamer`
