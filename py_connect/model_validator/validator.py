"""validator.py"""

from ..hw_devices import *


class Validator():

    def __init__(self):
        pass

    def _log_error(self, msg):
        """Log an error msg

        Args:
            msg (str): The msg
        """
        print("[ERROR]: {}".format(msg))
        
    def validate_connection(self, device):  # noqa C901
        """Given a computational device validate all it's connections.

        Args:
            device (Computational object): A computational device object.

        Returns:
            (bool): Indicating if it is valid or not.
        """
        ret_val = False

        # Iterate through all the connected devices.
        break_flag = False
        for connection in device.connected_devices:
            # Get connected device for assertion
            connected_dev = connection.device

            # Iterate through all the pin connections
            l_pin = len(connection.pins.connections)
            i = 0
            while i < l_pin and not break_flag:
                pin_con = connection.pins_connections[i]
                comp_pin = pin_con.comp_pin
                non_comp = pin_con.non_comp_pin

                # Check types of devices that have the connected pins
                if isinstance(comp_pin.device, NonComputational):
                    self._log_error("Should be pin from computational device")
                    break_flag = True

                if isinstance(non_comp.device, Computational):
                    self._log_error("Should be pin from non computational device")
                    break_flag = True

                # Checks for power pin with io pin
                flag_comp = isinstance(comp_pin, PowerPin)
                flag_non = isinstance(non_comp, PowerPin)
                if (flag_comp and not flag_non) or (flag_non and not flag_comp):
                    self._log_error("Conn power with no power")
                    break_flag = True
                elif flag_comp and flag_non:
                    if comp_pin.function != non_comp.function:
                        self._log_error("Wrong power modes.")
                        break_flag = True
                    else:
                        continue

                # Check for different modes.
                # Make a dictionary with fucntions for faster search.
                functions = {}
                for f in comp_pin.functions:
                    functions[f] = True

                # I2C and PWM functions
                f_non = non_comp.functions[0]
                if (f_non == IOType.I2C_SDA) or \
                   (f_non == IOType.I2C_SCL) or \
                   (f_non == IOType.PWM): 
                    try:
                        _ = functions[f_non]
                    except KeyError:
                        self._log_error("Should be the same function")
                        break_flag = True
                        break
                
                # Check GPIO functions
                if (f_non == IOType.GPIO_INPUT) or (f_non == IOType.GPIO_OUTPUT):
                    try:
                        _ = functions[IOType.GPIO_BOTH]
                    except KeyError:
                        self._log_error("Should be gpio pin")
                        break_flag = True
                        break

                i += 1
            # Break loop if there is wrong mode
            if break_flag:
                break
        else:
            ret_val = True

        return ret_val
