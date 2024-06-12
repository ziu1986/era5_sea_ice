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
    data_list_nh, file_list_nh = read_data(infile.replace('*','*0[8,9]*'), input['dir'], debug=debug)
    data_list_sh, file_list_sh = read_data(infile.replace('*','*0[2,3]*'), input['dir'], debug=debug)
    # Get list of unique years
    year_list = []
    for data_nh, data_sh in zip(data_list_nh, data_list_sh):
        year_list.append(dt.datetime.strptime(str(data_nh.time.min().to_numpy())[:-2], '%Y%m%d').date().year)
        year_list.append(dt.datetime.strptime(str(data_sh.time.min().to_numpy())[:-2], '%Y%m%d').date().year)
    year_list = np.unique(year_list)
    if debug:
        print_msg(func_name, "List of years: ", year_list, mode=debug)
    # Get mysic
    my_sic_list = []
    # Loop over data
    for iyear in year_list:
        min_nh = 10000
        min_sh = 10000
        for i in (0,1):
            j = year_list[0]-iyear+i
            print_msg(func_name, "Process files:\n%s\n%s" % (file_list_nh[j], file_list_sh[j]))
            # Get multi-year sea ice maps
            my_sic_nh = data_list_nh[j]['sic'].where(data_list_nh[j]['sic'].lat>0, drop=True)
            my_sic_sh = data_list_sh[j]['sic'].where(data_list_sh[j]['sic'].lat<=0, drop=True)
            # Minimum of sea ice fraction
            if my_sic_nh.sum(dim=('lat','lon')).min() < min_nh:
                min_nh = my_sic_nh.sum(dim=('lat','lon')).min()
                # Multi-year sea ice
                my_sic_nh_tmp = my_sic_nh.where(my_sic_nh.sum(dim=('lat','lon'))==min_nh, drop=True).mean(dim='time').squeeze().drop('lev')
            if my_sic_sh.sum(dim=('lat','lon')).min() < min_sh:
                min_sh = my_sic_sh.sum(dim=('lat','lon')).min()
                # Multi-year sea ice
                my_sic_sh_tmp = my_sic_sh.where(my_sic_sh.sum(dim=('lat','lon'))==min_sh, drop=True).mean(dim='time').squeeze().drop('lev')
            if debug: 
                print_msg(func_name, "Minimum sea ice:\nNH - %s\nSH - %s" % (min_nh, min_sh), mode=debug)
                print_msg(func_name, "NH\n", (my_sic_nh), mode=debug)
                print_msg(func_name, "\nSH\n", (my_sic_sh), mode=debug)
        # Concatenate the hemispheres
        my_sic_list.append(xr.concat((my_sic_nh_tmp, my_sic_sh_tmp), dim='lat'))

    # Concatenate the multi-yerar sea ice
    my_sic = xr.concat((my_sic_list), dim='time')
   # Rename variable name and attributes
    my_sic.name = 'my_sic'
    for key in nc_attrs:
            if(debug):
                print(key, nc_attrs[key])
            my_sic.attrs[key] = nc_attrs[key]
    my_sic.coords['time'] = ('time', np.array(year_list)+1)

    if debug:
        print_msg(func_name, my_sic, mode=debug)   

    # Write
    my_sic.to_netcdf(os.sep.join([tgt['output'],"sic_multi-year_%s_%s.nc" % (year_list[0], year_list[-1])]))
    # Finish
    print_msg(func_name, " Finished.")

if __name__ == "__main__":
    main()
