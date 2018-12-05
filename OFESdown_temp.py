#import random

from netCDF4 import Dataset
import numpy as np

import os
#import time

url = 'http://apdrc.soest.hawaii.edu:80/dods/public_ofes/OfES/ncep_0.1_global_mmean/temp'
dataset = Dataset(url, mode = 'r')
print(dataset)

# Reading all the variables
lat = dataset.variables['lat'][:]
lon = dataset.variables['lon'][:]
lev = dataset.variables['lev'][:]
timev = dataset.variables['time'][:]


y2 = (np.abs(lat-(-30)).argmin())
lat = lat[0:y2+1]

for tt in range(189,len(timev)-1): #stopped at 11 (completed), 34, 34, 34,129(wifi),136
    print(tt+"/"+len(timev)+"\n")
    
    for zz in range(1,len(lev)-1): 
        print("zz="+zz,"/"+(len(lev)-1)+"\n")
        print("Loading...\n")
        temp = dataset.variables['temp'][tt, zz, 1:y2+1, :]
        temp = np.transpose(temp) #equiv to: np.transpose(temp,(4,3,2,1))
        
        
        if zz==1:
            
            os.chdir("/Volumes/AC_Thunder_1/")
            if os.path.isdir("OFES_temp_mmean"):
                os.chdir("OFES_temp_mmean")
            else:
                os.makedirs("OFES_temp_mmean")
                os.chdir("OFES_temp_mmean")
        
            ncfile = "OFES_temp_mmean_"+str(tt).zfill(3)+".nc" 

            if os.path.isfile(ncfile) :
                os.remove(ncfile)
       #create ncfile, dimensions and variables
            rootgrp = Dataset(ncfile, "w", format="NETCDF4")
            
            rootgrp.createDimension("t", len(timev))
            rootgrp.createDimension("z", len(lev))
            rootgrp.createDimension("y", len(lat))
            rootgrp.createDimension("x", len(lon))
       
        
            times = rootgrp.createVariable("time","f8","t")
            times.units = "days since 1-1-1 00:00:0.0"
            levs = rootgrp.createVariable("level","f4","z")
            levs.units = "[m]"
            lats = rootgrp.createVariable("lat","f4","y")
            lons = rootgrp.createVariable("lon","f4","x")
            
            temps = rootgrp.createVariable("temp","f4",("x","y","z"))
            temps.units = "degC"
            temps.missingvalue = "-1.0E34"
            temps.longname = "potential temperature"
            
        # and write variables
            
            print("Writing...\n")
            times[:] = timev
            lons[:] = lon
            lats[:] = lat
            levs[:] = lev
            
            temps[:, 0:y2,zz] = temp
            
        elif zz>1:
        #only write variables
            print("Writing...\n")
            temps[:,0:y2,zz] = temp
            
      
    rootgrp.close() #close ncfile
dataset.close()             
