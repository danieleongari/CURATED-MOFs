#!/usr/bin/env python
"""Check consistency of CURATED MOF database"""

import os
import sys
import pandas
import click
import collections

from ase import io, geometry

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
    """Check that there are no overlapping atoms."""
    messages = []

    for cif in cifs:
        try:
            atoms = io.read(cif)
        except Exception as exc:
            raise ValueError(f'Unable to parse file {cif}') from exc
        overlaps = geometry.get_duplicate_atoms(atoms, cutoff=0.1)
        if len(overlaps) != 0:
            messages.append(f'Overlapping atoms detected in {cif}')
    
    if messages:
       print(messages)
       sys.exit(1)

    print('No overlapping atoms found.')


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
