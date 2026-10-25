#!/bin/bash
# timing/verdict sample of M-cells: sample_cells.sh classes.tsv seed per_case parallel cap  -> runs/sample.tsv
cd ~/MathDyad/erdos85/h1m; mkdir -p runs
CL=$1; SEED=$2; PER=$3; PAR=$4; CAP=$5
python3 - "$CL" "$SEED" "$PER" > runs/sample_list.txt <<'PY'
import sys, random
cl, seed, per = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
rows = [l.rstrip("\n").split("\t") for l in open(cl) if not l.startswith("#")]
rng = random.Random(seed)
for j in sorted({r[0] for r in rows}):
    rs = [r for r in rows if r[0] == j]
    for r in rng.sample(rs, min(per, len(rs))):
        print(r[0], r[1])
PY
run() { j=$1; M=$2; s=$(date +%s.%N)
  r=$(bash -c "ulimit -v 4000000; timeout $((CAP+120)) ~/.venv/bin/python h1mcell.py 7 $j $CAP kissat --pairsb --slots --ph --edgeswap --M $M" 2>&1 | tail -1)
  printf "%s\t%s\t%s\t%.1f\n" "$j" "$M" "$r" "$(echo "$(date +%s.%N) - $s" | bc)" >> runs/sample.tsv; }
export -f run; export CAP
xargs -P "$PAR" -L 1 bash -c 'run "$0" "$1"' < runs/sample_list.txt
echo DONE >> runs/sample.tsv
