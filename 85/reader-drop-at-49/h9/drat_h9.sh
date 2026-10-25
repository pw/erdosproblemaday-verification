#!/bin/bash
# DRAT-certify each H9 cell: CaDiCaL writes a text DRAT proof, drat-trim checks it against the CNF.
# Negative control: drat-trim must REJECT a valid proof checked against a weakened CNF (one clause dropped).
D=/tmp/erdos85-1019/h9; OUT=$HOME/MathDyad/erdos85/h9/drat.tsv
echo -e "cell\tcadical\tdrat_bytes\tdrat_trim\tseconds" > $OUT
for f in $D/h9_t*_rep*.cnf; do
  c=$(basename $f .cnf); p=$D/$c.drat; t0=$(date +%s)
  r=$(nice -n 19 timeout 1800 /usr/bin/cadical -q --no-binary $f $p | grep '^s ')
  if [ "$r" != "s UNSATISFIABLE" ]; then
    r="kissat: $(nice -n 19 timeout 3600 $HOME/MathDyad/tools/kissat/build/kissat -q --no-binary $f $p | grep '^s ')"
  fi
  v=$(nice -n 19 timeout 3600 $HOME/.local/bin/drat-trim $f $p 2>&1 | grep -E '^s (VERIFIED|NOT VERIFIED)' | head -1)
  echo -e "$c\t$r\t$(stat -c %s $p)\t$v\t$(( $(date +%s) - t0 ))" >> $OUT
  rm -f $p
done
# negative control on the first cell: drop the last 4-literal clause of the formula, keep the proof of the full formula
f=$(ls $D/h9_t*_rep*.cnf | head -1); p=$D/negctl.drat
/usr/bin/cadical -q --no-binary $f $p > /dev/null
python3 - "$f" > $D/negctl.cnf <<'PY'
import sys
lines = open(sys.argv[1]).read().splitlines()
hdr = lines[0].split(); body = [l for l in lines[1:] if l.strip()]
# drop every clause containing a degree-counter auxiliary? no: drop ALL 4-literal clauses (the C4 constraints)
keep = [l for l in body if len(l.split()) != 5]
print(f"p cnf {hdr[2]} {len(keep)}"); print("\n".join(keep))
PY
v=$($HOME/.local/bin/drat-trim $D/negctl.cnf $p 2>&1 | grep -E '^s (VERIFIED|NOT VERIFIED)|ERROR|WARNING' | head -2 | tr '\n' ' ')
echo -e "NEGCTL(no C4 clauses, proof of full formula)\t-\t-\t$v\t-" >> $OUT
rm -f $p
