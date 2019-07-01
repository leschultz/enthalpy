#!/usr/bin/env python3
from ast import literal_eval

import numpy as np
import sys
import os

from functions import *

runs = int(sys.argv[1])  # The number of runs to generate
template = sys.argv[2]  # Template file path
elements = sys.argv[3]  # Elements
fraction = float(sys.argv[4])  # Fraction of second element
potential = sys.argv[5]  # The potential used
potential_type = sys.argv[6]  # The type of potential
side = int(sys.argv[7])  # The length of the cubic simulation box
unit_cell_type = sys.argv[8]  # fcc, hcp, or bcc
lattice_param = float(sys.argv[9])  # The lattice paramter
timestep = float(sys.argv[10])  # The timestep
min_style = sys.argv[11]  # The energy minimization style
iterations = int(sys.argv[12])  # The number of minimization iterations

# Open and read template
template = open(template)
template_contents = template.read()
template.close()

runs = np.arange(runs)
runs = ['run_'+str(i) for i in runs]

for run in runs:
    contents = run_creator(
                           template_contents,
                           elements,
                           fraction,
                           potential,
                           potential_type,
                           side,
                           unit_cell_type,
                           lattice_param,
                           timestep,
                           min_style,
                           iterations
                           )

    # Write the input file
    path = os.path.join(run, 'steps.in')

    if not os.path.exists(run):
        os.makedirs(run)

    file_out = open(path, 'w')
    file_out.write(contents)
    file_out.close()
