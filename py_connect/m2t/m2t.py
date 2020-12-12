"""m2t.py

The m2t engine for producing code for handling the code generation.
"""

import os
import autopep8
from jinja2 import Environment, FileSystemLoader
from ..exceptions import NotImplementedDriverError
from ..hw_devices import *
from ..get_impls import ImplementationsGetter


class Generator():
    """Generate code"""

    TEMPLATES = {OSType.RASPBIAN: "pidevices"}
    MSG_MAP = {
        SensorTypes.DISTANCE: "distance",
        SensorTypes.TEMPERATURE: "temperature",
        SensorTypes.HUMIDITY: "humidity",
        SensorTypes.GAS: "gas",
        SensorTypes.PRESSURE: "pressure",
        SensorTypes.ENV: "env",
        SensorTypes.IMU: "imu",
        SensorTypes.ACCELEROMETER: "three_axis",
        SensorTypes.MAGNETOMETER: "three_axis",
        SensorTypes.GYROSCOPE: "three_axis",
        SensorTypes.LINE_FOLLOWER: "lf",
        SensorTypes.BUTTON: "button",
        SensorTypes.BUTTON_ARRAY: "button_array",
        ActuatorTypes.LED: "led",
        ActuatorTypes.LEDS_CONTROLLER: "leds",
        ActuatorTypes.MOTOR_CONTROLLER: "motor_controller",
        ActuatorTypes.SERVO: "servo",
        ActuatorTypes.SERVO_CONTROLLER: "servo_controller",
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

        # Check if an implementation exists
        checker = ImplementationsGetter(tmpl_type)
        if driver_class not in checker.get():
            raise NotImplementedDriverError(
                f"Peripheral {connection.peripheral.name} doesn't have a "
                "pidevices implementation\n"
            )

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

        # Comunication endpoint
        com_endpoint = connection.com_endpoint

        # Create dictionary for data result.
        data_type = "sensor" if is_sensor else "actuator"
        data_tmpl = self.env.get_template(f"{tmpl_type}_{data_type}_data.tmpl")
        for msg_entrie in com_endpoint.msg.msg_entries:
            data_str = data_tmpl.render(msg_type=self.MSG_MAP[msg_entrie.type])
            data_str = data_str.strip("\n")

        # Freq value
        freq = com_endpoint.msg.msg_entries[-1].frequency
        output = tmpl.render(device_class=driver_class,
                             is_sensor=is_sensor,
                             args=args,
                             topic=com_endpoint.topic_name,
                             username=com_endpoint.conn_params.username,
                             password=com_endpoint.conn_params.password,
                             host=com_endpoint.conn_params.host,
                             port=com_endpoint.conn_params.port,
                             data=data_str,
                             freq=freq)
        output = autopep8.fix_code(output)

        return output

    def write_source(self, source_str, name):
        with open(name, "w") as f:
            f.write(source_str)
