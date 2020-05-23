"""hw_devices_parser.py"""

from textx import metamodel_from_file
from textx.export import metamodel_export, model_export
from pyecore.ecore import BadValueError
from pyecore.resources import ResourceSet, URI
from ..hw_devices import *
from ..definitions import DEVICE_GRAMMAR, DEVICES_DB


class DeviceHandler():
    """A class for creating and handling an in memory hw_devices pyecore model
    from a textx hw_devices model.

    Args:
    """

    MM_GRAMMAR = DEVICE_GRAMMAR  # path of grammar
    # Mapper of os ecore types.
    OS_MAPPER = {
        "raspbian": OSType.RASPBIAN,
        "riot": OSType.RIOT
    }
    # Mapper of peripheral type ecore types.
    PER_MAPPER = {
        "sensor": PeripheralType.SENSOR,
        "actuator": PeripheralType.ACTUATOR
    }
    # Mapper of power_pin type ecore types.
    POWER_MAPPER = {
        "gnd": PowerType.GND,
        "3v3": PowerType.Power3V3,
        "5v": PowerType.Power5V,
    }
    # Mapper of gpio type ecore types.
    GPIO_MAPPER = {
        "input": GPIOType.INPUT,
        "output": GPIOType.OUTPUT,
        "both": GPIOType.BOTH,
    }
    # Multipliers for values
    FREQ_MULT = {"hz": 1., "ghz": 10.**9}
    MEM_MULT = {"b": 1., "kb": 1024, "mb": 1024*1024, "gb": 1024*1024*1024}
    # Possible values of gpio pin functionalities per hw interface.
    GPIO_TYPES = ["input", "output", "both"]
    I2C_TYPES = ["sda", "scl"]
    SPI_TYPES = ["mosi", "miso", "sclk", "ce"]
    UART_TYPES = ["rx", "tx"]
    PWM_TYPES = ["pwm"]

    def __init__(self, device_file, devices_db_path=None):
        """Constructor"""
        # Load metamodel.
        self._hw_mm = metamodel_from_file(self.MM_GRAMMAR, debug=False)

        # Update devices db path
        if devices_db_path:
            devices_db_path = devices_db_path.rstrip("/") + "/"
            self.db_path = devices_db_path
        else:
            self.db_path = DEVICES_DB

        # Load model.
        try:
            self._model = self._hw_mm.model_from_file(self.db_path + device_file)
        except FileNotFoundError:
            print("File not found in db. Use absolute path.")
            self._model = self._hw_mm.model_from_file(device_file)

        # A dictionary for storing the hw interfaces
        self.hw_interfaces = {
            "gpio": {},
            "i2c": {},
            "spi": {},
            "uart": {},
            "adc": {},
            "pwm": {}
        }
        # Dictionary for power pins
        self.power_pins = {}

        # Parse model.
        self.parse_model()

    def parse_model(self):
        """Parse the textx model.

        Parse the in memory textx model and create an in memory pyecore model.
        """
        # Create proper device object
        if isinstance(self._model, self._get_class("Board")):
            self.dev = self._instantiate_device(self._model, Board)

            # Make master all i2c and spi interfaces
            for key, i2c in self.hw_interfaces["i2c"].items():
                i2c.is_master = True
            for key, spi in self.hw_interfaces["spi"].items():
                spi.is_master = True
                # Update the max master conns
                spi.max_master_cons = len(spi.ce)
        elif isinstance(self._model, self._get_class("Peripheral")):
            self.dev = self._instantiate_device(self._model, Peripheral)
            setattr(self.dev, "type", self._per_type)

    def _instantiate_device(self, model, device_class):
        """Instantiate a board object from textx model.

        Args:
            model (textx model): The model.
            device_class (class): Class for devices.

        Returns:
            (Board instance): A Board instance
        """
        dev = device_class()

        count_dic = {}  # Dictionary for checking duplicates

        # Parse attributes
        for key, val in model.__dict__.items():
            if key[0] != "_" and val:
                self._handle_attr(val, dev)

        # Create hw_interfaces
        for hw_key in self.hw_interfaces.keys():
            for key, interface in self.hw_interfaces[hw_key].items():
                dev.hw_interfaces.append(interface)

        return dev

    def _handle_attr(self, attr, dev):
        """Set an attribute in the device object.

        Args:
            attr (textx object): The attribute to be added
            dev (Device object): The device to be updated
        """
        attr_val = None
        list_flag = False

        if attr.name == "os":
            attr_val = self.OS_MAPPER[attr.val]
        elif attr.name == "network":
            attr_val = self._create_network(attr.val)
            list_flag = True
        elif attr.name == "bluetooth":
            attr_val = Bluetooth(version=attr.val.version)
        elif attr.name == "cpu":
            attr_val = CPU(cpu_family=attr.val.cpu_family,
                           max_freq=float(attr.val.max_freq
                                          * self.FREQ_MULT[attr.val.unit]),
                           fpu=attr.val.fpu)
        elif attr.name == "memory":
            attr_val = self._create_memory(attr.val)
        elif attr.name == "type":
            self._per_type = self.PER_MAPPER[attr.val]
        elif attr.name == "pins":
            list_flag = True
            attr_val = self._create_pins(attr.val)
        else:
            attr_val = attr.val

        # Set attribute
        if list_flag:
            getattr(dev, attr.name).extend(attr_val)
        elif attr_val:
            setattr(dev, attr.name, attr_val)

    def _gpio_pin(self, pin_obj, gpio_type):
        """Instantiate a gpio hw interface."""
        self.hw_interfaces["gpio"][pin_obj.name] = \
            GPIO(name=pin_obj.name, pin=pin_obj, type=self.GPIO_MAPPER[gpio_type])

    def _busable_pin(self, pin_obj, type, bus, prefix, clss):
        """Create a hw interface for a busable pin update attrs.

        Args:
            pin_obj (Pin object): The pin to be added as attribute.
            type (str): The name of the attribute.
            bus (int): The bus of the hw interface.
            prefix (str): Prefix for getting the right dictionary. Ex i2c
        """
        name = f"{prefix}_{bus}"
        try:
            try:
                setattr(self.hw_interfaces[prefix][name], type, pin_obj)
            except KeyError:
                self.hw_interfaces[prefix][name] = clss(name=name, bus=bus)
                setattr(self.hw_interfaces[prefix][name], type, pin_obj)
        except BadValueError:
            getattr(self.hw_interfaces[prefix][name], type).append(pin_obj)

    def _pwm_pin(self, pin_obj):
        """Create a pwm hw interface

        Args:
            pin_obj (Pin object): The pin to be added as attribute.

        """
        self.hw_interfaces["pwm"][pin_obj.name] = PWM(pin=pin_obj)

    def _create_network(self, networks):
        # Create new interfaces and append to list
        net_ls = []
        for net_inter in networks:
            if isinstance(net_inter, self._get_class("WIFI")):
                net = Wifi()
                freq_ls = []
                # Append frequencies.
                for f in net_inter.freq:
                    freq_ls.append(
                        WifiFreq(freq=f*self.FREQ_MULT[net_inter.unit])
                    )
                getattr(net, "freqs").extend(freq_ls)
                #print(f"Wifi: {[f.freq for f in net.freqs]}")
            elif isinstance(net_inter, self._get_class("ETHERNET")):
                net = Ethernet()
            setattr(net, "name", net_inter.name)
            net_ls.append(net)

        return net_ls

    def _create_memory(self, memory):
        """Create memory object"""
        ram_val = float(memory.ram.val * self.MEM_MULT[memory.ram.unit])\
            if memory.ram is not None else None
        rom_val = float(memory.rom.val * self.MEM_MULT[memory.rom.unit])\
            if memory.rom is not None else None
        external_memory_val =\
            float(memory.external_memory.val
                  * self.MEM_MULT[memory.external_memory.unit]) \
            if memory.external_memory is not None else None

        return \
            Memory(ram=ram_val, rom=rom_val, external_memory=external_memory_val)

    def _create_pins(self, pins):
        """Create pins"""
        attr_val = []
        # Iterate through all pins
        for pin in pins:
            pin_obj = None  # The pin object to be appended

            # Power pin
            if isinstance(pin, self._get_class("POWER_PIN")):
                pin_obj = PowerPin(name=pin.name, number=pin.number,
                                   type=self.POWER_MAPPER[pin.type])
                self.power_pins[pin.name] = pin_obj
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
                        self._busable_pin(
                            pin_obj, func.type, func.bus, "i2c", I2C
                        )
                    elif func.type in self.SPI_TYPES:
                        self._busable_pin(
                            pin_obj, func.type, func.bus, "spi", SPI
                        )
                    elif func.type in self.UART_TYPES:
                        self._busable_pin(
                            pin_obj, func.type, func.bus, "uart", UART
                        )
                    elif func.type in self.PWM_TYPES:
                        self._pwm_pin(pin_obj)
            attr_val.append(pin_obj)

        return attr_val

    def _get_class(self, name):
        """Get class from textx meta model.

        Args:
            name (str): The name of the class.

        Returns:
            (class): The class type
        """
        return self._hw_mm.namespaces["hw_devices"][name]

    def export_xmi(self, path=None):
        """Export model xmi."""
        name = self.dev.name + ".xmi"
        if path:
            path = path.rstrip("/") + "/"
            name = path + name
        # Save model
        rset = ResourceSet()
        r = rset.create_resource(URI(name))
        r.append(self.dev)
        r.save()
