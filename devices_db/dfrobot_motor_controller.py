import sys
from pyecore.resources import ResourceSet, URI
sys.path.append(".")

from py_connect.hw_devices import *  # noqa E402


NAME = "devices_db/dfrobot_motor_controller.xmi"  # Name of the xmi


dev = Peripheral(vcc=5.0,
                 name="motor_controller",
                 type=PeripheralType.ACTUATOR,
                 operating_voltage=5.)
pin_1 = DigitalPin(name="m1", number=1)
pin_2 = DigitalPin(name="e1", number=2)
pin_3 = DigitalPin(name="m2", number=3)
pin_4 = DigitalPin(name="e2", number=4)

gpio_1 = GPIO(pin=pin_1, type=GPIOType.INPUT)
gpio_2 = GPIO(pin=pin_3, type=GPIOType.INPUT)

pwm_1 = PWM(pin=pin_2, frequency=50)
pwm_2 = PWM(pin=pin_4, frequency=50)

dev.pins.extend([pin_1, pin_2, pin_3, pin_4])
dev.hw_interfaces.extend([gpio_1, gpio_2, pwm_1, pwm_2])

# Save model
rset = ResourceSet()
r = rset.create_resource(URI(NAME))
r.append(dev)
r.save()
