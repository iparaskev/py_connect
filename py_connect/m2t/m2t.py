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
    MAPPER = {"pidevices": PIDEVICES_MAP}

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
        driver_class = self.MAPPER[tmpl_type][connection.peripheral.name]

        # Constructor args
        args = {}

        for hw_conn in connection.hw_int_connections:
            # Handle gpio connection
            if isinstance(hw_conn.board_hw, GPIO) \
               or isinstance(hw_conn.board_hw, PWM):
                args[hw_conn.peripheral_hw.pin.name] = \
                    int(hw_conn.board_hw.pin.name.split("_")[-1])

            # Handle i2c connection
            if isinstance(hw_conn.board_hw, I2C):
                args["bus"] = hw_conn.board_hw.bus

            # Handle spi connection
            # TODO: Which chip enable pin?
            if isinstance(hw_conn.board_hw, SPI):
                args["port"] = hw_conn.board_hw.bus
                args["device"] = \
                    hw_conn.board_hw.master_conns.index(hw_conn.peripheral_hw)

            # Handle uart connection
            if isinstance(hw_conn.board_hw, UART):
                pass

        output = tmpl.render(device_class=driver_class,
                             is_sensor=is_sensor,
                             args=args)
        output = autopep8.fix_code(output)

        return output
