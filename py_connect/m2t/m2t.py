"""m2t.py

The m2t enginge for producing code for handling the code generation.
"""

import os
import autopep8
from jinja2 import Environment, FileSystemLoader
from ..hw_devices import *


class Generator():
    """Generate code"""

    def __init__(self):
        """Construct the generator."""

        path = os.path.dirname(os.path.abspath(__file__))
        # Load templates
        file_loader = FileSystemLoader(path + "/templates")
        self.env = Environment(loader=file_loader)

    def generate(self, comp_device):
        """Genearate code from a device.

        Args:
            comp_device (Device object): A computational device object. That 
                has n connected devices.

        Returns:
            (str): A string that contains the generated code.
        """
        # TODO: Use different template regarding the type of the board
        # For example raspberry pi, riot ...
        tmpl_type = "pidevices"

        # Iterate through all connected devices
        for dev in comp_device.devices:
            if dev.type == DeviceType.SENSOR:
                tmpl = self.env.get_template(tmpl_type + "_sensor.py.tmpl")
                args = {}  # Arguments for the driver constructor

                if isinstance(dev, GpioDevice):

                    # Get information from pins.
                    for pin in dev.gpio_pins:
                        if isinstance(pin, GpioInput):
                            args[pin.conn_from.name] = pin.conn_from.number

                        if isinstance(pin, GpioOutput):
                            args[pin.conn_to.name] = pin.conn_to.number

                # handle i2c devices
                if isinstance(dev, I2cDevice):
                    args['bus'] = dev.i2c_bus

            # Generate code for device
            output = tmpl.render(device_class=dev.name, args=gpio_pins)
            output = autopep8.fix_code(output)

        return output

    def _handle_gpio(self, device):
        """_handle_gpio

        Args:
            device ():

        Returns:
        """
        pass
