
from .hw_devices import getEClassifier, eClassifiers
from .hw_devices import name, nsURI, nsPrefix, eClass
from .hw_devices import Device, Pin, PowerPin, GpioPin, I2cPin, SpiPin, UartPin, PwmPin, Power3V3, Power5V, Gnd, Input, Output, Sda, Scl


from . import hw_devices

__all__ = ['Device', 'Pin', 'PowerPin', 'GpioPin', 'I2cPin', 'SpiPin', 'UartPin',
           'PwmPin', 'Power3V3', 'Power5V', 'Gnd', 'Input', 'Output', 'Sda', 'Scl']

eSubpackages = []
eSuperPackage = None
hw_devices.eSubpackages = eSubpackages
hw_devices.eSuperPackage = eSuperPackage

Device.pins.eType = Pin
Power3V3.connections.eType = Power3V3
Power5V.connections.eType = Power5V
Gnd.connections.eType = Gnd
Input.connection.eType = Input
Output.connection.eType = Output
Sda.connections.eType = Sda
Scl.connections.eType = Scl

otherClassifiers = []

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)
