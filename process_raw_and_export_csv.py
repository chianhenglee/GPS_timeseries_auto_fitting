import os

import numpy as np
import pandas as pd

#from processing_functions import check_leap_year
from processing_functions import get_digit_date
from lonlat2twd97 import lonlat2twd97


filenames = os.listdir('time_series_data')
datafoldername = 'time_series_data/'

export_folder = 'processed_timeseries'
try:
	os.mkdir(export_folder)
except:
	print('The folder "processed_timeseries" already exist. Continuing...')

sitenames = [i[0:-4] for i in filenames]


for curr_file in filenames:

	#curr_file = filenames[0]
	sitename = curr_file[0:-4]

	data = pd.read_csv(datafoldername+curr_file, delim_whitespace=True, header=None)
	data.columns = ["date", "lon", "lat", "vert"]

	# convert lon lat to local E N
	# we don't need twq97 so let the first data point to be 0.
	E_97, N_97 = lonlat2twd97(data.lon, data.lat)
	E = (E_97 - np.min(E_97))*1000
	N = (N_97 - np.min(N_97))*1000
	U = (data.vert - np.min(data.vert))*1000   # convert from m to mm

	digit_date = get_digit_date(data.date) # Processing date to digit unit
	data = data.assign(digit_date = digit_date)  # final processed data
	data = data.assign(E_mm=E,N_mm=N,U_mm=U)

	pd.DataFrame.to_csv(data,export_folder+'/'+sitename+'.csv')