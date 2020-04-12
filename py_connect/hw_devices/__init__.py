
from .hw_devices import getEClassifier, eClassifiers
from .hw_devices import name, nsURI, nsPrefix, eClass
from .hw_devices import Device, Board, Peripheral, PeripheralType, Pin, PowerPin, IOPin, CpuFamily, DigitalPin, AnalogPin, HwInterface, I2C, SPI, UART, PWM, USB, GPIOType, GPIO, ADC, Memory, CPU, Wireless, USBType, B2PConnection, HwInt2HwInt, Power2Power, Gnd, Power5V, Power3V3, Hw2Hw


from . import hw_devices

__all__ = ['Device', 'Board', 'Peripheral', 'PeripheralType', 'Pin', 'PowerPin', 'IOPin', 'CpuFamily', 'DigitalPin', 'AnalogPin', 'HwInterface', 'I2C', 'SPI', 'UART',
           'PWM', 'USB', 'GPIOType', 'GPIO', 'ADC', 'Memory', 'CPU', 'Wireless', 'USBType', 'B2PConnection', 'HwInt2HwInt', 'Power2Power', 'Gnd', 'Power5V', 'Power3V3', 'Hw2Hw']

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
B2PConnection.board.eType = Board
B2PConnection.peripheral.eType = Peripheral
B2PConnection.hw_int_connections.eType = HwInt2HwInt
B2PConnection.power_connections.eType = Power2Power
HwInt2HwInt.board_hw.eType = HwInterface
HwInt2HwInt.peripheral_hw.eType = HwInterface
Power2Power.board_power.eType = PowerPin
Power2Power.peripheral_power.eType = PowerPin
I2C.master_cons.eType = I2C
I2C.slave_cons.eType = I2C
I2C.slave_cons.eOpposite = I2C.master_cons
SPI.master_conns.eType = SPI
SPI.slave_conns.eType = SPI
SPI.slave_conns.eOpposite = SPI.master_conns
Gnd.outbound.eType = Gnd
Gnd.inbound.eType = Gnd
Gnd.inbound.eOpposite = Gnd.outbound
Power5V.outbound.eType = Power5V
Power5V.inbound.eType = Power5V
Power5V.inbound.eOpposite = Power5V.outbound
Power3V3.outbound.eType = Power3V3
Power3V3.inbound.eType = Power3V3
Power3V3.inbound.eOpposite = Power3V3.outbound

otherClassifiers = [PeripheralType, CpuFamily, GPIOType, USBType]

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)
