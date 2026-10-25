#!/bin/bash
# Negative control for the DRAT column: a proof of the FULL h5_t2 formula, checked against the formula with every
# R1/R1b "at least one" clause removed (the clauses the proof leans on), must NOT verify.
ulimit -v 12000000
f=/tmp/erdos85-fs/cells/h5_t2_rep0_r1b_all.cnf; p=/tmp/erdos85-fs/negctl.drat
nice -n 19 /usr/bin/cadical -q --no-binary $f $p | grep '^s '
python3 - $f > /tmp/erdos85-fs/negctl.cnf <<'PY'
import sys
L = open(sys.argv[1]).read().splitlines(); hdr = L[0].split(); body = [l for l in L[1:] if l.strip()]
# R1/R1b clauses are the only all-positive clauses of length >= 7 over edge variables (<= 946); drop them
def r1(l):
    t = [int(x) for x in l.split()[:-1]]
    return len(t) >= 7 and all(0 < v <= 946 for v in t)
keep = [l for l in body if not r1(l)]
sys.stderr.write(f"dropped {len(body) - len(keep)} clauses\n")
print(f"p cnf {hdr[2]} {len(keep)}"); print("\n".join(keep))
PY
echo "full formula:     $($HOME/.local/bin/drat-trim $f $p 2>&1 | tr -d '\r' | grep -E '^s (VERIFIED|NOT VERIFIED)' | head -1)"
echo "weakened formula: $($HOME/.local/bin/drat-trim /tmp/erdos85-fs/negctl.cnf $p 2>&1 | tr -d '\r' | grep -E '^s (VERIFIED|NOT VERIFIED)|ERROR|failed' | head -2 | tr '\n' ' ')"
rm -f $p
