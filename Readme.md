# HomeAssistant v3 Roadmap
In versie drie gaat over naar AppDeamon voor logica en automatiseringen.


## Roadmap

De grootste stap van v2 naar v3 is de overstap van AppDeamon voor logica en automatiseringen. HomeAssistant blijft de basis om de verschillende platformen (Zigbee, MQTT, HomeKit etcetera) aan elkaar te knopen. Maar voor o.a. alle automatiseringen maken we gebruik van AppDeamon in plaats van YAML. Daarnaast is deze stap een reden om de codebase grondig tegen het licht te houden, en om enkele nieuwe functionaliteiten toe te voegen en te verbeteren.

De hoofdthemas zijn als volgt, en worden hieronder toegelicht:

- [ ] Ruimtes als objecten configureren, 
- [ ] Daarnaast Apps per overkoepelend thema
- [ ] Direct gebruik maken van Zigbee-groepen en scenes
- [ ] Opschonen codebase

### Ruimtes als objecten
Op dit moment groepeert HomeAssistant een aantal (alle) entiteiten per ruimte in eenzelfde 'Area'. Aan deze areas hebben geen status, of attributen. Wanneer een ruimte een entiteit is, met een status/attributen, dan kunnen we veel functionaliteiten hergebruiken en generaliseren. 



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


    
