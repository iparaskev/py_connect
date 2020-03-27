import unittest
import sys
from devices_models import *
sys.path.append(".")

from py_connect.hw_devices import *  # noqa E402
from py_connect.model_validator.validator import Validator  # noqa E402


class TestMetaModel(unittest.TestCase):
    """Test meta model connections."""

    def test_one_connection(self):
        """Test a connection between a pi and a sonar."""
        pi = Pi()
        sonar = SonarHC_SRO4()
        val = Validator()

        # Make a connection
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
        self.assertEqual(ret, True, "Should be True")

        # Wrong connections
        connection.pins_connections.append(
            ConnectedPins(comp_pin=pi.power_5_1,
                          non_comp_pin=pi.power_5_2))
        ret = val.validate_connection(pi.pi)
        self.assertEqual(ret, False, "Should be False")
        connection.pins_connections.pop()

        connection.pins_connections.append(
            ConnectedPins(comp_pin=pi.power_5_1,
                          non_comp_pin=sonar.pin_1))
        ret = val.validate_connection(pi.pi)
        self.assertEqual(ret, False, "Should be False")
        connection.pins_connections.pop()

        connection.pins_connections.append(
            ConnectedPins(comp_pin=pi.power_5_1,
                          non_comp_pin=sonar.gnd_1))
        ret = val.validate_connection(pi.pi)
        self.assertEqual(ret, False, "Should be False")
        connection.pins_connections.pop()


if __name__ == "__main__":
    unittest.main()
