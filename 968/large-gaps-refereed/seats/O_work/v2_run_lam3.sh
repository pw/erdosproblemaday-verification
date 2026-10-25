#!/bin/bash
cd /tmp/oaimath/026/seats/O_work
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
ulimit -v 8000000
exec timeout 1800 nice -n 19 python3 v2_cf.py 3.0 33 1e14,1e15,3e15 > v2_cf_lam3.out 2>&1
