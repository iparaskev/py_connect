import sys
from devices_models import *
sys.path.append(".")

from py_connect.hw_devices import *  # noqa E402
from py_connect.m2t.m2t import Generator  # noqa E402
from py_connect.model_validator.validator import Validator  # noqa E402


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

    m2t.generate(pi.pi)


def generate_vl():
    """Generate vl"""
    pi = Pi()
    tof = VL53L1X()
    val = Validator()
    m2t = Generator()

    # Make connections
    connection = ConnectedDevice(device=tof.tof)
    connection.pins_connections.append(ConnectedPins(comp_pin=pi.gnd_1,
                                                     non_comp_pin=tof.gnd_1))
    connection.pins_connections.append(
        ConnectedPins(comp_pin=pi.power_5_1,
                      non_comp_pin=tof.power_5_1))
    connection.pins_connections.append(ConnectedPins(comp_pin=pi.bcm_2,
                                                     non_comp_pin=tof.pin_1))
    connection.pins_connections.append(ConnectedPins(comp_pin=pi.bcm_3,
                                                     non_comp_pin=tof.pin_2))
    pi.pi.connected_devices.append(connection)
    ret = val.validate_connection(pi.pi)

    m2t.generate(pi.pi)


generate_sonar()
generate_vl()
