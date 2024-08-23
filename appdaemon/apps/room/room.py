import appdaemon.plugins.hass.hassapi as hass
from .lighting import LightinModule
from .climate import ClimateModule
from .shading import ShadingModule
from .media import MediaModule

class Room(hass.Hass):

    def initialize(self):
        self.room_name = self.args.get("room_name")
        self.motion_sensor = self.args.get("motion_sensor")
        self.light_sensor = self.args.get("light_sensor")
        self.light_threshold = self.args.get("light_threshold")
        self.light_delay = self.args.get("light_delay")
        self.lights = self.args.get("lights")
        self.climate = self.args.get("climate")
        self.climate_schedule = self.args.get("climate_schedule")
        self.media_player = self.args.get("media_player")
        self.shading = self.args.get("shading")

        self.log(f"Initializing Room: {self.room_name}")

        # Activeer verlichting als de bijbehorende sensoren en drempelwaarden aanwezig zijn
        if self.motion_sensor and self.light_sensor and self.lights:
            self.run_lighting_module()

        # Activeer klimaatregeling als de entiteiten aanwezig zijn
        if self.climate and self.climate_schedule:
            self.run_climate_module()

        # Activeer zonwering als de entiteit aanwezig is
        if self.shading:
            self.run_shading_module()

        # Activeer mediaspeler als de entiteit aanwezig is
        if self.media_player:
            self.run_media_module()

