import os

from plotly import tools
import plotly.offline as pyo
import plotly.graph_objs as go

import numpy as np
import pandas as pd

from fit_one_site import fit_one_site

filenames = os.listdir('processed_timeseries')
datafoldername = 'processed_timeseries/'

sitenames = [i[0:-4] for i in filenames]

##### First make all time series w.r.t. to a specific station #####

print('Here is all the stations in the folder:')
print(sitenames)
ref_site = input('Desired reference station:')
ref_site_filename = datafoldername+ref_site+'.csv'


ref_vel = fit_one_site(ref_site_filename)[4]
#ref_time,ref_Efit,ref_Nfit,ref_Ufit,ref_vel = fit_one_site(ref_site_filename)


##### Specify the name of the export folder #####
export_folder = 'fitted_timeseries_graphs_ref_to_'+ref_site
try:
	os.mkdir(export_folder)
except:
	print('The folder "'+export_folder+'" already exist. Continuing...')



## create empty variables to store velocity for future use
sitenames=[]
lon = []
lat = []
vel_E = []
vel_N = []
vel_U = []

for curr_file in filenames:

	#curr_file = filenames[0]
	sitename = curr_file[0:-4]
	print(sitename)

	data = pd.read_csv(datafoldername+curr_file)


	########## Reference to given station ###########

	time = data.digit_date
	E = data.E_mm-(time*ref_vel[0])
	N = data.N_mm-(time*ref_vel[1])
	U = data.U_mm-(time*ref_vel[2])


	########## Linear fitting ##########

	### E component ###

	# s = G*m
	# s is the displacement component
	# m is the parameters (slope, intercept)
	# G is the Green's function (time, ones)

	G = np.vstack([time,np.ones(len(time))]).T
	sE = np.vstack(E)

	[slopeE,interceptE],sum_residualE = np.linalg.lstsq(G,sE,rcond=None)[0:2]

	#print(slopeE,interceptE)

	traceE_fit = go.Scatter(
		x = time,
		y = slopeE*time+interceptE,
		mode = 'lines+text',
	    line = dict(
	    		width = 2,
	    		color = 'rgba(0,0,255,.9)'
	    		),
		)

	trace_print_Evel = go.Scatter(
		x = [time[round(len(time)/2)]],
		y = [np.max(sE)],
		mode = 'text',
		text = ['velocity = '+str(slopeE)[1:-1]+' mm/yr'],
		textposition = 'bottom center'
		)

	### N component ###

	G = np.vstack([time,np.ones(len(time))]).T
	sN = np.vstack(N)

	[slopeN,interceptN],sum_residualN = np.linalg.lstsq(G,sN,rcond=None)[0:2]

	#print(slopeN,interceptN)

	traceN_fit = go.Scatter(
		x = time,
		y = slopeN*time+interceptN,
		mode = 'lines+text',
	    line = dict(
	    		width = 2,
	    		color = 'rgba(0,0,255,.9)'
	    		),
		xaxis = 'x2',
	    yaxis = 'y2'
		)

	trace_print_Nvel = go.Scatter(
		x = [time[round(len(time)/2)]],
		y = [np.max(sN)],
		mode = 'text',
		text = ['velocity = '+str(slopeN)[1:-1]+' mm/yr'],
		textposition = 'bottom center',
		xaxis = 'x2',
	    yaxis = 'y2'
		)

	### U component ###

	G = np.vstack([time,np.ones(len(time))]).T
	sU = np.vstack(U)

	[slopeU,interceptU],sum_residualU = np.linalg.lstsq(G,sU,rcond=None)[0:2]
	
	#print(slopeU,interceptU)

	traceU_fit = go.Scatter(
		x = time,
		y = slopeU*time+interceptU,
		mode = 'lines+text',
	    line = dict(
	    		width = 2,
	    		color = 'rgba(0,0,255,.9)'
	    		),
		xaxis = 'x3',
	    yaxis = 'y3'
		)

	trace_print_Uvel = go.Scatter(
		x = [time[round(len(time)/2)]],
		y = [np.max(sU)],
		mode = 'text',
		text = ['velocity = '+str(slopeU)[1:-1]+' mm/yr'],
		textposition = 'bottom center',
		xaxis = 'x3',
	    yaxis = 'y3'
		)
	##### save result #####

	sitenames.append(sitename)
	lon.append(data.lon[0]) # just get the first obs of lon lat
	lat.append(data.lat[0]) # just get the first obs of lon lat
	vel_E.append(slopeE[0]) # because slope is stored in two layers of []
	vel_N.append(slopeN[0])
	vel_U.append(slopeU[0])

	# we create pd dataframe at the bottom of the script

	########## Linear fitting Ends ##########



	### Plotting

	traceE = go.Scatter(
	    x = time,
	    y = E,
	    mode = 'lines+markers',
	    name = sitename+'_E',
	    marker = dict(
	    		size = 6,
	    		color = 'rgba(255, 0, 0, .9)',
	    		line = dict(
	    			width = 0,
	    			color = 'rgb(0, 0, 0)'
	    			)
	    		),
	    line = dict(
	    		width = 0.75,
	    		color = 'rgba(255,0,0,.9)'
	    		)
	)

	traceN = go.Scatter(
	    x = time,
	    y = N,
	    mode = 'lines+markers',
	    name = sitename+'_N',
	    marker = dict(
	    		size = 6,
	    		color = 'rgba(255, 0, 0, .9)',
	    		line = dict(
	    			width = 0,
	    			color = 'rgb(0, 0, 0)'
	    			)
	    		),
	    line = dict(
	    		width = 0.75,
	    		color = 'rgba(255,0,0,.9)'
	    		),
	    xaxis = 'x2',
	    yaxis = 'y2'
	)

	traceU = go.Scatter(
	    x = time,
	    y = U,
	    mode = 'lines+markers',
	    name = sitename+'_U',
	    marker = dict(
	    		size = 6,
	    		color = 'rgba(255, 0, 0, .9)',
	    		line = dict(
	    			width = 0,
	    			color = 'rgb(0, 0, 0)'
	    			)
	    		),
	    line = dict(
	    		width = 0.75,
	    		color = 'rgba(255,0,0,.9)'
	    		),
	    xaxis = 'x3',
	    yaxis = 'y3'
	)


	#data = go.Data([traceE,traceN,traceU])
	data_fig = [traceE,traceN,traceU,traceE_fit,traceN_fit,traceU_fit]
	data_fig.append(trace_print_Evel)
	data_fig.append(trace_print_Nvel)
	data_fig.append(trace_print_Uvel)

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
							title= 'East (mm)',
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
							title= 'North (mm)',
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
							title= 'Vertical (mm)',
							gridwidth= 1,
							domain = [0,0.3],
							anchor='x3'
							)
				)

	fig = go.Figure(data = data_fig, layout = layout)
	pyo.plot(fig, filename=export_folder+'/'+sitename+'.html',auto_open=False)



df = pd.DataFrame( {'site': pd.Series(sitenames, dtype=str), 
					'lon': pd.Series(lon, dtype=float),
					'lat': pd.Series(lat, dtype=float),
					'vel_E': pd.Series(vel_E, dtype=float),
					'vel_N': pd.Series(vel_N, dtype=float),
					'vel_U': pd.Series(vel_U, dtype=float)})

pd.DataFrame.to_csv(df,'fitted_velocity_ref_to_'+ref_site+'.csv')


print(df.head(10))
print(df.site[0])
print(df.lon[0])
print(df.lat[0])
print(df.vel_E[0])
print(df.vel_E[0]+1)

