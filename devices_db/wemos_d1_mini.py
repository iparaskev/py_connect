import sys
from pyecore.resources import ResourceSet, URI
sys.path.append(".")

from py_connect.hw_devices import *  # noqa E402


NAME = "devices_db/wemos_d1_mini.xmi"  # Name of the xmi


dev = Board(vcc=3.3,
            operating_voltage=3.3,
            name="wemos_d1_mini", 
            cpu=CPU(cpu_family=CpuFamily.ESP8266, max_freq=160.),
            memory=Memory(ram=0.8, rom=16.),
            wireless=Wireless(wifi=True),
            timers=1,
            i2cs=1, 
            spis=1,
            uarts=1,
            adcs=1,
            battery=True,
            digital_pins=11)

pin_1 = DigitalPin(name="reset", number=1)
pin_2 = AnalogPin(name="a0", number=2, vmax=3.3)
pin_3 = DigitalPin(name="d0", number=3)
pin_4 = DigitalPin(name="d5", number=4)
pin_5 = DigitalPin(name="d6", number=5)
pin_6 = DigitalPin(name="d7", number=6)
pin_7 = DigitalPin(name="d8", number=7)
pin_8 = Power3V3(number=8)
pin_9 = DigitalPin(name="tx", number=9)
pin_10 = DigitalPin(name="rx", number=10)
pin_11 = DigitalPin(name="d1", number=11)
pin_12 = DigitalPin(name="d2", number=12)
pin_13 = DigitalPin(name="d3", number=13)
pin_14 = DigitalPin(name="d4", number=14)
pin_15 = Gnd(number=15)
pin_16 = Power5V(number=16)

uart = UART(tx=pin_9, rx=pin_10)
adc = ADC(pin=pin_2)
i2c = I2C(sda=pin_11, scl=pin_12)
spi = SPI(mosi=pin_6, miso=pin_5, sclk=pin_4, ce=[pin_7])
gpio_1 = GPIO(pin=pin_3, type=GPIOType.BOTH)
gpio_2 = GPIO(pin=pin_4, type=GPIOType.BOTH)
gpio_3 = GPIO(pin=pin_5, type=GPIOType.BOTH)
gpio_4 = GPIO(pin=pin_6, type=GPIOType.BOTH)
gpio_5 = GPIO(pin=pin_7, type=GPIOType.BOTH)
gpio_6 = GPIO(pin=pin_12, type=GPIOType.BOTH)
gpio_7 = GPIO(pin=pin_13, type=GPIOType.BOTH)
gpio_8 = GPIO(pin=pin_11, type=GPIOType.BOTH)
gpio_9 = GPIO(pin=pin_14, type=GPIOType.BOTH)

dev.pins.extend([pin_1, pin_2, pin_3, pin_4, pin_5, pin_6, pin_7, pin_8,
                 pin_9, pin_10, pin_11, pin_12, pin_13, pin_14, pin_15]) 

dev.hw_interfaces.extend([gpio_1, gpio_2, gpio_3, gpio_4, gpio_5, gpio_6, 
                          gpio_7, gpio_8, gpio_9, uart, adc, i2c, spi])

# Save model
rset = ResourceSet()
r = rset.create_resource(URI(NAME))
r.append(dev)
r.save()
