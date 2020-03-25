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

    operating_voltage = EAttribute(eType=EFloat, derived=False, changeable=True)
    pins = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, pins=None, operating_voltage=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if operating_voltage is not None:
            self.operating_voltage = operating_voltage

        if pins:
            self.pins.extend(pins)


class Pin(EObject, metaclass=MetaEClass):

    number = EAttribute(eType=EInt, derived=False, changeable=True)
    name = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, number=None, name=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if number is not None:
            self.number = number

        if name is not None:
            self.name = name


class PowerPin(Pin):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class GpioPin(Pin):

    h_chip = EAttribute(eType=EInt, derived=False, changeable=True, default_value=0)

    def __init__(self, *, h_chip=None, **kwargs):

        super().__init__(**kwargs)

        if h_chip is not None:
            self.h_chip = h_chip


class Power3V3(PowerPin):

    conn_to = EReference(ordered=True, unique=True, containment=False, upper=-1)
    conn_from = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, conn_to=None, conn_from=None, **kwargs):

        super().__init__(**kwargs)

        if conn_to:
            self.conn_to.extend(conn_to)

        if conn_from is not None:
            self.conn_from = conn_from


class Power5V(PowerPin):

    conn_to = EReference(ordered=True, unique=True, containment=False, upper=-1)
    conn_from = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, conn_to=None, conn_from=None, **kwargs):

        super().__init__(**kwargs)

        if conn_to:
            self.conn_to.extend(conn_to)

        if conn_from is not None:
            self.conn_from = conn_from


class Gnd(PowerPin):

    conn_to = EReference(ordered=True, unique=True, containment=False, upper=-1)
    conn_from = EReference(ordered=True, unique=True, containment=False, upper=-1)

    def __init__(self, *, conn_to=None, conn_from=None, **kwargs):

        super().__init__(**kwargs)

        if conn_to:
            self.conn_to.extend(conn_to)

        if conn_from:
            self.conn_from.extend(conn_from)


class Input(GpioPin):

    conn_from = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, conn_from=None, **kwargs):

        super().__init__(**kwargs)

        if conn_from is not None:
            self.conn_from = conn_from


class Output(GpioPin):

    conn_to = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, conn_to=None, **kwargs):

        super().__init__(**kwargs)

        if conn_to is not None:
            self.conn_to = conn_to


class I2cSda(GpioPin):

    connections = EReference(ordered=True, unique=True, containment=False, upper=-1)

    def __init__(self, *, connections=None, **kwargs):

        super().__init__(**kwargs)

        if connections:
            self.connections.extend(connections)


class I2cScl(GpioPin):

    connections = EReference(ordered=True, unique=True, containment=False, upper=-1)

    def __init__(self, *, connections=None, **kwargs):

        super().__init__(**kwargs)

        if connections:
            self.connections.extend(connections)


class Pwm(GpioPin):

    connection = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, connection=None, **kwargs):

        super().__init__(**kwargs)

        if connection is not None:
            self.connection = connection


class UartRx(GpioPin):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class UartTx(GpioPin):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class SpiMiso(GpioPin):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class SpiSclk(GpioPin):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class SpiMosi(GpioPin):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class SpiCe(GpioPin):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
