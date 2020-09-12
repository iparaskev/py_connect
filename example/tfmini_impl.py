"""tfmini_impl.py"""

from .distance_sensor import DistanceSensor

# Already implemented
# -*- coding: utf-8 -*
import serial


class TfMini(DistanceSensor):
    """Class implementing tfmini. Source code is borrowed from
    https://github.com/TFmini/TFmini-RaspberryPi.
    """

    def __init__(self, port="COM12", baudrate=115200):
        self._port = port
        self._baudrate = 115200

        self.start()

    def start(self):
        self.serial = serial.Serial(self._port, self._baudrate)

        if not self.serial.is_open:
            self.serial.open()

    def read(self):
        while True:
            #time.sleep(0.1)
            count = self.serial.in_waiting
            if count > 8:
                recv = self.serial.read(9)
                self.serial.reset_input_buffer()

                if recv[0] == 0x59 and recv[1] == 0x59:
                    distance = recv[2] + recv[3] * 256
                    #strength = recv[4] + recv[5] * 256
                    self.serial.reset_input_buffer()
                    return distance

    def stop(self):
        if self.serial:
            self.serial.close()
