#
# Als een input_boolean wordt getriggerd
# Loopt over de attributen (kamers,scenes)
# Itereert en zet alle kamers op de goede scene
#

entity_id = data.get('entity_id')
kamers = data.get('kamers').split(',')
scenes = data.get('scenes').split(',')
aantal = len(kamers)
logger.warning("kamers  {}".format(kamers))
logger.warning("Scenes  {}".format(scenes))
logger.warning("Aantal  {}".format(aantal))

for i in range(aantal):
    entity = f'kamer_scenes_{kamers[i]}'
    option = scenes[i]
    service_data = {"entity_id": entity, "option": option}
    hass.services.call("input_select", "select_option", service_data, False)