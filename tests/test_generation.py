import sys
from test.devices_models import *
sys.path.append(".")

from py_connect.hw_devices import *  # noqa E402
from py_connect.m2t.m2t import Generator  # noqa E402


def generate_sonar():
    """Generate driver for sonar."""
    pi = Pi()
    sonar = SonarHC_SRO4()
    val = Validator()
    m2t = Generator()

    # Make connections
    connection = ConnectedDevice(device=sonar.sonar)
    connection.pins_connections.append(ConnectedPins(comp_pin=pi.gnd_1,
                                                     non_comp_pin=sonar.gnd_1))
    connection.pins_connections.append(
        ConnectedPins(comp_pin=pi.power_5_1,
                      non_comp_pin=sonar.power_5_1))
    connection.pins_connections.append(ConnectedPins(comp_pin=pi.bcm_5,
                                                     non_comp_pin=sonar.pin_1))
    connection.pins_connections.append(ConnectedPins(comp_pin=pi.bcm_6,
                                                     non_comp_pin=sonar.pin_2))
    pi.pi.connected_devices.append(connection)
    ret = val.validate_connection(pi.pi)
