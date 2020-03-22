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


class Device(EObject, metaclass=MetaEClass):

    operating_voltage = EAttribute(eType=EFloat, derived=False, changeable=True, upper=-1)
    pins = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, pins=None, operating_voltage=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if operating_voltage:
            self.operating_voltage.extend(operating_voltage)

        if pins:
            self.pins.extend(pins)


class Pin(EObject, metaclass=MetaEClass):

    number = EAttribute(eType=EInt, derived=False, changeable=True, upper=-1)
    name = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, number=None, name=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if number:
            self.number.extend(number)

        if name is not None:
            self.name = name


class SpiPin(EObject, metaclass=MetaEClass):

    def __init__(self, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()


class UartPin(EObject, metaclass=MetaEClass):

    def __init__(self, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()


class PwmPin(EObject, metaclass=MetaEClass):

    def __init__(self, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()


class PowerPin(Pin):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class GpioPin(Pin):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class I2cPin(Pin):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class Power3V3(PowerPin):

    connections = EReference(ordered=True, unique=True, containment=False, upper=-1)

    def __init__(self, *, connections=None, **kwargs):

        super().__init__(**kwargs)

        if connections:
            self.connections.extend(connections)


class Power5V(PowerPin):

    connections = EReference(ordered=True, unique=True, containment=False, upper=-1)

    def __init__(self, *, connections=None, **kwargs):

        super().__init__(**kwargs)

        if connections:
            self.connections.extend(connections)


class Gnd(PowerPin):

    connections = EReference(ordered=True, unique=True, containment=False, upper=-1)

    def __init__(self, *, connections=None, **kwargs):

        super().__init__(**kwargs)

        if connections:
            self.connections.extend(connections)


class Input(GpioPin):

    connection = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, connection=None, **kwargs):

        super().__init__(**kwargs)

        if connection is not None:
            self.connection = connection


class Output(GpioPin):

    connection = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, connection=None, **kwargs):

        super().__init__(**kwargs)

        if connection is not None:
            self.connection = connection


class Sda(I2cPin):

    connections = EReference(ordered=True, unique=True, containment=False, upper=-1)

    def __init__(self, *, connections=None, **kwargs):

        super().__init__(**kwargs)

        if connections:
            self.connections.extend(connections)


class Scl(I2cPin):

    connections = EReference(ordered=True, unique=True, containment=False, upper=-1)

    def __init__(self, *, connections=None, **kwargs):

        super().__init__(**kwargs)

        if connections:
            self.connections.extend(connections)
