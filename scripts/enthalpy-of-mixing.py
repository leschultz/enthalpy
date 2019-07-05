#!/usr/bin/env python3

import pandas as pd

import sys
import os
import re

dfcryst = sys.argv[1]  # File containing bcc, fcc, and hcp thermod data
dfglass = sys.argv[2]  # File contiaining mean amorphous enthalpies
exportpath = sys.argv[3]  # The export directory for data

# Load data
dfcryst = pd.read_csv(dfcryst)
dfglass = pd.read_csv(dfglass)

# Drop unused potential
dfcryst = dfcryst[dfcryst['potential'] != 'SmAl.lammps.eam']

# Parse potential to get system name function
sys_from_pot = lambda x: '-'.join(re.findall('[A-Z][^A-Z]*', x.split('.')[0]))

# Parse binary composition into fractions function
frac_list_from_comp = lambda x: [1-float(x[-4:]), float(x[-4:])]

# Gather the specific enthalpy
dfcryst['enthalpy/atoms'] = dfcryst['v_Enth']/dfcryst['atoms']

# Insert the material system
dfcryst['system'] = dfcryst['potential'].apply(sys_from_pot)

# Find the phases with the lowest enthlapy (most favorable)
dfcryst = dfcryst.loc[dfcryst.groupby([
                                       'system',
                                       'element'
                                       ])['enthalpy/atoms'].idxmin()]

# Get element fractions
dfglass['compositions'] = dfglass['composition'].apply(frac_list_from_comp)

# Remove irrelevant data
dfcryst = dfcryst[['system', 'element', 'phase', 'enthalpy/atoms']]
dfglass = dfglass[['system', 'compositions', 'enthalpy/atoms_mean']]
dfglass.columns = list(dfglass.columns)[:-1]+['enthalpy/atoms']

count = 0
df = pd.DataFrame(columns=['system', 'composition', 'mixing_enthalpy/atom'])
for row in dfglass.values:
    fractions = dict(zip(row[0].split('-'), row[1]))

    # Math element fraction with crystal enthalpy
    cryst = dfcryst[dfcryst['system'] == row[0]][['element', 'enthalpy/atoms']]
    cryst = [cryst[cryst['element'] == i]['enthalpy/atoms'] for i in fractions]

    # Enthalpy of mixing
    mix = row[2]-sum([i.values*j for i, j in zip(cryst, row[1])])[0]

    comp = '{:.2f}'.format(row[1][1])
    df.loc[count] = [row[0], row[0].split('-')[-1]+comp, mix]

    count += 1

# Path to export
if not os.path.exists(exportpath):
    os.makedirs(exportpath)

df.to_csv(
          os.path.join(exportpath, 'enthalpy_of_mixing.txt'),
          index=False
          )
