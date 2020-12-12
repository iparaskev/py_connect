"""connections_parser.py"""

from os.path import basename
from textx import metamodel_from_file
from pyecore.resources import ResourceSet, URI
from .hw_devices_parser import DeviceHandler
from ..hw_devices import B2PConnection, ComEndpoint, ConnParams, Msg
from ..hw_devices import PeripheralType, SensorTypes, ActuatorTypes
from ..hw_devices import SensorDataType, ActuatorDataType
from ..hw_devices.hw_connections import *
from ..hw_devices.power_connections import *
from ..definitions import CONNECTION_GRAMMAR
from ..exceptions import UnicludedDeviceError


class ConnectionsHandler():
    """Class for handling connections"""

    MM_GRAMMAR = CONNECTION_GRAMMAR  # path of grammar

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

    FREQ_UNITS = {
        "hz": 1,
        "khz": 10**2,
        "mhz": 10**3,
        "ghz": 10**4,
    }

    def __init__(self, connections_file):
        """Constructor"""
        # Get file name
        self._filename = basename(connections_file).split(".")[0]

        # Load metamodel.
        self._hw_mm = metamodel_from_file(self.MM_GRAMMAR, debug=False,
                                          use_regexp_group=True)

        # Load model.
        self._model = self._hw_mm.model_from_file(connections_file)

        # Load initial devices
        self._devices =\
            {i.name: DeviceHandler(i.name + ".hwd") for i in self._model.includes}

        # The connections of the file.
        self.connections = self._create_connections(self._model.connections)

        # Resource set for exporting devices.
        self.rset = ResourceSet()
        self._devs_rsets = {}

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
        board = self.get_device(connection.board.device,
                                connection.board.number)
        periph = self.get_device(connection.peripheral.device,
                                 connection.peripheral.number)

        conn = B2PConnection(name=connection.name,
                             peripheral_impl=connection.impl,
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

        # Communication endpoint
        if connection.com_endpoint:
            conn.com_endpoint = self._create_endpoint(connection.com_endpoint,
                                                      conn.peripheral.type)

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

    def _create_endpoint(self, com_endpoint, per_type):
        """_create_endpoint

        Args:
            com_endpoint ():

        Returns:
        """
        endpoint = ComEndpoint(topic_name=com_endpoint.topic)
        endpoint.conn_params = ConnParams(
            username=com_endpoint.con_params.username,
            password=com_endpoint.con_params.password,
            host=com_endpoint.con_params.host,
            port=com_endpoint.con_params.port
        )

        msg = Msg()
        entries = []
        for name in com_endpoint.msg.msg_entries:
            if per_type == PeripheralType.SENSOR:
                type = getattr(SensorTypes, name.upper())
                entries.append(SensorDataType(type=type))
                if com_endpoint.freq:
                    entries[-1].frequency = \
                        com_endpoint.freq.val \
                        * self.FREQ_UNITS[com_endpoint.freq.unit]
            else:
                type = getattr(ActuatorTypes, name.upper())
                entries.append(ActuatorDataType(type=type))

        msg.msg_entries.extend(entries)
        endpoint.msg = msg

        return endpoint

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
            if key not in self._devices.keys():
                raise UnicludedDeviceError(f"{key} hasn't been included.")

            dev = DeviceHandler(key + ".hwd")
            dev.dev.name = dev_name
            self._devices[dev_name] = dev
        return dev

    def export_xmi(self, connection, path=None):
        """Export model xmi.

        Args:
            connection ():

        Returns:
        """
        try:
            con = self.connections[connection]
        except KeyError:
            print("Invalid connection name.")
        prefix = self._filename
        if path:
            path = path.rstrip("/") + "/"
            prefix = path + prefix

        name = prefix + "_" + con.name + ".xmi"

        # Create resources for exporting
        self._create_rset(con.board, prefix)
        self._create_rset(con.peripheral, prefix)

        # Create connection resource
        r_con = self.rset.create_resource(URI(name))
        r_con.append(con)
        r_con.save()

    def _create_rset(self, dev, prefix):
        """Create a resource for exporting only once.

        Look in a dictionary and if it doesn't exist create and save it.

        Args:
            dev (Device object): The device to look up.
            prefix (str): Filename prefix
        """
        name = dev.name
        try:
            _ = self._devs_rsets[name]
        except KeyError:
            self._devs_rsets[name] =\
                self.rset.create_resource(prefix + "_" + name + ".xmi")
            self._devs_rsets[name].append(dev)
            self._devs_rsets[name].save()
