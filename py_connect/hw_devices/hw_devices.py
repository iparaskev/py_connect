"""Definition of meta model 'hw_devices'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *


name = 'hw_devices'
nsURI = 'http://www.example.org/hw_devices'
nsPrefix = 'hw_devices'

eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)
DeviceType = EEnum('DeviceType', literals=['SENSOR', 'ACTUATOR'])

IOType = EEnum('IOType', literals=['GPIO_INPUT', 'GPIO_OUTPUT',
                                   'GPIO_BOTH', 'I2C_SDA', 'I2C_SCL', 'PWM'])

PowerType = EEnum('PowerType', literals=['GND', 'POWER_3V3', 'POWER_5V'])


class Device(EObject, metaclass=MetaEClass):

    operating_voltage = EAttribute(eType=EFloat, derived=False, changeable=True)
    name = EAttribute(eType=EString, derived=False, changeable=True)
    pins = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, operating_voltage=None, name=None, pins=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if operating_voltage is not None:
            self.operating_voltage = operating_voltage

        if name is not None:
            self.name = name

        if pins:
            self.pins.extend(pins)


class Pin(EObject, metaclass=MetaEClass):

    number = EAttribute(eType=EInt, derived=False, changeable=True)

    def __init__(self, *, number=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if number is not None:
            self.number = number


class IOPinFunction(EObject, metaclass=MetaEClass):

    type = EAttribute(eType=IOType, derived=False, changeable=True)
    hw_port = EAttribute(eType=EInt, derived=False, changeable=True, default_value=0)

    def __init__(self, *, type=None, hw_port=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if type is not None:
            self.type = type

        if hw_port is not None:
            self.hw_port = hw_port


class D2DConnection(EObject, metaclass=MetaEClass):

    device = EReference(ordered=True, unique=True, containment=False)
    pin_connections = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, device=None, pin_connections=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if device is not None:
            self.device = device

        if pin_connections:
            self.pin_connections.extend(pin_connections)


class Pin2PinConnection(EObject, metaclass=MetaEClass):

    comp_pin = EReference(ordered=True, unique=True, containment=False)
    non_comp_pin = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, comp_pin=None, non_comp_pin=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if comp_pin is not None:
            self.comp_pin = comp_pin

        if non_comp_pin is not None:
            self.non_comp_pin = non_comp_pin


class Computational(Device):

    connected_devices = EReference(ordered=True, unique=True, containment=False, upper=-1)

    def __init__(self, *, connected_devices=None, **kwargs):

        super().__init__(**kwargs)

        if connected_devices:
            self.connected_devices.extend(connected_devices)


class NonComputational(Device):

    type = EAttribute(eType=DeviceType, derived=False, changeable=True)
    driver_name = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, type=None, driver_name=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if driver_name is not None:
            self.driver_name = driver_name


class PowerPin(Pin):

    function = EAttribute(eType=PowerType, derived=False, changeable=True)

    def __init__(self, *, function=None, **kwargs):

        super().__init__(**kwargs)

        if function is not None:
            self.function = function


class IOPin(Pin):

    name = EAttribute(eType=EString, derived=False, changeable=True)
    functions = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, name=None, functions=None, **kwargs):

        super().__init__(**kwargs)

        if name is not None:
            self.name = name

        if functions:
            self.functions.extend(functions)
