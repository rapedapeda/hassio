import appdaemon.plugins.hass.hassapi as hass

class MediaModule:
    def __init__(self, app, room_name, media):
        self.app = app
        self.room_name = room_name
        self.media = media

    def run(self):
        self.app.log(f"Starting media module for {self.room_name}")
        # Voeg hier je zonwering logic toe

