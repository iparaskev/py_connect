"""connections_parser.py"""

from os.path import join, dirname
from textx import metamodel_from_file
from textx.export import metamodel_export, model_export
from pyecore.ecore import BadValueError
from pyecore.resources import ResourceSet, URI

import sys
sys.path.append(".")

from py_connect.hw_devices_language.hw_devices_parser import DeviceHandler # noqa E402
from py_connect.hw_devices import B2PConnection # noqa E402
from py_connect.hw_devices.hw_connections import *  # noqa E402
from py_connect.hw_devices.power_connections import *  # noqa E402


class ConnectionsHandler():
    """Class for handling connections"""

    MM_GRAMMAR = join(dirname(__file__), "connection.tx")  # path of grammar
    #TODO fix this ugly thing when the structure will be ready
    DEVICE_DB = "/home/iasonas/Projects/thesis/devices_db"

    # Map for the hw interface connections.
    CONN_MAP = {
        "power": Power2Power,
        "gpio": Gpio2Gpio,
        "i2c": I2c2I2c,
        "spi": Spi2Spi,
        "uart": Uart2Uart,
        "pwm": Pwm2Pwm,
        "adc": Adc2Adc,
    }

    def __init__(self, connections_file):
        """Constructor"""
        # Load metamodel.
        self._hw_mm = metamodel_from_file(self.MM_GRAMMAR, debug=False)

        # Load model.
        self._model = self._hw_mm.model_from_file(join(self.DEVICE_DB,
                                                       connections_file))

        # Load initial devices
        self._devices =\
            {i.name: DeviceHandler(i.name + ".hwd") for i in self._model.includes}

        # The connections of the file.
        self.connections = self._create_connections(self._model.connections)

    def _create_connections(self, connections):
        conns = {}
        for connection in connections:
            if connection.name in conns.keys():
                # TODO: Throw exception of duplcicate name
                print("Duplciate connection name.")
                pass
            # handle connection
            conns[connection.name] = self._instantiate_con(connection)

        return conns

    def _instantiate_con(self, connection):
        # Get device handler objects for faster manipulation.
        board = self.get_device(connection.board)
        periph = self.get_device(connection.peripheral.device,
                                 connection.peripheral.number)

        conn = B2PConnection(name=connection.name,
                             board=board.dev,
                             peripheral=periph.dev)
        # Power connections
        power_connections = []
        for p_con in connection.power_conns:
            #TODO: key error means wrong pin name of device
            p2p_con =\
                self._create_conn(self.CONN_MAP["power"], "pin_1",
                                  board.power_pins[p_con.board_power], "pin_2",
                                  periph.power_pins[p_con.peripheral_power])
            power_connections.append(p2p_con)
        getattr(conn, "power_connections").extend(power_connections)

        # Hardware connections
        hw_connections = []
        for h_conn in connection.hw_conns:
            h2h_con =\
                self._create_conn(
                    self.CONN_MAP[h_conn.type], "hwint_1",
                    board.hw_interfaces[h_conn.type][h_conn.board_int], "hwint_2",
                    periph.hw_interfaces[h_conn.type][h_conn.peripheral_int]
                )

            # Extra steps for specific hw interfaces.
            if h_conn.type == "i2c":
                h2h_con.slave_address = int(str(h_conn.slave_addr), 16)
            elif h_conn.type == "uart":
                h2h_con.baudrate = h_conn.baudrate
            # TODO: Use multiplier
            elif h_conn.type == "pwm":
                h2h_con.frequency = h_conn.frequency.val
            hw_connections.append(h2h_con)
        getattr(conn, "hw_connections").extend(hw_connections)

        return conn

    def _create_conn(self, clss, key_1, val_1, key_2, val_2):
        """_create_connection

        Args:
            key_1 ():
            val_1 ():
            key_2 ():
            val_2 ():

        Returns:
        """
        args = {key_1: val_1, key_2: val_2}
        conn = clss(**args)
        conn.connect()
        return conn

    def get_device(self, key, number=0):
        """Get a device handler instance for the connection.

        Args:
            key (str): The name of the device in the db.
            number (int): An intiger indicating if it is the same device or
                different.

        Returns:
            (DeviceHandler object): A device handler instance.
        """
        dev_name = f"{key}_{number}" if number else key
        try:
            dev = self._devices[dev_name]
        except KeyError:
            dev = DeviceHandler(key + ".hwd")
            self._devices[dev_name] = dev
        return dev

    def export_xmi(self, connection):
        """Export model xmi.

        Args:
            connection ():

        Returns:
        """
        try:
            con = self.connections[connection]
        except KeyError:
            print("Invalid connection name.")
        prefix = self.DEVICE_DB + "/" + con.name
        name = prefix + ".xmi"
        # Save model
        rset = ResourceSet()
        r = rset.create_resource(URI(name))
        r_b = rset.create_resource(prefix + "_board.xmi")
        r_p = rset.create_resource(prefix + "_peripheral.xmi")
        r_b.append(con.board)
        r_p.append(con.peripheral)
        r.append(con)
        r.save()
        r_b.save()
        r_p.save()
