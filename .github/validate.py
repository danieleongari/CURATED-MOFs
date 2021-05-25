#!/usr/bin/env python
"""Check consistency of CURATED MOF database"""

import os
import sys
import pandas
import click
import collections
import warnings

from pymatgen.io.cif import CifParser

SCRIPT_PATH = os.path.split(os.path.realpath(__file__))[0]
ROOT_DIR = os.path.join(SCRIPT_PATH, os.pardir)

FRAMEWORKS_CSV = os.path.join(ROOT_DIR, 'mof-frameworks.csv')

FRAMEWORKS_DF = pandas.read_csv(FRAMEWORKS_CSV)

@click.group()
def cli():
    pass


@cli.command('unique-mof-names')
def validate_unique_mof_names():
    """Check that CURATED-MOF names are unique."""
    names = FRAMEWORKS_DF['name'].str.lower()
    names = names.str.replace('-',' ')

    duplicates = [item for item, count in collections.Counter(list(names)).items() if count > 1]

    if duplicates:
        print('Warning: Duplicate CURATED-MOF names detected: {}'.format(duplicates))
        sys.exit(1)

    print('No duplicate CURATED-MOF names found.')

@cli.command('overlapping-atoms')
@click.argument('cifs', type=str, nargs=-1)
def overlapping_atoms(cifs):
    """Fix overlapping atoms.
    
    If overlapping atoms are detected, try removing them via pymatgen.
    """
    errors = []

    # catch pymatgen warnings for overlapping atoms
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        for cif in cifs:
            try:
                s = CifParser(cif).get_structures(primitive=True)[0]
            except ValueError as exc:
                s = CifParser(cif, occupancy_tolerance=1000).get_structures(primitive=True)[0]
                s.to(filename=cif)
                print(f'Fixed overlapping atoms in {cif}')
            except Exception as exc:
                errors.append(f'Unable to parse file {cif}')
    
    if errors:
       print(errors)
       sys.exit(1)


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
