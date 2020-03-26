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


class Device(EObject, metaclass=MetaEClass):

    operating_voltage = EAttribute(eType=EFloat, derived=False, changeable=True)
    name = EAttribute(eType=EString, derived=False, changeable=True)
    power_pins = EReference(ordered=True, unique=True, containment=False, upper=-1)

    def __init__(self, *, operating_voltage=None, name=None, power_pins=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if operating_voltage is not None:
            self.operating_voltage = operating_voltage

        if name is not None:
            self.name = name

        if power_pins:
            self.power_pins.extend(power_pins)


class Pin(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, name=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name


class UartRx(EObject, metaclass=MetaEClass):

    def __init__(self, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()


class UartTx(EObject, metaclass=MetaEClass):

    def __init__(self, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()


class SpiMiso(EObject, metaclass=MetaEClass):

    def __init__(self, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()


class SpiSclk(EObject, metaclass=MetaEClass):

    def __init__(self, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()


class SpiMosi(EObject, metaclass=MetaEClass):

    def __init__(self, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()


class SpiCe(EObject, metaclass=MetaEClass):

    def __init__(self, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()


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


class PowerPin(Pin):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class IOPin(Pin):

    number = EAttribute(eType=EInt, derived=False, changeable=True)

    def __init__(self, *, number=None, **kwargs):

        super().__init__(**kwargs)

        if number is not None:
            self.number = number


class Computational(Device):

    pins = EReference(ordered=True, unique=True, containment=False, upper=-1)
    devices = EReference(ordered=True, unique=True, containment=False, upper=-1)

    def __init__(self, *, pins=None, devices=None, **kwargs):

        super().__init__(**kwargs)

        if pins:
            self.pins.extend(pins)

        if devices:
            self.devices.extend(devices)


class NonComputational(Device):

    type = EAttribute(eType=DeviceType, derived=False, changeable=True)
    driver = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, type=None, driver=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if driver is not None:
            self.driver = driver


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


class GpioDevice(NonComputational):

    gpio_pins = EReference(ordered=True, unique=True, containment=False, upper=-1)

    def __init__(self, *, gpio_pins=None, **kwargs):

        super().__init__(**kwargs)

        if gpio_pins:
            self.gpio_pins.extend(gpio_pins)


class I2cDevice(NonComputational):

    i2c_pins = EReference(ordered=True, unique=True, containment=False, upper=-1)

    def __init__(self, *, i2c_pins=None, **kwargs):

        super().__init__(**kwargs)

        if i2c_pins:
            self.i2c_pins.extend(i2c_pins)


class GpioPin(IOPin):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class I2cPin(IOPin):

    i2c_bus = EAttribute(eType=EInt, derived=False, changeable=True)

    def __init__(self, *, i2c_bus=None, **kwargs):

        super().__init__(**kwargs)

        if i2c_bus is not None:
            self.i2c_bus = i2c_bus


class GpioInput(GpioPin):

    conn_from = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, conn_from=None, **kwargs):

        super().__init__(**kwargs)

        if conn_from is not None:
            self.conn_from = conn_from


class GpioOutput(GpioPin):

    conn_to = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, conn_to=None, **kwargs):

        super().__init__(**kwargs)

        if conn_to is not None:
            self.conn_to = conn_to


class I2cSda(I2cPin):

    conn_to = EReference(ordered=True, unique=True, containment=False, upper=-1)
    conn_from = EReference(ordered=True, unique=True, containment=False, upper=-1)

    def __init__(self, *, conn_to=None, conn_from=None, **kwargs):

        super().__init__(**kwargs)

        if conn_to:
            self.conn_to.extend(conn_to)

        if conn_from:
            self.conn_from.extend(conn_from)


class I2cScl(I2cPin):

    conn_to = EReference(ordered=True, unique=True, containment=False, upper=-1)
    conn_from = EReference(ordered=True, unique=True, containment=False, upper=-1)

    def __init__(self, *, conn_to=None, conn_from=None, **kwargs):

        super().__init__(**kwargs)

        if conn_to:
            self.conn_to.extend(conn_to)

        if conn_from:
            self.conn_from.extend(conn_from)


class Pwm(GpioPin):

    conn_to = EReference(ordered=True, unique=True, containment=False)
    conn_from = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, conn_to=None, conn_from=None, **kwargs):

        super().__init__(**kwargs)

        if conn_to is not None:
            self.conn_to = conn_to

        if conn_from is not None:
            self.conn_from = conn_from


class CompositeDevice(GpioDevice, I2cDevice):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
