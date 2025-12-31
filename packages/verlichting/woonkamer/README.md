# Verlichting - Woonkamer

## Helpers
- `input_boolean.verlichting_woonkamer_auto` - Auto modus schakelaar
- `input_number.woonkamer_aanwezigheid_timeout` - Timeout (10 min)
- `input_number.woonkamer_illuminance_threshold` - Lux drempel (20 lx)

## Template Sensors
- `binary_sensor.woonkamer_occupancy` - Combineert PIR (initiëren) en mmWave (verlengen)
- `sensor.woonkamer_illuminance` - Wijst naar `sensor.woonkamer_eettafel_illuminance` (via GUI)

## Sensoren Vereist
- `binary_sensor.beweging_eetkamer_occupancy` (PIR, Zigbee2MQTT)
- `binary_sensor.beweging_woonkamer_mmwave` (mmWave sensor)
- `sensor.woonkamer_eettafel_illuminance` (Zigbee2MQTT device: `woonkamer_eettafel`)
- `light.woonkamer`
