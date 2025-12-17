# Home Assistant 2026 Update

## Overzicht

Grote refactoring van de Home Assistant configuratie om gebruik te maken van moderne Home Assistant features en best practices.

## Doelstellingen

### 1. Package Structuur
- **Huidig**: Configuratie verspreid over verschillende folders (`automations/`, `input_boolean/`, `groups/`, etc.)
- **Doel**: Alles per domein georganiseerd in packages
- **Voordeel**: Overzichtelijk, modulair, gemakkelijk te onderhouden

### 2. GUI Configureerbaar
- **Huidig**: Veel configuratie in YAML hardcoded
- **Doel**: Zoveel mogelijk configureerbaar via Home Assistant GUI
- **Voorbeelden**:
  - Helper groups voor deuren/ramen via GUI ipv YAML
  - Input helpers aanpasbaar zonder YAML edits
  - Scenes en automations waar mogelijk via GUI

### 3. Native Home Assistant
- **Huidig**: Complexe logica in AppDaemon
- **Doel**: Migratie naar native HA automations, blueprints, en scripts
- **Voordeel**:
  - Minder dependencies
  - Betere integratie met HA ecosystem
  - GUI debugging en tracing

### 4. Moderne HA Patterns
- **Huidig**: Oude patterns en workarounds
- **Doel**: Gebruik maken van nieuwe HA features
- **Voorbeelden**:
  - Template triggers ipv poll-based automations
  - Choose/if-then in automations
  - Helpers voor state management
  - Blueprint automations waar zinvol

## Migratievolgorde

### ✅ Fase 0: Voorbereiding
- [x] Branch `2026-update` aangemaakt
- [x] Documentatie structuur opgezet
- [x] Planning gemaakt

### 🔄 Fase 1: Beveiliging
**Status**: In Progress
**Documentatie**: [docs/2026-update/beveiliging.md](docs/2026-update/beveiliging.md)

**Scope**:
- Migratie AppDaemon alarm logica naar native HA
- Package structuur: `packages/beveiliging/`
- Automatische armed_home/disarmed op basis van tijd/zon
- Presence-based armed_away
- Trigger logic voor deuren/ramen

**Deliverables**:
- [ ] Package `packages/beveiliging/alarm.yaml`
- [ ] Package `packages/beveiliging/helpers.yaml`
- [ ] Package `packages/beveiliging/automations.yaml`
- [ ] Helpers aangemaakt via GUI
- [ ] AppDaemon alarm apps uitgezet
- [ ] Volledig getest

### ⏳ Fase 2: Schoonmaken
**Status**: Planned
**Documentatie**: [docs/2026-update/schoonmaken.md](docs/2026-update/schoonmaken.md)

**Scope**: TBD
- Stofzuiger automations
- Schema's en zones
- Mogelijk blueprint usage

### ⏳ Fase 3: Verlichting
**Status**: Planned
**Documentatie**: [docs/2026-update/verlichting.md](docs/2026-update/verlichting.md)

**Scope**: TBD
- Adaptive lighting
- Presence-based automations
- Scene management
- Special modes (kerst, etc.)

### ⏳ Fase 4: Media
**Status**: Planned
**Documentatie**: [docs/2026-update/media.md](docs/2026-update/media.md)

**Scope**: TBD
- Media player automations
- Volume management
- Source switching

### ⏳ Fase 5: Klimaat
**Status**: Planned
**Documentatie**: [docs/2026-update/klimaat.md](docs/2026-update/klimaat.md)

**Scope**: TBD
- Ventilatie (WTW)
- Verwarming
- Occupancy-based control
- Presets en modes

## Algemene Principes

### Package Structuur
Elk domein krijgt eigen package folder:
```
packages/
├── beveiliging/
│   ├── alarm.yaml
│   ├── helpers.yaml
│   └── automations.yaml
├── schoonmaken/
│   └── ...
├── verlichting/
│   └── ...
└── ...
```

### Naming Conventions
- **Entities**: `<domein>_<functie>` (bijv. `alarm_gewenste_modus`, `beveiliging_deuren_ramen`)
- **Automations**: `<domein>_<actie>_<trigger>` (bijv. `beveiliging_armed_away_niemand_thuis`)
- **Files**: lowercase, underscores (bijv. `automations.yaml`, `helpers.yaml`)

### Helpers in GUI
Waar mogelijk helpers via GUI aanmaken:
- Input booleans
- Input selects
- Input numbers
- Groups
- Scenes (eenvoudige)

Alleen in YAML als:
- Complex logic vereist (templates)
- Deel van package die samen hoort
- Version control belangrijk

### Documentatie
- Hoofddocument (`2026-UPDATE.md`): Overzicht en voortgang
- Per domein document (`docs/2026-update/<domein>.md`): Gedetailleerd plan
- In-code comments: Uitleg van complexe logica
- Commit messages: Duidelijke omschrijving van wijzigingen

### Testing
Voor elke fase:
1. Implementeer in branch
2. Test alle scenario's
3. Vergelijk gedrag met oude implementatie
4. Documenteer afwijkingen/verbeteringen
5. Commit en push
6. Volgende fase

Pas na volledige 2026-update:
- Review hele branch
- Merge naar master
- Oude code archiveren/verwijderen

## Aandachtspunten

### Backward Compatibility
- Zorg dat entity_id's consistent blijven waar mogelijk
- InfluxDB/Recorder configuratie updaten waar nodig
- Dashboards kunnen entity_id wijzigingen nodig hebben

### Dependencies
- Sommige automations zijn cross-domein (bijv. alarm + verlichting)
- Documenteer dependencies
- Test interacties tussen domeinen

### Configuration Validation
Na elke fase:
```bash
ha core check
```

Of via Developer Tools > YAML in HA GUI.

### Backups
Voor grote wijzigingen:
1. Git commit huidige staat
2. HA snapshot maken
3. Dan migratie uitvoeren

## Resources

### Home Assistant Documentatie
- [Packages](https://www.home-assistant.io/docs/configuration/packages/)
- [Automations](https://www.home-assistant.io/docs/automation/)
- [Helpers](https://www.home-assistant.io/integrations/#helper)
- [Blueprints](https://www.home-assistant.io/docs/automation/using_blueprints/)

### Huidige Configuratie
- AppDaemon apps: `appdaemon/apps/`
- Automations: `automations/`
- Helpers: `input_boolean/`, `input_number/`, `input_select/`, etc.
- Groups: `groups/`

## Voortgang

**Gestart**: 2025-12-17
**Huidige Fase**: Beveiliging (Fase 1)
**Geschatte Voltooiing**: TBD (afhankelijk van testing en scope)

## Notities

- Branch blijft actief tijdens hele refactoring
- Incrementele commits per domein
- Master blijft stabiel/werkend
- Merge naar master pas na volledige 2026-update en testing
