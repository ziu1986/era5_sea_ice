# Script to process sea ice cover data 
import os, glob # Access environment variables
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid
from mytools.med_tools import *

b_plot = False
my_sic_list = []
time_list = []
# Access environment variable for directory
nc_data = os.environ['DATA']
nc_subd = '/ESCIMO'

# Data directory
for year in range(1979,2013):
    time_list.append(year+1)
    #year = 2000
    nc_src_ref = '/RC1SD-base-08/ECHAM5/RC1SD-base-08__'+str(year)+'0[8,9]_ECHAM5.nc'
    nc_src_ref_sh = '/RC1SD-base-08/ECHAM5/RC1SD-base-08__'+str(year)+'0[2,3]_ECHAM5.nc'
    # Load data
    data = [xr.open_dataset(each) for each in sorted(glob.glob(nc_data+nc_subd+nc_src_ref))]
    data_sh = [xr.open_dataset(each) for each in sorted(glob.glob(nc_data+nc_subd+nc_src_ref_sh))]

    # Compute temporal mean and split hemispheres
    nh = xr.concat(([each.icecov.where(each.lat>0,drop=True) for each in data]), dim='time')
    sh = xr.concat(([each.icecov.where(each.lat<=0,drop=True) for each in data_sh]), dim='time')
    # Minimum of sea ice fraction
    min_nh = nh.sum(axis=(1,2)).min()
    min_sh = sh.sum(axis=(1,2)).min()
    # Multi-year sea ice
    my_nh = nh.where(nh.sum(axis=(1,2))==min_nh, drop=True).mean(axis=0)
    my_sh = sh.where(sh.sum(axis=(1,2))==min_sh, drop=True).mean(axis=0)
    # Concatenate the hemispheres
    my_sic_list.append(xr.concat((my_nh, my_sh), dim='lat'))
    # Plotting
    if b_plot:
        execefile("my_sic_mask.py")
    # Close the files after plotting
    for i in range(2):
        data[i].close()
        data_sh[i].close()
# Concatenate the multi-yerar sea ice
my_sic = xr.concat((my_sic_list), dim='time')
# Set sime meta-data
my_sic.name = 'my_sic'
my_sic.coords['time'] = ('time', time_list)
my_sic.attrs['units'] = 'fraction'

# Write
my_sic.to_netcdf("sic_multi-year_%s_%s.nc" % (time_list[0], time_list[-1]), format='NETCDF3_CLASSIC')
