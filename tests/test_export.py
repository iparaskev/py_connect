"""test_xmi_export.py"""

import unittest
import os
from pyecore.resources import ResourceSet, URI
from py_connect import DeviceHandler
from py_connect import ConnectionsHandler
from py_connect import I2C, GPIO, PWM, UART, ADC, SPI


cons_path = \
    "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/test_connections/"


def load_model(name):
    """Load a device model from a xmi.
    Args:
        name (str): Name of the device.
    Returns:
        (Device Object): A board or a peripheral device object.
    """
    f_path = os.path.abspath(__file__)
    root_path = "/".join(os.path.dirname(f_path).split("/")[:-1])
    rset = ResourceSet()
    resource = rset.get_resource(URI(root_path + "/models/hw_devices.ecore"))
    mm_root = resource.contents[0]
    rset.metamodel_registry[mm_root.nsURI] = mm_root

    # Load model instance
    r = rset.get_resource(URI(name + ".xmi"))
    return r.contents[0]


class TestExport(unittest.TestCase):

    def test_device_export(self):
        pi = DeviceHandler("rpi_3b_plus.hwd")
        pi.export_xmi()

        model = load_model("rpi_3b_plus")

        for pin_1, pin_2 in zip(pi.dev.pins, model.pins):
            self.assertEqual(pin_1.name, pin_2.name, "Not same pins")
            self.assertEqual(pin_1.number, pin_2.number, "Not same pins")
        for hw_1, hw_2 in zip(pi.dev.hw_interfaces, model.hw_interfaces):
            self.assertEqual(hw_1.name, hw_2.name, "Not same hw")
            if isinstance(hw_1, I2C):
                self.assertEqual(hw_1.sda.name, hw_2.sda.name, "Not same i2c")
                self.assertEqual(hw_1.scl.name, hw_2.scl.name, "Not same i2c")
            elif isinstance(hw_1, GPIO):
                self.assertEqual(hw_1.pin.name, hw_2.pin.name, "Not same gpio")
            elif isinstance(hw_1, SPI):
                self.assertEqual(hw_1.mosi.name, hw_2.mosi.name, "Not same spi")
                self.assertEqual(hw_1.miso.name, hw_2.miso.name, "Not same spi")
                self.assertEqual(hw_1.sclk.name, hw_2.sclk.name, "Not same spi")
                self.assertEqual(hw_1.ce[0].name, hw_2.ce[0].name, "Not same spi")

    def test_connection_export(self):
        con_file = "debug_connection"
        con = ConnectionsHandler(cons_path + con_file + ".cd")
        con_name = "rpi_bme680"
        mem_model = con.connections[con_name]
        con.export_xmi(con_name)
        model = load_model(con_file + "_" + con_name)

        self.assertEqual(mem_model.board.name, model.board.name,
                         "Not same boards")
        self.assertEqual(mem_model.peripheral.name, model.peripheral.name,
                         "Not same peripherals")
        # Check power connections
        for power_1, power_2 in zip(mem_model.power_connections,
                                    model.power_connections):
            self.assertEqual(power_1.pin_1.name, power_2.pin_1.name,
                             "Not same power pins.")
            self.assertEqual(power_1.pin_2.name, power_2.pin_2.name,
                             "Not same power pins.")
        for hw_1, hw_2 in zip(mem_model.hw_connections, model.hw_connections):
            self.assertEqual(hw_1.hwint_1.name, hw_2.hwint_1.name,
                             "Not same hw interfaces.")
            self.assertEqual(hw_1.hwint_2.name, hw_2.hwint_2.name,
                             "Not same hw interfaces.")


if __name__ == "__main__":
    unittest.main()
