import sys
from pyecore.resources import ResourceSet
sys.path.append(".")

from py_connect.hw_devices import *  # noqa E402


NAME = "rpi_3b_plus.xmi"  # Name of the xmi


dev = Computational(vcc=5.0, name="pi_3", cpu_family=CpuFamily.ARM_CORTEX_A,
                    max_freq=1400, ram=1000, external_memory=16000,
                    fpu=True, dma=True, wifi=True, 
                    ble=True, ethernet=True, timers=1,
                    rtc=False, usb2s=4, i2cs=2, 
                    spis=2, uarts=2, pwms=2)
pin_1 = PowerPin(function=PowerType.POWER_3V3, number=1)
pin_2 = PowerPin(function=PowerType.POWER_5V, number=2)
pin_3 = DigitalPin(name="bcm_2", number=3,
                   functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0),
                              IOPinFunction(type=IOType.I2C_SDA, hw_port=1)]) 
pin_4 = PowerPin(function=PowerType.POWER_5V, number=4)
pin_5 = DigitalPin(name="bcm_3", number=5,
                   functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0),
                              IOPinFunction(type=IOType.I2C_SCL, hw_port=1)]) 
pin_6 = PowerPin(function=PowerType.GND, number=6)
pin_7 = DigitalPin(name="bcm_4", number=7,
                   functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0),
                              IOPinFunction(type=IOType.GPCLK, hw_port=0)]) 
pin_8 = DigitalPin(name="bcm_14", number=8,
                   functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0),
                              IOPinFunction(type=IOType.UART_TX, hw_port=0)]) 
pin_9 = PowerPin(function=PowerType.GND, number=9)
pin_10 = DigitalPin(name="bcm_15", number=10,
                    functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0),
                               IOPinFunction(type=IOType.UART_RX, hw_port=0)]) 
pin_11 = DigitalPin(name="bcm_17", number=11,
                    functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0),
                               IOPinFunction(type=IOType.SPI_CE, hw_port=1)])
pin_12 = DigitalPin(name="bcm_18", number=12,
                    functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0),
                               IOPinFunction(type=IOType.PWM, hw_port=0),
                               IOPinFunction(type=IOType.SPI_CE, hw_port=1)]) 
pin_13 = DigitalPin(name="bcm_27", number=13,
                    functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0)])
pin_14 = PowerPin(function=PowerType.GND, number=14)
pin_15 = DigitalPin(name="bcm_22", number=15,
                    functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0)])
pin_16 = DigitalPin(name="bcm_23", number=16,
                    functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0)])
pin_17 = PowerPin(function=PowerType.POWER_3V3, number=17)
pin_18 = DigitalPin(name="bcm_24", number=18,
                    functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0)])
pin_19 = DigitalPin(name="bcm_10", number=19,
                    functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0),
                               IOPinFunction(type=IOType.SPI_MOSI, hw_port=0)]) 
pin_20 = PowerPin(function=PowerType.GND, number=20)
pin_21 = DigitalPin(name="bcm_9", number=21,
                    functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0),
                               IOPinFunction(type=IOType.SPI_MISO, hw_port=0)]) 
pin_22 = DigitalPin(name="bcm_25", number=22,
                    functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0)])
pin_23 = DigitalPin(name="bcm_11", number=23,
                    functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0),
                               IOPinFunction(type=IOType.SPI_SCLK, hw_port=0)]) 
pin_24 = DigitalPin(name="bcm_8", number=24,
                    functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0),
                               IOPinFunction(type=IOType.SPI_CE, hw_port=0)])
pin_25 = PowerPin(function=PowerType.GND, number=25)
pin_26 = DigitalPin(name="bcm_7", number=26,
                    functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0),
                               IOPinFunction(type=IOType.SPI_CE, hw_port=0)])
pin_27 = DigitalPin(name="bcm_0", number=27,
                    functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0),
                               IOPinFunction(type=IOType.I2C_SDA, hw_port=0)])
pin_28 = DigitalPin(name="bcm_1", number=28,
                    functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0),
                               IOPinFunction(type=IOType.I2C_SCL, hw_port=0)])
pin_29 = DigitalPin(name="bcm_5", number=29,
                    functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0)])
pin_30 = PowerPin(function=PowerType.GND, number=30)
pin_31 = DigitalPin(name="bcm_6", number=31,
                    functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0)])
pin_32 = DigitalPin(name="bcm_12", number=32,
                    functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0),
                               IOPinFunction(type=IOType.PWM, hw_port=0)])
pin_33 = DigitalPin(name="bcm_13", number=33,
                    functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0),
                               IOPinFunction(type=IOType.PWM, hw_port=1)])
pin_34 = PowerPin(function=PowerType.GND, number=34)
pin_35 = DigitalPin(name="bcm_19", number=35,
                    functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0),
                               IOPinFunction(type=IOType.PWM, hw_port=1),
                               IOPinFunction(type=IOType.SPI_MISO, hw_port=1)]) 
pin_36 = DigitalPin(name="bcm_16", number=36,
                    functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0),
                               IOPinFunction(type=IOType.SPI_CE, hw_port=1)])
pin_37 = DigitalPin(name="bcm_26", number=37,
                    functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0)])
pin_38 = DigitalPin(name="bcm_20", number=38,
                    functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0),
                               IOPinFunction(type=IOType.SPI_MOSI, hw_port=1)])
pin_39 = PowerPin(function=PowerType.GND, number=39)
pin_40 = DigitalPin(name="bcm_21", number=40,
                    functions=[IOPinFunction(type=IOType.GPIO_BOTH, hw_port=0),
                               IOPinFunction(type=IOType.SPI_SCLK, hw_port=1)])

dev.pins.extend([pin_1, pin_2, pin_3, pin_4, pin_5, pin_6, pin_7, pin_8,
                 pin_9, pin_10, pin_11, pin_12, pin_13, pin_14, pin_16, pin_16,
                 pin_17, pin_18, pin_19, pin_20, pin_21, pin_22, pin_23, pin_24,
                 pin_25, pin_26, pin_27, pin_28, pin_29, pin_30, pin_31, pin_32,
                 pin_33, pin_34, pin_35, pin_36, pin_37, pin_38, pin_39, pin_40])

# Save model
rset = ResourceSet()
r = rset.create_resource(URI(NAME))
r.append(dev)
r.save()
