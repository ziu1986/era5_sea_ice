# Compute multi-year sea ice cover fraction

> Author: Stefanie Falk (Stefanie.Falk@kit.edu)
> 
> First published: 10.5194/gmd-11-1115-2018
> 
> Date: 2024-06-11

The python script `compute_my_sic_from_sic.py` computes multi-year sea ice cover fractions based on ERA5 sea ice cover preprocessed for use with EMAC.

For simplicity, we assume that the sea ice cover fraction which has been present during the seasonal minimum, e.g. August/September in the Northern Hemisphere and February/March in the Southern, can be considered "mulit-year" in the following year.

This doesn't take ice movement into account. For an approach using tracking data, check the script `compute_my_sic_from_age.py`.

## Installation
Download and install `miniconda` and run the following in your terminal session:

```bash
$ conda env create -f environment.yml
```

Activate the `conda` environment

```bash
$ conda activate mysic
```

## Usage
Use you can use either `ipython` once the environment is installed or execute the script from command line:

```bash
python3 ./compute_my_sic_from_sic.py [examples/user_config.yml] [--debug --verbose --clean]
```

### On HPC
The user may first allocate a node to run the script on interactively.

``` bash
salloc -p cpuonly -n 1 -t 10:00 --mem=5000
```

And activate the `conda` environment accordingly.
