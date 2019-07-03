#!/usr/bin/env python3

import pandas as pd

import sys
import re

dfcryst = sys.argv[1]  # File containing bcc, fcc, and hcp thermod data
dfglass = sys.argv[2]  # File contiaining mean amorphous enthalpies

# Load data
dfcryst = pd.read_csv(dfcryst)
dfglass = pd.read_csv(dfglass)

# Drop unused potential
dfcryst = dfcryst[dfcryst['potential'] != 'SmAl.lammps.eam']

# Parse potential to get system name function
sys_from_pot = lambda x: '-'.join(re.findall('[A-Z][^A-Z]*', x.split('.')[0]))

# Parse binary composition into list of fractions function
frac_list_from_comp = lambda x: [1-float(x[-4:]), float(x[-4:])]

# Gather the specific enthalpy
dfcryst['enthalpy/atoms'] = dfcryst['v_Enth']/dfcryst['atoms']

# Insert the material system
dfcryst['system'] = dfcryst['potential'].apply(sys_from_pot)

# Find the phases with the lowest enthlapy (most favorable)
dfcryst = dfcryst.loc[dfcryst.groupby(['system', 'element'])['enthalpy/atoms'].idxmin()]

# Get element fractions
dfglass['compositions'] = dfglass['composition'].apply(frac_list_from_comp)

# Remove irrelevant data
dfcryst = dfcryst[['system', 'element', 'phase', 'enthalpy/atoms']]
dfglass = dfglass[['system', 'compositions', 'enthalpy/atoms_count']]
dfglass.columns = list(dfglass.columns)[:-1]+['enthalpy/atoms']

print(dfcryst)
print(dfglass)
