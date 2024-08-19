# HomeAssistant v2024 Roadmap

In deze versie gaat over het versimpelen van de codebase, beter gebruik maken van nieuwe HA-mogelijkheden en het meer configuratie via de UI van Homeassistant, in plaats van YAML.

## Introductie

De grootste stap van v2021 naar v2024 is de gedeeltelijke overstap van YAML naar de UI voor een deel van de configuratie. HomeAssistant blijft de basis om de verschillende platformen (Zigbee, MQTT, HomeKit etcetera) aan elkaar te knopen.  Voor de automatiseringen maken we gebruik van YAML, maar helpers (groepen, knoppen en dergelijken) configureren we vanuit de UI. Dat maakt het onderhoud gemakkelijker, en toegankelijker voor andere leden van het huishouden. Daarnaast is de stap van v2021 naar v2024 een reden om de codebase grondig tegen het licht te houden, en om enkele nieuwe functionaliteiten toe te voegen en te verbeteren.

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

Op dit moment groepeert HomeAssistant een aantal (alle) entiteiten per ruimte in eenzelfde 'Area'. Ook zijn er sinds 2024.4 'Floors', en labels beschikbaar. Hiermee kunnen meerdere ruimtes worden gegegroepeerd. Versie 2 maakt hiervan nog geen gebruik. Door functies, en instellingen per ruimte in te richting is het mogelijk om efficiënt te werken, compacte code te schrijven. Als voorbeeld kun je hierbij denken aan één automatisering om de lampen aan- en uit te doen die alle ruimtes kan bedienen.

### Automatiseren van functies

De roadmap van deze update omvat het verder automatiseren van de volgende functies: verlichting, verwarming, zonwering, ventilatie en beveiliging. Sommige functionaliteiten zijn op huisniveau, terwijl andere functies op ruimteniveau zijn. Hieronder een overzicht:

| Functie | Ruimte | Huis |
| ------- | ------ | ---- |
| Verlichting | X | |
| Verwarming | X | |
| Zonwering | X | |
| Ventilatie | X | X |
| Beveiliging | | X |

**Verlichting**: De verlichting schakelt op dit moment automatisch op basis van de aanwezige bewegingssensoren en het aanwezige daglicht in een ruimte. Dit werkt goed. De scripts die dit automatiseren zijn echter gedateerd. Daarnaast gaan we gebruik maken van scenes en groepen op Zigbee-niveau. Hiermee ontlasten we het netwerk en verminderen we vertragingen. Daarnaast zorgt dit ervoor dat we fysieke knoppen los van Homeassistant de lampen op zigbeeniveau kunnen laten aansturen. Dit heeft als groot voordeel dat bediening van de verlichting ook bij uitval van het systeem werkt.

**Verwarming**: De huidige versie voorziet niet in het automatisch verwarmen van ruimtes; hiervoor gebruiker we nu de App van Tado. Het is de bedoeling om de verwarming 100% lokaal te gaan regelen, door de thermostaat en radiatorknoppen via HomeKit te bedienen, en automatische verwarmingsschemas in Homeassistant vast te leggen.

**Zonwering**: De besturing van de zonwering is nog nog niet op kamerniveau geregeld. Het zonnescherm of het rolluik gaat wel automatisch dicht op basis van onder andere de stand van de zon, maar gebruikt de temperatuur in de woonkamer als referentie voor de kamertemperatuur. Dat is problematisch omdat de temperatuur in het kantoor veelal hoger ligt dan in de woonkamer. Deze referentiewaarde moet, per kamer worden bepaald. Daarnaast maakt de zonwering gebruik van het KNMI voor onder andere de zonintensiteit en de actuele buitentemperatuur. Dat is niet ideaal, vanwege de afhankelijkheid van cloudservices, maar vooralsnog werkt dit prima. In de toekomst kunnen deze entiteiten simpel vervangen worden door een lokaal weerstation op het dak.

**Ventilatie**: De ventilatie is op dit moment al afdoende geregeld. Deze schakelt op de aanwezigheid van personen, en neemt daarin per ruimte ook de CO2-concentratie in mee. Niet in elke ruimte is een CO2-meter aanwezig, waardoor de scripts nu specifiek gemaakt zijn voor ruimtes waarin zij wel zijn. Het doel van deze versie is om deze scripts te algemeniseren.

