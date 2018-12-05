#import random

from netCDF4 import Dataset
import numpy as np

import os
#import time

url = 'http://apdrc.soest.hawaii.edu:80/dods/public_ofes/OfES/ncep_0.1_global_mmean/salt'
dataset = Dataset(url, mode = 'r')


print dataset

# Reading all the variables
lat = dataset.variables['lat'][:]
lon = dataset.variables['lon'][:]
lev = dataset.variables['lev'][:]
timev = dataset.variables['time'][:]


y2 = (np.abs(lat-(-30)).argmin())
lat = lat[0:y2+1]

for tt in range(609,610):#(69,len(timev)-1): 
    print tt,"/", len(timev),"\n"
    
    for zz in range(1,len(lev)-1): 
        print "zz=",zz,"/",(len(lev)-1),"\n"
        print "Loading...\n"
        salt = dataset.variables['salinity'][tt, zz, 1:y2+1, :]
        salt = np.transpose(salt) #equiv to: np.transpose(temp,(4,3,2,1))
        
        
        if zz==1:
            
            os.chdir("/Volumes/AC_Thunder_1/")
            if os.path.isdir("OFES_salt_mmean"):
                os.chdir("OFES_salt_mmean")
            else:
                os.makedirs("OFES_salt_mmean")
                os.chdir("OFES_salt_mmean")
        
            ncfile = "OFES_salt_mmean_"+str(tt).zfill(3)+".nc" 

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
            
            salts = rootgrp.createVariable("salt","f4",("x","y","z"))
            salts.units = "psu * 1000 + 35"
            salts.missingvalue = "-1.0E34"
            salts.longname = "salinity"
            
        # and write variables
            
            print "Writing...\n"
            times[:] = timev
            lons[:] = lon
            lats[:] = lat
            levs[:] = lev
            
            salts[:, 0:y2,zz] = salt
            
        elif zz>1:
        #only write variables
            print "Writing...\n"
            salts[:,0:y2,zz] = salt
            
      
    rootgrp.close() #close ncfile
dataset.close()             
    #print "Sleaping...\n"
    #time.sleep(120+random.randint(1,10)) #not sure this helps...
    

