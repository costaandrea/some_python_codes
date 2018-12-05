#!/usr/bin/env python2
import os
from netCDF4 import Dataset
import numpy as np
from numba import jit
import vmodes

os.chdir("/Volumes/AC_Thunder_2/netcdf_files/")

dataset = Dataset("bsose_i105_2008to2012_3day_Strat.nc", mode = 'r')
lat = dataset.variables['lat'][:]
lon = dataset.variables['lon'][:]
depth = dataset.variables['depth'][:]
time = dataset.variables['time'][:]
dataset.close()

yt = (np.abs(lat-(-60)).argmin())
xt = (np.abs(lon-(-0)).argmin())


seasons = ['Spring', 'Summer', 'Autumn', 'Winter']

for sss in range(1,4):
    season = seasons[sss];
    print ['\n',season,'\r']  
    
    @jit(nopython=True) 
    def loop_lon():
        for ii in range(0,len(lon)):
            #print(ii+'\n')
            os.chdir("/Volumes/AC_Thunder_1/SOSE_seasonal_averages/")
            dataset = Dataset(''.join(['SOSE_drdz_',season,'.nc']), mode = 'r')
            drdzl = dataset.variables['drdz'][:,:,ii]
            dataset.close()
            dataset = Dataset(''.join(['SOSE_GAMMA_',season,'.nc']), mode = 'r')
            rhol = dataset.variables['gamma'][:,:,ii]
            dataset.close()
            
            
            for jj in range(0,len(lat)):
                
                wmode = np.empty([len(depth),3,len(lat)])
                wmode[:] = np.nan
                pmode = np.empty([len(depth),3,len(lat)])
                pmode[:] = np.nan
                
                #one profile
                drdz=drdzl[:,jj]
                rho=rhol[:,jj]
                inds = np.where(~np.isnan(drdz))
                z= depth[inds]
                rho= rho[inds]
                drdz= drdz[inds]
                
                g = 9.806 - .5*(9.832-9.780)*np.cos(2*lat[yt]*np.pi/180) #could be precalc
                N2 = -g/rho*drdz
                
                if len(N2)>0:
                    C1 = np.empty([len(lat)])
                    C1[:]=np.nan
                    C2 = np.empty([len(lat)])
                    C2[:]=np.nan
                    C3 = np.empty([len(lat)])
                    C3[:]=np.nan
                    R1 = np.empty([len(lat)])
                    R1[:]=np.nan
                    R2 = np.empty([len(lat)])
                    R2[:]=np.nan
                    R3 = np.empty([len(lat)])
                    R3[:]=np.nan
                    z = rho*g*z*1e-4 #[db]
                    del rho
                    #calculate vertical modes
                    wmode_t, pmode_t, rmodes_t, ce = vmodes.dynmodes(N2,z,3)
                    #plot them
                    #vmodes.plot_modes(N2, z, 3, wmodes, pmodes, rmodes)
                    if wmode_t.shape[0] > len(z):
                        wmode_t = wmode_t[0:len(z),:];
                        pmode_t = pmode_t[0:len(z),:];
                
                    f = 2* 7.292115e-5* np.sin(lat[yt]*np.pi/180)
                    
                    if len(ce)==1:
                        C1[jj] = ce[0]
                        R1[jj] = ce[0]/np.abs(f)
                        C2[jj]=np.nan
                        R2[jj]=np.nan
                        C3[jj]=np.nan
                        R3[jj]=np.nan
                        
                        tmp = np.empty([wmode_t.shape[1],2])
                        tmp[:] = np.nan
                        tmp2 = np.concatenate([wmode_t.T, tmp],axis=1)
                        wmode[0:wmode_t.shape[1],:,jj] = tmp2
                        tmp2 = np.concatenate([pmode_t.T, tmp],axis=1)
                        pmode[0:wmode_t.shape[1],:,jj] = tmp2
                        del tmp
                        del tmp2
                    elif len(ce)==2:
                        C1[jj] = ce[0]
                        R1[jj] = ce[0]/np.abs(f)
                        C2[jj] = ce[1]
                        R2[jj] = ce[1]/np.abs(f)
                        C3[jj]=np.nan
                        R3[jj]=np.nan
                        
                        tmp = np.empty([wmode_t.shape[1],1])
                        tmp[:] = np.nan
                        tmp2 = np.concatenate([wmode_t.T, tmp],axis=1)
                        wmode[0:wmode_t.shape[1],:,jj] = tmp2
                        tmp2 = np.concatenate([pmode_t.T, tmp],axis=1)
                        pmode[0:wmode_t.shape[1],:,jj] = tmp2
                        del tmp
                        del tmp2
                    elif len(ce)==3:
                        C1[jj] = ce[0]
                        R1[jj] = ce[0]/np.abs(f)
                        C2[jj] = ce[1]
                        R2[jj] = ce[1]/np.abs(f)
                        C3[jj] = ce[2]
                        R3[jj] = ce[2]/np.abs(f)
                        
                        wmode[0:wmode_t.shape[1],:,jj] = wmode_t.T;
                        pmode[0:wmode_t.shape[1],:,jj] = pmode_t.T;
                    elif len(ce)==0:
                        C1[jj]=np.nan
                        R1[jj]=np.nan
                        C2[jj]=np.nan
                        R2[jj]=np.nan
                        C3[jj]=np.nan
                        R3[jj]=np.nan
                        
                        tmp = np.empty([wmode_t.shape[0],3])
                        tmp[:] = np.nan
                        wmode[0:wmode_t.shape[1],:,jj] = tmp
                        pmode[0:wmode_t.shape[1],:,jj] = tmp
                        del tmp 
                        del wmode_t 
                        del pmode_t
                
                
        if os.path.isdir("Rossby_SL_SOSE"):
            os.chdir("Rossby_SL_SOSE")          
        elif ~os.path.isdir("Rossby_SL_SOSE"):
             os.makedirs("Rossby_SL_SOSE")
             os.chdir("Rossby_SL_SOSE")       
                       
        ncfile = ''.join(['Rossby_SL_SOSE_',season,'_',"%04.0d"%(ii,),'.nc'])        
                
        if os.path.isfile(ncfile):
            os.remove(ncfile)                   
            
                
        #create ncfile, dimensions and variables    
        rootgrp = Dataset(ncfile, "w", format="NETCDF4")
        rootgrp.createDimension("t", len(time))
        rootgrp.createDimension("z", len(depth))
        rootgrp.createDimension("y", len(lat))
        rootgrp.createDimension("x", len(lon))
        rootgrp.createDimension("n", 1) #mode number
           
            
        times = rootgrp.createVariable("time","f8","t")
        times.units = "days since 1-1-1 00:00:0.0"
        levs = rootgrp.createVariable("level","f4","z")
        levs.units = "[m]"
        lats = rootgrp.createVariable("lat","f4","y")
        lons = rootgrp.createVariable("lon","f4","x")
                
        C1s = rootgrp.createVariable("C1","f4",("x","y"))
        C1s.units = "m/s"
        #temps.missingvalue = "-1.0E34"
        C1s.longname = "SL phase speed mode 1"
                
        C2s = rootgrp.createVariable("C2","f4",("x","y"))
        C2s.units = "m/s"
        #temps.missingvalue = "-1.0E34"
        C2s.longname = "SL phase speed mode 2"
                
        C3s = rootgrp.createVariable("C3","f4",("x","y"))
        C3s.units = "m/s"
        #temps.missingvalue = "-1.0E34"
        C3s.longname = "SL phase speed mode 3"
                
        R1s = rootgrp.createVariable("R1","f4",("x","y"))
        R1s.units = "m"
        #temps.missingvalue = "-1.0E34"
        R1s.longname = "SL 1 deformation radius"
        
        R2s = rootgrp.createVariable("R2","f4",("x","y"))
        R2s.units = "m"
        #temps.missingvalue = "-1.0E34"
        R2s.longname = "SL 2 deformation radius"
        
        R3s = rootgrp.createVariable("R3","f4",("x","y"))
        R3s.units = "m"
        #temps.missingvalue = "-1.0E34"
        R3s.longname = "SL 3 deformation radius"
        
        wmode1 = rootgrp.createVariable("wmode1","f4",("x","y","z","n"))
        wmode1.units = " "
        #temps.missingvalue = "-1.0E34"
        wmode1.longname = "1st mode vertical velocity"
        
        wmode2 = rootgrp.createVariable("wmode2","f4",("x","y","z","n"))
        wmode2.units = " "
        #temps.missingvalue = "-1.0E34"
        wmode2.longname = "2nd mode vertical velocity"
        
        wmode3 = rootgrp.createVariable("wmode3","f4",("x","y","z","n"))
        wmode3.units = " "
        #temps.missingvalue = "-1.0E34"
        wmode3.longname = "3rd mode vertical velocity"
        
        pmode1 = rootgrp.createVariable("pmode1","f4",("x","y","z","n"))
        pmode1.units = " "
        #temps.missingvalue = "-1.0E34"
        pmode1.longname = "1st mode vertical pression"
        
        pmode2 = rootgrp.createVariable("pmode2","f4",("x","y","z","n"))
        pmode2.units = " "
        #temps.missingvalue = "-1.0E34"
        pmode2.longname = "2nd mode vertical pression"
        
        pmode3 = rootgrp.createVariable("pmode3","f4",("x","y","z","n"))
        pmode3.units = " "
        #temps.missingvalue = "-1.0E34"
        pmode3.longname = "3rd mode vertical pression"
        
        # and write variables
        #print "Writing...\n"
        times[:] = time
        lons[:] = lon
        lats[:] = lat
        levs[:] = depth
                
        C1s[ii,:] = C1
        C2s[ii,:] = C2
        C3s[ii,:] = C3
        R1s[ii,:] = R1
        R2s[ii,:] = R2
        R3s[ii,:] = R3
        wmode1[ii,:,:,:] = wmode[:,0,:]
        wmode2[ii,:,:,:] = wmode[:,1,:]
        wmode3[ii,:,:,:] = wmode[:,2,:]
        pmode1[ii,:,:,:] = wmode[:,0,:]
        pmode2[ii,:,:,:] = wmode[:,1,:]
        pmode3[ii,:,:,:] = wmode[:,2,:]
        