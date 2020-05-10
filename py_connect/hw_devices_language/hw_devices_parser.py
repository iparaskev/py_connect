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
    FREQ_MULT = {"hz": 1., "ghz": 10.**9}
    MEM_MULT = {"b": 1., "kb": 1024, "mb": 1024*1024, "gb": 1024*1024*1024}

    def __init__(self, device_file):
        """Constructor"""
        # Load metamodel.
        self._hw_mm = metamodel_from_file(self.MM_GRAMMAR, debug=False)

        # Load model.
        self._model = self._hw_mm.model_from_file(join(self.DEVICE_DB, device_file))

        # Parse model.
        self.parse_model()

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

    #TODO cleaner setattr
    def _handle_attr(self, attr, dev):  # noqa C901
        """Handle an attribute"""
        attr_val = None
        net_flag = False

        if attr.name == "os":
            attr_val = self.OS_MAPPER[attr.val]
        elif attr.name == "network":
            # Create new interfaces and append to list
            net_ls = []
            for net_inter in attr.val:
                net = self._instantiate_network(net_inter)
                net_ls.append(net)
            attr_val = net_ls
            net_flag = True
        elif attr.name == "bluetooth":
            attr_val = Bluetooth(version=attr.val.version)
        elif attr.name == "cpu":
            attr_val = CPU(cpu_family=attr.val.cpu_family,
                           max_freq=float(attr.val.max_freq
                                          * self.FREQ_MULT[attr.val.unit]),
                           fpu=attr.val.fpu)
        elif attr.name == "memory":
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
            pass
        else:
            attr_val = attr.val

        # Set attribute
        if net_flag:
            getattr(dev, attr.name).extend(attr_val)
        else:
            setattr(dev, attr.name, attr_val)
        print(f"Attribute: {attr.name} Value: {getattr(dev, attr.name)}")

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
