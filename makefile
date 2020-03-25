SHELL := /bin/bash

# VARIABLES
GEN = pyecoregen
targets = python_model

# DIRECTORIES
TARGET_DIR = py_connect
MODELS_DIR = models

all: $(targets)

devices_model: $(MODELS_DIR)/hw_devices.ecore
	$(GEN) -e $^ -o $(TARGET_DIR)
