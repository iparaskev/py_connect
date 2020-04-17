"""model_loader.py"""

import os
import importlib
from pyecore.resources import ResourceSet, URI
import sys
sys.path.append(".")


def load_model(name):
    """Load a device model from a xmi.

    Args:
        name (str): Name of the device.

    Returns:
        (Device Object): A board or a peripheral device object.
    """
    f_path = os.path.abspath(__file__)
    root_path = "/".join(os.path.dirname(f_path).split("/")[:-1])
    rset = ResourceSet()
    resource = rset.get_resource(URI(root_path + "/models/hw_devices.ecore"))
    mm_root = resource.contents[0]
    rset.metamodel_registry[mm_root.nsURI] = mm_root

    # Load model instance
    r = rset.get_resource(URI(root_path + "/devices_db/" + name + ".xmi"))
    return r.contents[0]


def load_model_py(name):
    """Load a device model from a xmi.

    Args:
        name (str): Name of the device.

    Returns:
        (Device Object): A board or a peripheral device object.
    """
    f_path = os.path.abspath(__file__)
    root_path = "/".join(os.path.dirname(f_path).split("/")[:-1])
    module = importlib.import_module("devices_db." + name)
    return getattr(module, "dev")


#print(load_model_py("rpi_3b_plus"))