def fit_one_site(filename):
	'''return 4 numpy arrays:
	time, E_fit, N_fit, U_fit
	and velocity [Evel,Nvel,Uvel]
	'''
	import pandas as pd
	import numpy as np

	
	data = pd.read_csv(filename)

	########## Linear fitting ##########

	time = data.digit_date
	E = data.E_mm
	N = data.N_mm
	U = data.U_mm

	# s = G*m
	# s is the displacement component
	# m is the parameters (slope, intercept)
	# G is the Green's function (time, ones)

	### E component ###
	G = np.vstack([time,np.ones(len(time))]).T
	sE = np.vstack(E)
	[slopeE,interceptE],sum_residualE = np.linalg.lstsq(G,sE,rcond=None)[0:2]

	### E component ###
	G = np.vstack([time,np.ones(len(time))]).T
	sN = np.vstack(N)
	[slopeN,interceptN],sum_residualN = np.linalg.lstsq(G,sN,rcond=None)[0:2]

	### U component ###
	G = np.vstack([time,np.ones(len(time))]).T
	sU = np.vstack(U)
	[slopeU,interceptU],sum_residualU = np.linalg.lstsq(G,sU,rcond=None)[0:2]


	Efit = slopeE*time
	Nfit = slopeN*time
	Ufit = slopeU*time

	ref_vel = [slopeE,slopeN,slopeU]

	return time,Efit,Nfit,Ufit,ref_vel


