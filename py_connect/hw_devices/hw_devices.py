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

CpuFamily = EEnum('CpuFamily', literals=['ARM_CORTEX-M', 'AVR', 'MSP430', 'MIPS', 'EFM32'])


class Device(EObject, metaclass=MetaEClass):

    vcc = EAttribute(eType=EFloat, derived=False, changeable=True)
    name = EAttribute(eType=EString, derived=False, changeable=True)
    pins = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, vcc=None, name=None, pins=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if vcc is not None:
            self.vcc = vcc

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

    cpu_family = EAttribute(eType=CpuFamily, derived=False, changeable=True)
    ram = EAttribute(eType=EInt, derived=False, changeable=True)
    rom = EAttribute(eType=EInt, derived=False, changeable=True)
    max_freq = EAttribute(eType=EInt, derived=False, changeable=True)
    fpu = EAttribute(eType=EBoolean, derived=False, changeable=True)
    dma = EAttribute(eType=EBoolean, derived=False, changeable=True)
    wifi = EAttribute(eType=EBoolean, derived=False, changeable=True)
    ble = EAttribute(eType=EBoolean, derived=False, changeable=True)
    ethernet = EAttribute(eType=EBoolean, derived=False, changeable=True)
    timers = EAttribute(eType=EInt, derived=False, changeable=True)
    rtc = EAttribute(eType=EInt, derived=False, changeable=True)
    usb2s = EAttribute(eType=EInt, derived=False, changeable=True)
    usb3s = EAttribute(eType=EInt, derived=False, changeable=True)
    i2cs = EAttribute(eType=EInt, derived=False, changeable=True)
    spis = EAttribute(eType=EInt, derived=False, changeable=True)
    uarts = EAttribute(eType=EInt, derived=False, changeable=True)
    pwms = EAttribute(eType=EInt, derived=False, changeable=True)
    connected_devices = EReference(ordered=True, unique=True, containment=False, upper=-1)

    def __init__(self, *, connected_devices=None, cpu_family=None, ram=None, rom=None, max_freq=None, fpu=None, dma=None, wifi=None, ble=None, ethernet=None, timers=None, rtc=None, usb2s=None, usb3s=None, i2cs=None, spis=None, uarts=None, pwms=None, **kwargs):

        super().__init__(**kwargs)

        if cpu_family is not None:
            self.cpu_family = cpu_family

        if ram is not None:
            self.ram = ram

        if rom is not None:
            self.rom = rom

        if max_freq is not None:
            self.max_freq = max_freq

        if fpu is not None:
            self.fpu = fpu

        if dma is not None:
            self.dma = dma

        if wifi is not None:
            self.wifi = wifi

        if ble is not None:
            self.ble = ble

        if ethernet is not None:
            self.ethernet = ethernet

        if timers is not None:
            self.timers = timers

        if rtc is not None:
            self.rtc = rtc

        if usb2s is not None:
            self.usb2s = usb2s

        if usb3s is not None:
            self.usb3s = usb3s

        if i2cs is not None:
            self.i2cs = i2cs

        if spis is not None:
            self.spis = spis

        if uarts is not None:
            self.uarts = uarts

        if pwms is not None:
            self.pwms = pwms

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
