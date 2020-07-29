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
    network = EReference(ordered=True, unique=True, containment=True, upper=-1)
    bluetooth = EReference(ordered=True, unique=True, containment=True)

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
    peripheral_impl = EAttribute(eType=EString, derived=False, changeable=True)
    hw_connections = EReference(ordered=True, unique=True, containment=True, upper=-1)
    power_connections = EReference(ordered=True, unique=True, containment=True, upper=-1)
    board = EReference(ordered=True, unique=True, containment=False)
    peripheral = EReference(ordered=True, unique=True, containment=False)
    com_endpoint = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, hw_connections=None, power_connections=None, name=None, board=None, peripheral=None, peripheral_impl=None, com_endpoint=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name

        if peripheral_impl is not None:
            self.peripheral_impl = peripheral_impl

        if hw_connections:
            self.hw_connections.extend(hw_connections)

        if power_connections:
            self.power_connections.extend(power_connections)

        if board is not None:
            self.board = board

        if peripheral is not None:
            self.peripheral = peripheral

        if com_endpoint is not None:
            self.com_endpoint = com_endpoint


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


class ComEndpoint(EObject, metaclass=MetaEClass):

    topic_name = EAttribute(eType=EString, derived=False, changeable=True)
    conn_params = EReference(ordered=True, unique=True, containment=True)
    msg = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, topic_name=None, conn_params=None, msg=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if topic_name is not None:
            self.topic_name = topic_name

        if conn_params is not None:
            self.conn_params = conn_params

        if msg is not None:
            self.msg = msg


class ConnParams(EObject, metaclass=MetaEClass):

    username = EAttribute(eType=EString, derived=False, changeable=True)
    password = EAttribute(eType=EString, derived=False, changeable=True)
    host = EAttribute(eType=EString, derived=False, changeable=True)
    port = EAttribute(eType=EInt, derived=False, changeable=True)

    def __init__(self, *, username=None, password=None, host=None, port=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if username is not None:
            self.username = username

        if password is not None:
            self.password = password

        if host is not None:
            self.host = host

        if port is not None:
            self.port = port


@abstract
class PerDeviceDataType(EObject, metaclass=MetaEClass):

    def __init__(self, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()


class Msg(EObject, metaclass=MetaEClass):

    msg_entries = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, msg_entries=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if msg_entries:
            self.msg_entries.extend(msg_entries)


class ThreeDimensions(EObject, metaclass=MetaEClass):

    x = EAttribute(eType=EFloat, derived=False, changeable=True)
    y = EAttribute(eType=EFloat, derived=False, changeable=True)
    z = EAttribute(eType=EFloat, derived=False, changeable=True)

    def __init__(self, *, x=None, y=None, z=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if x is not None:
            self.x = x

        if y is not None:
            self.y = y

        if z is not None:
            self.z = z


class Color(EObject, metaclass=MetaEClass):

    r = EAttribute(eType=EInt, derived=False, changeable=True)
    g = EAttribute(eType=EInt, derived=False, changeable=True)
    b = EAttribute(eType=EInt, derived=False, changeable=True)

    def __init__(self, *, r=None, g=None, b=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if r is not None:
            self.r = r

        if g is not None:
            self.g = g

        if b is not None:
            self.b = b


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

    pin_1 = EReference(ordered=True, unique=True, containment=False)
    pin_2 = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, pin_1=None, pin_2=None, **kwargs):

        super().__init__(**kwargs)

        if pin_1 is not None:
            self.pin_1 = pin_1

        if pin_2 is not None:
            self.pin_2 = pin_2


class Wifi(Network):

    freqs = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, freqs=None, **kwargs):

        super().__init__(**kwargs)

        if freqs:
            self.freqs.extend(freqs)


class Ethernet(Network):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


@abstract
class SensorDataType(PerDeviceDataType):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


@abstract
class ActuatorDataType(PerDeviceDataType):

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
    hwint_1 = EReference(ordered=True, unique=True, containment=False)
    hwint_2 = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, slave_address=None, hwint_1=None, hwint_2=None, **kwargs):

        super().__init__(**kwargs)

        if slave_address is not None:
            self.slave_address = slave_address

        if hwint_1 is not None:
            self.hwint_1 = hwint_1

        if hwint_2 is not None:
            self.hwint_2 = hwint_2


class Spi2Spi(HwInt2HwInt):

    ce_index = EAttribute(eType=EInt, derived=False, changeable=True)
    hwint_1 = EReference(ordered=True, unique=True, containment=False)
    hwint_2 = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, ce_index=None, hwint_1=None, hwint_2=None, **kwargs):

        super().__init__(**kwargs)

        if ce_index is not None:
            self.ce_index = ce_index

        if hwint_1 is not None:
            self.hwint_1 = hwint_1

        if hwint_2 is not None:
            self.hwint_2 = hwint_2


class Uart2Uart(HwInt2HwInt):

    baudrate = EAttribute(eType=EInt, derived=False, changeable=True, default_value=-1)
    hwint_1 = EReference(ordered=True, unique=True, containment=False)
    hwint_2 = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, baudrate=None, hwint_1=None, hwint_2=None, **kwargs):

        super().__init__(**kwargs)

        if baudrate is not None:
            self.baudrate = baudrate

        if hwint_1 is not None:
            self.hwint_1 = hwint_1

        if hwint_2 is not None:
            self.hwint_2 = hwint_2


