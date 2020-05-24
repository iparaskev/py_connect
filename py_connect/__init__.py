"""py_connect init"""

import argparse
from .hw_devices import *
from .hw_devices.power_connections import *
from .hw_devices.hw_connections import *
from .hw_devices_language import *
from .definitions import DEVICES_DB
from .m2t import *


def parse_args():
    """Initialize argument parser.
    Returns:
        An instance of argparse.Argument parser.
    """

    parser = argparse.ArgumentParser()

    # Add arguments
    parser.add_argument("--device", help="Path to a device specification.")
    parser.add_argument("--store", help="Move device specification to db.",
                        action="store_true")
    parser.add_argument("--xmi", help="Export xmi.",
                        action="store_true")
    parser.add_argument("--xmi_path", help="Folder for saving xmi files.")
    parser.add_argument("--db_path", help="Path to custom devices db.")
    parser.add_argument("--connections",
                        help="Path to a connection specification.")
    parser.add_argument("--source",
                        help="Flag for getting source code.",
                        action="store_true")
    parser.add_argument("--specific_con",
                        help="The name of the specific connection.")

    return parser.parse_args()


def main():  # noqa C901
    args = parse_args()

    # Device actions
    if args.device:
        dev = DeviceHandler(args.device, devices_db_path=args.db_path)

        # Save to xmi.
        if args.xmi:
            dev.export_xmi(path=args.xmi_path)

        # Store to db
        if args.store and args.db_path:
            with open(args.device, "r") as f:
                lines = f.readlines()
            with open(dev.db_path + args.device, "w") as f:
                f.writelines(lines)

    # Connection args
    if args.connections:
        connections = ConnectionsHandler(args.connections)

        # Save to xmi.
        if args.xmi:
            if args.specific_con:
                connections.export_xmi(args.specific_con, path=args.xmi_path)
            else:
                for key in connections.connections.keys():
                    connections.export_xmi(key, path=args.xmi_path)

        if args.source:
            m2t = Generator()
            if args.specific_con:
                source = m2t.generate(connections.connections[args.specific_con])
                print(source)
            else:
                for key in connections.connections.keys():
                    source = m2t.generate(connections.connections[key])
                    print(source)


if __name__ == "__main__":
    main()
