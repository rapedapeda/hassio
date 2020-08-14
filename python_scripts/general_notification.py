#
# Wordt gebruikt voor algemene notifications
# Stuur de volgende attributen mee:
# recipients (lijst), title, message, thread-id
# Werking: checkt de lijst van recipients
# Itereert en stuurt iedereen het bericht
#
recipients = data.get('recipients').split(',')
title = data.get('title')
message = data.get('message')
threadid = data.get('threadid')

aantal = len(recipients)
#logger.warning("Recipients:  {}".format(recipients))
#logger.warning("Title:  {}".format(title))
#logger.warning("Message:  {}".format(message))
#logger.warning("Thread-id:  {}".format(threadid))

for i in range(aantal):
    recipient = recipients[i]
    service_data = {"title": title, "message": message}
    hass.services.call("notify", recipient, service_data)
    logger.warning("Verstuurd aan:  {}".format(recipient))