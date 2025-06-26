# LiH bulk

Data are

- `abinit_lih_bulk16.dat` for 2x2x2 LiH cell
- `abinit_lih_bulk54.dat` for 3x3x3 LiH cell

Data are
Nv   EcMP2 (Ha)  EcCCSD (Ha)

## First extrapolation to infinite Nv

Run `extrap_nvirtuals.py` for the two data sets 2x2x2 and 3x3x3.
Change `filename` in `extrap_nvirtuals.py`

Report manually the Nv-extrapolated Ec in `abinit_lih_bulk_volume.dat`


## Second extrapolation to infinite supercell

Run `extrap_volumes.py`


