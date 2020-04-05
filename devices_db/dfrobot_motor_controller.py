import sys
from pyecore.resources import ResourceSet, URI
sys.path.append(".")

from py_connect.hw_devices import *  # noqa E402


NAME = "devices_db/dfrobot_motor_controller.xmi"  # Name of the xmi


dev = NonComputational(vcc=5.0, name="motor_controller", type=DeviceType.ACTUATOR)
pin_1 = DigitalPin(name="m1", number=1,
                   functions=[IOPinFunction(type=IOType.GPIO_INPUT, hw_port=0)])
pin_2 = DigitalPin(name="e1", number=2,
                   functions=[IOPinFunction(type=IOType.PWM, hw_port=0)])
pin_3 = DigitalPin(name="m2", number=3,
                   functions=[IOPinFunction(type=IOType.GPIO_INPUT, hw_port=0)])
pin_4 = DigitalPin(name="e2", number=4,
                   functions=[IOPinFunction(type=IOType.PWM, hw_port=0)])

dev.pins.extend([pin_1, pin_2, pin_3, pin_4])

# Save model
rset = ResourceSet()
r = rset.create_resource(URI(NAME))
r.append(dev)
r.save()
