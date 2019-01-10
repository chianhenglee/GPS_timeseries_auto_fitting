import os

from plotly import tools
import plotly.offline as pyo
import plotly.graph_objs as go

import numpy as np
import pandas as pd

filename = 'processed_timeseries/FUGN.csv'
sitename = 'FUGN'

data = pd.read_csv(filename)


### Try linear fitting

time = data.digit_date
E = data.E_mm
N = data.N_mm
U = data.U_mm

### E component ###

# s = G*m
# s is the displacement component
# m is the parameters (slope, intercept)
# G is the Green's function (time, ones)

G = np.vstack([time,np.ones(len(time))]).T
sE = np.vstack(E)

[slopeE,interceptE],sum_residualE = np.linalg.lstsq(G,sE,rcond=None)[0:2]

print(slopeE,interceptE)

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

print(slopeN,interceptN)

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

print(slopeN,interceptN)

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


### Plotting

traceE = go.Scatter(
    x = data.digit_date,
    y = data.E_mm,
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
    x = data.digit_date,
    y = data.N_mm,
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
    x = data.digit_date,
    y = data.U_mm,
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
pyo.plot(fig, filename='test_fit.html',auto_open=True)

