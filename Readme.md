# HomeAssistant v3 Roadmap

In versie drie gaat over het versimpelen van de codebase, beter gebruik maken van nieuwe HA-mogelijkheden en het meer configuratie via de UI van Homeassistant, in plaats van YAML.

## Introductie

De grootste stap van v2 naar v3 is de gedeeltelijke overstap van YAML naar de UI voor logica, entiteiten en automatiseringen. HomeAssistant blijft de basis om de verschillende platformen (Zigbee, MQTT, HomeKit etcetera) aan elkaar te knopen.  Voor o.a. alle automatiseringen maken we gebruik van YAML, maar helpers (groepen, knoppen en dergelijken) configureren we vanuit de UI. Dat maakt het onderhoud gemakkelijker, en toegankelijker voor andere leden van het huishouden. Daarnaast is de stap van v2 naar v3 een reden om de codebase grondig tegen het licht te houden, en om enkele nieuwe functionaliteiten toe te voegen en te verbeteren.

De uitgangspunten voor versie 3 zijn als volgt, en worden hieronder toegelicht:

- Minimaliseren van gebruikersinput;
- Ruimtes als uitgangspunt;
- Automatiseren van verlichting, verwarming, zonwering, ventilatie en beveiliging;
- Maximaliseren robuustheid (o.a. geen cloudservices, backup bij uitval Homeassistant);
- Opschonen codebase.

### Minimaliseren van gebruikersinput

Hierover kan ik kort zijn: het doel van automatiseren is ervoor zorgen dat in ons huis, de verlichting, de verwarming, de ventilatie etcetera zich automatisch aanpast aan de omstandigheden - zonder - dat hierbij gebruikersinput nodig is.

### Ruimtes als uitgangspunt

Door de opzet per ruimte, verdieping of het gehele huis in te richting kan er efficiënt gebruik worden gemaakt van herhaling is scripts. Dit maakt de codebase klein en de werking van het huis en iedere ruimte univorm en herkenbaar.

Op dit moment groepeert HomeAssistant een aantal (alle) entiteiten per ruimte in eenzelfde 'Area'. Ook zijn er sinds 2024.4 'Floors', en labels beschikbaar. Hiermee kunnen meerdere ruimtes worden gegegroepeerd. Versie 2 maakt hiervan nog geen gebruik. Door functies, en instellingen per ruimte in te richting is het mogelijk om efficiënt te werken, compacte code te schrijven. Als voorbeeld kun je hierbij denken aan één automatisering om de lampen aan- en uit te doen die alle ruimtes kan bedienen. In de regel maken gebruikers voor iedere ruimte een aparte automatiserings die dit doet, eventueel via een Blueprint. Hoewel dit de scripts simpeler maakt, zorgt dit voor een bulk aan automatiseringen die vrijwel exact hetzelfde doen. Dat is voor ons niet wenselijk.

### Automatiseren van functies

De roadmap van versie 3 omvat het automatiseren van de volgende functies: verlichting, verwarming, zonwering, ventilatie en beveiliging. Sommige functionaliteiten zijn op huisniveau, terwijl andere functies op ruimteniveau zijn. Hieronder een overzicht:

| Functie | Ruimte | Huis |
| ------- | ------ | ---- |
| Verlichting | X | |
| Verwarming | X | |
| Zonwering | X | |
| Ventilatie | X | X |
| Beveiliging | | X |

**Verlichting**: De verlichting schakelt op dit moment automatisch op basis van de aanwezige bewegingssensoren en het aanwezige daglicht in een ruimte. Dit werkt goed. De scripts die dit automatiseren zijn echter gedateerd. Daarnaast gaan we gebruik maken van scenes en groepen op Zigbee-niveau. Hiermee ontlasten we het netwerk en verminderen we vertragingen. Daarnaast zorgt dit ervoor dat we fysieke knoppen los van Homeassistant de lampen op zigbeeniveau kunnen laten aansturen. Dit heeft als groot voordeel dat bediening van de verlichting ook bij uitval van het systeem werkt.

**Verwarming**: De huidige versie voorziet niet in het automatisch verwarmen van ruimtes; hiervoor gebruiker we nu de App van Tado. Het is de bedoeling om de verwarming 100% lokaal te gaan regelen, door de thermostaat en radiatorknoppen via HomeKit te bedienen, en automatische verwarmingsschemas in Homeassistant vast te leggen.

**Zonwering**: De besturing van de zonwering is nog nog niet op kamerniveau geregeld. Het zonnescherm of het rolluik gaat wel automatisch dicht op basis van onder andere de stand van de zon, maar gebruikt de temperatuur in de woonkamer als referentie voor de kamertemperatuur. Dat is problematisch omdat de temperatuur in het kantoor veelal hoger ligt dan in de woonkamer. Deze referentiewaarde moet, vanaf versie 3, per kamer worden bepaald. Daarnaast maakt de zonwering maakt gebruik van het KNMI voor onder andere de zonintensiteit en de actuele buitentemperatuur. Dat is niet ideaal, vanwege de afhankelijkheid van cloudservices, maar vooralsnog werkt dit prima. In de toekomst kunnen deze entiteiten simpel vervangen worden door een lokaal weerstation op het dak.

**Ventilatie**: De ventilatie is op dit moment al afdoende geregeld. Deze schakelt op de aanwezigheid van personen, en neemt daarin per ruimte ook de CO2-concentratie in mee. Niet in elke ruimte is een CO2-meter aanwezig, waardoor de scripts nu specifiek gemaakt zijn voor ruimtes waarin zij wel zijn. In versie 3 gaan we deze scripts algemeniseren.

**Beveiliging**: De beveiliging heeft als doel om bij afwezigheid, in de avond of nacht, meldingen te geven (via Homekit) bij onraad (denk aan personen die geregistreerd worden op camera's, deuren of ramen die geopend worden).

### Maximaliseren robuustheid

Elke cloudservices is er één teveel, alles moet lokaal *kunnen* werken. Dat wil niet zeggen dat er geen cloudservices worden gebruikt. Het uitgangspunt is dat de functies die hierboven zijn beschreven zoveel mogelijk blijven werken zonder internet.

## Beschrijving functies

De volgende wijzigingen worden doorgevoerd:
    - [ ] Class aanmaken met de naam `Ruimte'
    - Attributen tijdens initieren:
        - [ ] self.naam
        - [ ] self.licht_drempelwaarde

    - Verlichting:
        - [ ] Daglicht: is er daglicht
        - [ ] Aanwezigheid: zijn er personen aanwezig
        - [ ] Detectie: automatische schakelen op beweging (input_boolean)
        - [ ] Scene: welke modus is actief (input_select)


    - [ ] Gewenste werkmodussen integreren
        - [ ] Verwarming [Auto, Normaal, Comfort, Uit]
        - [ ] Verwarmingsschema: instellen met een schedule entity van HA
        - [ ] Verlichting [Auto, Handmatig] 

### Apps per overkoepelend thema

- [ ] Ventilatie (WTW)
    - [ ] Status: [Auto, Normaal, Boost, Uit] 
    - [ ] Automatisch modi
        - [ ] Boost: op basis van luchtvochtigheid per ruimte tov gemiddelde
        - [ ] Uit: op basis van afwezigheid personen
        - [ ] Boost: op basis van gemeten CO2
        - [ ] Nachtkoeling: kopieren eigenschappen WTW-unit

- [ ] Zonwering
    - [ ] Zonstand
    - [ ] Temperatuur
    - [ ] ...


    
