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
    data_list, file_list = read_data(infile, input['dir'])
    year_list = []
    # Loop over data
    for data, ifile in zip(data_list, file_list):
        print_msg(func_name, "Process file: %s" % (ifile))
        outfile = ifile.replace('sst', 'multi_year_sic')
        print_msg(func_name, "Save to: %s" % (outfile))
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
