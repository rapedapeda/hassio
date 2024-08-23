import appdaemon.plugins.hass.hassapi as hass

#
# Ramon's Hello World App
#
# Args:
#

class HelloWorldRamon(hass.Hass):

  def initialize(self):
     self.log("Hello from Ramon")
