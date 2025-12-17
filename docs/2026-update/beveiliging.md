# Beveiliging Package - Gedetailleerd Plan

**Fase**: 1
**Status**: In Progress
**Gestart**: 2025-12-17

## Inhoudsopgave
1. [Huidige Situatie](#huidige-situatie)
2. [Gewenste Eindresultaat](#gewenste-eindresultaat)
3. [Functionele Eisen](#functionele-eisen)
4. [Architectuur](#architectuur)
5. [Implementatie Details](#implementatie-details)
6. [Testing Scenario's](#testing-scenarios)
7. [Migratie Stappen](#migratie-stappen)

## Huidige Situatie

### AppDaemon Implementatie

**Locatie**: `appdaemon/apps/alarm/`

**Apps**:
1. **AlarmMode** (`alarm_mode.py`):
   - Automatische alarm state management
   - Gebruikt `noone_home()` / `anyone_home()` helpers
   - Sunrise/sunset scheduling met offsets (-1h / +1h)
   - Logic:
     - Niemand thuis → `armed_away`
     - Iemand thuis + nacht → `armed_home`
     - Iemand thuis + dag → `disarmed`

2. **AlarmTrigger** (`alarm_trigger.py`):
   - Monitort sensor groups
   - Triggert alarm bij intrusion
   - Configuratie:
     - `binary_sensor.ramen_1`: armed_away
     - `binary_sensor.ramen_deuren_bg`: armed_away + armed_night

### Alarm Entity
**Locatie**: `configuration.yaml:39-41`
```yaml
alarm_control_panel:
  - platform: manual
    name: Huis
```

### Sensor Groups
- `binary_sensor.ramen_1` - Ramen verdieping 1
- `binary_sensor.ramen_deuren_bg` - Ramen/deuren begane grond

### Presence Detection
- `group.aanwezigheid_personen` (Ramon + Flore)
- Device trackers via HomeKit input booleans

## Gewenste Eindresultaat

### Native Home Assistant Package
Alles in `packages/beveiliging/`:
- Alarm entity configuratie
- Helper entities (input_select, groups)
- Automatiseringen

### GUI Configureerbaar
- Sensor groups voor deuren/ramen aanpasbaar via GUI
- Input helpers zichtbaar in UI
- Automatiseringen traceable via automation traces

### Geen AppDaemon Dependency
Alle logica in native HA automations.

## Functionele Eisen

### 1. Automatische Armed_Home
**Trigger**: Zonsondergang OF 19:00 uur (wat het EERST komt)
- Gewenste alarm modus wordt `armed_home`
- Als iemand thuis is, gaat alarm naar `armed_home`

**Voorbeelden**:
- Zonsondergang 18:30 → armed_home om 18:30
- Zonsondergang 20:00 → armed_home om 19:00

### 2. Automatische Disarm
**Trigger**: Zonsopgang OF 08:00 uur (wat het LAATST komt)
- Gewenste alarm modus wordt `disarmed`
- Als iemand thuis is, gaat alarm naar `disarmed`

**Voorbeelden**:
- Zonsopgang 09:00 → disarmed om 09:00
- Zonsopgang 06:00 → disarmed om 08:00

### 3. Armed_Away bij Niemand Thuis
**Trigger**: Laatste persoon verlaat huis
- Alarm gaat direct naar `armed_away`
- Ongeacht gewenste modus of tijd van dag

### 4. Thuiskomst
**Trigger**: Eerste persoon komt thuis
- Als alarm `armed_away` was:
  - Ga naar gewenste modus (`armed_home` of `disarmed`)
  - Afhankelijk van tijd/zon

### 5. Manual Override
**Gedrag**: Handmatige wijzigingen worden gerespecteerd
- Manual change blijft actief tot volgende wijziging gewenste modus
- Voorbeeld: Om 15:00 handmatig op `armed_away` → blijft zo tot 's avonds gewenste modus wijzigt naar `armed_home`

### 6. Alarm Triggering
**Trigger**: Deur of raam gaat open tijdens `armed_away`
- Alarm gaat naar `triggered` state
- Configureerbaar welke sensoren gemonitord worden

## Architectuur

### Kernconcepten

#### 1. Gewenste Modus Helper
**Entity**: `input_select.alarm_gewenste_modus`
- Waarden: `armed_home`, `disarmed`
- Houdt bij wat alarm zou moeten zijn op basis van tijd/zon
- Volledig **onafhankelijk** van daadwerkelijke alarm state

#### 2. Presence Override
**Logic**: Armed_away heeft altijd voorrang
- Niemand thuis → altijd `armed_away`
- Ongeacht gewenste modus

#### 3. Manual Override Respect
**Logic**: Synchronisatie alleen bij wijziging gewenste modus
- Alarm synchroniseert met gewenste modus alleen als:
  - Gewenste modus wijzigt (trigger)
  - Iemand thuis is (conditie)
- Handmatige wijzigingen blijven intact tussen wijzigingen

### State Machine Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                 Gewenste Modus Logic                         │
│         (onafhankelijk van alarm state)                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Trigger 1: sun.sun → below_horizon                          │
│  Trigger 2: time → 19:00                                     │
│     ↓                                                         │
│  Action: alarm_gewenste_modus → "armed_home"                 │
│                                                               │
│  ─────────────────────────────────────────────────────       │
│                                                               │
│  Trigger 1: sun.sun → above_horizon                          │
│  Trigger 2: time → 08:00                                     │
│     ↓                                                         │
│  Action: alarm_gewenste_modus → "disarmed"                   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    Alarm State Logic                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Trigger: group.aanwezigheid_personen → off                  │
│     ↓                                                         │
│  Action: alarm → armed_away (OVERRIDE)                       │
│                                                               │
│  ─────────────────────────────────────────────────────────   │
│                                                               │
│  Trigger: group.aanwezigheid_personen → on                   │
│  Condition: alarm state = armed_away                         │
│     ↓                                                         │
│  Action: alarm → gewenste_modus                              │
│                                                               │
│  ─────────────────────────────────────────────────────────   │
│                                                               │
│  Trigger: alarm_gewenste_modus → state change                │
│  Condition: iemand thuis + not triggered                     │
│     ↓                                                         │
│  Action: alarm → nieuwe gewenste_modus                       │
│    (respecteert manual override tot dit moment)              │
│                                                               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    Trigger Logic                             │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Trigger: group.beveiliging_deuren_ramen → on                │
│  Condition: alarm state = armed_away                         │
│     ↓                                                         │
│  Action: alarm_control_panel.alarm_trigger                   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Waarom deze architectuur?

**Voordelen**:
1. **Duidelijke scheiding**: Tijd/zon logic los van presence logic
2. **Zichtbaar**: Gewenste modus is zichtbaar in UI voor debugging
3. **Manual override**: Automatisch gerespecteerd door trigger-based sync
4. **Uitbreidbaar**: Gemakkelijk extra modi of condities toe te voegen
5. **Debugbaar**: Elke stap is traceable via automation traces

## Implementatie Details

### Package Structuur

```
packages/beveiliging/
├── alarm.yaml          # Alarm control panel entity
├── helpers.yaml        # Input select + groups
└── automations.yaml    # 6 automations
```

### File: `alarm.yaml`

**Inhoud**: Alarm control panel entity (migratie van huidige config)

```yaml
alarm_control_panel:
  - platform: manual
    name: Huis
    code: "0000"
    arming_time: 0
    delay_time: 0
    trigger_time: 600
    disarmed:
      trigger_time: 0
    armed_home:
      arming_time: 0
      delay_time: 0
```

**Opmerking**: Mogelijk later `code_arm_required: false` toevoegen als je code niet wilt gebruiken.

### File: `helpers.yaml`

**Inhoud**: Input select voor gewenste modus

```yaml
input_select:
  alarm_gewenste_modus:
    name: "Alarm Gewenste Modus"
    options:
      - "armed_home"
      - "disarmed"
    initial: "disarmed"
    icon: mdi:shield-check
```

**Opmerking**: Group `group.beveiliging_deuren_ramen` wordt via GUI aangemaakt (niet in YAML).

### File: `automations.yaml`

#### Automatisering 1: Gewenste Modus → Armed_Home

```yaml
- id: beveiliging_gewenste_modus_armed_home
  alias: "Beveiliging: Gewenste Modus Armed Home"
  description: "Zet gewenste alarm modus op armed_home bij zonsondergang of 19:00 (wat eerst komt)"

  trigger:
    - platform: sun
      event: sunset
      id: sunset
    - platform: time
      at: "19:00:00"
      id: time

  mode: single

  action:
    - service: input_select.select_option
      target:
        entity_id: input_select.alarm_gewenste_modus
      data:
        option: armed_home
```

**Note**: Beide triggers zetten gewenste modus, wat het eerst komt activeert. De tweede trigger heeft geen effect (modus is al armed_home).

#### Automatisering 2: Gewenste Modus → Disarmed

```yaml
- id: beveiliging_gewenste_modus_disarmed
  alias: "Beveiliging: Gewenste Modus Disarmed"
  description: "Zet gewenste alarm modus op disarmed bij zonsopgang of 08:00 (wat laatst komt)"

  trigger:
    - platform: sun
      event: sunrise
      id: sunrise
    - platform: time
      at: "08:00:00"
      id: time

  mode: single

  action:
    - service: input_select.select_option
      target:
        entity_id: input_select.alarm_gewenste_modus
      data:
        option: disarmed
```

**Note**: Beide triggers zetten gewenste modus op disarmed. De tweede van de twee heeft geen effect.

#### Automatisering 3: Armed_Away (Niemand Thuis)

```yaml
- id: beveiliging_armed_away_niemand_thuis
  alias: "Beveiliging: Armed Away Niemand Thuis"
  description: "Activeer armed_away wanneer niemand thuis is"

  trigger:
    - platform: state
      entity_id: group.aanwezigheid_personen
      to: "off"

  condition:
    - condition: not
      conditions:
        - condition: state
          entity_id: alarm_control_panel.huis
          state:
            - armed_away
            - triggered

  mode: single

  action:
    - service: alarm_control_panel.alarm_arm_away
      target:
        entity_id: alarm_control_panel.huis
      data:
        code: "0000"
```

#### Automatisering 4: Gewenste Modus (Thuisgekomen)

```yaml
- id: beveiliging_gewenste_modus_thuisgekomen
  alias: "Beveiliging: Gewenste Modus Thuisgekomen"
  description: "Zet alarm naar gewenste modus wanneer iemand thuiskomt"

  trigger:
    - platform: state
      entity_id: group.aanwezigheid_personen
      to: "on"

  condition:
    - condition: state
      entity_id: alarm_control_panel.huis
      state: armed_away

  mode: single

  action:
    - choose:
        - conditions:
            - condition: state
              entity_id: input_select.alarm_gewenste_modus
              state: armed_home
          sequence:
            - service: alarm_control_panel.alarm_arm_home
              target:
                entity_id: alarm_control_panel.huis
              data:
                code: "0000"
        - conditions:
            - condition: state
              entity_id: input_select.alarm_gewenste_modus
              state: disarmed
          sequence:
            - service: alarm_control_panel.alarm_disarm
              target:
                entity_id: alarm_control_panel.huis
              data:
                code: "0000"
```

#### Automatisering 5: Pas Alarm Aan bij Wijziging Gewenste Modus

```yaml
- id: beveiliging_pas_alarm_aan_gewenste_modus
  alias: "Beveiliging: Pas Alarm Aan Gewenste Modus"
  description: "Synchroniseer alarm met gewenste modus wanneer deze wijzigt (respecteert manual overrides)"

  trigger:
    - platform: state
      entity_id: input_select.alarm_gewenste_modus

  condition:
    - condition: state
      entity_id: group.aanwezigheid_personen
      state: "on"
    - condition: not
      conditions:
        - condition: state
          entity_id: alarm_control_panel.huis
          state: triggered

  mode: single

  action:
    - choose:
        - conditions:
            - condition: state
              entity_id: input_select.alarm_gewenste_modus
              state: armed_home
          sequence:
            - service: alarm_control_panel.alarm_arm_home
              target:
                entity_id: alarm_control_panel.huis
              data:
                code: "0000"
        - conditions:
            - condition: state
              entity_id: input_select.alarm_gewenste_modus
              state: disarmed
          sequence:
            - service: alarm_control_panel.alarm_disarm
              target:
                entity_id: alarm_control_panel.huis
              data:
                code: "0000"
```

**Belangrijk**: Deze automatisering triggert alleen bij STATE CHANGE van gewenste modus. Dus:
- Manual override om 15:00 → geen trigger
- Gewenste modus wijzigt 's avonds → trigger → alarm sync
- Dit respecteert manual overrides!

#### Automatisering 6: Trigger Alarm bij Deuren/Ramen

```yaml
- id: beveiliging_trigger_deuren_ramen
  alias: "Beveiliging: Trigger Alarm Deuren Ramen"
  description: "Trigger alarm wanneer deuren of ramen opengaan tijdens armed_away"

  trigger:
    - platform: state
      entity_id: group.beveiliging_deuren_ramen
      to: "on"

  condition:
    - condition: state
      entity_id: alarm_control_panel.huis
      state: armed_away

  mode: single

  action:
    - service: alarm_control_panel.alarm_trigger
      target:
        entity_id: alarm_control_panel.huis
      data:
        code: "0000"
```

## Testing Scenario's

### Tijd/Zon Testing

| Scenario | Zonsondergang | Test Tijd | Verwacht Resultaat |
|----------|---------------|-----------|-------------------|
| 1 | 18:30 | 18:30 | Gewenste modus → armed_home |
| 2 | 20:00 | 19:00 | Gewenste modus → armed_home |
| 3 | 18:45 | 19:00 | Geen wijziging (al armed_home) |

| Scenario | Zonsopgang | Test Tijd | Verwacht Resultaat |
|----------|------------|-----------|-------------------|
| 4 | 06:00 | 08:00 | Gewenste modus → disarmed |
| 5 | 09:00 | 09:00 | Gewenste modus → disarmed |
| 6 | 07:00 | 08:00 | Gewenste modus → disarmed |

### Presence Testing

| Scenario | Aanwezigheid | Gewenste Modus | Alarm Voor | Verwacht Alarm Na |
|----------|--------------|----------------|------------|------------------|
| 7 | Niemand thuis | armed_home | disarmed | armed_away |
| 8 | Niemand thuis | disarmed | armed_home | armed_away |
| 9 | Iemand komt thuis | armed_home | armed_away | armed_home |
| 10 | Iemand komt thuis | disarmed | armed_away | disarmed |

### Manual Override Testing

| Scenario | Tijd | Actie | Gewenste Modus | Verwacht Gedrag |
|----------|------|-------|----------------|-----------------|
| 11 | 15:00 | Manual → armed_away | disarmed | Blijft armed_away |
| 12 | 19:00 | Gewenste → armed_home | armed_home | Sync naar armed_home |
| 13 | 12:00 | Manual → armed_home | disarmed | Blijft armed_home |
| 14 | 08:00 | Gewenste → disarmed | disarmed | Sync naar disarmed |

### Trigger Testing

| Scenario | Alarm State | Sensor | Verwacht Resultaat |
|----------|-------------|--------|-------------------|
| 15 | armed_away | Deur open | Alarm triggered |
| 16 | armed_home | Deur open | Geen trigger |
| 17 | disarmed | Deur open | Geen trigger |

### Edge Cases

| Scenario | Situatie | Verwacht Gedrag |
|----------|----------|----------------|
| 18 | Alarm triggered + iemand komt thuis | Blijft triggered (geen auto-reset) |
| 19 | Laatste persoon weg tijdens triggered | Blijft triggered |
| 20 | Gewenste modus wijzigt tijdens triggered | Geen alarm wijziging |
| 21 | Gewenste modus wijzigt tijdens armed_away | Geen alarm wijziging (niemand thuis) |

## Migratie Stappen

### Stap 1: Package Structuur Aanmaken
- [ ] Folder `packages/beveiliging/` aanmaken
- [ ] Packages toevoegen aan `configuration.yaml`

### Stap 2: Alarm Entity Migreren
- [ ] `packages/beveiliging/alarm.yaml` aanmaken
- [ ] Alarm config uit `configuration.yaml` verwijderen
- [ ] Config check uitvoeren
- [ ] HA herstarten
- [ ] Testen: alarm entity bestaat nog (`alarm_control_panel.huis`)

### Stap 3: Helpers Implementeren
- [ ] `packages/beveiliging/helpers.yaml` aanmaken met input_select
- [ ] Config check + restart
- [ ] Via GUI: Group `group.beveiliging_deuren_ramen` aanmaken
- [ ] Sensoren toevoegen aan group:
  - [ ] `binary_sensor.ramen_1`
  - [ ] `binary_sensor.ramen_deuren_bg`
  - [ ] Andere relevante deur/raam sensoren
- [ ] Testen: Helpers verschijnen in UI

### Stap 4: Automatiseringen Implementeren
- [ ] `packages/beveiliging/automations.yaml` aanmaken
- [ ] Automatisering 1+2 implementeren (gewenste modus)
- [ ] Config check + restart
- [ ] **Test**: Wijzig tijd/simuleer zon voor test
- [ ] Automatisering 3+4 implementeren (presence)
- [ ] Config check + restart
- [ ] **Test**: Simuleer weg/thuiskomen
- [ ] Automatisering 5 implementeren (sync)
- [ ] Config check + restart
- [ ] **Test**: Manual override scenarios
- [ ] Automatisering 6 implementeren (trigger)
- [ ] Config check + restart
- [ ] **Test**: Trigger scenarios

### Stap 5: Parallel Testen
- [ ] AppDaemon apps blijven actief
- [ ] Beide systemen draaien tegelijk
- [ ] Vergelijk gedrag:
  - [ ] Zelfde alarm states?
  - [ ] Zelfde triggers?
  - [ ] Verschillen documenteren
- [ ] Minimaal 48 uur parallel testen

### Stap 6: AppDaemon Uitschakelen
- [ ] In `appdaemon/apps/apps.yaml`: Comment out alarm apps
- [ ] AppDaemon herstarten
- [ ] 24 uur monitoren: alleen native HA werkt
- [ ] **Volledig testen**: Alle scenario's opnieuw

### Stap 7: Opruimen
- [ ] Als alles werkt: AppDaemon alarm code verwijderen
  - [ ] `appdaemon/apps/alarm/` folder
  - [ ] Alarm entries in `appdaemon/apps/apps.yaml`
- [ ] Git commit: "Migratie beveiliging naar native HA compleet"
- [ ] Update `2026-UPDATE.md`: Fase 1 ✅

### Stap 8: Documentatie
- [ ] In-code comments toevoegen waar nodig
- [ ] Dashboard aanpassingen documenteren
- [ ] Notities voor volgende fases

## Aandachtspunten

### Entity ID's
- Alarm: `alarm_control_panel.huis` blijft hetzelfde
- InfluxDB logging blijft werken (domain `alarm_control_panel` blijft)
- Dashboards hoeven niet aangepast

### Dependencies
- `group.aanwezigheid_personen` moet correct zijn
- Device tracker automations moeten blijven werken
- Vakantie mode interactie checken

### Sensor Groups
- Huidige: `binary_sensor.ramen_1`, `binary_sensor.ramen_deuren_bg`
- Nieuw: `group.beveiliging_deuren_ramen` (GUI group)
- Zorg dat alle sensoren erin zitten!

### Timing
- Zonsopgang/zonsondergang tijden variëren per seizoen
- Test in verschillende seizoenen of simuleer
- Let op: zomer vs winter gedrag

### Code in Services
- Alarm services vereisen `code: "0000"`
- Als je code wilt verwijderen: `code_arm_required: false` in alarm config

### Automation Modes
- Alle automations: `mode: single`
- Voorkomt race conditions
- Als automation al draait, nieuwe trigger wordt genegeerd

## Rollback Plan

Als er problemen zijn:

1. **Tijdens testing fase**:
   - Disable nieuwe automations via GUI
   - AppDaemon blijft actief als fallback
   - Debugging via automation traces

2. **Na AppDaemon uit**:
   - Re-enable AppDaemon apps
   - Restart AppDaemon
   - Disable HA automations
   - Troubleshoot in native HA

3. **Complete rollback**:
   - Git checkout master
   - Verwijder packages
   - Herstel oude config
   - Restart HA

## Success Criteria

Fase 1 is compleet als:
- ✅ Alle 6 automatiseringen werken foutloos
- ✅ Alle test scenario's slagen (incl. edge cases)
- ✅ 48+ uur stabiele werking zonder AppDaemon
- ✅ Geen regressies t.o.v. oude situatie
- ✅ Gewenste modus zichtbaar en correct in UI
- ✅ Manual overrides werken zoals verwacht
- ✅ AppDaemon alarm code verwijderd
- ✅ Documentatie up-to-date

## Volgende Stappen

Na succesvolle beveiliging package:
1. Commit en push naar branch `2026-update`
2. Update `2026-UPDATE.md`: Fase 1 → ✅
3. Plan Fase 2: Schoonmaken
4. Herhaal proces voor volgend domein
