#
# Als een input_boolean wordt getriggerd
# Loopt over de attributen (kamers,scenes)
# Itereert en zet alle kamers op de goede scene
#

entity_id = data.get('entity_id')
aantal = len(hass.states.get(entity_id).attributes['kamers'])
kamers = hass.states.get(entity_id).attributes['kamers']
scenes = hass.states.get(entity_id).attributes['scenes']

for i in range(aantal):
    entity = f'kamer_scenes_{kamers[i]}'
    option = scenes[i]
    service_data = {"entity_id": entity, "option": option}
    hass.services.call("input_select", "select_option", service_data, False)