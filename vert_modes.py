#!/usr/bin/env python2
import os
from netCDF4 import Dataset
import numpy as np
#my stuff
import vmodes

os.chdir("/Volumes/AC_Thunder_2/netcdf_files/")

dataset = Dataset("bsose_i105_2008to2012_3day_Strat.nc", mode = 'r')
lat = dataset.variables['lat'][:]
lon = dataset.variables['lon'][:]
yt = (np.abs(lat-(-60)).argmin())
xt = (np.abs(lon-(-0)).argmin())
depth = dataset.variables['depth'][:]
drdz = dataset.variables['Strat'][0,:,yt,xt]
dataset.close()

dataset = Dataset("bsose_i105_2008to2012_3day_GAMMA.nc", mode = 'r')
rho = dataset.variables['GAMMA'][0,:,yt,xt]
dataset.close()

#from masked to "normal" array
drdz = drdz.filled(np.nan)
rho = rho.filled(np.nan)

#one profile
inds = np.where(~np.isnan(drdz))
depth= depth[inds]
drdz= drdz[inds]
rho= rho[inds]

g = 9.806 - .5*(9.832-9.780)*np.cos(2*lat[yt]*np.pi/180)
N2 = -g/rho*drdz

depth = rho*g*depth*1e-4 #[db]
#calculate vertical modes
wmodes, pmodes, rmodes, ce = vmodes.dynmodes(N2,depth,3)
#plot them
vmodes.plot_modes(N2, depth, 3, wmodes, pmodes, rmodes)

f = 2* 7.292115e-5* np.sin(lat[yt]*np.pi/180)
R1 = ce[0]/np.abs(f) #[m]
print R1
R2 = ce[1]/np.abs(f) #[m]
print R2
R3 = ce[2]/np.abs(f) #[m]
print R3