# Audit reproduction commands

Run from this audit directory unless a different directory is shown.

## Frozen author package

```bash
sha256sum /home/exedev/erdos_scratch/erdos86_q9_1506_20260811.tar.gz
cd /home/exedev/erdos_scratch/erdos86_q9_1506_20260811
sha256sum SHA256SUMS q9_edges_1506.json
sha256sum -c SHA256SUMS
./reproduce.sh
```

## Independent proof checks

```bash
python3 verify_q9_independent.py
python3 check_bundle_consistency.py
python3 negative_mutation_test.py
python3 check_site_gate.py
```

## Rebuilt generator

```bash
g++ -O3 -fopenmp -std=c++20 q9_min_conflicts_author.cpp \
  -o q9_min_conflicts_rebuilt

./q9_min_conflicts_rebuilt \
  q9_upstream/q9_edges_repair_from1503_iter2.json \
  reproduced_q9_1506_exact_path.json 1 1000000 1

./q9_min_conflicts_rebuilt public_q9_1505.json \
  reproduced_q9_1506_seed1.json 12 1000000 1
```

The one-thread canonical-path output is byte-identical to the author witness.
The 12-thread output is a distinct valid 1506-edge graph.

## Current public baseline

```bash
git ls-remote \
  https://github.com/rafalwronapl/erdos86-hypercube-c4.git \
  HEAD refs/heads/main

git clone --depth 1 \
  https://github.com/rafalwronapl/erdos86-hypercube-c4.git \
  public_upstream_current
```
