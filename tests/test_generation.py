import sys
sys.path.append(".")

from py_connect.hw_devices import *  # noqa E402
from py_connect.m2t.m2t import Generator  # noqa E402


# Create a raspberry pi
pi = Computational(operating_voltage=3.3)
pi_power = Power5V(name="pi_5v")
pi_gnd = Gnd(name="pi_gnd")
pi_echo = GpioInput(number=14, name="echo_pin")
pi_trigger = GpioOutput(number=15, name="trigger_pin")
pi.power_pins.extend([pi_power, pi_gnd])
pi.pins.extend([pi_echo, pi_trigger])

# Create a sonar
sonar = GpioDevice(operating_voltage=5.0, type=DeviceType.SENSOR)
sonar.driver = "HcSr04RPiGPIO"
sonar_power = Power5V(name="sonar_5v")
sonar_gnd = Gnd(name="sonar_gnd")
sonar_echo = GpioOutput(number=3, name="echo")
sonar_trigger = GpioInput(number=4, name="trigger")
sonar.power_pins.extend([sonar_power, sonar_gnd])
sonar.gpio_pins.extend([sonar_echo, sonar_trigger])

# Create vl53l1x
tof = I2cDevice(operating_voltage=3.3, type=DeviceType.SENSOR)
tof.driver = "VL53L1X"
sonar_power = Power5V(name="sonar_5v")
sonar_gnd = Gnd(name="sonar_gnd")
sonar_echo = GpioOutput(number=3, name="echo")
sonar_trigger = GpioInput(number=4, name="trigger")
# Make a connection
pi.devices.append(sonar)
pi_power.conn_to.append(sonar_power)
pi_gnd.conn_to.append(sonar_gnd)
pi_echo.conn_from = sonar_echo
pi_trigger.conn_to = sonar_trigger

# Create validator
gen = Generator()

print(gen.generate(pi))
