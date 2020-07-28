"""test_connections.py"""

import unittest
import os
from py_connect import ConnectionsHandler
from py_connect import Board, Peripheral, Distance, Temperature, Humidity, Gas


cons_path = \
    "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/test_connections/"


class TestConnection(unittest.TestCase):

    def test_gpio_connection(self):
        connections = ConnectionsHandler(cons_path + "debug_connection.cd")
        gpio_con = connections.connections["rpi_sonar"]
        gpio_con_2 = connections.connections["rpi_sonar_2"]

        # Good connection
        # Just check args
        self.assertEqual(gpio_con.name, "rpi_sonar", "Wrong connection name.")
        self.assertIsInstance(gpio_con.board, Board, "Should be board.")
        self.assertIsInstance(gpio_con.peripheral, Peripheral,
                              "Should be peripheral.")
        self.assertEqual(gpio_con.board.name, "rpi_3b_plus",
                         "Should be rpi_3b_plus")
        self.assertEqual(gpio_con.peripheral.name, "hc_sr04",
                         "Should be hc_sr04")
        # Check right power connections.
        self.assertEqual(gpio_con.power_connections[0].pin_1,
                         self.target(gpio_con.board.pins, "gnd_1"),
                         "Should be gnd_1.")
        self.assertEqual(gpio_con.power_connections[0].pin_2,
                         self.target(gpio_con.peripheral.pins, "gnd"),
                         "Should be gnd.")
        self.assertEqual(gpio_con.power_connections[1].pin_1,
                         self.target(gpio_con.board.pins, "power_5v_1"),
                         "Should be power_5v_1.")
        self.assertEqual(gpio_con.power_connections[1].pin_2,
                         self.target(gpio_con.peripheral.pins, "vcc"),
                         "Should be vcc.")

        # Check right hw_connections
        self.assertEqual(gpio_con.hw_connections[0].hwint_1,
                         self.target(gpio_con.board.hw_interfaces, "bcm_7"),
                         "Should be bcm_23")
        self.assertEqual(gpio_con.hw_connections[0].hwint_2,
                         self.target(gpio_con.peripheral.hw_interfaces, "echo"),
                         "Should be echo")
        self.assertEqual(gpio_con.hw_connections[1].hwint_1,
                         self.target(gpio_con.board.hw_interfaces, "bcm_24"),
                         "Should be bcm_24")
        self.assertEqual(gpio_con.hw_connections[1].hwint_2,
                         self.target(gpio_con.peripheral.hw_interfaces, "trigger"),
                         "Should be trigger.")

        # Different objects of same device
        self.assertNotEqual(gpio_con.peripheral, gpio_con_2.peripheral,
                            "Should be different.")

    def target(self, ls, name):
        for p in ls:
            if p.name == name:
                return p

    def test_i2c(self):
        connections = ConnectionsHandler(cons_path + "debug_connection.cd")
        i2c_con = connections.connections["rpi_bme680"]

        self.assertEqual(i2c_con.hw_connections[0].hwint_1,
                         self.target(i2c_con.board.hw_interfaces, "i2c_1"),
                         "Should be i2c_1 of rpi.")
        self.assertEqual(i2c_con.hw_connections[0].hwint_2,
                         self.target(i2c_con.peripheral.hw_interfaces, "i2c_0"),
                         "Should be i2c_0 of bme.")
        self.assertEqual(i2c_con.hw_connections[0].slave_address, int(0x77),
                         "Should be 0x77.")

    def test_spi(self):
        connections = ConnectionsHandler(cons_path + "debug_connection.cd")
        spi_con = connections.connections["rpi_icm"]

        self.assertEqual(spi_con.hw_connections[0].hwint_1,
                         self.target(spi_con.board.hw_interfaces, "spi_0"),
                         "Should be spi_0 of rpi.")
        self.assertEqual(spi_con.hw_connections[0].hwint_2,
                         self.target(spi_con.peripheral.hw_interfaces, "spi_0"),
                         "Should be spi_0 of bme.")
        ce_index = spi_con.hw_connections[0].ce_index
        ce_pin = spi_con.hw_connections[0].hwint_1.ce[ce_index]
        self.assertEqual(ce_pin.name, "bcm_8", "Should be bcm_8.")

    def test_comm_endpoint(self):
        connections = ConnectionsHandler(cons_path + "debug_connection.cd")
        con = connections.connections["rpi_sonar"]

        # Simple communication checks
        self.assertEqual(con.com_endpoint.topic_name, "sonar_1.distance")
        self.assertEqual(con.com_endpoint.conn_params.username,
                         "testuser", "Should be testuser.")
        self.assertEqual(con.com_endpoint.conn_params.password,
                         "testuser", "Should be testuser.")
        self.assertEqual(con.com_endpoint.conn_params.host,
                         "r4a-platform.ddns.net", "Should be ...")
        self.assertEqual(con.com_endpoint.conn_params.port,
                         5782, "Should be 5782")
        self.assertIsInstance(con.com_endpoint.msg.msg_entries[0], Distance)

        con = connections.connections["rpi_bme680"]
        self.assertIsInstance(con.com_endpoint.msg.msg_entries[0], Temperature)
        self.assertIsInstance(con.com_endpoint.msg.msg_entries[1], Humidity)
        self.assertIsInstance(con.com_endpoint.msg.msg_entries[2], Gas)


if __name__ == "__main__":
    unittest.main()
