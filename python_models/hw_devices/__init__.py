
from .hw_devices import getEClassifier, eClassifiers
from .hw_devices import name, nsURI, nsPrefix, eClass
from .hw_devices import Device, Pin, PowerPin, GpioPin, Power3V3, Power5V, Gnd, Input, Output, I2cSda, I2cScl, Pwm, UartRx, UartTx, SpiMiso, SpiSclk, SpiMosi, SpiCe


from . import hw_devices

__all__ = ['Device', 'Pin', 'PowerPin', 'GpioPin', 'Power3V3', 'Power5V', 'Gnd', 'Input', 'Output',
           'I2cSda', 'I2cScl', 'Pwm', 'UartRx', 'UartTx', 'SpiMiso', 'SpiSclk', 'SpiMosi', 'SpiCe']

eSubpackages = []
eSuperPackage = None
hw_devices.eSubpackages = eSubpackages
hw_devices.eSuperPackage = eSuperPackage

Device.pins.eType = Pin
Input.connection.eType = Output
Output.connection.eType = Input
I2cSda.connections.eType = I2cSda
I2cScl.connections.eType = I2cScl
Pwm.connection.eType = Pwm
Power3V3.conn_to.eType = Power3V3
Power3V3.conn_from.eType = Power3V3
Power3V3.conn_from.eOpposite = Power3V3.conn_to
Power5V.conn_to.eType = Power5V
Power5V.conn_from.eType = Power5V
Power5V.conn_from.eOpposite = Power5V.conn_to
Gnd.conn_to.eType = Gnd
Gnd.conn_from.eType = Gnd
Gnd.conn_from.eOpposite = Gnd.conn_to

otherClassifiers = []

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)
