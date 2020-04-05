
from .hw_devices import getEClassifier, eClassifiers
from .hw_devices import name, nsURI, nsPrefix, eClass
from .hw_devices import Device, Board, Peripheral, PeripheralType, Pin, PowerPin, IOPin, PowerType, CpuFamily, DigitalPin, AnalogPin, HwInterface, I2C, SPI, UART, PWM, USB, GPIOType, GPIO, ADC, Memory, CPU, Wireless, USBType


from . import hw_devices

__all__ = ['Device', 'Board', 'Peripheral', 'PeripheralType', 'Pin', 'PowerPin', 'IOPin', 'PowerType', 'CpuFamily', 'DigitalPin',
           'AnalogPin', 'HwInterface', 'I2C', 'SPI', 'UART', 'PWM', 'USB', 'GPIOType', 'GPIO', 'ADC', 'Memory', 'CPU', 'Wireless', 'USBType']

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
UART.connection.eType = UART
PWM.pin.eType = DigitalPin
PWM.connection.eType = PWM
USB.connection.eType = USB
GPIO.pin.eType = IOPin
GPIO.connection.eType = GPIO
ADC.pin.eType = AnalogPin
ADC.connection.eType = ADC
I2C.master_cons.eType = I2C
I2C.slave_cons.eType = I2C
I2C.slave_cons.eOpposite = I2C.master_cons
SPI.master_conns.eType = SPI
SPI.slave_conns.eType = SPI
SPI.slave_conns.eOpposite = SPI.master_conns

otherClassifiers = [PeripheralType, PowerType, CpuFamily, GPIOType, USBType]

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)
