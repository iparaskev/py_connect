import sys
sys.path.append(".")

from py_connect.hw_devices import *  # noqa E402


class Pi():
    """Make a pi model."""

    def __init__(self):
        self.pi = Computational(operating_voltage=3.3, name="my_pi")
        self.gnd_1 = PowerPin(function=PowerType.GND, number=6)
        self.gnd_2 = PowerPin(function=PowerType.GND, number=9)
        self.gnd_3 = PowerPin(function=PowerType.GND, number=14)
        self.gnd_4 = PowerPin(function=PowerType.GND, number=20)
        self.gnd_5 = PowerPin(function=PowerType.GND, number=30)
        self.gnd_6 = PowerPin(function=PowerType.GND, number=34)
        self.gnd_7 = PowerPin(function=PowerType.GND, number=39)
        self.gnd_8 = PowerPin(function=PowerType.GND, number=25)
        self.power_3_1 = PowerPin(function=PowerType.POWER_3V3, number=1)
        self.power_3_2 = PowerPin(function=PowerType.POWER_3V3, number=17)
        self.power_5_1 = PowerPin(function=PowerType.POWER_5V, number=2)
        self.power_5_2 = PowerPin(function=PowerType.POWER_5V, number=4)
        self.bcm_2 = IOPin(name="bcm_2",
                           number=2,
                           functions=[IOPinFunction(type=IOType.GPIO_BOTH,
                                                    hw_port=-1),
                                      IOPinFunction(type=IOType.I2C_SDA,
                                                    hw_port=1)])
        self.bcm_3 = IOPin(name="bcm_3",
                           number=3,
                           functions=[IOPinFunction(type=IOType.GPIO_BOTH,
                                                    hw_port=-1),
                                      IOPinFunction(type=IOType.I2C_SCL,
                                                    hw_port=1)])
        self.bcm_5 = IOPin(name="bcm_5",
                           number=5,
                           functions=[IOPinFunction(type=IOType.GPIO_BOTH,
                                                    hw_port=-1)])
        self.bcm_6 = IOPin(name="bcm_6",
                           number=6,
                           functions=[IOPinFunction(type=IOType.GPIO_BOTH,
                                                    hw_port=-1)])
        self.pi.pins.extend([self.gnd_1, self.gnd_2, self.gnd_3, self.gnd_4,
                             self.gnd_5, self.gnd_6, self.gnd_7, self.gnd_8,
                             self.power_3_1, self.power_3_2, self.power_5_1,
                             self.power_5_2, self.bcm_2, self.bcm_3, self.bcm_5,
                             self.bcm_6])


class SonarHC_SRO4():
    """A sonar device."""

    def __init__(self):
        self.sonar = NonComputational(operating_voltage=3.3, name="my_sonar")
        self.gnd_1 = PowerPin(function=PowerType.GND, number=1)
        self.power_5_1 = PowerPin(function=PowerType.POWER_5V, number=2)
        self.pin_1 = IOPin(name="echo",
                           number=3,
                           functions=[IOPinFunction(type=IOType.GPIO_OUTPUT,
                                                    hw_port=-1)])
        self.pin_2 = IOPin(name="trigger",
                           number=4,
                           functions=[IOPinFunction(type=IOType.GPIO_INPUT,
                                                    hw_port=-1)])
        self.sonar.pins.extend([self.gnd_1, self.power_5_1, self.pin_1,
                                self.pin_2])


class VL53L1X():
    """Bme sensor."""

    def __init__(self):
        self.tof = NonComputational(operating_voltage=3.3, name="tof")
        self.gnd_1 = PowerPin(function=PowerType.GND, number=1)
        self.power_5_1 = PowerPin(function=PowerType.POWER_5V, number=2)
        self.pin_1 = IOPin(name="sda",
                           number=3,
                           functions=[IOPinFunction(type=IOType.I2C_SDA,
                                                    hw_port=-1)])
        self.pin_2 = IOPin(name="trigger",
                           number=4,
                           functions=[IOPinFunction(type=IOType.I2C_SCL,
                                                    hw_port=-1)])
        self.tof.pins.extend([self.gnd_1, self.power_5_1, self.pin_1,
                              self.pin_2])

