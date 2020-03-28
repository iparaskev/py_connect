"""validator.py"""

from ..hw_devices import *


class Validator():

    # Lists that have the pin types per hardware interface
    I2C_TYPES = [IOType.I2C_SDA, IOType.I2C_SCL]
    GPIO_TYPES = [IOType.GPIO_INPUT, IOType.GPIO_OUTPUT, IOType.GPIO_BOTH]
    PWM_TYPES = [IOType.PWM]
    SPI_TYPES = []
    UART_TYPES = []

    def __init__(self):
        pass

    def _log_error(self, msg):
        """Log an error msg

        Args:
            msg (str): The msg
        """
        print("[ERROR]: {}".format(msg))
        
    def validate_connection(self, device, connection): 
        """Given a computational device validate all it's connections.

        Args:
            device (Computational object): A computational device object.
            connection (ConnecetedDevice object): A connection object between 
                the device and a non computational device.

        Returns:
            (bool): Indicating if it is valid or not.
        """
        ret_val = True  # The return value
        connected_dev = connection.device  # Get connected device for assertion

        # TODO follow same for other interfaces with more than one pin.
        # Dictionary for storing if both i2c functions has been used properly
        # Goes to connected device
        self._cur_i2c = {IOType.I2C_SDA: False, IOType.I2C_SCL: False}

        # Check if the devices of the connection are of the right type
        if isinstance(device, NonComputational):
            ret_val = False
            self._log_error("Should be a computational device")
        if isinstance(connected_dev, Computational):
            ret_val = False
            self._log_error("Should be a non computational device")

        for i, pin_con in enumerate(connection.pins_connections):
            # Break in case of wrong assertion
            if not ret_val:
                break

            comp_pin = pin_con.comp_pin
            non_comp = pin_con.non_comp_pin

            # Check if pins have the right ansenstors
            ra_flag = (non_comp.device == connected_dev)
            if not ra_flag:
                self._log_error("Should use pin of non comp dev.")
            ra_flag_comp = (comp_pin.device == device)
            if not ra_flag_comp:
                self._log_error("Should use pin of comp dev.")

            # Checks for power pin with io pin
            power_flag = self._check_power(comp_pin, non_comp)

            # Continue if both pins aren't power
            io_flag = True
            if power_flag is None:
                power_flag = True
                io_flag = self._io_checks(comp_pin, non_comp)
            
            ret_val = (ra_flag and ra_flag_comp and power_flag and io_flag)
        
        # Check if all i2c pins has been connected to the sensor.
        i2c_flag = self._check_complete(self._cur_i2c, "Missing a connection")

        ret_val = ret_val and i2c_flag

        return ret_val

    def _io_checks(self, comp_pin, non_comp):
        """Validation when the pins are both io.

        Args:
            comp_pin (IOPin object): The pin of the computational device.
            non_pin (IOPin object): The pin of the non compoutational device.

        Returns:
            (bool): True if the connection is correct, false otherwise.
        """
        # Check for different modes.
        # Make a dictionary with fucntions for faster search.
        comp_funcs = {}
        for f in comp_pin.functions:
            comp_funcs[f.type] = True

        # Different handle per hardware interface type
        non_comp_type = non_comp.functions[0].type

        # Check for GPIO Pin Type
        # Maybe check for reverse connections.
        if non_comp_type in self.GPIO_TYPES:
            type_flag = self._simple_try(comp_funcs, IOType.GPIO_BOTH, 
                                         "Should be gpio pin")

        # Check for I2C Pin Type
        if non_comp_type in self.I2C_TYPES:
            type_flag = self._simple_try(comp_funcs, non_comp_type, 
                                         "Should be the same i2c function")
            # Continue with checking if both pins have been used.
            if type_flag:
                self._cur_i2c[non_comp_type] = True

        # Check for PWM Pin Type
        if non_comp_type in self.PWM_TYPES:
            type_flag = self._simple_try(comp_funcs, non_comp_type, 
                                         "Should be pwm")

        return type_flag
    
    def _simple_try(self, funcs, f_type, msg):
        """_simple_try

        Args:
            funcs ():
            f_type ():
            msg ():

        Returns:
        """
        type_flag = True
        try:
            _ = funcs[f_type]
        except KeyError:
            type_flag = False
            self._log_error(msg)
        return type_flag

    def _check_power(self, comp, non_comp):
        """_check_power

        Args:
            comp (Pin object): Pin of computational device
            non_comp (Pin object): Pin on non computational device

        Returns:
            (bool or None): True if both are the proper power pins. False if
                one is power pin and the other iopin and None if both are 
                io pins.
        """
        f_comp = isinstance(comp, PowerPin)
        f_non = isinstance(non_comp, PowerPin)
        ret = None
        # Both Power
        if f_comp and f_non:
            ret = (comp.function == non_comp.function)
        elif f_comp or f_non:
            ret = False
            self._log_error("Must both or neither be power.")
        return ret

    def _check_complete(self, dic, msg):
        """_check_complete

        Args:
            dic ():
            msg ():

        Returns:
            (bool): Indicating proper connection of all i2c pins
        """
        ret = True
        sumo = sum(dic.values())
        if sumo and (sumo != len(dic)):
            ret = False
            self._log_error(msg)
        return ret
