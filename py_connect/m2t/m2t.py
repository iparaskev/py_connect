"""m2t.py

The m2t enginge for producing code for handling the code generation.
"""

import os
import autopep8
from jinja2 import Environment, FileSystemLoader
from ..hw_devices import *


def generate(comp_device):
    """Generate code"""
    path = "/".join(os.path.dirname(os.path.abspath(__file__)).split("/")[:])

    file_loader = FileSystemLoader(path + "/templates")
    env = Environment(loader=file_loader)

    # Iterate through all connected devices
    for dev in comp_device.devices:
        if dev.type == DeviceType.SENSOR:
            tmpl = env.get_template("pidevices_sensor.py.tmpl")
            
            # Dictionary with the gpio pins
            gpio_pins = {}
            i2c_bus = None
            spi_bus = None

            # Get information from pins.
            for pin in dev.pins:

                # GPIO Pins
                if isinstance(pin, Input):
                    gpio_pins[pin.conn_from.name] = pin.conn_from.number

                if isinstance(pin, Output):
                    gpio_pins[pin.conn_to.name] = pin.conn_to.number

        # Generate code for device
        output = tmpl.render(device_class=dev.name, args=gpio_pins)
        output = autopep8.fix_code(output)
        print(output)

