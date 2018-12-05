#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 15:00:14 2018

@author: andreacosta
"""

from netCDF4 import Dataset
import numpy as np
import os
from numba.decorators import jit

#dataset
url = 'http://apdrc.soest.hawaii.edu:80/dods/public_ofes/OfES/ncep_0.1_global_mmean/salt';
dataset = Dataset(url, mode = 'r')
print(dataset)

# Reading all the variables
lat = dataset.variables['lat'][:]
lon = dataset.variables['lon'][:]
lev = dataset.variables['lev'][:]
time = dataset.variables['time'][:]


p = lev/10 #[dbar]

@jit
def downl():
    for tt in range(1,len(time)):
        os.chdir('/Volumes/AC_Thunder_1/OFES_salt_mmean/')  
        dataset = Dataset("bsose_i105_2008to2012_3day_GAMMA.nc", mode = 'r')
        salt = dataset.variables['salt'][:]
        del(dataset)
        salt = np.squeeze(salt)
        salt[salt==-1.0E34]=np.nan 
        salt = salt/1000*35 #[psu]
        
        os.chdir('/Volumes/AC_Thunder_1/OFES_temp_mmean/')
        dataset = Dataset("'OFES_temp_mmean_001.nc", mode = 'r')
        temp = dataset.variables['temp'][:]
        temp[temp==-1.0E34]=np.nan
    
    
    