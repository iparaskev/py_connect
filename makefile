SHELL := /bin/bash

# VARIABLES
GEN = pyecoregen
targets = devices_model db

# DIRECTORIES
TARGET_DIR = py_connect
MODELS_DIR = models
DB_DIR = devices_db

all: $(targets)

devices_model: $(MODELS_DIR)/hw_devices.ecore
	$(GEN) -e $^ -o $(TARGET_DIR)

db: $(DB_DIR)/*.py
	for file in $^; do \
	    python $$file; \
	done
