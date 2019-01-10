

import os

from plotly import tools
import plotly.offline as pyo
import plotly.graph_objs as go

import numpy as np
import pandas as pd

#from processing_functions import check_leap_year
from processing_functions import get_digit_date
from lonlat2twd97 import lonlat2twd97


filenames = os.listdir('time_series_data')
datafoldername = 'time_series_data/'

sitenames = [i[0:-4] for i in filenames]


for curr_file in filenames:

	#curr_file = filenames[0]
	sitename = curr_file[0:-4]

	data = pd.read_csv(datafoldername+curr_file, delim_whitespace=True, header=None)
	data.columns = ["date", "lon", "lat", "vert"]

	# convert lon lat to local E N
	# we don't need twq97 so let the first data point to be 0.
	E_97, N_97 = lonlat2twd97(data.lon, data.lat)
	E = E_97 - np.min(E_97)
	N = N_97 - np.min(N_97)
	U = data.vert - np.min(data.vert)

	digit_date = get_digit_date(data.date) # Processing date to digit unit
	data = data.assign(digit_date = digit_date)  # final processed data
	data = data.assign(E=E,N=N,U=U)



	traceE = go.Scatter(
	    x = digit_date,
	    y = data.E,
	    mode = 'lines+markers',
	    name = sitename+'_E'
	)

	traceN = go.Scatter(
	    x = digit_date,
	    y = data.N,
	    mode = 'lines+markers',
	    name = sitename+'_N',
	    xaxis = 'x2',
	    yaxis = 'y2'
	)

	traceU = go.Scatter(
	    x = digit_date,
	    y = data.U,
	    mode = 'lines+markers',
	    name = sitename+'_U',
	    xaxis = 'x3',
	    yaxis = 'y3'
	)



	#data = go.Data([traceE,traceN,traceU])
	data = [traceE,traceN,traceU]

	layout = go.Layout(
				title= sitename,
				hovermode= 'closest',
				showlegend= False,
				height=900,
				width=1100,
				xaxis= dict(
							#title= 'Year',
							zeroline= False,
							gridwidth= 1,
							domain = [0,1]
							),
				yaxis= dict(
							title= 'Displacement (m)',
							gridwidth= 1,
							domain = [0.7,1]
							),
				xaxis2= dict(
							#title= 'Year222',
							zeroline= False,
							gridwidth= 1,
							domain = [0,1],
							anchor = 'y2'
							),
				yaxis2= dict(
							title= 'Displacement (m)',
							gridwidth= 1,
							domain = [0.35,0.65],
							anchor = 'x2'
							),
				xaxis3= dict(
							title= 'Year',
							zeroline= False,
							gridwidth= 1,
							domain = [0,1],
							anchor = 'y3'
							),
				yaxis3= dict(
							title= 'Displacement (m)',
							gridwidth= 1,
							domain = [0,0.3],
							anchor='x3'
							),
				)

	fig = go.Figure(data = data, layout = layout)
	pyo.plot(fig, filename=sitename+'.html',auto_open=False)

'''
	fig = tools.make_subplots(rows=3, cols=1,
				subplot_titles=(sitename+'_E', 
								sitename+'_N',
								sitename+'_U')
				)

	fig.append_trace(traceE,1,1)
	fig.append_trace(traceN,2,1)
	fig.append_trace(traceU,3,1)

	#fig['layout'].update(height=900, width=1000,showlegend=False) #title='Multiple Subplots')
'''



	#pio.write_image(fig, 'images/'+curr_file[0:-4]+'.png')

	









