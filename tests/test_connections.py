import unittest
import sys
sys.path.append(".")

from py_connect.m2t.m2t import Generator  # noqa E402
from py_connect.hw_devices import B2PConnection  # noqa E402
from py_connect.hw_devices.hw_connections import *  # noqa E402
from py_connect.hw_devices.power_connections import *  # noqa E402
from py_connect.model_loader import *  # noqa E402


class TestConnections(unittest.TestCase):
    """Test meta model connections."""

    def test_sonar_pi(self):
        """Test a connection between a pi and a sonar."""
        pi = load_model_py("rpi_3b_plus")
        sonar = load_model_py("hc_sr04")
        generator = Generator()

        connection = B2PConnection(board=pi, peripheral=sonar)

        # Power connections
        gnd_con = Power2Power(board_power=pi.pins[5],
                              peripheral_power=sonar.pins[3])
        source_con = Power2Power(board_power=pi.pins[1],
                                 peripheral_power=sonar.pins[0])

        # Hw interfaces connections
        echo = HwInt2HwInt(board_hw=pi.hw_interfaces[0],
                           peripheral_hw=sonar.hw_interfaces[1])
        trigger = HwInt2HwInt(board_hw=pi.hw_interfaces[1],
                              peripheral_hw=sonar.hw_interfaces[0])

        # Check connections
        gnd_con.connect()
        source_con.connect()
        echo.connect()
        trigger.connect()

        connection.hw_int_connections.extend([echo, trigger])
        connection.power_connections.extend([gnd_con, source_con])

        source = generator.generate(connection)
        print(source)

    def test_icm_pi(self):
        """Test an spi connection"""
        pi = load_model_py("rpi_3b_plus")
        imu = load_model_py("icm_20948")
        generator = Generator()

        connection = B2PConnection(board=pi, peripheral=imu)

        # Power connections
        gnd_con = Power2Power(board_power=pi.pins[5],
                              peripheral_power=imu.pins[0])
        source_con = Power2Power(board_power=pi.pins[0],
                                 peripheral_power=imu.pins[1])

        spi_t = HwInt2HwInt(board_hw=pi.hw_interfaces[-3],
                            peripheral_hw=pi.hw_interfaces[-2])
        spi_con = HwInt2HwInt(board_hw=pi.hw_interfaces[-3],
                              peripheral_hw=imu.hw_interfaces[0])

        # Check connections
        gnd_con.connect()
        source_con.connect()
        spi_t.connect()
        spi_con.connect()

        connection.hw_int_connections.extend([spi_con])
        connection.power_connections.extend([gnd_con, source_con])

        source = generator.generate(connection)
        print(source)


if __name__ == "__main__":
    unittest.main()
