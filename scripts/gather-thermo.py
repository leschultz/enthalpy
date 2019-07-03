#!/usr/bin/env python3

from PyQt5 import QtGui  # Added to be able to import ovito

from ovito.modifiers import VoronoiAnalysisModifier
from ovito.io import import_file

from matplotlib import pyplot as pl

from os.path import join

import pandas as pd

import sys
import os

from functions import *

runpath = sys.argv[1]  # The top directory of runs
exportpath = sys.argv[2]  # The export directory for data
sysfilename = sys.argv[3]  # The name for the thermodynamic data file
trajfilename = sys.argv[4]  # The name for the trajectory file

# Count the number of runs for progress status
paths = []

runs = -1
for path, subdirs, files in os.walk(runpath):

    # Only paths containing files needed
    condition = (sysfilename in files)

    if not condition:
        continue

    paths.append(path)  # The path for viable job
    runs += 1

runs = str(runs)  # Only convert to string once

# Loop through runs and gather ICO fractions
count = 0
for path in paths:

    # Status update
    print('Analyzing ('+str(count)+'/'+runs+'): '+path)

    split = path.split('/')

    potential, element, phase = split[1:]

    # Relevant files
    sysfile = join(path, sysfilename)
    trajfile = join(path, trajfilename)

    # Gather the thermodynamic data
    cols, data = system_parse(sysfile)

    # Gather trajectory file paramters
    natoms = trajectory_parse(trajfile)

    data = [[potential, element, phase, natoms]+data[0]]
    cols = ['potential', 'element', 'phase', 'atoms']+cols

    if count == 0:
        df = pd.DataFrame(data, columns=cols)

    else:
        df.loc[count] = data[0]

    count += 1

# Path to export
if not os.path.exists(exportpath):
    os.makedirs(exportpath)

df.to_csv(
          join(exportpath, 'run_thermo_data.txt'),
          index=False
          )
