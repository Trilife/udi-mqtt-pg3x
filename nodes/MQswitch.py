"""
mqtt-poly NodeServer/Plugin for EISY/Polisy

(C) 2024

node MQSwitch
"""

import udi_interface

LOGGER = udi_interface.LOGGER

class MQSwitch(udi_interface.Node):
    id = "mqsw"
    
    """
    This is the class that all the Nodes will be represented by. You will
    add this to Polyglot/ISY with the interface.addNode method.
    """

    def __init__(self, polyglot, primary, address, name, device):
        """
        Super runs all the parent class necessities.
        :param polyglot: Reference to the Interface class
        :param primary: Parent address
        :param address: This nodes address
        :param name: This nodes name
        """
        super().__init__(polyglot, primary, address, name)

        self.controller = self.poly.getNode(self.primary)
        self.cmd_topic = device["cmd_topic"]
        self.on = False

    def updateInfo(self, payload, topic: str):
        if payload == "ON":
            if not self.on:
                self.reportCmd("DON")
                self.on = True
            self.setDriver("ST", 100)
        elif payload == "OFF":
            if self.on:
                self.reportCmd("DOF")
                self.on = False
            self.setDriver("ST", 0)
        else:
            LOGGER.error("Invalid payload {}".format(payload))

    def set_on(self, command):
        self.on = True
        self.controller.mqtt_pub(self.cmd_topic, "ON")

    def set_off(self, command):
        self.on = False
        self.controller.mqtt_pub(self.cmd_topic, "OFF")

    def query(self, command=None):
        """
        Called by ISY to report all drivers for this node. This is done in
        the parent class, so you don't need to override this method unless
        there is a need.
        """
        self.controller.mqtt_pub(self.cmd_topic, "")
        self.reportDrivers()
        
    # all the drivers - for reference
    drivers = [
        {"driver": "ST", "value": 0, "uom": 78, "name": "Power"}
    ]

    """
    This is a dictionary of commands. If ISY sends a command to the NodeServer,
    this tells it which method to call. DON calls setOn, etc.
    """
    commands = {
        "QUERY": query,
        "DON": set_on,
        "DOF": set_off
    }

    hint = [4, 2, 0, 0]
