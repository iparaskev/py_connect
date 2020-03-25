import sys
sys.path.append(".")

from py_connect.hw_devices import *  # noqa E402
from py_connect.m2t import m2t  # noqa E402


# Create a raspberry pi
pi = Computational(operating_voltage=3.3)
pi_power = Power5V(number=2, name="pi_5v")
pi_gnd = Gnd(number=6, name="pi_gnd")
pi_echo = Input(number=14, name="echo_pin")
pi_trigger = Output(number=15, name="trigger_pin")
pi.pins.extend([pi_power, pi_gnd, pi_echo, pi_trigger])

# Create a sonar
sonar = NonComputational(operating_voltage=5.0, type=DeviceType.SENSOR)
sonar.name = "HcSr04RPiGPIO"
sonar_power = Power5V(number=1, name="sonar_5v")
sonar_gnd = Gnd(number=2, name="sonar_gnd")
sonar_echo = Output(number=3, name="echo")
sonar_trigger = Input(number=4, name="trigger")
sonar.pins.extend([sonar_power, sonar_gnd, sonar_echo, sonar_trigger])

# Make a connection
pi.devices.append(sonar)
pi_power.conn_to.append(sonar_power)
pi_gnd.conn_to.append(sonar_gnd)
pi_echo.conn_from = sonar_echo
pi_trigger.conn_to = sonar_trigger

m2t.generate(pi)
