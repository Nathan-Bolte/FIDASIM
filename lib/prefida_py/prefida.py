#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import numpy as np
#import matplotlib.pyplot as plt
#import scipy as sp
#import pandas as pd
import os
from prefida_py import check_inputs
from prefida_py import check_grid
from prefida_py import check_beam
from prefida_py import check_plasma
from prefida_py import check_fields
from prefida_py import check_distribution
from prefida_py import check_spec
from prefida_py import check_npa
from prefida_py import write_namelist
from prefida_py import write_geometry
from prefida_py import write_equilibrium
from prefida_py import write_distribution
from prefida_py import get_fidasim_dir


def prefida(inputs, grid, nbi, plasma, fields, fbm, spec=None, npa=None):
    """Brief Description

    ;+#prefida
    ;+Checks FIDASIM inputs and writes FIDASIM input files
    ;+***
    ;+##Input Arguments
    ;+     **inputs**: Inputs structure
    ;+
    ;+     **grid**: Interpolation grid structure
    ;+
    ;+     **nbi**: Neutral beam geometry structure
    ;+
    ;+     **plasma**: Plasma parameters structure
    ;+
    ;+     **fields**: Electromagnetic fields structure
    ;+
    ;+     **dist**: Fast-ion distribution structure
    ;+
    ;+##Keyword Arguments
    ;+     **spec**: Optional, Spectral geometry structure
    ;+
    ;+     **npa**: Optional, NPA geometry structure
    ;+
    ;+##Example Usage
    ;+```idl
    ;+IDL> prefida, inputs, grid, nbi, plasma, fields, dist, spec=spec, npa=npa
    ;+```

    History
    -------
    Created on Mon Sep 12 18:20:13 2016 by Nathan Bolte

    To Do
    -----

    """
    # CHECK INPUTS
    inputs = check_inputs(inputs)

    # MAKE DIRECTORIES IF THEY DONT EXIST
    if not os.path.isdir(inputs['result_dir']):
        os.makedirs(inputs['result_dir'])

    # CHECK INTERPOLATION GRID
    check_grid(grid)

    # CHECK BEAM INPUTS
    check_beam(inputs, nbi)

    # CHECK PLASMA PARAMETERS
    check_plasma(inputs, grid, plasma)

    # CHECK ELECTROMAGNETIC FIELDS
    check_fields(inputs, grid, fields)

    # CHECK FAST-ION DISTRIBUTION
    check_distribution(inputs, grid, fbm)

    # CHECK FIDA/BES
    if spec is not None:
        check_spec(inputs, spec)

    # CHECK NPA
    if npa is not None:
        check_npa(inputs, npa)

    # WRITE FIDASIM INPUT FILES
    write_namelist(inputs.input_file, inputs)

    # WRITE GEOMETRY FILE
    write_geometry(inputs.geometry_file, nbi, spec=spec, npa=npa)

    # WRITE EQUILIBRIUM FILE
    write_equilibrium(inputs.equilibrium_file, plasma, fields)

    # WRITE DISTRIBUTION FILE
    write_distribution(inputs.distribution_file, fbm)

    print ''
    print ''
    success('FIDASIM pre-processing completed')
    print  'To run FIDASIM use the following command'
    print  get_fidasim_dir() + '/fidasim ' + inputs['result_dir'] + '/' + inputs['runid'] + '_inputs.dat'
    print ''
    print ''
###############################################################################
if __name__ == "__main__":
    prefida()
