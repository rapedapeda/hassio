#
# Als een input_boolean wordt getriggerd
# Loopt over de attributen (kamers,scenes)
# Itereert en zet alle kamers op de goede scene
#
kamer = data.get('kamer').split(',')
scene = data.get('scene').split(',')
aantal = len(kamer)
#logger.warning("kamers  {}".format(kamers))
#logger.warning("Scenes  {}".format(scenes))
#logger.warning("Aantal  {}".format(aantal))

for i in range(aantal):
    entity = f'input_select.kamer_scenes_modus_{kamer[i]}'
    option = scene[i]
    service_data = {"entity_id": entity, "option": option}
    hass.services.call("input_select", "select_option", service_data, False)