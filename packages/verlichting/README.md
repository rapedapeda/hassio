# Verlichting Package

Automatische verlichting met twee hoofdfuncties.

## Overzicht

### Functie 1: Aan/Uit Logica (`aan_uit.yaml`)

Automatische verlichting op basis van beweging en lichtsterkte.

**Werking:**
- Licht gaat **AAN** bij beweging als het donker genoeg is
- Licht blijft **AAN** zolang er beweging is
- Licht gaat **UIT** na timeout zonder beweging
- Lux hysteresis (5 min) voorkomt disco-effect

**Kamers:** hal, woonkamer, keuken, kantoor, overloopeerste

**Per kamer configureerbaar:**
- `input_boolean.verlichting_{kamer}_auto` - Auto modus aan/uit
- `input_number.{kamer}_aanwezigheid_timeout` - Timeout in minuten
- `input_number.{kamer}_illuminance_threshold` - Lux drempelwaarde

**Vereisten:**
- `binary_sensor.{kamer}_occupancy` - Beweging (PIR/deur)
- `sensor.{kamer}_illuminance` - Lichtsterkte
- `light.{kamer}` - Lamp(groep)

---

### Functie 2: Scene Selectie (`scene_selectie.yaml`)

Automatische scene selectie op basis van schedule (tijd van dag).

**Werking:**
- Bij lamp aanzetten: juiste scene wordt geactiveerd
- Bij schedule wijziging: scene wordt aangepast (als lamp aan staat)
- Handmatige aanpassing blijft behouden tot volgende schedule wijziging

**Kamers:** slaapkamer

**Per kamer configureerbaar:**
- `schedule.verlichting_{kamer}` - Tijdschema met scene attribute

**Vereisten:**
- `light.{kamer}` - Lamp(groep)
- `schedule.verlichting_{kamer}` - Schedule met custom attribute `scene`
- `scene.{kamer}_{affix}` - Zigbee2MQTT scenes (bijv. `0_normaal`, `1_vol`)

**Schedule setup:**
1. Maak schedule aan in GUI
2. Voeg custom attribute `scene` toe
3. Waarde tijdens actieve periode: `1_vol` (of andere affix)
4. Fallback buiten periode: `0_normaal`

---

## Kamers

| Kamer | Functie 1 | Functie 2 | Opmerkingen |
|-------|-----------|-----------|-------------|
| Hal | ✓ | - | Timeout 1 min, threshold 10 lx |
| Woonkamer | ✓ | - | mmWave verlengt timeout, threshold 20 lx |
| Keuken | ✓ | - | Timeout 10 min, threshold 20 lx |
| Kantoor | ✓ | - | Timeout 10 min, threshold 35 lx |
| Overloop Eerste | ✓ | - | Timeout 1 min, threshold 50 lx |
| Slaapkamer | - | ✓ | Handmatig aan/uit, scenes 9-19u |
| Kerst | - | - | Kerstverlichting aan/uit op basis van alarm modus |

---

## Nieuwe kamer toevoegen

### Voor Functie 1 (auto aan/uit):
1. Maak `packages/verlichting/{kamer}/helpers.yaml`
2. Voeg triggers toe aan `aan_uit.yaml`
3. Maak GUI groups (occupancy, illuminance)
4. Zie kamer README voor details

### Voor Kerstverlichting (`kerst.yaml`):
1. Zet `input_boolean.kerst` aan via UI
2. Verlichting volgt automatisch alarm modus (aan = thuis, uit = weg)

### Voor Functie 2 (scene selectie):
1. Maak Zigbee2MQTT scenes
2. Maak schedule in GUI met scene attribute
3. Voeg triggers toe aan `scene_selectie.yaml`

---

## Naamgevingsconventies

Zie [docs/naamgeving.md](../../docs/naamgeving.md) voor volledige documentatie.

**Zigbee2MQTT:**
- Devices: `{kamer}` of `{kamer}_{locatie}`

**Helpers:**
- `input_boolean.verlichting_{kamer}_auto`
- `input_number.{kamer}_aanwezigheid_timeout`
- `input_number.{kamer}_illuminance_threshold`

**Groups:**
- `binary_sensor.{kamer}_occupancy`
- `sensor.{kamer}_illuminance`

**Schedules:**
- `schedule.verlichting_{kamer}`

**Scenes:**
- `scene.{kamer}_{affix}` (bijv. `scene.slaapkamer_0_normaal`)
