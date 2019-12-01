import pandas as pd
import numpy as np
import os
import math
import serial
import time
import datetime

# Andrea Patrucco, 22/11/2019
# Python class to handle signals coming from the SensorLogger Android app.

# Serial port definition. Let the OS handle BT to COM transformation.
# TODO: implement some Linux scripting to handle reading /dev/rfcomm0

DEFAULT_BAUDRATE = 115200
DEFAULT_PORT = "COM32"
DEFAULT_TERMINATOR = b"\n"
DEFAULT_TIMEOUT = 2 # seconds

DATETIME_LOG_FORMAT = r"%Y-%m-%d %H:%M:%S.%f"
DATETIME_FILES_FORMAT = r"%Y_%m_%d_%H_%M_%S"


class BtSerialDevice:
	def __init__(self, name = "SerialDevice", port = DEFAULT_PORT, baud = DEFAULT_BAUDRATE, \
		terminator = DEFAULT_TERMINATOR, timeout = DEFAULT_TIMEOUT, \
		log_file = None, logging = True, listen_timeout = None):
		self.name = name
		self.port = port
		self.baud = baud
		self.terminator = terminator
		self.timeout = timeout
		if log_file is None:
			self.log_file = self.name + "_" + datetime.datetime.now().strftime(DATETIME_FILES_FORMAT) + '.txt'
		else:
			self.log_file = log_file
		self.logging = logging
		self.listen_timeout = listen_timeout

	def open(self):
		self.serial = serial.Serial(self.port, self.baud, \
			timeout = self.timeout)
		self.add_log("OPEN", "Serial port object created.")
		pass

	def read_until_char(self, endchar = b'\r'):
		if not self.serial is None:
			last_char = b'.' # any, try with null
			bstr = ''
			while (last_char != endchar): # add some basic timeout here!
				last_char = self.serial.read(1)
				bstr = bstr + last_char.decode('utf-8')
			bstr_log = bstr.replace(self.terminator.decode('utf-8'), '')
			self.add_log("RX", bstr_log)
		else:
			bstr = None
			self.add_log("RX", "Error: Serial Port is Undefined.")
		return bstr

	def listen(self, timeout = None, terminator = None):
		if terminator is None:
			terminator = self.terminator
		t0 = datetime.datetime.now()
		if timeout is None:
			to = self.listen_timeout
		if to is None:
			to = np.inf
		t1 = t0
		while ((t1 - t0).seconds < to):
			b = self.read_until_char(endchar = terminator)
		pass

	def add_log(self, logtype, data):
		if self.logging:
			log = open(self.log_file, 'a')
			log.write(datetime.datetime.now().strftime(DATETIME_LOG_FORMAT) + "\t" + logtype + "\t" + data + "\n")
			log.close()
		pass