class Pwm2Pwm(HwInt2HwInt):

    frequency = EAttribute(eType=EInt, derived=False, changeable=True, default_value=0)
    hwint_1 = EReference(ordered=True, unique=True, containment=False)
    hwint_2 = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, frequency=None, hwint_1=None, hwint_2=None, **kwargs):

        super().__init__(**kwargs)

        if frequency is not None:
            self.frequency = frequency

        if hwint_1 is not None:
            self.hwint_1 = hwint_1

        if hwint_2 is not None:
            self.hwint_2 = hwint_2


class Gpio2Gpio(HwInt2HwInt):

    hwint_1 = EReference(ordered=True, unique=True, containment=False)
    hwint_2 = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, hwint_1=None, hwint_2=None, **kwargs):

        super().__init__(**kwargs)

        if hwint_1 is not None:
            self.hwint_1 = hwint_1

        if hwint_2 is not None:
            self.hwint_2 = hwint_2


class Distance(SensorDataType):

    distance = EAttribute(eType=EFloat, derived=False, changeable=True)

    def __init__(self, *, distance=None, **kwargs):

        super().__init__(**kwargs)

        if distance is not None:
            self.distance = distance


class Temperature(SensorDataType):

    temperature = EAttribute(eType=EFloat, derived=False, changeable=True)

    def __init__(self, *, temperature=None, **kwargs):

        super().__init__(**kwargs)

        if temperature is not None:
            self.temperature = temperature


class Humidity(SensorDataType):

    humidity = EAttribute(eType=EFloat, derived=False, changeable=True)

    def __init__(self, *, humidity=None, **kwargs):

        super().__init__(**kwargs)

        if humidity is not None:
            self.humidity = humidity


class Gas(SensorDataType):

    gas = EAttribute(eType=EFloat, derived=False, changeable=True)

    def __init__(self, *, gas=None, **kwargs):

        super().__init__(**kwargs)

        if gas is not None:
            self.gas = gas


class LineFollower(SensorDataType):

    irs = EReference(ordered=True, unique=True, containment=False, upper=-1)

    def __init__(self, *, irs=None, **kwargs):

        super().__init__(**kwargs)

        if irs:
            self.irs.extend(irs)


class MotorController(ActuatorDataType):

    rpm = EAttribute(eType=EBoolean, derived=False, changeable=True)
    motors = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, motors=None, rpm=None, **kwargs):

        super().__init__(**kwargs)

        if rpm is not None:
            self.rpm = rpm

        if motors:
            self.motors.extend(motors)


class LedsController(ActuatorDataType):

    leds = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, leds=None, **kwargs):

        super().__init__(**kwargs)

        if leds:
            self.leds.extend(leds)


class ServoController(ActuatorDataType):

    degrees = EAttribute(eType=EBoolean, derived=False, changeable=True)
    servos = EReference(ordered=True, unique=True, containment=False, upper=-1)

    def __init__(self, *, degrees=None, servos=None, **kwargs):

        super().__init__(**kwargs)

        if degrees is not None:
            self.degrees = degrees

        if servos:
            self.servos.extend(servos)


class ButtonArray(SensorDataType):

    buttons = EReference(ordered=True, unique=True, containment=False, upper=-1)

    def __init__(self, *, buttons=None, **kwargs):

        super().__init__(**kwargs)

        if buttons:
            self.buttons.extend(buttons)


class Button(SensorDataType):

    value = EAttribute(eType=EInt, derived=False, changeable=True)

    def __init__(self, *, value=None, **kwargs):

        super().__init__(**kwargs)

        if value is not None:
            self.value = value


class Imu(SensorDataType):

    accelerometer = EReference(ordered=True, unique=True, containment=False)
    magnetometer = EReference(ordered=True, unique=True, containment=False)
    gyroscope = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, accelerometer=None, magnetometer=None, gyroscope=None, **kwargs):

        super().__init__(**kwargs)

        if accelerometer is not None:
            self.accelerometer = accelerometer

        if magnetometer is not None:
            self.magnetometer = magnetometer

        if gyroscope is not None:
            self.gyroscope = gyroscope


class IrMeasurement(SensorDataType):

    ir_value = EAttribute(eType=EInt, derived=False, changeable=True)

    def __init__(self, *, ir_value=None, **kwargs):

        super().__init__(**kwargs)

        if ir_value is not None:
            self.ir_value = ir_value


class Servo(ActuatorDataType):

    value = EAttribute(eType=EFloat, derived=False, changeable=True)

    def __init__(self, *, value=None, **kwargs):

        super().__init__(**kwargs)

        if value is not None:
            self.value = value


class Motor(ActuatorDataType):

    speed = EAttribute(eType=EFloat, derived=False, changeable=True)

    def __init__(self, *, speed=None, **kwargs):

        super().__init__(**kwargs)

        if speed is not None:
            self.speed = speed


class Led(ActuatorDataType):

    intensity = EAttribute(eType=EInt, derived=False, changeable=True)
    color = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, intensity=None, color=None, **kwargs):

        super().__init__(**kwargs)

        if intensity is not None:
            self.intensity = intensity

        if color is not None:
            self.color = color


class Accelerometer(SensorDataType, ThreeDimensions):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class Magnetometer(SensorDataType, ThreeDimensions):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class Gyroscope(SensorDataType, ThreeDimensions):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
