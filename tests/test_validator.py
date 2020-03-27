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
        self.assertEqual(ret, False, "Should be True")

        ret = val._check_power(pi.gnd_1, sonar.power_5_1)
        self.assertEqual(ret, True, "Should be False")

        ret = val._check_power(pi.gnd_1, sonar.pin_1)
        self.assertEqual(ret, True, "Should be False")

        ret = val._check_power(pi.bcm_2, sonar.pin_1)
        self.assertEqual(ret, None, "Should be None")

    def test_check_io_type(self):
        """Test power functions."""
        pi = Pi()
        tof = VL53L1X()
        val = Validator()
        
        fs = {}
        for f in pi.bcm_2.functions:
            fs[f.type] = True

        ret = val._check_io_type(tof.pin_1.functions[0].type,
                                 [IOType.I2C_SDA, IOType.PWM, IOType.I2C_SCL],           
                                 fs, tof.pin_1.functions[0].type, "Same")
        self.assertEqual(ret, True, "Should be True")

        fs = {}
        for f in pi.bcm_5.functions:
            fs[f.type] = True
        ret = val._check_io_type(tof.pin_1.functions[0].type,
                                 [IOType.I2C_SDA, IOType.PWM, IOType.I2C_SCL],           
                                 fs, tof.pin_1.functions[0].type, "Same")
        self.assertEqual(ret, False, "Should be False")


if __name__ == "__main__":
    unittest.main()
