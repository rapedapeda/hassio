# Naamgevingsconventies

## Zigbee2MQTT Devices

### Regel: `{kamer}` of `{kamer}_{locatie}`

**Standaard (1 device per kamer):**
```
Device naam: hal
Entities: sensor.hal_illuminance
          binary_sensor.hal_occupancy
          sensor.hal_temperature
          sensor.hal_battery
```

**Bij meerdere devices per kamer:**
```
Device namen: woonkamer_raam
              woonkamer_haldeur

Entities: sensor.woonkamer_raam_illuminance
          binary_sensor.woonkamer_raam_occupancy
          sensor.woonkamer_haldeur_illuminance
          binary_sensor.woonkamer_haldeur_occupancy

Group: binary_sensor.woonkamer_occupancy (combinatie van alle occupancy sensors)
```

**Locatie suffix alleen bij meerdere devices van hetzelfde type in dezelfde kamer.**

---

## Home Assistant Entities

### Lights

**Standaard:**
```
light.{kamer}
```

**Voorbeelden:**
```
light.hal
light.woonkamer
light.slaapkamer
```

**Bij meerdere losse lights:** Maak een light group `light.{kamer}` via GUI.

---

### Binary Sensor Groups

**Standaard:**
```
binary_sensor.{kamer}_beweging      # Occupancy group (PIR + deur sensoren)
binary_sensor.{kamer}_lichtstatus   # Template: lux vs threshold
```

**Bij PIR + mmWave:**
```
binary_sensor.{kamer}_beweging          # Alleen PIR (kan licht initiëren)
binary_sensor.{kamer}_beweging_verlengen # PIR + mmWave (voor timeout)
```

---

### Package Helpers

**Formaat:** `{domein}_{kamer}_{functie}`

**Voorbeelden:**
```
input_boolean.verlichting_hal_auto
input_number.hal_aanwezigheid_timeout
input_number.hal_lux_threshold
```

---

## Uitzonderingen

### Deur/Raam sensoren
Naam IS de locatie, geen kamer prefix nodig:
```
binary_sensor.voordeur
binary_sensor.achterdeur
binary_sensor.raam_woonkamer  (alleen als onduidelijk welk raam)
```

### Niet-kamer-specifieke devices
```
sensor.buiten_temperature
sensor.zolder_co2
sensor.meterkast_power
```

---

## Waarom deze conventie?

1. **Simpel:** Meeste kamers hebben 1 device, dus geen suffix nodig
2. **Schaalbaar:** Makkelijk uitbreiden met locatie suffix bij tweede device
3. **Consistent:** Alle entities van een kamer beginnen met kamernaam
4. **Automation-vriendelijk:** `sensor.{kamer}_illuminance` werkt altijd (met room slug extractie)
