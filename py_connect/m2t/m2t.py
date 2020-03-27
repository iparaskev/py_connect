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

    def generate(self, device):
        """Genearate code from a device.

        Args:
            device (Computational object): A computational device object. That 
                has n connected devices.

        Returns:
            (str): A string that contains the generated code.
        """
        # TODO: Use different template regarding the type of the board
        # For example raspberry pi, riot ...
        tmpl_type = "pidevices"
        
        tmpl = self.env.get_template(tmpl_type + ".py.tmpl")

        for con_dev in device.connected_devices:
            # Get if it is sensor or actuator
            is_sensor = \
                True if con_dev.device.type == DeviceType.SENSOR else False

            # Get name of driver implementation.
            driver_class = con_dev.device.driver_name

            # Constructor args
            args = {}

            # From pins get constructor arguments.
            for pins in con_dev.pins_connections:
                if isinstance(pins.non_comp_pin, PowerPin):
                    continue
                pin_func = pins.non_comp_pin.functions[0].type

                # Gpio pins
                if pin_func == IOType.GPIO_INPUT or \
                   pin_func == IOType.GPIO_OUTPUT or \
                   pin_func == IOType.GPIO_BOTH or \
                   pin_func == IOType.PWM:
                    args[pins.non_comp_pin.name] = pins.comp_pin.number

                if pin_func == IOType.I2C_SDA or pin_func == IOType.I2C_SCL:
                    for f in pins.comp_pin.functions:
                        if f.type == pin_func:
                            args['bus'] = f.hw_port
            
            output = tmpl.render(device_class=driver_class,
                                 is_sensor=is_sensor,
                                 args=args)
            output = autopep8.fix_code(output)
            print(output)

        return ""


