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
        
    def validate_connection(self, device):  
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
            l_pin = len(connection.pins_connections)
            i = 0
            while i < l_pin and not break_flag:
                pin_con = connection.pins_connections[i]
                comp_pin = pin_con.comp_pin
                non_comp = pin_con.non_comp_pin

                # Check if pins have the right ansenstors
                break_flag = not (non_comp.device == connected_dev)
                if break_flag:
                    self._log_error("Should use pin of non comp dev.")
                break_flag = not (comp_pin.device == device)
                if break_flag:
                    self._log_error("Should use pin of comp dev.")

                # Check types of devices that have the connected pins
                break_flag = isinstance(comp_pin.device, NonComputational)
                if break_flag:
                    self._log_error("Should be pin from comp device.")
                break_flag = isinstance(non_comp.device, Computational)
                if break_flag:
                    self._log_error("Should be pin from non comp device.")
    
                # Checks for power pin with io pin
                break_flag = self._check_power(comp_pin, non_comp)

                # Continue if both pins aren't power
                if break_flag is None:

                    # Check for different modes.
                    # Make a dictionary with fucntions for faster search.
                    comp_funcs = {}
                    for f in comp_pin.functions:
                        comp_funcs[f.type] = True

                    break_flag = self._check_io_type(non_comp.functions[0].type,
                                                     [IOType.I2C_SDA, IOType.PWM,
                                                      IOType.I2C_SCL],
                                                     comp_funcs, 
                                                     non_comp.functions[0].type,
                                                     "Should ne the same function")
                    break_flag = not break_flag
                    break_flag = self._check_io_type(non_comp.functions[0].type,
                                                     [IOType.GPIO_INPUT,
                                                      IOType.GPIO_OUTPUT,
                                                      IOType.GPIO_BOTH],
                                                     comp_funcs, IOType.GPIO_BOTH,
                                                     "Should ne the gpio pin")
                    break_flag = not break_flag
                    
                i += 1
            # Break loop if there is wrong mode
            if break_flag:
                break
        else:
            ret_val = True

        return ret_val

    def _check_dev_type(self, dev, cls, msg):
        """Check class type of device

        Args:
            dev (Device object): The device to be checked.
            cls (class type): The checked class type.
            msg (str): The error msg

        Returns:
            (bool)
        """
        ret = isinstance(dev, cls)
        if ret:
            self._log_error(msg)
        return ret

    # TODO make valid results
    def _check_power(self, comp, non_comp):
        """_check_power

        Args:
            comp (Pin object): Pin of computational device
            non_comp (Pin object): Pin on non computational device

        Returns:
        """
        f_comp = isinstance(comp, PowerPin)
        f_non = isinstance(non_comp, PowerPin)
        ret = None
        # Both Power
        if f_comp and f_non:
            ret = (comp.function == non_comp.function)
            ret = not ret
        elif f_comp or f_non:
            ret = False
            self._log_error("Must both or neither be power.")
            ret = not ret
        return ret

    def _check_io_type(self, non_type, types, funcs, check_func, msg):
        """Check proper connection for io pins.

        Args:
            non_type (IOType object): The type of the non computational pin 
                function.
            types (list): A list with the possible types to check
            funcs (dict): A dictionary for hashing the supported io functions 
                of the computational pin.
            check_func (IOType object): The value that must be in computational
                pin's functions.
            msg (str): The error msg

        Returns:
            (bool)
        """
        ret = True
        cond = sum([non_type == typ for typ in types])
        if cond:
            try:
                _ = funcs[check_func]
            except KeyError:
                self._log_error(msg)
                ret = False
        return ret
