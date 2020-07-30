"""py_connect init"""

import argparse
from .hw_devices import *
from .hw_devices.power_connections import *
from .hw_devices.hw_connections import *
from .hw_devices_language import *
from .definitions import DEVICES_DB
from .m2t import *
from .drawer import *
from .get_impls import *
from .exceptions import NotImplementedDriverError
from .search_repos import search_repos


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
                        help="Flag for generating source code.",
                        action="store_true")
    parser.add_argument("--schematic",
                        help="The name of the source code.",
                        action="store_true")
    parser.add_argument("--specific_con",
                        help="The name of the specific connection.")
    parser.add_argument("--update_pidevices",
                        help="Update pidevices implementations.",
                        action="store_true")

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

        # Generate source code.
        if args.source:
            m2t = Generator()
            try:
                if args.specific_con:
                    conn_name = args.specific_con
                    source =\
                        m2t.generate(connections.connections[args.specific_con])
                    m2t.write_source(source, conn_name + ".py")
                else:
                    for key in connections.connections.keys():
                        conn_name = key
                        source = m2t.generate(connections.connections[key])
                        m2t.write_source(source, conn_name + ".py")
            except NotImplementedDriverError as e:
                print(e)
                search_repos(connections.connections[conn_name].peripheral.name,
                             "python")

        # Schematic image.
        if args.schematic:
            drawer = Drawer()
            if args.specific_con:
                conn_name = args.specific_con
                drawer.draw_connection(connections.connections[args.specific_con])
                drawer.save(conn_name + ".png")
            else:
                for key in connections.connections.keys():
                    conn_name = key
                    print(conn_name)
                    drawer.draw_connection(connections.connections[key])
                    drawer.save(conn_name + ".png")

    if args.update_pidevices:
        getter = ImplementationsGetter("pidevices")
        getter.update_pidevices("better_imports")


if __name__ == "__main__":
    main()
