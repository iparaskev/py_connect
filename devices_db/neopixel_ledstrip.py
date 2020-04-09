import sys
from pyecore.resources import ResourceSet, URI
sys.path.append(".")

from py_connect.hw_devices import *  # noqa E402


NAME = "devices_db/neopixel_ledstrip.xmi"  # Name of the xmi


dev = Peripheral(vcc=5.0, 
                 name="neopixel_ledstrip",
                 type=PeripheralType.ACTUATOR,
                 operating_voltage=5.,
                 pwms=1)
pin_1 = Power5V(number=1)
pin_2 = DigitalPin(name="data_in", number=2)
pin_3 = Gnd(number=3)

pwm = PWM(pin=pin_2)

dev.pins.extend([pin_1, pin_2, pin_3])
dev.hw_interfaces.extend([pwm])

# Save model
rset = ResourceSet()
r = rset.create_resource(URI(NAME))
r.append(dev)
r.save()
