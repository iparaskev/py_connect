
from .hw_devices import getEClassifier, eClassifiers
from .hw_devices import name, nsURI, nsPrefix, eClass
from .hw_devices import Device, Board, Peripheral, PeripheralType, Pin, PowerPin, IOPin, CpuFamily, DigitalPin, AnalogPin, HwInterface, I2C, SPI, UART, PWM, USB, GPIOType, GPIO, ADC, Memory, CPU, USBType, B2PConnection, HwInt2HwInt, Power2Power, Hw2Hw, OSType, Usb2Usb, Adc2Adc, I2c2I2c, Spi2Spi, Uart2Uart, Pwm2Pwm, Gpio2Gpio, Network, Wifi, Ethernet, Bluetooth, PowerType, WifiFreq


from . import hw_devices

__all__ = ['Device', 'Board', 'Peripheral', 'PeripheralType', 'Pin', 'PowerPin', 'IOPin', 'CpuFamily', 'DigitalPin', 'AnalogPin', 'HwInterface', 'I2C', 'SPI', 'UART', 'PWM', 'USB', 'GPIOType', 'GPIO', 'ADC', 'Memory', 'CPU',
           'USBType', 'B2PConnection', 'HwInt2HwInt', 'Power2Power', 'Hw2Hw', 'OSType', 'Usb2Usb', 'Adc2Adc', 'I2c2I2c', 'Spi2Spi', 'Uart2Uart', 'Pwm2Pwm', 'Gpio2Gpio', 'Network', 'Wifi', 'Ethernet', 'Bluetooth', 'PowerType', 'WifiFreq']

eSubpackages = []
eSuperPackage = None
hw_devices.eSubpackages = eSubpackages
hw_devices.eSuperPackage = eSuperPackage

Device.pins.eType = Pin
Device.hw_interfaces.eType = HwInterface
Device.network.eType = Network
Device.bluetooth.eType = Bluetooth
Board.cpu.eType = CPU
Board.memory.eType = Memory
I2C.sda.eType = DigitalPin
I2C.scl.eType = DigitalPin
SPI.miso.eType = DigitalPin
SPI.ce.eType = DigitalPin
SPI.mosi.eType = DigitalPin
SPI.sclk.eType = DigitalPin
UART.rx.eType = DigitalPin
UART.tx.eType = DigitalPin
PWM.pin.eType = DigitalPin
GPIO.pin.eType = IOPin
ADC.pin.eType = AnalogPin
B2PConnection.hw_connections.eType = HwInt2HwInt
B2PConnection.power_connections.eType = Power2Power
B2PConnection.board.eType = Board
B2PConnection.peripheral.eType = Peripheral
Power2Power.pin_1.eType = PowerPin
Power2Power.pin_2.eType = PowerPin
I2c2I2c.hwint_1.eType = I2C
I2c2I2c.hwint_2.eType = I2C
Spi2Spi.hwint_1.eType = SPI
Spi2Spi.hwint_2.eType = SPI
Uart2Uart.hwint_1.eType = UART
Uart2Uart.hwint_2.eType = UART
Pwm2Pwm.hwint_1.eType = PWM
Pwm2Pwm.hwint_2.eType = PWM
Gpio2Gpio.hwint_1.eType = GPIO
Gpio2Gpio.hwint_2.eType = GPIO
Wifi.freqs.eType = WifiFreq

otherClassifiers = [PeripheralType, CpuFamily, GPIOType, USBType, OSType, PowerType]

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)
