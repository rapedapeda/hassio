# Home Assistant: specificatie van configuratie
**Versie 2024-01-01**

## Inleiding
In de afgelopen jaren is de automatisering van het huis steeds verder uitgebreid. De eerste versie uit 2019 was vooral een zoektocht naar de mogelijkheden en grenzen van Home Assistant. Later, in 2021 (v1.0), zijn de automatiseringen verbeterd en geuniformiseerd. Hierdoor was een enkele automatisering verantwoordelijk voor meerdere acties en meerdere kamers. Deze versie verminderde het aantal automatiseringen aanzienlijk.

In de afgelopen 2 jaren zijn er een hoop zaken gestroomlijnd binnen Home Assistant, en is onze situatie ook veranderd door een verhuizing. Om een aantal voorbeelden te noemen: 

- Een verhuizing: van een klein appartement, naar een huis met meerdere (slaap)kamers, een buitenruimte, een type D ventilatiesysteem etcetera.
- Er zijn camera's voor en achter het huis geinstalleerd (eerst via Home Assistant, maar inmiddels direct via HomeKit Secure Video.
- De stofzuigrobot is op dit moment (vanwege een convectorput) niet meer in gebruik
- We hebben een verwarmingssysteem dat meerdere zones heeft.
- We inmiddels ook fysieke pulsdrukkers in verschillende kamers hebben geinstalleerd voor een handmatige bediening.
- Home Assistant heeft inmiddels een sterk verbeterde GUI, waardoor het logisch is om sommige helpers via de GUI te configureren 
- Zigbee2MQTT is ook sterk verbeterd. Sinds 0.34 is het mogelijk om light groups en scenes automatisch toe te voegen aan Home Assistant.
- ...

Samengevat is er genoeg reden om de code eens goed te herzien en een aantal functionaliteiten toe te voegen, om beter aan te pakken. Het uitgangspunt is om automatiseringen en scripts zo efficient en generiek mogelijk op te stellen. Samengevat:

- [ ] Verlichting per kamer uniform regelen
- [ ] Verwarming per kamer uniform regelen
- [ ] Maximaal gebruik maken van Zigbee-groepen en scenes
- [ ] Opschonen van de codebase

## Automatisering generaliseren per ruimte
...

## Thema 1: verlichting
Deze sectie beschrijft de use-cases voor de verlichting op kamerniveau. De volgende use-cases zijn uitgewerkt:

### 1.1 Het moet mogelijk zijn om per kamer te zien of er voldoende daglicht is
De input hiervoor zijn een of meerdere daglichtsensoren, die in een group worden gegroepeerd. Dat moet via de UI kunnen. Een aparte template-sensor is nodig om het gemeten daglicht te vergelijken met een drempelwaarde. Die drempelwaarde moet kunnen worden ingesteld via de UI.

Sensoren:
    - een of meerdere daglichtsensoren
Helpers:
    - input_number.**ruimte**_daglicht_drempelwaarde: om de drempelwaarde in te stellen
    - group.**ruimte**_daglichtsensoren (via UI): hierin worden alle daglichtsensoren toegevoegd, en de max/min/gem berekend
    - binary_sensor.**ruimte**_daglicht: toetst de group.**ruimte**_daglichtsensoren aan de input_number.**ruimte**_daglicht_drempelwaarde
Automatiseringen: geen

Resultaat:
    - een binary_sensor die als input geldt voor andere use-cases

### 1.2 Het moet mogelijk zijn om per kamer te zien of er personen aanwezig zijn
Hiervoor gebruiken we een of meerdere bewegingssensoren (binary_sensors), die moeten via de UI kunnen worden toegevoegd aan een groep. Dezelfde groep wordt in een aparte template-sensor gebruikt om de aanwezigheid van de kamer aan te geven, inclusief een delay voordat hij naar 'uit' gaat (om te zorgen dat als iemand even stilzit, de lampen niet meteen uitgaat). De delay moet ook via de UI kunnen worden aangepast.

Sensoren:
    - een of meerdere bewegingssensoren
Helpers:
    - input_number.**ruimte**_aanwezigheid_vertraging
    - group.**ruimte**_bewegingssensoren
    - binary_sensor.**ruimte**_aanwezigheid: geeft de status van de group door, en hanteert een delay_off als de group naar 'off' gaat ter hoogte van de waarde van input_number.**ruimte**_aanwezigheid_vertraging
Automatiseringen: geen

Resultaat (output):
    - een binary_sensor die als input geldt voor andere use-cases

### 1.2 Wanneer er aanwezigheid is gedetecteerd gaan de lampen aan afhankelijk van het daglichtniveau
De input hiervan zijn bewegingssensoren

2. Wanneer er geen aanwezigheid van personen is, of het daglicht toereikend is dan gaat de verlichting uit
