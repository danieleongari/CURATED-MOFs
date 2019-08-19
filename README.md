# Clean, Uniform and Refined with Automatic Tracking from Experimental Database (CURATED) MOFs

## Why these MOFs?
* the MOF is super famous
* in our group we worked a lot with it
* the MOF has been found from computational screening for a specific applicatation, and its good performance confirmed from experiments.
Consider adding a few words about the choice, in the `notes` column of `mof-frameworks.csv`
* elegant + porous + stable

## Which CSD refcode?
The CSD refcode is not mandatory to be the origin of the cif structure, because there may be better reference (e.g., one where some problems have already been fixed).
Anyway, try to use as the refcode the oldest CSD entry for that MOF, which presumibly is its first synthesis.
For the moment we limit ourself to *real* MOFs only: therefore, the CSD should point to a reference paper that indicates the synthesis procedure and some standard experimental characterization.

## Wishlist/cif_conventional/cifs_tofix
* `wishlist.txt` is a dirty document to annotate interesting MOFs to add
* `cif_conventional/` contains the "conventional" (typically cubic) version of the MOF
Note that if your cubic mof contains <300 atoms, you may want to use it as the main cif, because the primitive will have anyway too small perpendicular widths

* `cif_tofix/` contains structures that require tedius fixes to do later, but that in the meanwhile are included in the list .csv

## Tips:
* check in the CoRE-MOF first if the desolvated/P1/symmetry-reduced structure is already present
* follow the cell symmetry list of [CP2K](https://manual.cp2k.org/trunk/CP2K_INPUT/FORCE_EVAL/SUBSYS/CELL.html)
