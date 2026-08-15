# Home Assistant configuratie

Deze repository bevat onze modulaire configuratie voor Home Assistant: de 2026-editie. Opgebouwd vanuit functionele thema's zoals: beveiliging, verlichting, verwarming, schoonmaken.

**Elk thema is ondergebracht in een zelfstandig package** — met automations, helpers en sensoren bij elkaar. De automations zijn generiek: één automation handelt alle kamers af door de kamernaam uit het triggerende entity ID te extraheren. Wil je een kamer toevoegen, dan volstaat het de juiste helpers (via de UI) aan te maken met de juiste naam. Wil je de hele config meenemen naar een nieuw huis, dan werkt alles opnieuw zodra de entities op orde zijn.

**Home automation is pas geslaagd als geen input nodig.** Het huis voert alledaagse taken autonoom uit — verlichting, verwarming, ventilatie, stofzuigen. Tegelijk werkt alles ook zonder Home Assistant: lichtschakelaars zijn via Zigbee direct aan lampen gekoppeld (binding), de stofzuiger is te bedienen via Valetudo, klimaat via HomeKit, de Tado app of de fysieke thermostaat. Het systeem grijpt niet in tijdens een handmatige aanpassing, en herneemt automatisch bij de volgende trigger. Home Assistant orkestreert, maar is geen single point of failure.

Alles draait lokaal. Home Assistant is niet bereikbaar van buiten het netwerk. Slimme apparaten zijn van het internet afgesloten; alleen een handvol entiteiten is via Apple Home beschikbaar voor bediening onderweg. Camera's en deurbel draaien via Scrypted naar een lokale HomeKit-instantie — beelden worden versleuteld opgeslagen en nooit de cloud in gestuurd.

In de woorden van Dieter Rams: less but better — geen over-engineering, geen dubbele logica, geen overbodige complexiteit.

## Thema's

**Beveiliging**
Het systeem weet wanneer bewoners thuis zijn op basis van telefoonlocatie (via HomeKit), en schakelt het alarm automatisch in of uit. Het houdt rekening met uitzonderingen: vakantie (langdurige afwezigheid), oppas (gezin weg maar iemand thuis), en handmatige overschrijving. Als bij afwezigheid deuren of ramen openen dan gaat het alarm af.

**Klimaat — Verwarming**
Onze levens, en de verwarming (lage temperatuur radiatoren) zorgen ervoor dat het niet nuttig is om 24/7 de verwarming aan te hebben. Verwarming volgt daarom een weekschema per kamer. Kamers zonder schema verwarmen op basis van aanwezigheid (beweging). Bij langdurige afwezigheid gedurende de dag schakelt de verwarming automatisch over op eco-modus (1 tot 2 graden lager dan volgens het schema); bij thuiskomst worden de schema-temperaturen hersteld.

**Klimaat — Ventilatie**
De WTW-installatie regelt zichzelf op basis van CO₂ en luchtvochtigheid. Op warme zomernachten koelt het huis passief via nachtventilatie. Bij afwezigheid staat alles uit.

**Klimaat — Zonwering**
Zonnescherm en rolluik bedienen zich automatisch op basis van instraling (gecorrigeerd voor verticale ramen), buiten- en binnentemperatuur en wind. 's Winters blijft het scherm open ook als de zon fel is — de buitentemperatuur is dan laag genoeg dat je juist de zonwarmte door het raam wil hebben.

**Verlichting**
Verlichting gaat aan bij beweging als het donker genoeg is, en uit na een instelbare time-out. Per kamer configureerbaar via de GUI. In de slaapkamer schakelt de juiste scène automatisch op basis van het tijdstip via een schedule-helper. 's Nachts willen we liever niet de lamp op 100%.

**Schoonmaken**
De robotstofzuiger draait automatisch bij afwezigheid, afhankelijk van de verdieping niet iedere dag (beneden wel, boven om de dag). Handmatige bediening per verdieping is mogelijk via de app. Tijdens vakantie staat alles gepauzeerd.

## Apparaten

| Categorie | Apparaten | Integratie |
|-----------|-----------|------------|
| Verlichting | Zigbee lampen (alle kamers) | Zigbee2MQTT |
| Klimaat | Tado thermostaten (woonkamer, hal, kantoor) | Lokaal Homekit + Tado Hijack |
| Ventilatie | WTW met Sonoff schakelaars | ESPHome |
| Zonwering | Zonnescherm achterkant, rolluik voorkant | Shelly |
| Energie | Zonnepanelen, P1 slimme meter | — |
| Schoonmaken | Robotstofzuiger (3 verdiepingen) | MQTT |
| Sensoren | Weerstation, KNMI, CO₂, temperatuur, luchtvochtigheid | Ecowitt, Zigbee2MQTT en Matter |
| Aanwezigheid | iPhone locatie via HomeKit | HomeKit |
| Beveiliging | Alarm, deuren- en raamcontacten, camera's* | Zigbee2MQTT |


## Opbouw

Elk thema staat in een eigen package onder `packages/`, inclusief gedetailleerde documentatie. Drempelwaarden zijn instelbaar via de Home Assistant interface zonder YAML te bewerken. Elk package heeft een eigen `README.md` met technische details.

## Documentatie

- [Naamgevingsconventies](docs/naamgeving.md)
- [Roadmap](docs/roadmap.md)
- [2026 migratie](docs/2026-update.md)
