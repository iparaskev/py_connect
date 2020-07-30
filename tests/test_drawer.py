"""test_m2t.py"""

import unittest
import os
from py_connect import Drawer
from py_connect import ConnectionsHandler
#from py_connect import Board, Peripheral, Distance, Temperature, Humidity, Gas


cons_path = \
    "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/test_connections/"


class TestDrawer(unittest.TestCase):

    def test_draw(self):
        connections = ConnectionsHandler(cons_path + "debug_connection.cd")
        drawer = Drawer()

        gpio_con = connections.connections["rpi_sonar"]
        motor_con = connections.connections["rpi_dfrobot"]
        bme_con = connections.connections["rpi_bme680"]

        #drawer.draw_connection(gpio_con)
        drawer.draw_connection(bme_con)
        drawer.save("test.png")


if __name__ == "__main__":
    unittest.main()
