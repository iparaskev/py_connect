"""paths"""

from os.path import dirname, join

ROOT_PATH = dirname(__file__)
DEVICES_DB = ROOT_PATH + "/devices_db/"
DEVICE_GRAMMAR = ROOT_PATH + "/hw_devices_language/hw_devices.tx"
CONNECTION_GRAMMAR = ROOT_PATH + "/hw_devices_language/connection.tx"
IMPLS_PATH = ROOT_PATH + "/m2t/driver_implementations"
PIDEVICES_IMPLS = IMPLS_PATH + "/pidevices.txt"
