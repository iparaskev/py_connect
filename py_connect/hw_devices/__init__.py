
from .hw_devices import getEClassifier, eClassifiers
from .hw_devices import name, nsURI, nsPrefix, eClass
from .hw_devices import Device, Board, Peripheral, PeripheralType, Pin, PowerPin, IOPin, CpuFamily, DigitalPin, AnalogPin, HwInterface, I2C, SPI, UART, PWM, USB, GPIOType, GPIO, ADC, Memory, CPU, Wireless, USBType, B2PConnection, HwInt2HwInt, Power2Power, Gnd, Power5V, Power3V3, Hw2Hw, OSType, Usb2Usb, Adc2Adc, I2c2I2c, Spi2Spi, Uart2Uart, Pwm2Pwm, Gpio2Gpio


from . import hw_devices

__all__ = ['Device', 'Board', 'Peripheral', 'PeripheralType', 'Pin', 'PowerPin', 'IOPin', 'CpuFamily', 'DigitalPin', 'AnalogPin', 'HwInterface', 'I2C', 'SPI', 'UART', 'PWM', 'USB', 'GPIOType', 'GPIO', 'ADC', 'Memory',
           'CPU', 'Wireless', 'USBType', 'B2PConnection', 'HwInt2HwInt', 'Power2Power', 'Gnd', 'Power5V', 'Power3V3', 'Hw2Hw', 'OSType', 'Usb2Usb', 'Adc2Adc', 'I2c2I2c', 'Spi2Spi', 'Uart2Uart', 'Pwm2Pwm', 'Gpio2Gpio']

eSubpackages = []
eSuperPackage = None
hw_devices.eSubpackages = eSubpackages
hw_devices.eSuperPackage = eSuperPackage

Device.pins.eType = Pin
Device.hw_interfaces.eType = HwInterface
Board.cpu.eType = CPU
Board.memory.eType = Memory
Board.wireless.eType = Wireless
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
B2PConnection.board.eType = Board
B2PConnection.peripheral.eType = Peripheral
B2PConnection.hw_int_connections.eType = HwInt2HwInt
B2PConnection.power_connections.eType = Power2Power
HwInt2HwInt.interface_1.eType = HwInterface
HwInt2HwInt.interface_2.eType = HwInterface
Power2Power.conn_1.eType = PowerPin
Power2Power.conn_2.eType = PowerPin

otherClassifiers = [PeripheralType, CpuFamily, GPIOType, USBType, OSType]

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)
