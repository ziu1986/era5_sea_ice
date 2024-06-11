# Script to process sea ice cover data
# Based on generate_my_sic_mask.py published with 10.5194/gmd-11-1115-2018
# Author: Stefanie Falk (KIT) - 2024-06-11

import os, glob # Access environment variables
import numpy as np
import pandas as pd
import xarray as xr
from tools.funcs import *

def main():
    # Configuration
    func_name = 'main'
    config, args = init()
    # YML
    input = config['input']
    tgt = config['target']
    nc_attrs = config['nc_attributes']
    infile = input['files']
    # Command line parser
    verbose = args.verbose
    debug = args.debug
    clean = args.clean
    #-------------------------------------------------------------------
    # Clean up and exit
    if clean:
        make_clean(tgt)
        print_msg(func_name, " Exit.")
        return
    #-------------------------------------------------------------------
    # Create directory structure
    make_dirs(tgt, verbose=verbose, debug=debug)
    #-------------------------------------------------------------------
    # Check if we run interactively
    b_interactive = hasattr(sys, 'ps1')
    if verbose:
        if b_interactive:
            print_msg(func_name, "INFO: We are running from the interpreter! All plots will be shown in debug mode.", mode=verbose)
        else:
            print_msg(func_name, "INFO: We are running from the command line! All plots will be redirected to file in debug mode.", mode=verbose)
    
    # Load data
    data_list_nh, file_list_nh = read_data(infile.replace('*','0[8,9]*'), input['dir'])
    data_list_sh, file_list_sh = read_data(infile.replace('*','0[2,3]*'), input['dir'])
    # Get list of unique years
    year_list = []
    for data_nh, data_sh in zip(data_list_nh, data_list_sh):
        year_list.append(dt.datetime.strptime(str(data_nh.time.min().to_numpy())[:-2], '%Y%m%d').date().year)
        year_list.append(dt.datetime.strptime(str(data_sh.time.min().to_numpy())[:-2], '%Y%m%d').date().year)
    year_list = np.unique(year_list)
    print(year_list)
    # Get mysic
    my_sic_list = []
    # Loop over data
    for data_nh, ifile_nh, data_sh, ifile_sh in zip(data_list_nh, file_list_nh, data_list_sh, file_list_sh):
        print_msg(func_name, "Process files:\n%s\n%s" % (ifile_nh, ifile_sh))
        #outfile = ifile.replace('sst', 'multi_year_sic')
        # Get multi-year sea ice maps
        my_sic_nh = data_nh['sic'].where(data_nh['sic'].lat>0, drop=True)
        my_sic_sh = data_sh['sic'].where(data_sh['sic'].lat<=0, drop=True)
        
        # Minimum of sea ice fraction
        min_nh = my_sic_nh.sum(dim=('lat','lon')).min()
        min_sh = my_sic_sh.sum(dim=('lat','lon')).min()
        if debug: 
            print_msg(func_name, "Minimum sea ice:\nNH - %s\nSH - %s" % (min_nh, min_sh), mode=debug)
        # Multi-year sea ice
        my_sic_nh = my_sic_nh.where(my_sic_nh.sum(dim=('lat','lon'))==min_nh, drop=True).mean(dim='time').squeeze()
        my_sic_sh = my_sic_sh.where(my_sic_sh.sum(dim=('lat','lon'))==min_sh, drop=True).mean(dim='time').squeeze()
        # Concatenate the hemispheres
        my_sic_list.append(xr.concat((my_sic_nh, my_sic_sh), dim='lat'))
    # Finish
    print_msg(func_name, " Finished.")

if __name__ == "__main__":
    main()

#my_sic_list = []
#time_list = []
# Access environment variable for directory
#nc_data = os.environ['DATA']
#nc_subd = '/ESCIMO'

# Data directory
#for year in range(1979,2013):
#    time_list.append(year+1)
    #year = 2000
#    nc_src_ref = '/RC1SD-base-08/ECHAM5/RC1SD-base-08__'+str(year)+'0[8,9]_ECHAM5.nc'
#    nc_src_ref_sh = '/RC1SD-base-08/ECHAM5/RC1SD-base-08__'+str(year)+'0[2,3]_ECHAM5.nc'
    # Load data
#    data = [xr.open_dataset(each) for each in sorted(glob.glob(nc_data+nc_subd+nc_src_ref))]
#    data_sh = [xr.open_dataset(each) for each in sorted(glob.glob(nc_data+nc_subd+nc_src_ref_sh))]

    # Compute temporal mean and split hemispheres
#    nh = xr.concat(([each.icecov.where(each.lat>0,drop=True) for each in data]), dim='time')
#    sh = xr.concat(([each.icecov.where(each.lat<=0,drop=True) for each in data_sh]), dim='time')
    # Minimum of sea ice fraction
#    min_nh = nh.sum(axis=(1,2)).min()
#    min_sh = sh.sum(axis=(1,2)).min()
    # Multi-year sea ice
#    my_nh = nh.where(nh.sum(axis=(1,2))==min_nh, drop=True).mean(axis=0)
#    my_sh = sh.where(sh.sum(axis=(1,2))==min_sh, drop=True).mean(axis=0)
    # Concatenate the hemispheres
#    my_sic_list.append(xr.concat((my_nh, my_sh), dim='lat'))
    # Plotting
#    if b_plot:
#        execefile("my_sic_mask.py")
    # Close the files after plotting
#    for i in range(2):
#        data[i].close()
#        data_sh[i].close()
# Concatenate the multi-yerar sea ice
#my_sic = xr.concat((my_sic_list), dim='time')
# Set sime meta-data
#my_sic.name = 'my_sic'
#my_sic.coords['time'] = ('time', time_list)
#my_sic.attrs['units'] = 'fraction'

# Write
#my_sic.to_netcdf("sic_multi-year_%s_%s.nc" % (time_list[0], time_list[-1]), format='NETCDF3_CLASSIC')
