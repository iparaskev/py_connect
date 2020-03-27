
from .hw_devices import getEClassifier, eClassifiers
from .hw_devices import name, nsURI, nsPrefix, eClass
from .hw_devices import Device, Computational, NonComputational, DeviceType, Pin, PowerPin, IOPinFunction, IOPin, IOType, PowerType, ConnectedDevice, ConnectedPins


from . import hw_devices

__all__ = ['Device', 'Computational', 'NonComputational', 'DeviceType', 'Pin', 'PowerPin',
           'IOPinFunction', 'IOPin', 'IOType', 'PowerType', 'ConnectedDevice', 'ConnectedPins']

eSubpackages = []
eSuperPackage = None
hw_devices.eSubpackages = eSubpackages
hw_devices.eSuperPackage = eSuperPackage

Computational.connected_devices.eType = ConnectedDevice
IOPin.functions.eType = IOPinFunction
ConnectedDevice.device.eType = NonComputational
ConnectedDevice.pins_connections.eType = ConnectedPins
ConnectedPins.comp_pin.eType = Pin
ConnectedPins.non_comp_pin.eType = Pin
Device.pins.eType = Pin
Pin.device.eType = Device
Pin.device.eOpposite = Device.pins

otherClassifiers = [DeviceType, IOType, PowerType]

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)
