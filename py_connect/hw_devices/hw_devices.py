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
PeripheralType = EEnum('PeripheralType', literals=['SENSOR', 'ACTUATOR'])

CpuFamily = EEnum('CpuFamily', literals=['ARM_CORTEX_M', 'AVR',
                                         'MSP430', 'MIPS', 'EFM32', 'ARM_CORTEX_A', 'ESP8266'])

GPIOType = EEnum('GPIOType', literals=['INPUT', 'OUTPUT', 'BOTH'])

USBType = EEnum('USBType', literals=['USB2', 'USB3'])

OSType = EEnum('OSType', literals=['RASPBIAN', 'RIOT'])

PowerType = EEnum('PowerType', literals=['GND', 'Power3V3', 'Power5V'])


class Device(EObject, metaclass=MetaEClass):

    vcc = EAttribute(eType=EFloat, derived=False, changeable=True)
    name = EAttribute(eType=EString, derived=False, changeable=True)
    operating_voltage = EAttribute(eType=EFloat, derived=False, changeable=True)
    pins = EReference(ordered=True, unique=True, containment=True, upper=-1)
    hw_interfaces = EReference(ordered=True, unique=True, containment=True, upper=-1)
    network = EReference(ordered=True, unique=True, containment=False, upper=-1)
    bluetooth = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, vcc=None, name=None, pins=None, operating_voltage=None, hw_interfaces=None, network=None, bluetooth=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if vcc is not None:
            self.vcc = vcc

        if name is not None:
            self.name = name

        if operating_voltage is not None:
            self.operating_voltage = operating_voltage

        if pins:
            self.pins.extend(pins)

        if hw_interfaces:
            self.hw_interfaces.extend(hw_interfaces)

        if network:
            self.network.extend(network)

        if bluetooth is not None:
            self.bluetooth = bluetooth


@abstract
class Pin(EObject, metaclass=MetaEClass):

    number = EAttribute(eType=EInt, derived=False, changeable=True)
    connected = EAttribute(eType=EBoolean, derived=False, changeable=True)
    name = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, number=None, connected=None, name=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if number is not None:
            self.number = number

        if connected is not None:
            self.connected = connected

        if name is not None:
            self.name = name


