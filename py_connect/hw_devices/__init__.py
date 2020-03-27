
from .hw_devices import getEClassifier, eClassifiers
from .hw_devices import name, nsURI, nsPrefix, eClass
from .hw_devices import Device, Computational, NonComputational, DeviceType, Pin, PowerPin, IOPinFunction, IOPin, IOType, PowerType


from . import hw_devices

__all__ = ['Device', 'Computational', 'NonComputational', 'DeviceType',
           'Pin', 'PowerPin', 'IOPinFunction', 'IOPin', 'IOType', 'PowerType']

eSubpackages = []
eSuperPackage = None
hw_devices.eSubpackages = eSubpackages
hw_devices.eSuperPackage = eSuperPackage

Device.pins.eType = Pin
IOPin.functions.eType = IOPinFunction

otherClassifiers = [DeviceType, IOType, PowerType]

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)
