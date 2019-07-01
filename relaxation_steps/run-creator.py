#!/usr/bin/env python3
from ast import literal_eval

import numpy as np
import sys
import os

from functions import *

template = sys.argv[1]  # Template file path
elements = sys.argv[2]  # Elements
potential = sys.argv[3]  # The potential used
potential_type = sys.argv[4]  # The type of potential
side = int(sys.argv[5])  # The length of the cubic simulation box
lattice_param = float(sys.argv[6])  # The lattice paramter
timestep = float(sys.argv[7])  # The timestep

# Open and read template
template = open(template)
template_contents = template.read()
template.close()

# Phases
phases = ['bcc', 'hcp', 'fcc']

# Modify the potential path based on the subdirectories added
potential = os.path.join('../../', potential)

element_list = elements.split(' ')

# Switch between 0 and 1 fraction for binary system
for el, frac in zip(element_list, np.arange(len(element_list))):
    for phase in phases:

        path = os.path.join(el, phase)

        contents = run_creator(
                               template_contents,
                               elements,
                               frac,
                               potential,
                               potential_type,
                               side,
                               phase,
                               lattice_param,
                               timestep,
                               )

        # Write the input file
        if not os.path.exists(path):
            os.makedirs(path)

        file_out = open(os.path.join(path, 'steps.in'), 'w')
        file_out.write(contents)
        file_out.close()
