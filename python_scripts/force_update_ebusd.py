entity_id = hass.states.entity_ids()

expanded_a_group = True
while entity_id and expanded_a_group:
    expanded_a_group = False
    for e in entity_id:
        if e.startswith('group.'):
            entity_id.remove(e)
            g = hass.states.get(e)
            if g and 'entity_id' in g.attributes:
                entity_id.extend(g.attributes['entity_id'])
                expanded_a_group = True

logger.info("Updating entities")

updated = []
for e in entity_id:
    if e.startswith('sensor.ebusd'):
        service_data = {'entity_id': e}
        if service_data in updated:
          continue
        updated.append(service_data)
        hass.services.call('homeassistant',
                           'update_entity',
                           service_data)
        logger.info(str(service_data));

logger.info("Finished updating entities")