@abstract
class HwInterface(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, derived=False, changeable=True)
    max_connections = EAttribute(eType=EInt, derived=False, changeable=True, default_value=1)
    num_connections = EAttribute(eType=EInt, derived=False, changeable=True, default_value=0)

    def __init__(self, *, name=None, max_connections=None, num_connections=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name

        if max_connections is not None:
            self.max_connections = max_connections

        if num_connections is not None:
            self.num_connections = num_connections


class Memory(EObject, metaclass=MetaEClass):

    ram = EAttribute(eType=EFloat, derived=False, changeable=True)
    rom = EAttribute(eType=EFloat, derived=False, changeable=True, default_value=0.0)
    external_memory = EAttribute(eType=EFloat, derived=False, changeable=True)

    def __init__(self, *, ram=None, rom=None, external_memory=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if ram is not None:
            self.ram = ram

        if rom is not None:
            self.rom = rom

        if external_memory is not None:
            self.external_memory = external_memory


class CPU(EObject, metaclass=MetaEClass):

    cpu_family = EAttribute(eType=CpuFamily, derived=False, changeable=True)
    max_freq = EAttribute(eType=EFloat, derived=False, changeable=True)
    fpu = EAttribute(eType=EBoolean, derived=False, changeable=True)

    def __init__(self, *, cpu_family=None, max_freq=None, fpu=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if cpu_family is not None:
            self.cpu_family = cpu_family

        if max_freq is not None:
            self.max_freq = max_freq

        if fpu is not None:
            self.fpu = fpu


class B2PConnection(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, derived=False, changeable=True)
    hw_connections = EReference(ordered=True, unique=True, containment=False, upper=-1)
    power_connections = EReference(ordered=True, unique=True, containment=False, upper=-1)
    board = EReference(ordered=True, unique=True, containment=False)
    peripheral = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, hw_connections=None, power_connections=None, board=None, peripheral=None, name=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name

        if hw_connections:
            self.hw_connections.extend(hw_connections)

        if power_connections:
            self.power_connections.extend(power_connections)

        if board is not None:
            self.board = board

        if peripheral is not None:
            self.peripheral = peripheral


@abstract
class Hw2Hw(EObject, metaclass=MetaEClass):

    def __init__(self, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

    def connect(self):

        raise NotImplementedError('operation connect(...) not yet implemented')


@abstract
class Network(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, name=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name


class Bluetooth(EObject, metaclass=MetaEClass):

    version = EAttribute(eType=EFloat, derived=False, changeable=True)

    def __init__(self, *, version=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if version is not None:
            self.version = version


class WifiFreq(EObject, metaclass=MetaEClass):

    freq = EAttribute(eType=EFloat, derived=False, changeable=True)

    def __init__(self, *, freq=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if freq is not None:
            self.freq = freq


class Board(Device):

    timers = EAttribute(eType=EInt, derived=False, changeable=True)
    rtc = EAttribute(eType=EInt, derived=False, changeable=True, default_value=0)
    battery = EAttribute(eType=EBoolean, derived=False, changeable=True)
    dma = EAttribute(eType=EBoolean, derived=False, changeable=True)
    os = EAttribute(eType=OSType, derived=False, changeable=True)
    cpu = EReference(ordered=True, unique=True, containment=True)
    memory = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, timers=None, rtc=None, battery=None, dma=None, cpu=None, memory=None, os=None, **kwargs):

        super().__init__(**kwargs)

        if timers is not None:
            self.timers = timers

        if rtc is not None:
            self.rtc = rtc

        if battery is not None:
            self.battery = battery

        if dma is not None:
            self.dma = dma

        if os is not None:
            self.os = os

        if cpu is not None:
            self.cpu = cpu

        if memory is not None:
            self.memory = memory


class Peripheral(Device):

    type = EAttribute(eType=PeripheralType, derived=False, changeable=True)

    def __init__(self, *, type=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type


class PowerPin(Pin):

    type = EAttribute(eType=PowerType, derived=False, changeable=True)

    def __init__(self, *, type=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type


class IOPin(Pin):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class I2C(HwInterface):

    bus = EAttribute(eType=EInt, derived=False, changeable=True, default_value=0)
    is_master = EAttribute(eType=EBoolean, derived=False, changeable=True)
    max_master_cons = EAttribute(eType=EInt, derived=False, changeable=True, default_value=1008)
    sda = EReference(ordered=True, unique=True, containment=False)
    scl = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, sda=None, scl=None, bus=None, is_master=None, max_master_cons=None, **kwargs):

        super().__init__(**kwargs)

        if bus is not None:
            self.bus = bus

        if is_master is not None:
            self.is_master = is_master

        if max_master_cons is not None:
            self.max_master_cons = max_master_cons

        if sda is not None:
            self.sda = sda

        if scl is not None:
            self.scl = scl


class SPI(HwInterface):

    bus = EAttribute(eType=EInt, derived=False, changeable=True, default_value=0)
    is_master = EAttribute(eType=EBoolean, derived=False, changeable=True)
    max_master_cons = EAttribute(eType=EInt, derived=False, changeable=True)
    miso = EReference(ordered=True, unique=True, containment=False)
    ce = EReference(ordered=True, unique=True, containment=False, upper=-1)
    mosi = EReference(ordered=True, unique=True, containment=False)
    sclk = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, miso=None, ce=None, mosi=None, sclk=None, bus=None, is_master=None, max_master_cons=None, **kwargs):

        super().__init__(**kwargs)

        if bus is not None:
            self.bus = bus

        if is_master is not None:
            self.is_master = is_master

        if max_master_cons is not None:
            self.max_master_cons = max_master_cons

        if miso is not None:
            self.miso = miso

        if ce:
            self.ce.extend(ce)

        if mosi is not None:
            self.mosi = mosi

        if sclk is not None:
            self.sclk = sclk


class UART(HwInterface):

    bus = EAttribute(eType=EInt, derived=False, changeable=True, default_value=0)
    rx = EReference(ordered=True, unique=True, containment=False)
    tx = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, rx=None, tx=None, bus=None, **kwargs):

        super().__init__(**kwargs)

        if bus is not None:
            self.bus = bus

        if rx is not None:
            self.rx = rx

        if tx is not None:
            self.tx = tx


class PWM(HwInterface):

    pin = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, pin=None, **kwargs):

        super().__init__(**kwargs)

        if pin is not None:
            self.pin = pin


class USB(HwInterface):

    type = EAttribute(eType=USBType, derived=False, changeable=True)
    bus = EAttribute(eType=EInt, derived=False, changeable=True, default_value=0)

    def __init__(self, *, type=None, bus=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if bus is not None:
            self.bus = bus


class GPIO(HwInterface):

    type = EAttribute(eType=GPIOType, derived=False, changeable=True)
    pin = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, type=None, pin=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if pin is not None:
            self.pin = pin


class ADC(HwInterface):

    pin = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, pin=None, **kwargs):

        super().__init__(**kwargs)

        if pin is not None:
            self.pin = pin


@abstract
class HwInt2HwInt(Hw2Hw):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class Power2Power(Hw2Hw):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class Wifi(Network):

    freqs = EReference(ordered=True, unique=True, containment=False, upper=-1)

    def __init__(self, *, freqs=None, **kwargs):

        super().__init__(**kwargs)

        if freqs:
            self.freqs.extend(freqs)


class Ethernet(Network):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class DigitalPin(IOPin):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class AnalogPin(IOPin):

    vmax = EAttribute(eType=EFloat, derived=False, changeable=True)

    def __init__(self, *, vmax=None, **kwargs):

        super().__init__(**kwargs)

        if vmax is not None:
            self.vmax = vmax


class Usb2Usb(HwInt2HwInt):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class Adc2Adc(HwInt2HwInt):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class I2c2I2c(HwInt2HwInt):

    slave_address = EAttribute(eType=EInt, derived=False, changeable=True)

    def __init__(self, *, slave_address=None, **kwargs):

        super().__init__(**kwargs)

        if slave_address is not None:
            self.slave_address = slave_address


class Spi2Spi(HwInt2HwInt):

    ce_index = EAttribute(eType=EInt, derived=False, changeable=True)

    def __init__(self, *, ce_index=None, **kwargs):

        super().__init__(**kwargs)

        if ce_index is not None:
            self.ce_index = ce_index


class Uart2Uart(HwInt2HwInt):

    baudrate = EAttribute(eType=EInt, derived=False, changeable=True, default_value=-1)

    def __init__(self, *, baudrate=None, **kwargs):

        super().__init__(**kwargs)

        if baudrate is not None:
            self.baudrate = baudrate


class Pwm2Pwm(HwInt2HwInt):

    frequency = EAttribute(eType=EInt, derived=False, changeable=True, default_value=0)

    def __init__(self, *, frequency=None, **kwargs):

        super().__init__(**kwargs)

        if frequency is not None:
            self.frequency = frequency


class Gpio2Gpio(HwInt2HwInt):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
