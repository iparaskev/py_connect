import unittest
import sys
sys.path.append(".")

from python_models.hw_devices import *  # noqa E402
from pyecore.valuecontainer import BadValueError  # noqa E402


class TestMetaModel(unittest.TestCase):
    """Test meta model connections."""
    
    def __init__(self, *args, **kwargs):
        """Create some custom devices."""
        super().__init__(*args, **kwargs)
        #self._create_pi()

    def _create_pi(self):
        # Create a raspberry pi
        self.pi = Device(operating_voltage=3.3)
        self.pi_power = Power5V(number=2, name="pi_5v")
        self.pi_gnd = Gnd(number=6, name="pi_gnd")
        self.pi_echo = Input(number=8, name="bcm_14")
        self.pi_trigger = Output(number=10, name="bcm_15")

        # Append pins to raspberry
        self.pi.pins.append(self.pi_power)
        self.pi.pins.append(self.pi_gnd)
        self.pi.pins.append(self.pi_echo)
        self.pi.pins.append(self.pi_trigger)
   
    def _create_esp32(self):
        """Create an esp32."""
        self.esp = Device(operating_voltage=3.3)
        self.esp_power = Power5V(number=2, name="esp_5v")
        self.esp_gnd = Gnd(number=6, name="esp_gnd")

    def _create_sonar(self):
        """Create a hc sr04 sonar."""
        self.sonar = Device(operating_voltage=5.0)
        self.sonar_power = Power5V(number=1, name="sonar_5v")
        self.sonar_gnd = Gnd(number=2, name="sonar_gnd")
        self.sonar_echo = Output(number=3, name="echo")
        self.sonar_trigger = Input(number=4, name="trigger")

        # Append pins to sonar
        self.sonar.pins.append(self.sonar_power)
        self.sonar.pins.append(self.sonar_gnd)
        self.sonar.pins.append(self.sonar_echo)
        self.sonar.pins.append(self.sonar_trigger)

    def test_creation(self):
        """Test the creation of a device."""
        pi = Device(operating_voltage=3.3)
        pi_power = Power5V(number=2, name="pi_5v")
        pi_gnd = Gnd(number=6, name="pi_gnd")
        pi_echo = Input(number=8, name="bcm_14")
        pi_trigger = Output(number=10, name="bcm_15")

        # Append pins to raspberry
        pi.pins.append(pi_power)
        self.assertEqual(pi.pins[0], pi_power, "Should be the same object")

        pi.pins.append(pi_gnd)
        self.assertEqual(pi.pins[1], pi_gnd, "Should be the gnd object")

        pi.pins.append(pi_echo)
        self.assertEqual(pi.pins[2], pi_echo, "Should be the echo object")

        pi.pins.append(pi_trigger)
        self.assertEqual(pi.pins[3], pi_trigger, "Should be the trigger object")

    def test_power_connections(self):
        """Test a connections between a raspberry pi and a sonar."""

        # Create devices
        self._create_pi()
        self._create_sonar()
        self._create_esp32()

        # Check proper connections.
        # Simple assertion
        self.pi_power.conn_to.append(self.sonar_power)
        self.assertEqual(self.sonar_power.conn_from, self.pi_power,
                         "Should be connected to the pi power.")

        # Wrong assertion
        with self.assertRaises(BadValueError):
            self.pi_power.conn_to.append(self.sonar_gnd)

        self.pi_gnd.conn_to.append(self.sonar_gnd)
        self.assertEqual(self.sonar_gnd.conn_from[0], self.pi_gnd,
                         "Should be connected to the pi gnd.")

    def test_sonar_complete(self):
        """Test complete connection of pi and sonar."""
        # Create devices
        self._create_pi()
        self._create_sonar()
        
        self.pi_power.conn_to.append(self.sonar_power)
        self.pi_gnd.conn_to.append(self.sonar_gnd)

        self.pi_echo.conn_from = self.sonar_echo
        self.assertEqual(self.sonar_echo.conn_to, self.pi_echo,
                         "Should be connected to the pi echo.")
        with self.assertRaises(BadValueError):
            self.pi_trigger.conn_to = self.sonar_echo

        self.pi_trigger.conn_to = self.sonar_trigger
        self.assertEqual(self.sonar_trigger.conn_from, self.pi_trigger,
                         "Should be connected to the pi echo.")


if __name__ == '__main__':
    unittest.main()
