# Roadmap

Mogelijke uitbreidingen en verbeteringen voor de toekomst.

---

## Energie: Slimme batterijsturing

**Doel:** Marstek Venus E 5.12 kWh optimaal inzetten op basis van dynamische energieprijzen (EnergyZero).

**Strategie:**
- Ontladen naar net tijdens dure uren (17:00–20:00, of prijs > drempel)
- Altijd 2.6 kWh (~51% SOC) reserveren voor nachtverbruik (19:00–07:00)
- Terugvallen op zelfverbruik buiten dure uren

**Beschikbare entiteiten:**
- `select.marstek_venus_e_5_12kwh_3nd_gen_battery_mode` — batterijmodus
- `number.marstek_venus_e_5_12kwh_3nd_gen_minimum_soc` — minimale SOC (harde grens)
- `sensor.marstek_venus_e_5_12kwh_3nd_gen` — huidige SOC (verifieer entiteitnaam)
- `sensor.energyzero_today_energy_current_hour_price` — actuele uurprijs
- `sensor.energyzero_today_energy_percentage_of_max` — prijs als % van dagmaximum

**Beoogde packagestructuur:**
```
packages/energie/batterij/
  helpers.yaml    — exportdrempel (€/kWh), nachtreserve (%), auto boolean
  sensoren.yaml   — binary_sensor.batterij_exporteren_voordelig
  strategie.yaml  — automations export starten/stoppen
```

**Openstaand:** exacte modesnamen van de battery mode select verifiëren in HA.

**Optioneel later:** goedkope nachturen benutten om batterij bij te laden van het net.

---

## Klimaat: Voorverwarming

**Doel:** Kamers voorverwarmen op basis van opwarmsnelheid, zodat de gewenste temperatuur precies op tijd bereikt wordt.

**Benodigde infrastructuur (deels geparkeerd):**
- Derivative sensor op `sensor.temperatuur_woonkamer` → opwarmsnelheid (°C/min)
- Statistics sensor voor gemiddelde opwarmsnelheid
- Binary sensor per kamer: "moet nu al beginnen met verwarmen?"

---

## Zonwering: Wintermodus

**Overweging:** In de winter is de instraling nooit hoog genoeg om zonwering te activeren (maandcheck 3–10). Geen aparte modus nodig — de huidige logica werkt gewoon minder. Monitoren of dit in de praktijk voldoende is.
