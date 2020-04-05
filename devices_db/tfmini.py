import sys
from pyecore.resources import ResourceSet, URI
sys.path.append(".")

from py_connect.hw_devices import *  # noqa E402


NAME = "devices_db/tfmini.xmi"  # Name of the xmi


dev = NonComputational(vcc=5.0, name="hc_sr04_sonar", type=DeviceType.SENSOR)
pin_1 = PowerPin(function=PowerType.POWER_5V, number=1)
pin_2 = PowerPin(function=PowerType.GND, number=2)
pin_3 = DigitalPin(name="tx", number=3,
                   functions=[IOPinFunction(type=IOType.GPIO_INPUT, hw_port=0),
                              IOPinFunction(type=IOType.UART_TX)])
pin_4 = DigitalPin(name="rx", number=4,
                   functions=[IOPinFunction(type=IOType.GPIO_INPUT, hw_port=0),
                              IOPinFunction(type=IOType.UART_RX)])

dev.pins.extend([pin_1, pin_2, pin_3, pin_4])

# Save model
rset = ResourceSet()
r = rset.create_resource(URI(NAME))
r.append(dev)
r.save()
