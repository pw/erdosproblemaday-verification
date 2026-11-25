#!/bin/bash
R=/tmp/e1125/dl787/repo; cd /tmp/e1125/dl787/bin
for f in ruzsa_lattice_test ruzsa_variants_test test_templates_and_e7 test_zero_centered_dd attack_k7_and_lattices; do
  extra=""; [ $f = attack_k7_and_lattices ] && extra="-fopenmp"
  g++ -O3 -std=c++17 $extra $R/code/$f.cpp -o $f > /tmp/e1125/787work/lat_$f.compile 2>&1; echo "$f compile rc=$?" >> /tmp/e1125/787work/lattice_results.txt
  s=$(date +%s); (ulimit -v 8000000; OMP_NUM_THREADS=4 timeout 1800 ./$f) > /tmp/e1125/787work/lat_$f.out 2>&1; echo "$f run rc=$? time=$(( $(date +%s)-s ))s" >> /tmp/e1125/787work/lattice_results.txt
done
echo DONE >> /tmp/e1125/787work/lattice_results.txt
