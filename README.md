py_connect
===============================

A library for modelling devices and their connections in the physical 
world and controlling them in the virtual world through auto generated 
source code for the raspberry pi. 

py_connect provides a DSL (Domain Specific Language) for defining devices 
and connections between them. The DSL has been built using 
[textx](https://github.com/textX/textX) and through custom parsers the 
defined models are translated to ecore models using 
[pyecore](https://github.com/pyecore/pyecore). 
  
![GIF demo](img/demo.svg)

Usage
-----
```
usage: py_connect [-h] [--device DEVICE] [--store] [--xmi] 
                  [--xmi_path XMI_PATH] [--db_path DB_PATH] 
		  [--connections CONNECTIONS] [--source] 
		  [--schematic] [--specific_con SPECIFIC_CON]
                  [--update_pidevices]

optional arguments:
  -h, --help            show this help message and exit
  --device DEVICE       Path to a device specification.
  --store               Move device specification to db.
  --xmi                 Export xmi.
  --xmi_path XMI_PATH   Folder for saving xmi files.
  --db_path DB_PATH     Path to custom devices db.
  --connections CONNECTIONS
                        Path to a connection specification.
  --source              Flag for generating source code.
  --schematic           Flag for generating schematics images.
  --specific_con SPECIFIC_CON
                        The name of the specific connection.
  --update_pidevices    Update pidevices implementations.
```

How It Works
------------

### Syntax

Assingment is declared by the character ":". An entity precedes the ":" 
and it's value follows. An entity has attributes, which could be 
single valued or other entities.
For example the definition of a device's name is done in a single line
`name: raspberry_pi`, but the device's memory is defined like this
```
 memory:
  ram: 2 gb
  rom: 16 gb
```

Some attributes' value is a list of other entities. A list entry is defined 
by "-" followed by it's value. For example the pins of a device are defined by
```
pins: 
  - power:
    name: power_5v_1
    number: 2
    type: 5v
  - io_digital: -> both, sda-1
      name: bcm_2
      number: 3
```

#### Device definition

A device could be either a peripheral device 
(sensor/actuator) or a board (raspberry pi). 
The following table contains all the attributes 
and their values
that define a device and whether they are 
mandatory or not for a valid definition.

  Attribute | Board | Peripheral | Mandatory | Value
  --------- | ----- | ---------- | --------- | -----
  name | x | x | x | string
  vcc | x | x | x | number
  operating_voltage | x | x | x | number
  pins | x | x | x | \[pin entities\]
  network | x | x | - | \[network entities\]
  bluetooth | x | x | - | bluetooth entity
  type | - | x | x | "sensor" \| "actuator"
  memory | x | - | x | memory entity
  timer | x | - | x | bool
  os | x | - | x | "raspbian"
  cpu | x | - | x | cpu entity
  rtc | x | - | - | bool
  battery | x | - | - | bool
  dma | x | - | - | bool
  
##### Pin
The pins could be either power pins or gpios. 
* Power pins
	``` 
	power:
	    name: string
	    number: number
	    type : "gnd" | "3v3" | "5v"	
	```
* Gpio pins
	``` 
	io_digital: -> functionalities
	    name: string
	    number: number	
	```
   The functionalities is list of strings separated by commas. The strings 
   declare a pin functionality related to a hardware interface.
   * gpio: "input" | "output" | "both"
   * i2c: "sda" | "scl"
   * spi: "mosi" | "miso" | "sclk" | "ce"
   * uart: "rx" | "tx"
   * pwm: "pwm"
   
   Except the gpio functionalities the functionalities 
   of the other interfaces are followed by the interface's id. An example
   pin could be defined like this
   ```
   io_digital: -> both, sda-1
       number: 2
       name: bcm_2
   ```

##### Network
The network entities could be either of type
wifi or ethernet
* Wifi
     ```
     wifi: 
         name: string
         freq: freq_1 , freq_2 unit
     ```
* Ethernet
     ```
     ethernet: 
         name: string
     ```
     
##### Memory
The memory entity describes the different types of memory a device could
support and their values.
```
memory: 
  ram: int unit 
  rom: int unit
  external_memory: int unit
````
Where value is an integer number and unit could be on of "mb", "kb", "gb" and "b".

##### Cpu
A CPU entitie describes the cpu architecture, its maximum frequency and fpu support.
```
cpu: 
  cpu_family: ARM_CORTEX_M | ARM_CORTEX_A | ESP32
  max_freq: number unit(hz | ghz)
  fpu: bool
```

##### Bluetooth
A bluetooth entitie describes a device's bluetooth support.
```
bluetooth: 
  version: number
```

#### Connection definition
A connection between two devices is defined
by the connection of their hardware interfaces ports and of their power
pins.

  Attribute | Mandatory | Value
  --------- | --------- | -----
  name | x | string
  board | x | string
  peripheral | x | string
  peripheral_impl | x | string
  operating_voltage | x | x | x | number
  power_connections | x | \[power_connection_entities\]
  hw_connections | x | \[hw_connection_entities\]
  
The peripheral and board attributes must have the names of valid devices 
which have been already included in the file and defined in a different 
file.

##### power_connections
```
 power_connections: 
      - board_pin -- peripheral_pin
      - board_pin_1 -- peripheral_pin_1
```
Where board_pin and peripheral_pin are the names attributes 
of power pins from the corresponding devices.

##### hw_connections
```
hw_connections: 
      - type: board_hw_int -- peripheral_hw_int
      - type: board_hw_int_1 -- peripheral_hw_int_
```
The type describes the connection type and the value could be one of
"gpio", "spi", "i2c", "uart" and "pwm". The values that follow are
the names of the hardware interfaces in each device, e.g. 
```
- i2c: i2c-1 -- i2c-0
```
First comes the interface of the board device and then follows the 
peripheral's. The name of the pin is used for the interfaces which use only one pin
(gpio and pwm).

### M2M
After the definations, m2t transormations are being applied on the 
generated models in order to transform them to ecore models. 

### Code generation

Currently only devices connected to the raspberry pi are supported. The 
control of the devices is being done through the 
[pidevices](https://github.com/iparaskev/pidevices) library. 

After the definition of the devices and their connection has been done
the source code could be generated by
```
$ py_connect --db_path devices --connections connection.cd --source
```
Where db_path is the path to the devices folder and connection.cd is 
the file, which contains the defined connections. The result of the 
command is python file named by the connection name. 

Installation
--------------------

To install clone the repo:

    $ git clone https://github.com/iparaskev/py_connect.git
    $ python setup.py install
    
Example
-------
Examples of device descriptions can be found in the [db_folder](py_connect/devices_db). Example
connections can be seen in [connections_folder](test_connections).
