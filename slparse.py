import pandas as pd
import numpy as np
import math
import os

# Patrucco, 01/12/2019
# Parsers for SensorLogger application.

# TODO: Implement more parsing options in case the python logger has been used instead.
def parse_sl_log(txt_tile, mode = 'phone_log'):
	f = open(txt_tile, "r", errors = "ignore")
	tc = f.read() # TODO: test this for large files.
	lines = tc.split('\n')
	acc = pd.DataFrame()
	gps = pd.DataFrame()
	for linea in lines:
		if "GPS" in linea:
			sl = linea.split('\t')
			gpd = sl[2].split(',')
			gpsdict = {'timestamp': float(sl[0]), 'latitude': float(gpd[0]), \
				'longitude': float(gpd[1]), 'speed_m_s': float(gpd[2])}
			gps = gps.append(pd.DataFrame(gpsdict, index = [0]))
		if "ACC" in linea:
			sl = linea.split('\t')
			acd = sl[2].split(',')
			accdict = {'timestamp': float(sl[0]), 'ax': float(acd[0]), \
				'ay': float(acd[1]), 'az': float(acd[2]), 'rx': float(acd[3]), \
				'ry': float(acd[4]), 'rz': float(acd[5])}
			acc = acc.append(pd.DataFrame(accdict, index = [0]))
	gps_o = gps.reset_index(drop = True)
	acc_o = acc.reset_index(drop = True)
	return acc_o, gps_o