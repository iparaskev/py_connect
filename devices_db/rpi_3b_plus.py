import sys
from pyecore.resources import ResourceSet, URI
sys.path.append(".")

from py_connect.hw_devices import *  # noqa E402


NAME = "devices_db/rpi_3b_plus.xmi"  # Name of the xmi


dev = Board(vcc=5.0, 
            name="pi_3", 
            operating_voltage=3.3, 
            cpu=CPU(cpu_family=CpuFamily.ARM_CORTEX_A, max_freq=1400., fpu=True),
            memory=Memory(ram=1000., external_memory=16000.),
            wireless=Wireless(wifi=True, ble=True),
            ethernet=True,
            timers=1,
            dma=True,
            usb2s=4,
            i2cs=2,
            spis=2,
            uarts=1,
            pwms=2,
            digital_pins=28)

pin_1 = Power3V3(number=1)
pin_2 = Power5V(number=2)
pin_3 = DigitalPin(name="bcm_2", number=3)
pin_4 = Power5V(number=4)
pin_5 = DigitalPin(name="bcm_3", number=5)
pin_6 = Gnd(number=6)
pin_7 = DigitalPin(name="bcm_4", number=7)
pin_8 = DigitalPin(name="bcm_14", number=8)
pin_9 = Gnd(number=9)
pin_10 = DigitalPin(name="bcm_15", number=10)
pin_11 = DigitalPin(name="bcm_17", number=11)
pin_12 = DigitalPin(name="bcm_18", number=12)
pin_13 = DigitalPin(name="bcm_27", number=13)
pin_14 = Gnd(number=14)
pin_15 = DigitalPin(name="bcm_22", number=15)
pin_16 = DigitalPin(name="bcm_23", number=16)
pin_17 = Power3V3(number=17)
pin_18 = DigitalPin(name="bcm_24", number=18)
pin_19 = DigitalPin(name="bcm_10", number=19)
pin_20 = Gnd(number=20)
pin_21 = DigitalPin(name="bcm_9", number=21)
pin_22 = DigitalPin(name="bcm_25", number=22)
pin_23 = DigitalPin(name="bcm_11", number=23)
pin_24 = DigitalPin(name="bcm_8", number=24)
pin_25 = Gnd(number=25)
pin_26 = DigitalPin(name="bcm_7", number=26)
pin_27 = DigitalPin(name="bcm_0", number=27)
pin_28 = DigitalPin(name="bcm_1", number=28)
pin_29 = DigitalPin(name="bcm_5", number=29)
pin_30 = Gnd(number=30)
pin_31 = DigitalPin(name="bcm_6", number=31)
pin_32 = DigitalPin(name="bcm_12", number=32)
pin_33 = DigitalPin(name="bcm_13", number=33)
pin_34 = Gnd(number=34)
pin_35 = DigitalPin(name="bcm_19", number=35)
pin_36 = DigitalPin(name="bcm_16", number=36)
pin_37 = DigitalPin(name="bcm_26", number=37)
pin_38 = DigitalPin(name="bcm_20", number=38)
pin_39 = Gnd(number=39)
pin_40 = DigitalPin(name="bcm_21", number=40)


gpio_1 = GPIO(type=GPIOType.BOTH, pin=pin_3)
gpio_2 = GPIO(type=GPIOType.BOTH, pin=pin_5)
gpio_3 = GPIO(type=GPIOType.BOTH, pin=pin_7)
gpio_4 = GPIO(type=GPIOType.BOTH, pin=pin_8)
gpio_5 = GPIO(type=GPIOType.BOTH, pin=pin_10)
gpio_6 = GPIO(type=GPIOType.BOTH, pin=pin_11)
gpio_7 = GPIO(type=GPIOType.BOTH, pin=pin_12)
gpio_8 = GPIO(type=GPIOType.BOTH, pin=pin_13)
gpio_9 = GPIO(type=GPIOType.BOTH, pin=pin_15)
gpio_10 = GPIO(type=GPIOType.BOTH, pin=pin_16)
gpio_11 = GPIO(type=GPIOType.BOTH, pin=pin_18)
gpio_12 = GPIO(type=GPIOType.BOTH, pin=pin_19)
gpio_13 = GPIO(type=GPIOType.BOTH, pin=pin_21)
gpio_14 = GPIO(type=GPIOType.BOTH, pin=pin_22)
gpio_15 = GPIO(type=GPIOType.BOTH, pin=pin_23)
gpio_16 = GPIO(type=GPIOType.BOTH, pin=pin_24)
gpio_17 = GPIO(type=GPIOType.BOTH, pin=pin_26)
gpio_18 = GPIO(type=GPIOType.BOTH, pin=pin_27)
gpio_19 = GPIO(type=GPIOType.BOTH, pin=pin_28)
gpio_20 = GPIO(type=GPIOType.BOTH, pin=pin_29)
gpio_21 = GPIO(type=GPIOType.BOTH, pin=pin_31)
gpio_22 = GPIO(type=GPIOType.BOTH, pin=pin_32)
gpio_23 = GPIO(type=GPIOType.BOTH, pin=pin_33)
gpio_24 = GPIO(type=GPIOType.BOTH, pin=pin_35)
gpio_25 = GPIO(type=GPIOType.BOTH, pin=pin_36)
gpio_26 = GPIO(type=GPIOType.BOTH, pin=pin_37)
gpio_27 = GPIO(type=GPIOType.BOTH, pin=pin_38)
gpio_28 = GPIO(type=GPIOType.BOTH, pin=pin_40)

pwm_1 = PWM(pin=pin_12)
pwm_2 = PWM(pin=pin_35)

i2c_1 = I2C(sda=pin_3, scl=pin_5, is_master=True)
i2c_2 = I2C(sda=pin_27, scl=pin_28, is_master=True)

spi_1 = SPI(mosi=pin_19, miso=pin_21, 
            sclk=pin_23, ce=[pin_24, pin_26],
            is_master=True)
spi_2 = SPI(mosi=pin_38, miso=pin_35, 
            sclk=pin_40, ce=[pin_12, pin_11, pin_36],
            is_master=True)

uart_1 = UART(rx=pin_10, tx=pin_8)

dev.pins.extend([pin_1, pin_2, pin_3, pin_4, pin_5, pin_6, pin_7, pin_8,
                 pin_9, pin_10, pin_11, pin_12, pin_13, pin_14, pin_15, pin_16,
                 pin_17, pin_18, pin_19, pin_20, pin_21, pin_22, pin_23, pin_24,
                 pin_25, pin_26, pin_27, pin_28, pin_29, pin_30, pin_31, pin_32,
                 pin_33, pin_34, pin_35, pin_36, pin_37, pin_38, pin_39, pin_40])
dev.hw_interfaces.extend([gpio_1, gpio_2, gpio_3, gpio_4, gpio_5, gpio_6,
                          gpio_7, gpio_8, gpio_9, gpio_10, gpio_11, gpio_12,  
                          gpio_13, gpio_14, gpio_15, gpio_16, gpio_17, gpio_18,  
                          gpio_19, gpio_20, gpio_20, gpio_21, gpio_22, gpio_23,  
                          gpio_24, gpio_25, gpio_26, gpio_27, gpio_28, pwm_1,
                          pwm_2, i2c_1, i2c_2, spi_1, spi_2, uart_1])
# Save model
rset = ResourceSet()
r = rset.create_resource(URI(NAME))
r.append(dev)
r.save()
