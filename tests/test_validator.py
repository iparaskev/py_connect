import unittest
import sys
from devices_models import *
sys.path.append(".")

from py_connect.hw_devices import *  # noqa E402
from py_connect.model_validator.validator import Validator  # noqa E402


class TestValidator(unittest.TestCase):
    """Test meta model connections."""

    def test_power(self):
        """Test power functions."""
        pi = Pi()
        sonar = SonarHC_SRO4()
        val = Validator()

        ret = val._check_power(pi.gnd_1, sonar.gnd_1)
        self.assertEqual(ret, True, "Should be True")

        ret = val._check_power(pi.gnd_1, sonar.power_5_1)
        self.assertEqual(ret, False, "Should be False")

        ret = val._check_power(pi.gnd_1, sonar.pin_1)
        self.assertEqual(ret, False, "Should be False")

        ret = val._check_power(pi.bcm_2, sonar.pin_1)
        self.assertEqual(ret, None, "Should be None")

    def test_io_checks(self):
        """Test power functions."""
        pi = Pi()
        tof = VL53L1X()
        sonar = SonarHC_SRO4()
        val = Validator()
        
        # gpio-gpio
        ret = val._io_checks(pi.bcm_2, sonar.pin_1)
        self.assertEqual(ret, True, "Should be True")

        # i2c-gpio
        ret = val._io_checks(tof.pin_2, sonar.pin_1)
        self.assertEqual(ret, False, "Should be False")

        # i2c_sda-i2_sdc
        val._cur_i2c = {IOType.I2C_SDA: False, IOType.I2C_SCL: False}
        ret = val._io_checks(pi.bcm_2, tof.pin_2)
        self.assertEqual(ret, False, "Should be False")

        # i2c_sda-i2_sda
        ret = val._io_checks(pi.bcm_2, tof.pin_1)
        self.assertEqual(ret, True, "Should be True")


if __name__ == "__main__":
    unittest.main()
