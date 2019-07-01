from ast import literal_eval
import numpy as np
import random


def run_creator(
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
                ):
    '''
    Generate a LAMMPS input file
    '''

    # Minimization parameters
    iterations = str(iterations)
    steps = 'minimize 0 0 '+iterations+' '+iterations

    # Replace keywords within a template document
    contents = template_contents
    contents = contents.replace('#replace_elements#', elements)
    contents = contents.replace('#replace_second_element_fraction#', str(fraction))
    contents = contents.replace('#replace_potential#', potential)
    contents = contents.replace('#replace_potential_type#', potential_type)
    contents = contents.replace('#replace_side#', str(side))
    contents = contents.replace('#replace_unit_cell_type#', unit_cell_type)
    contents = contents.replace('#replace_lattice_param#', str(lattice_param))
    contents = contents.replace('#replace_timestep#', str(timestep))
    contents = contents.replace('#replace_min_style#', min_style)
    contents = contents.replace('#replace_holds#', steps)

    return contents


def input_parse(infile):
    '''
    Parse the input file for important parameters

    inputs:
        infile = The name and path of the input file
    outputs:
        param = Dictionary containing run paramters
    '''

    holdsteps = []
    temperatures = []
    with open(infile) as f:
        for line in f:

            line = line.strip().split(' ')

            if 'run' == line[0]:
                holdsteps.append(int(line[-1]))

            if 'mydumprate' in line:
                line = [i for i in line if i != '']
                dumprate = int(line[-1])

            if 'pair_coeff' in line:
                line = [i for i in line if i != '']
                elements = line[4:]

            if 'fraction' in line:
                line = [i for i in line if i != '']
                fraction = float(line[-1])

            if ('temp' in line) and ('fix' in line):
                line = [i for i in line if i != '']
                temperatures.append(float(line[5]))

    param = {
             'holdsteps': holdsteps,
             'dumprate': dumprate,
             'elements': elements,
             'fraction': fraction,
             'temperatures': temperatures,
             }

    return param


def system_parse(sysfile):
    '''
    Parse the thermodynamic data file

    inputs:
        sysfile = The name and path of the thermodynamic data file
    outputs:
        columns = The columns for the data
        data = The data from the file
    '''

    data = []
    with open(sysfile) as f:
        line = next(f)
        for line in f:

            if '#' in line:
                values = line.strip().split(' ')
                columns = values[1:]

            else:
                values = line.strip().split(' ')
                values = list(map(literal_eval, values))
                data.append(values)

    return columns, data
