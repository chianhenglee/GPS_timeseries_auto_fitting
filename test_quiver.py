import os

from plotly import tools
import plotly.offline as pyo
import plotly.graph_objs as go

import plotly.figure_factory as ff

import numpy as np
import pandas as pd

filename = 'fitted_velocity.csv'

df = pd.read_csv(filename)





#lon,lat = np.meshgrid(np.arange(-2, 2, .2),np.arange(-2, 2, .25))
lon = df.lon
lat = df.lat
Evel = df.vel_E
Nvel = df.vel_N
Uvel = df.vel_U

fig = ff.create_quiver(lon,lat,Evel,Nvel,
                       scale=.02,
                       arrow_scale=.1,
                       name='quiver',
                       line=dict(width=1))


pyo.plot(fig,filename='Quiver map.html')
