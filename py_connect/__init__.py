"""py_connect init"""

import argparse
from .hw_devices import *
from .hw_devices.power_connections import *
from .hw_devices.hw_connections import *
from .hw_devices_language import *
from .definitions import DEVICES_DB


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
    parser.add_argument("--connections",
                        help="Path to a connection specification.")
    parser.add_argument("--db_path", help="Path to custom devices db.")

    return parser.parse_args()


def main():
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


if __name__ == "__main__":
    main()
