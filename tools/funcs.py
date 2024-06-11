# Helper functions
# Author: Stefanie Falk (KIT)

import os, sys, glob, shutil
import argparse
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import datetime as dt
import yaml

def init():
    func_name = 'init'
    # Parse command line arguments
    parser = argparse.ArgumentParser(sys.argv)
    parser.add_argument(dest='config_file', nargs='?', default="examples/user_config.yml", help='Configuration file')
    parser.add_argument('-v', dest='verbose', action='store_true')
    parser.add_argument('--debug', dest='debug', action='store_true')
    parser.add_argument('--clean', dest='clean', action='store_true')
    args = parser.parse_args()
    print_msg(func_name, r"Loading configuration: %s" % args.config_file)
    # Read configuration
    with open(r'%s' % args.config_file) as file:
        config_list = yaml.load(file, Loader=yaml.FullLoader)
    file.close()
    return(config_list, args)

def print_msg(func_name, *message, **kwargs):
    mode = kwargs.get("mode", None)
    if mode=='debug':
        mode_str = "*debug*\n......"
    elif mode=='verbose':
        mode_str= "..."
    elif mode=='error':
        mode_str='ERROR:'
    else:
        mode_str= "-> "
    print("%s%s()" % (mode_str, func_name), *message)

def make_clean(dir_list):
    func_name = 'make_clean'
    print_msg(func_name, "Removing directories")
    for key in dir_list.keys():
        dir = dir_list[key]
        if os.path.exists(dir) and dir != '.':
            print_msg(func_name, dir)
            shutil.rmtree(dir)
    print_msg(func_name, "Done cleaning up.")

def make_dirs(dir_list, **kwargs):
    func_name = 'make_dirs'
    debug = kwargs.get('debug', False)
    for key in dir_list.keys():
        if not os.path.exists(dir_list[key]):
            if debug: print_msg(func_name, "Creating directory %s" % (dir_list[key]), mode=debug)
            os.makedirs(dir_list[key])
        else:
            if debug: print_msg(func_name, "Nothing to do.", mode=debug)

def read_data(*arg,**kwarg):
    func_name = 'read_data'
    # Get arguments
    infile = arg[0]
    input_dir = arg[1]

    data_list = []
    file_list = []
    if (infile.find('*')>=0) | (infile.find('?')>=0):
        for ifile in sorted(glob.glob(os.sep.join([input_dir, infile]))):
            file_list.append(os.path.basename(ifile))
            data_list.append(xr.open_dataset(ifile))
    elif (type(infile)==list):
        for ifile in sorted(infile):
            file_list.append(ifile)
            data_list.append(xr.open_dataset(os.sep.join([input_dir, ifile])))
    else:
        file_list.append(infile)
        data_list.append(xr.open_dataset(os.sep.join([input_dir, infile])))

    return(data_list, file_list)
