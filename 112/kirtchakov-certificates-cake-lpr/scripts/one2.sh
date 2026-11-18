#!/bin/bash
# One cube: regenerate the formula with Kirtchakov's generator, compare its SHA-256 with his ledger,
# solve with CaDiCaL 3.0.1 (his recorded options minus the -t time limit), stream the text LRAT proof
# through sha256 + byte count into cake_lpr (CakeML-verified checker) without writing it to disk.
# Writes res/<name>.json; skips if it exists. Usage: one.sh name N p q s pf qf sf
set -u
W=$HOME/MathDyad/erdos112/kirtchakov/work; C=$HOME/MathDyad/tools/cadical-3.0.1/build/cadical; L=$HOME/MathDyad/tools/cake_lpr/cake_lpr
n=$1; shift; cd $W || exit 1
[ -s res/$n.json ] && exit 0
[ -d tmp/$n ] && exit 0
mkdir -p locks; mkdir locks/$n 2>/dev/null || exit 0
mkdir -p res tmp
T=tmp/$n; mkdir -p $T
python3 make_structured.py "$@" $T/$n.cnf > $T/gen.log 2>&1 || { echo "{\"name\":\"$n\",\"error\":\"gen\"}" > res/$n.json; exit 0; }
cnf_sha=$(sha256sum $T/$n.cnf | cut -d' ' -f1)
led=$(grep "^$n VERIFIED" CERTLOG.txt)
led_cnf=$(echo "$led" | sed -n 's/.*cnf_sha256=\([0-9a-f]*\).*/\1/p')
led_lrat=$(echo "$led" | sed -n 's/.*lrat_sha256=\([0-9a-f]*\).*/\1/p')
led_bytes=$(echo "$led" | sed -n 's/.*lrat_bytes=\([0-9]*\).*/\1/p')
led_steps=$(echo "$led" | sed -n 's/.*after \([0-9]*\) checked steps.*/\1/p')
mkfifo $T/p.fifo
s0=$(date +%s.%N)
/usr/bin/time -f "%e %M" -o $T/solve.time $C --lrat --no-binary $T/$n.cnf $T/p.fifo > $T/$n.sol 2>&1 &
spid=$!
tee < $T/p.fifo >(sha256sum | cut -d' ' -f1 > $T/lrat.sha) >(wc -c > $T/lrat.bytes) | /usr/bin/time -f "%e %M" -o $T/check.time $L --CML_HEAP_SIZE=1536 $T/$n.cnf /dev/stdin > $T/cake.out 2> $T/cake.err
crc=$?
wait $spid; src=$?
sleep 1
s1=$(date +%s.%N)
python3 - "$n" "$cnf_sha" "$led_cnf" "$led_lrat" "$led_bytes" "$led_steps" "$src" "$crc" "$T" "$s0" "$s1" > res/$n.json.tmp <<'PY'
import json,sys
n,cs,lc,ll,lb,lst,src,crc,T,s0,s1=sys.argv[1:]
rd=lambda f: open(f'{T}/{f}').read().strip() if __import__('os').path.exists(f'{T}/{f}') else ''
sol=rd(n+'.sol'); sline=[l for l in sol.splitlines() if l.startswith('s ')]
st=rd('solve.time').split()[-2:]; ct=rd('check.time').split()[-2:]
r=dict(name=n, cnf_sha256=cs, cnf_matches_ledger=(cs==lc), solver_rc=int(src), solver_status=sline[0] if sline else '',
       lrat_sha256=rd('lrat.sha'), lrat_bytes=int(rd('lrat.bytes') or 0), lrat_matches_ledger=(rd('lrat.sha')==ll and rd('lrat.bytes')==lb),
       ledger_steps=int(lst), cake_stdout=rd('cake.out'), cake_stderr=rd('cake.err')[-300:], cake_rc=int(crc),
       cake_verified=(rd('cake.out')=='s VERIFIED UNSAT'), solve_secs=float(st[0]) if st else None, solve_maxrss_kb=int(st[1]) if len(st)>1 else None,
       check_secs=float(ct[0]) if ct else None, check_maxrss_kb=int(ct[1]) if len(ct)>1 else None, wall=round(float(s1)-float(s0),1))
print(json.dumps(r))
PY
mv res/$n.json.tmp res/$n.json
rm -rf $T
