import sys
from pyecore.resources import ResourceSet, URI
sys.path.append(".")

from py_connect.hw_devices import *  # noqa E402


NAME = "devices_db/hc_sr04.xmi"  # Name of the xmi


dev = Peripheral(vcc=5.0, 
                 name="hc_sr04_sonar",
                 type=PeripheralType.SENSOR,
                 operating_voltage=5.,
                 digital_pins=2)
pin_1 = Power5V(number=1)
pin_2 = DigitalPin(name="trigger", number=2)
pin_3 = DigitalPin(name="echo", number=3)
pin_4 = Gnd(number=4)

gpio_1 = GPIO(pin=pin_2, type=GPIOType.INPUT)
gpio_2 = GPIO(pin=pin_3, type=GPIOType.OUTPUT)

dev.pins.extend([pin_1, pin_2, pin_3, pin_4])
dev.hw_interfaces.extend([gpio_1, gpio_2])

# Save model
rset = ResourceSet()
r = rset.create_resource(URI(NAME))
r.append(dev)
r.save()
