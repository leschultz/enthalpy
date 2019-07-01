#!/usr/bin/env python3
from ast import literal_eval

import numpy as np
import sys
import os
import re

from functions import *

template = sys.argv[1]  # Template file path
potentials_path = sys.argv[2]  # The potentials used
side = int(sys.argv[3])  # The length of the cubic simulation box
lattice_param = float(sys.argv[4])  # The lattice paramter

# Open and read template
template = open(template)
template_contents = template.read()
template.close()

# Phases
phases = ['bcc', 'hcp', 'fcc']

# Gather system information
potentials = set(os.listdir(potentials_path))

for pot in potentials:

    # Modify the potential path based on the subdirectories added
    potential_path = os.path.join(*['../../..', potentials_path, pot])

    split = pot.split('.')

    if 'eam' == split[-1]:
        potential_type = 'eam/alloy'

    if 'fs' == split[-1]:
        potential_type = 'eam/fs'

    element_list = re.findall('[A-Z][^A-Z]*', split[0])
    elements = ' '.join(element_list)

    # Switch between 0 and 1 fraction for binary system
    for el, frac in zip(element_list, np.arange(len(element_list))):
        for phase in phases:

            path = os.path.join(*[pot, el, phase])

            contents = run_creator(
                                   template_contents,
                                   elements,
                                   frac,
                                   potential_path,
                                   potential_type,
                                   side,
                                   phase,
                                   lattice_param,
                                   )

            # Write the input file
            if not os.path.exists(path):
                os.makedirs(path)

            file_out = open(os.path.join(path, 'pure.in'), 'w')
            file_out.write(contents)
            file_out.close()
