"""connections_parser.py"""

from os.path import join, dirname
from textx import metamodel_from_file
from textx.export import metamodel_export, model_export
from pyecore.ecore import BadValueError
from hw_devices_parser import DeviceHandler

import sys
sys.path.append(".")

from py_connect.hw_devices import B2PConnection  # noqa E402
from py_connect.hw_devices.hw_connections import *  # noqa E402
from py_connect.hw_devices.power_connections import *  # noqa E402


class ConnectionsHandler():
    """Class for handling connections"""

    MM_GRAMMAR = join(dirname(__file__), "connection.tx")  # path of grammar
    DEVICE_DB = dirname(__file__)  # path of devices db

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
            p2p_con = Power2Power(pin_1=board.power_pins[p_con.board_power],
                                  pin_2=periph.power_pins[p_con.peripheral_power])
            p2p_con.connect()
            power_connections.append(p2p_con)
        getattr(conn, "power_connections").extend(power_connections)

        # Hardware connections
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


def main():
    connections = ConnectionsHandler("debug_connection.cd")
    print(connections.connections)
    print(connections.connections["rpi_sonar"].board)
    print(connections.connections["rpi_sonar"].peripheral)
    print(connections.connections["rpi_sonar_2"].board)
    print(connections.connections["rpi_sonar_2"].peripheral)
    print(connections.connections["rpi_sonar"].power_connections[0].pin_1.name)


if __name__ == "__main__":
    main()