**Beveiliging**: De beveiliging heeft als doel om bij afwezigheid, in de avond of nacht, meldingen te geven (via Homekit) wanneer ramen of deuren geopend zijn, of als er beweging is gedetecteerd.

### Maximaliseren robuustheid

Elke cloudservices is er één teveel, alles moet lokaal *kunnen* werken. Dat wil niet zeggen dat er geen cloudservices worden gebruikt. Het uitgangspunt is dat de functies die hierboven zijn beschreven zoveel mogelijk blijven werken zonder internet. 

Voor de gevallen dat bediening of monitoring noodzakelijk is, wordt HomeKit gebruikt. Dit is weliswaar geen lokale service (hoewel het ook zonder internetverbinding werkt), maar ontzorgt op een aantal punten in onderhoud en zorgt voor een vlekkenloze gebruikservaring op iOS-apparaten. Via de Homebridge plugin van Home Assistant worden alleen hoogstnoodzakelijke entiteiten ontsloten, zodat Homekit als simpele afstandsbediening werkt. Home Assistant zelf kan op deze manier losgekoppeld blijven van het internet, en de firewall kan gesloten blijven. Dat betekent dat de aanvalsvector minimaal is (met de aanname dat Homekit een te vertrouwen service is).

## Beschrijving functies

Onderstaande secties beschrijven de functies per thema, zoals hierboven geïntroduceerd.

### Verlichting

De verlichting schakelt op aanwezigheid en het omgevingslicht. Daarvoor is per ruimte het volgende nodig:

- [ ] Een helper (groep) met lichtsensoren
- [ ] Een helper (groep) met bewegingssensoren
- [ ] Een groep met lampen (op Zigbee-niveau)
- [ ] Enkele scenes (op Zigbee-niveau): gedimd, normaal, vol
- [ ] Een helper (input select) om de actieve scene vast te leggen
- [ ] Een helper (input slider) met een drempelwaarde voor de minimale lichtsterkte
- [ ] Een helper (input slider) met een vertraging voor het in- en uitschakelen op basis van omgevingslicht
- [ ] Een helper (input slider) met een vertraging voor het uitschakelen van licht wanneer er niemand meer aanwezig is

Naast deze basisfunctionaliteit is het belangrijk dat verlichting ook te **bedienen is fysieke schakelaars** die gebruik maken van de aanwezige schakelmateriaal. Hiervoor is per ruimte (waar dit gewenst is) gebruik gemaakt van een Philips Hue wall switch die achter een bestaande pulsdrukker is gemonteerd. Vooralsnog maakt deze functie gebruik van automations, en niet van Zigbee bindings. De reden hiervoor is dat het niet mogelijk lijkt te zijn om scenes direct via Zigbee te toggelen.

- [ ] Short press: zorgt ervoor dat lampen handmatig aan of uit schakelen
- [ ] Long press: toggle actieve scene

### Verwarming

De verwarming maakt gebruik van Tado-materiaal. Deze zijn afgesloten van het internet en te bedienen via de Homekit Device-integratie. Het instellen van schema's gaat via Home Assistant.

- [ ] Een schema via Home Assistant dat onderscheid maakt tussen weekdagen en weekenddagen
- [ ] Een automatisering om een schema in of uit te schakelen op basis van 
...

### Zonwering

...

### Ventilatie

...

### Beveiliging

De beveiliging maakt gebruik van eigen automatiseringen en helpers, gezien de eenvoudige eisen is een *addon* als Alarmo op dit moment niet noodzakelijk. De volgende functies nodig:

- [ ] Een helper (groep) per verdieping met raamsensoren
- [ ] Een helper (groep) met deursensoren op de begane grond
- [ ] Een automatisering om als het alarm is ingeschakeld op night of away het alarm te triggeren
- [ ] Automatische schakeling van het alarm op basis van:
  - [ ] Aan- of afwezigheid van personen
  - [ ] Tijd om de nacht-stand in of uit te schakelen


De volgende wijzigingen worden doorgevoerd:

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


    
