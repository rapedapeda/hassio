# Home Assistant configuratie (v2024)

Welkom! Deze repository bevat de configuratie voor mijn smart home-setup die continu wordt geoptimaliseerd. Het doel van deze setup is om een gebruiksvriendelijke, robuuste en schaalbare oplossing te bieden voor het automatiseren van verschillende aspecten van ons huis.

## Uitgangspunten

De configuratie is opgebouwd rondom enkele belangrijke ontwerpprincipes:

### Ruimteniveau, Verdiepingsniveau en Huisniveau

Door automatiseringen te structureren per kamer, verdieping of het hele huis, kunnen scripts en instellingen efficiënt worden hergebruikt. Dit maakt de codebase klein, overzichtelijk en consistent in gebruik. HomeAssistant groepeert entiteiten per ruimte in 'Areas', en sinds v2024.4 kunnen ruimtes ook gegroepeerd worden in 'Floors' en met labels. Hierdoor is het mogelijk om bijvoorbeeld één automatisering voor verlichting te schrijven die alle kamers bedient.

### Pluggable Design

De setup is flexibel opgezet zodat niet elke kamer dezelfde functies of apparaten hoeft te bevatten. Dit betekent bijvoorbeeld dat niet elke ruimte een media-speler heeft, of dat sommige kamers geavanceerdere sensoren hebben dan andere. De configuratie blijft daardoor modulair en makkelijk uit te breiden zonder alles opnieuw te hoeven inrichten.

### Complexe Logica in AppDaemon

Voor eenvoudige automatiseringen wordt YAML gebruikt, maar voor complexe processen is gekozen voor AppDaemon. Dit stelt ons in staat om één app te schrijven die meerdere kamers, verdiepingen of het hele huis beheert. Dit maakt het mogelijk om complexe automatiseringen centraal te beheren en code herbruikbaar en overzichtelijk te houden.

## Beschrijving van functies

De automatiseringen zijn opgesplitst in verschillende thema’s, afhankelijk van het niveau waarop ze actief zijn (ruimte, verdieping, of huis).

### Verlichting

*Werkt op ruimteniveau*

De verlichting schakelt automatisch op basis van aanwezigheid en omgevingslicht (binnen en buiten). De logica houdt rekening met tijd van de dag, de stand van de gordijnen of rolluiken, en eventuele manuele bedieningen via fysieke schakelaars. Door gebruik te maken van Zigbee-scenes en groepen wordt het netwerk ontlast en werkt de bediening ook bij uitval van HomeAssistant.

### Verwarming

*Werkt op ruimteniveau*

De verwarming wordt 100% lokaal geregeld met Tado-apparaten via HomeKit. Automatische schema’s voor verschillende dagtypes en aanwezigheid zorgen voor een optimale temperatuur per kamer. Hierdoor kan de verwarming flexibel inspelen op veranderende situaties zonder afhankelijk te zijn van cloudservices.

### Zonwering

*Werkt op ruimteniveau*

De zonwering reageert op de stand van de zon, de temperatuur in de betreffende kamer en weersomstandigheden zoals wind en regen. Hoewel er momenteel gebruik wordt gemaakt van KNMI-data voor zonintensiteit en buitentemperatuur, is er in de toekomst ruimte voor een lokaal weerstation om de afhankelijkheid van cloudservices verder te verkleinen.

### Ventilatie

*Werkt op huisniveau*

De ventilatie wordt automatisch aangepast op basis van CO2-niveaus en luchtvochtigheid in verschillende ruimtes. Een Tasmota-aangestuurde WTW-installatie zorgt voor de aansturing. De automatisering imiteert daarnaast de bypass-functie om het huis ’s zomers extra te koelen tijdens koele nachten.

### Beveiliging

*Werkt op huisniveau*

De beveiliging schakelt automatisch in bij afwezigheid en waarschuwt bij beweging of open ramen en deuren. Integratie met HomeKit zorgt voor een eenvoudige bediening en meldingen, zonder afhankelijk te zijn van cloudservices.

### Stofzuigen

*Werkt op verdiepingsniveau*

De robots voor verschillende verdiepingen werken volgens een schoonmaakschema dat rekening houdt met aanwezigheid en frequentie. Ze passen hun schema’s automatisch aan tijdens vakanties en verplaatsen zich naar een vooraf ingestelde locatie bij een volle opvangbak.

## Toekomstige verbeteringen en roadmap

De configuratie blijft in ontwikkeling. Toekomstige plannen omvatten onder andere:

    - Integratie van een lokaal weerstation voor nauwkeurige data.
    - Optimalisatie van bestaande AppDaemon-apps voor nog efficiëntere code.
    - Verdere automatisering van huishoudelijke taken zoals het beheer van apparaten en energiebesparing.
    - Automatische volgsysteem van multi-room-audio op basis van locatie van personen in huis.