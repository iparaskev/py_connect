"""test_m2t.py"""

import unittest
import os
from py_connect import Generator
from py_connect import ConnectionsHandler
#from py_connect import Board, Peripheral, Distance, Temperature, Humidity, Gas


cons_path = \
    "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/test_connections/"


class TestM2t(unittest.TestCase):

    def test_simple_m2t(self):
        connections = ConnectionsHandler(cons_path + "debug_connection.cd")
        m2t = Generator()

        gpio_con = connections.connections["rpi_sonar"]

        gpio_source = m2t.generate(gpio_con)
        comu_source = m2t.generate_com(gpio_con)

        #print(comu_source)
        m2t.write_source(comu_source, "test_pub.py")


if __name__ == "__main__":
    unittest.main()
