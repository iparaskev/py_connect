
from .hw_devices import getEClassifier, eClassifiers
from .hw_devices import name, nsURI, nsPrefix, eClass
from .hw_devices import Device, Pin, PowerPin, IOPin, Power3V3, Power5V, Gnd, GpioInput, GpioOutput, I2cSda, I2cScl, Pwm, UartRx, UartTx, SpiMiso, SpiSclk, SpiMosi, SpiCe, Computational, NonComputational, DeviceType, GpioDevice, I2cDevice, CompositeDevice, GpioPin, I2cPin, SpiPin, UartPin


from . import hw_devices

__all__ = ['Device', 'Pin', 'PowerPin', 'IOPin', 'Power3V3', 'Power5V', 'Gnd', 'GpioInput', 'GpioOutput', 'I2cSda', 'I2cScl', 'Pwm', 'UartRx', 'UartTx', 'SpiMiso',
           'SpiSclk', 'SpiMosi', 'SpiCe', 'Computational', 'NonComputational', 'DeviceType', 'GpioDevice', 'I2cDevice', 'CompositeDevice', 'GpioPin', 'I2cPin', 'SpiPin', 'UartPin']

eSubpackages = []
eSuperPackage = None
hw_devices.eSubpackages = eSubpackages
hw_devices.eSuperPackage = eSuperPackage

Device.power_pins.eType = PowerPin
Computational.pins.eType = Pin
Computational.devices.eType = NonComputational
GpioDevice.gpio_pins.eType = GpioPin
I2cDevice.i2c_pins.eType = I2cPin
Power3V3.conn_to.eType = Power3V3
Power3V3.conn_from.eType = Power3V3
Power3V3.conn_from.eOpposite = Power3V3.conn_to
Power5V.conn_to.eType = Power5V
Power5V.conn_from.eType = Power5V
Power5V.conn_from.eOpposite = Power5V.conn_to
Gnd.conn_to.eType = Gnd
Gnd.conn_from.eType = Gnd
Gnd.conn_from.eOpposite = Gnd.conn_to
GpioInput.conn_from.eType = GpioOutput
GpioOutput.conn_to.eType = GpioInput
GpioOutput.conn_to.eOpposite = GpioInput.conn_from
I2cSda.conn_to.eType = I2cSda
I2cSda.conn_from.eType = I2cSda
I2cSda.conn_from.eOpposite = I2cSda.conn_to
I2cScl.conn_to.eType = I2cScl
I2cScl.conn_from.eType = I2cScl
I2cScl.conn_from.eOpposite = I2cScl.conn_to
Pwm.conn_to.eType = Pwm
Pwm.conn_from.eType = Pwm
Pwm.conn_from.eOpposite = Pwm.conn_to

otherClassifiers = [DeviceType]

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)
