
from .hw_devices import getEClassifier, eClassifiers
from .hw_devices import name, nsURI, nsPrefix, eClass
from .hw_devices import Device, Computational, NonComputational, DeviceType, Pin, PowerPin, IOPinFunction, IOPin, IOType, PowerType, D2DConnection, Pin2PinConnection


from . import hw_devices

__all__ = ['Device', 'Computational', 'NonComputational', 'DeviceType', 'Pin', 'PowerPin',
           'IOPinFunction', 'IOPin', 'IOType', 'PowerType', 'D2DConnection', 'Pin2PinConnection']

eSubpackages = []
eSuperPackage = None
hw_devices.eSubpackages = eSubpackages
hw_devices.eSuperPackage = eSuperPackage

Computational.connected_devices.eType = D2DConnection
IOPin.functions.eType = IOPinFunction
D2DConnection.device.eType = NonComputational
D2DConnection.pin_connections.eType = Pin2PinConnection
Pin2PinConnection.comp_pin.eType = Pin
Pin2PinConnection.non_comp_pin.eType = Pin
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
