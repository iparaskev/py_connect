"""m2t.py

The m2t engine for producing code for handling the code generation.
"""

import os
import autopep8
from jinja2 import Environment, FileSystemLoader
from ..hw_devices import *


class Generator():
    """Generate code"""

    TEMPLATES = {OSType.RASPBIAN: "pidevices"}
    PIDEVICES_MAP = {
        "hc_sr04": "HcSr04RPiGPIO",
        "icm_20948": "ICM_20948"
    }

    def __init__(self):
        """Construct the generator."""

        path = os.path.dirname(os.path.abspath(__file__))

        # Load templates
        file_loader = FileSystemLoader(path + "/templates")
        self.env = Environment(loader=file_loader)

    def generate(self, connection):
        """Genearate code for a connection

        Args:
            connection (B2PConnection object): A connection between a board and
                a peripheral device.

        Returns:
            (str): A string that contains the generated code.
        """
        # TODO: Use different template regarding the type of the board
        # For example raspberry pi, riot ...
        tmpl_type = self.TEMPLATES[connection.board.os]

        tmpl = self.env.get_template(tmpl_type + ".py.tmpl")

        # Get if it is sensor or actuator
        is_sensor = \
            True if connection.peripheral.type == PeripheralType.SENSOR else False

        # Get name of driver implementation.
        driver_class = connection.peripheral_impl

        # Constructor args
        args = {}

        for hw_conn in connection.hw_connections:
            # Handle gpio or pwm connection
            if isinstance(hw_conn, Gpio2Gpio) or isinstance(hw_conn, Pwm2Pwm):
                args[hw_conn.hwint_2.pin.name] = \
                    int(hw_conn.hwint_1.pin.name.split("_")[-1])
            # Handle i2c connection
            elif isinstance(hw_conn, I2c2I2c):
                args["bus"] = hw_conn.hwint_1.bus
            # Handle spi connection
            elif isinstance(hw_conn, Spi2Spi):
                args["port"] = hw_conn.hwint_1.bus
                args["device"] = hw_conn.ce_index
            # Handle uart connection
            elif isinstance(hw_conn, Uart2Uart):
                pass

        output = tmpl.render(device_class=driver_class,
                             is_sensor=is_sensor,
                             args=args)
        output = autopep8.fix_code(output)

        return output
