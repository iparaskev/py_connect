import sys
from pyecore.resources import ResourceSet, URI
sys.path.append(".")

from py_connect.hw_devices import *  # noqa E402


NAME = "devices_db/wemos_d1_mini.xmi"  # Name of the xmi


dev = Computational(vcc=3.3, name="wemos_d1_mini", cpu_family=CpuFamily.XTENSA,
                    max_freq=160, ram=0.8, rom=16,
                    wifi=True, timers=1, i2cs=2, 
                    spis=1, uarts=1, adcs=1,
                    battery=True, digital_pins=13)
pin_1 = DigitalPin(name="reset", number=1,
                   functions=[IOPinFunction(type=IOType.RST)])
pin_2 = AnalogPin(name="a0", number=2, vmax=3.3)
pin_3 = DigitalPin(name="d0", number=3,
                   functions=[IOPinFunction(type=IOType.GPIO_BOTH)])
pin_4 = DigitalPin(name="d5", number=4,
                   functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0),
                              IOPinFunction(type=IOType.SPI_SCLK, hw_port=0)]) 
pin_5 = DigitalPin(name="d6", number=5,
                   functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0),
                              IOPinFunction(type=IOType.SPI_MISO, hw_port=0)]) 
pin_6 = DigitalPin(name="d7", number=6,
                   functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0),
                              IOPinFunction(type=IOType.SPI_MOSI, hw_port=0)]) 
pin_7 = DigitalPin(name="d8", number=7,
                   functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0),
                              IOPinFunction(type=IOType.SPI_CE, hw_port=0)]) 
pin_8 = PowerPin(function=PowerType.POWER_3V3, number=8)
pin_9 = DigitalPin(name="tx", number=9,
                   functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0),
                              IOPinFunction(type=IOType.UART_TX, hw_port=0)]) 
pin_10 = DigitalPin(name="rx", number=10,
                    functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0),
                               IOPinFunction(type=IOType.UART_RX, hw_port=0)]) 
pin_11 = DigitalPin(name="d1", number=11,
                    functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0),
                               IOPinFunction(type=IOType.I2C_SCL, hw_port=0)]) 
pin_12 = DigitalPin(name="d2", number=12,
                    functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0),
                               IOPinFunction(type=IOType.I2C_SDA, hw_port=0)]) 
pin_13 = DigitalPin(name="d3", number=13,
                    functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0)])
pin_14 = DigitalPin(name="d4", number=14,
                    functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0)])
pin_14 = PowerPin(function=PowerType.GND, number=14)
pin_15 = PowerPin(function=PowerType.POWER_5V, number=15)

dev.pins.extend([pin_1, pin_2, pin_3, pin_4, pin_5, pin_6, pin_7, pin_8,
                 pin_9, pin_10, pin_11, pin_12, pin_13, pin_14, pin_15]) 

# Save model
rset = ResourceSet()
r = rset.create_resource(URI(NAME))
r.append(dev)
r.save()
