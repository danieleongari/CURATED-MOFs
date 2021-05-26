#!/usr/bin/env python
"""Check consistency of CURATED MOF database"""

import os
import sys
import pandas
import click
import collections
import warnings
from pathlib import Path

from pymatgen.io.cif import CifParser
from mofchecker import MOFChecker

THIS_DIR = Path(__file__).resolve().parent
ROOT_DIR = THIS_DIR.parent
CIF_DIR = ROOT_DIR / 'cifs'
FRAMEWORKS_CSV = ROOT_DIR / 'mof-frameworks.csv'

FRAMEWORKS_DF = pandas.read_csv(FRAMEWORKS_CSV)

@click.group()
def cli():
    pass


@cli.command('unique-mof-names')
def validate_unique_mof_names():
    """Check that CURATED-MOF names are unique."""
    names = list(FRAMEWORKS_DF['name'].str.lower()) + list(FRAMEWORKS_DF['alternative names'].dropna().str.lower())
    names = [ n for l in names for n in  l.split(',') if l ]
    names = [ n.lower().replace('-', ' ') for n in names ]

    duplicates = [item for item, count in collections.Counter(list(names)).items() if count > 1]

    if duplicates:
        print('Warning: Duplicate CURATED-MOF names detected: {}'.format(duplicates))
        sys.exit(1)

    print('No duplicate CURATED-MOF names found.')


@cli.command('matching-cif-files')
def validate_matching_cif_files():
    """Check that each CURATED-MOF has a matching CIF file."""
    for refcode in FRAMEWORKS_DF['CSD refcode'].str:
        assert Path(CIF_DIR / (str(refcode) +  '.cif')).is_file
        

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
                assert s.is_ordered
            except (ValueError,AssertionError) as exc:
                s = CifParser(cif, occupancy_tolerance=1000).get_structures(primitive=True)[0]
                s.to(filename=cif)
                print(f'Fixed overlapping atoms in {cif}')
            except Exception as exc:
                errors.append(f'Unable to parse file {cif}')
    
    if errors:
       print('\n'.join(errors))
       sys.exit(1)


@cli.command('unique-structures')
@click.argument('cifs', type=str, nargs=-1)
def unique_structures(cifs):
    """Check if structures are unique.

    Uses the mofchecker to compare the atom graph of all structures, making sure that they are unique.
    """
    hashes = {}
    errors = []
    
    for cif in cifs:

        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            structure = CifParser(
                cif,
                occupancy_tolerance=1000,  # CSD overspecifies equivalent sites
            ).get_structures(primitive=True)[0]

        print(f'structure graph for {cif} with {len(structure)} atoms')
        if len(structure) > 1000:
            print(f'Skipping structure graph for {cif} with {len(structure)} atoms')
            continue

        mofchecker = MOFChecker(structure)
        graph_hash = mofchecker.graph_hash

        if graph_hash in hashes:
            errors.append(f'Warning: {cif} and {hashes[graph_hash]} have the same structure graph hash')
        else:
            hashes[graph_hash] = cif

    if errors:
       print('\n'.join(errors))
       sys.exit(1)

if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
