"""hw_devices_parser.py"""

from os.path import join, dirname
from textx import metamodel_from_file
from textx.export import metamodel_export, model_export

import sys
sys.path.append(".")

from py_connect.hw_devices import *  # noqa E402


class DeviceHandler():
    """A class for creating and handling an in memory hw_devices pyecore model
    from a textx hw_devices model.

    Args:
    """

    MM_GRAMMAR = join(dirname(__file__), "hw_devices.tx")
    DEVICE_DB = dirname(__file__)
    OS_MAPPER = {
        "raspbian": OSType.RASPBIAN,
        "riot": OSType.RIOT
    }
    PER_MAPPER = {
        "sensor": PeripheralType.SENSOR,
        "actuator": PeripheralType.ACTUATOR
    }
    POWER_MAPPER = {
        "gnd": PowerType.GND,
        "3v3": PowerType.Power3V3,
        "5v": PowerType.Power5V,
    }
    GPIO_MAPPER = {
        "input": GPIOType.INPUT,
        "output": GPIOType.OUTPUT,
        "both": GPIOType.BOTH,
    }
    FREQ_MULT = {"hz": 1., "ghz": 10.**9}
    MEM_MULT = {"b": 1., "kb": 1024, "mb": 1024*1024, "gb": 1024*1024*1024}
    GPIO_TYPES = ["input", "output", "both"]
    I2C_TYPES = ["sda", "scl"]
    SPI_TYPES = ["mosi", "miso", "sclk", "ce"]
    UART_TYPES = ["rx", "tx"]
    PWM_TYPES = ["pwm"]

    def __init__(self, device_file):
        """Constructor"""
        # Load metamodel.
        self._hw_mm = metamodel_from_file(self.MM_GRAMMAR, debug=False)

        # Load model.
        self._model = self._hw_mm.model_from_file(join(self.DEVICE_DB, device_file))

        # A dictionary for storing the hw interfaces
        self.hw_interfaces = {
            "gpio": {},
            "i2c": {},
            "spi": {},
            "uart": {},
            "adc": {},
            "pwm": {}
        }

        # Parse model.
        self.parse_model()
        print(self.hw_interfaces)

    def parse_model(self):
        """Parse the textx model.

        Parse the in memory textx model and create an in memory pyecore model.
        """
        # Create proper device object
        if isinstance(self._model, self._get_class("Board")):
            self.dev = self._instantiate_board(self._model)
        elif isinstance(self._model, self._get_class("Peripheral")):
            self.dev = self._instantiate_peripheral(self._model)

    def _instantiate_board(self, model):
        """Instantiate a board object from textx model.

        Args:
            model (textx model): The model.

        Returns:
            (Board instance): A Board instance
        """
        dev = Board()

        count_dic = {}  # Dictionary for checking duplicates

        # Parse attributes
        for attr in model.attrs:
            try:
                count_dic[attr.name] += 1
                # TODO raise duplicate exception
            except KeyError:
                count_dic[attr.name] = 1

            self._handle_attr(attr, dev)

    #TODO: cleaner setattr
    def _handle_attr(self, attr, dev):  # noqa C901
        """Handle an attribute"""
        attr_val = None
        list_flag = False

        if attr.name == "os":                             # os attribute
            attr_val = self.OS_MAPPER[attr.val]
        elif attr.name == "network":                      # network attribute
            # Create new interfaces and append to list
            net_ls = []
            for net_inter in attr.val:
                net = self._instantiate_network(net_inter)
                net_ls.append(net)
            attr_val = net_ls
            list_flag = True
        elif attr.name == "bluetooth":                   # bluetooth attribute
            attr_val = Bluetooth(version=attr.val.version)
        elif attr.name == "cpu":
            attr_val = CPU(cpu_family=attr.val.cpu_family,
                           max_freq=float(attr.val.max_freq
                                          * self.FREQ_MULT[attr.val.unit]),
                           fpu=attr.val.fpu)
        elif attr.name == "memory":                      # memory attribute
            ram_val = float(attr.val.ram.val * self.MEM_MULT[attr.val.ram.unit])\
                if attr.val.ram is not None else None
            rom_val = float(attr.val.rom.val * self.MEM_MULT[attr.val.rom.unit])\
                if attr.val.rom is not None else None
            external_memory_val =\
                float(attr.val.external_memory.val
                      * self.MEM_MULT[attr.val.external_memory.unit]) \
                if attr.val.external_memory is not None else None
            attr_val = \
                Memory(ram=ram_val, rom=rom_val,
                       external_memory=external_memory_val)
        elif attr.name == "type":
            pass
        elif attr.name == "pins":
            list_flag = True
            attr_val = []
            # Iterate through all pins
            for pin in attr.val:
                pin_obj = None  # The pin object to be appended

                # Power pin
                if isinstance(pin, self._get_class("POWER_PIN")):
                    pin_obj = PowerPin(name=pin.name, number=pin.number,
                                       type=self.POWER_MAPPER[pin.type])
                # Analog pin
                elif isinstance(pin, self._get_class("IO_ANALOG")):
                    pin_obj = AnalogPin(name=pin.name,
                                        number=pin.number,
                                        vmax=pin.vmax)
                # Digital pin
                else:
                    pin_obj = DigitalPin(name=pin.name,
                                         number=pin.number)

                    # Parse function to make hw interfaces
                    for func in pin.funcs:
                        if func.type in self.GPIO_TYPES:
                            self._gpio_pin(pin_obj, func.type)
                        elif func.type in self.I2C_TYPES:
                            self._i2c_pin(pin_obj, func.type, func.bus)
                        elif func.type in self.SPI_TYPES:
                            self._spi_pin(pin_obj, func.type, func.bus)
                        elif func.type in self.UART_TYPES:
                            self._uart_pin(pin_obj, func.type, func.bus)
                        elif func.type in self.PWM_TYPES:
                            self._pwm_pin(pin_obj, func.type, func.freq)
                attr_val.append(pin_obj)
        else:
            attr_val = attr.val

        # Set attribute
        if list_flag:
            getattr(dev, attr.name).extend(attr_val)
        else:
            setattr(dev, attr.name, attr_val)
        #print(f"Attribute: {attr.name} Value: {getattr(dev, attr.name)}")

    def _gpio_pin(self, pin_obj, gpio_type):
        """Instanciate a gpio hw interface."""
        self.hw_interfaces["gpio"][pin_obj.name] = \
            GPIO(name=pin_obj.name, pin=pin_obj, type=self.GPIO_MAPPER[gpio_type])

    def _i2c_pin(self, pin_obj, i2c_type, bus):
        """Handle an i2c pin."""
        name = f"i2c_{bus}"
        try:
            setattr(self.hw_interfaces["i2c"][name], i2c_type, pin_obj)
        except KeyError:
            self.hw_interfaces["i2c"][name] = I2C(name=name, bus=bus)
            setattr(self.hw_interfaces["i2c"][name], i2c_type, pin_obj)

    def _spi_pin(self, pin_obj, spi_type, bus):
        """Handle an spi pin."""
        pass

    def _uart_pin(self, pin_obj, uart_type, bus):
        """Handle an uart pin."""
        pass

    def _pwm_pin(self, pin_obj, freq):
        """Handle an pwm pin."""
        pass

    def _instantiate_network(self, net_inter):
        if isinstance(net_inter, self._get_class("WIFI")):
            net = Wifi()
            freq_ls = []
            # Append frequencies.
            for f in net_inter.freq:
                freq_ls.append(
                    WifiFreq(freq=f*self.FREQ_MULT[net_inter.unit])
                )
            getattr(net, "freqs").extend(freq_ls)

            print(f"Wifi: {[f.freq for f in net.freqs]}")
        elif isinstance(net_inter, self._get_class("ETHERNET")):
            net = Ethernet()
        setattr(net, "name", net_inter.name)
        print(f"Net: {net.name}")

        return net

    def _instantiate_peripheral(self, model):
        """Instantiate a peripheral object from textx model.

        Args:
            model (textx model): The model.

        Returns:
            (Peripheral instance): A Peripheral instance
        """
        pass

    def _get_class(self, name):
        """Get class from textx meta model.

        Args:
            name (str): The name of the class.

        Returns:
            (class): The class type
        """
        return self._hw_mm.namespaces["hw_devices"][name]


def main():
    pi = DeviceHandler("debug.hwd")


if __name__ == "__main__":
    main()
