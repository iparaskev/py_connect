"""connections_parser.py"""

from os.path import join, dirname
from textx import metamodel_from_file
from textx.export import metamodel_export, model_export
from pyecore.ecore import BadValueError

import sys
sys.path.append(".")

from py_connect.hw_devices import *  # noqa E402


class ConnectionsHandler():
    """Class for handling connections"""

    MM_GRAMMAR = join(dirname(__file__), "connection.tx")  # path of grammar
    DEVICE_DB = dirname(__file__)  # path of devices db

    def __init__(self, connections_file):
        """Constructor"""
        # Load metamodel.
        self._hw_mm = metamodel_from_file(self.MM_GRAMMAR, debug=False)

        # Load model.
        self._model = self._hw_mm.model_from_file(join(self.DEVICE_DB,
                                                       connections_file))
        print(dir(self._model))
        print(self._model.includes)
        print(self._model.connections)
        print(self._model.includes)
        print(self._model.connections[0].name)
        print(self._model.connections[0].board)
        print(self._model.connections[0].peripheral)
        print(self._model.connections[0].power_conns)
        print(self._model.connections[0].power_conns[0])
        print(self._model.connections[0].hw_conns)


def main():
    connections = ConnectionsHandler("debug_connection.cd")


if __name__ == "__main__":
    main()
