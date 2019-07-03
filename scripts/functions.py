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
                ):
    '''
    Generate a LAMMPS input file
    '''

    # Replace keywords within a template document
    contents = template_contents

    contents = contents.replace(
                                '#replace_elements#',
                                elements
                                )

    contents = contents.replace(
                                '#replace_second_element_fraction#',
                                str(fraction)
                                )

    contents = contents.replace(
                                '#replace_potential#',
                                potential
                                )

    contents = contents.replace(
                                '#replace_potential_type#',
                                potential_type
                                )

    contents = contents.replace(
                                '#replace_side#',
                                str(side)
                                )

    contents = contents.replace(
                                '#replace_unit_cell_type#',
                                unit_cell_type
                                )

    contents = contents.replace(
                                '#replace_lattice_param#',
                                str(lattice_param)
                                )

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


def trajectory_parse(trajfile):
    '''
    Pares the trajectory file for relevant system simulation information.

    input:
        trajfile = The name and path of the trajectory file
    outputs:
        natoms = The number of atoms for the system
    '''

    # Only one trajectory should be in the file so the number
    with open(trajfile) as f:
        for line in f:
            if 'NUMBER OF ATOMS' in line:  # Unique because of single frame
                line = next(f)
                natoms = int(line)

    return natoms
