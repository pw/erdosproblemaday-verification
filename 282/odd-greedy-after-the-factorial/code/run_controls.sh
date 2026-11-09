#!/bin/bash
# Re-runs every control behind the #282 entry. Needs og (gcc -O2 -o og og.c -lgmp), python3 + sympy, gmpy2.
PY=${PY:-/home/exedev/MathDyad/.venv/bin/python}
echo "== literature controls (og one a b): numerator sequence, then length"
for f in "4 23" "3 179" "5 139" "5 5809" "5 1444613"; do set -- $f; echo "$1/$2: $(./og one $1 $2 | tr '\n' ' ')"; done
echo "== OEIS A030541-A030546, A031285 vs og"; $PY oeis_rotation.py
echo "== Pihko 2010 Table 4 and Theorem 3.5"; $PY - <<'P'
import subprocess, os
from sympy import primerange, factorial
pihko={1:'3,4,5,4,1',2:'3,4,5,2,1',3:'3,4,1',4:'3,4,1',5:'3,4,5,2,1',6:'3,4,5,4,1',7:'3,4,5,2,1',8:'3,4,1',9:'3,4,1',10:'3,4,5,2,1'}
ok=sum(subprocess.run(['./og','one','3',str(24*t-1)],capture_output=True,text=True).stdout.split('\n')[0]==s for t,s in pihko.items())
print('Table 4 (3/(24t-1), t=1..10):',ok,'/ 10 identical')
n=bad=0
for p in primerange(5,400):
    out=subprocess.run(['./og','one','2',str(2*factorial(p-1)-1)],capture_output=True,text=True,env={**os.environ,'OG_FAST':'1'}).stdout.split('\n')[0]
    n+=1; bad+= out!=','.join(map(str,list(range(2,p))+[1]))
print('Theorem 3.5 (2/(2(p-1)!-1) -> 2..p-1,1), odd primes 5..397:',n-bad,'/',n)
P
echo "== July exact checker's histogram, b <= 999"; ./og scan 1 999 > /tmp/scan999.$$; $PY - /tmp/scan999.$$ <<'P'
import re,ast,sys
src=open('/home/exedev/MathDyad/runs/erdos282_wave5p_reverify.py').read()
exp=ast.literal_eval(re.search(r'EXPECTED_999_DISTRIBUTION = (\{.*?\})',src,re.S).group(1))
got={int(x.split(':')[0]):int(x.split(':')[1]) for x in open(sys.argv[1]).read().split('HIST')[1].split()}
print('identical to the July exact-Fraction histogram' if got==exp else 'MISMATCH', sum(got.values()))
P
echo "== mutations"; sed 's/ul s = q2 ? r : r + a;/ul s = q2 ? r + a : r;/' og.c > /tmp/ogm1.$$.c && gcc -O2 -o /tmp/ogm1.$$ /tmp/ogm1.$$.c -lgmp && echo "true b<=199:     $(./og scan 1 199 | grep HIST)"; echo "parity flipped:  $(/tmp/ogm1.$$ scan 1 199 | grep HIST)"
sed 's/ul g = gcdul(s, bn);/ul g = 1;/' og.c > /tmp/ogm2.$$.c && gcc -O2 -o /tmp/ogm2.$$ /tmp/ogm2.$$.c -lgmp && echo "g=1: $(/tmp/ogm2.$$ scan 1 199 2>&1 >/dev/null | head -1)"
echo "== replay engine vs fast engine, every 3 <= N <= 400, both families (full traces)"; bad=0; for N in $(seq 3 400); do for m in 1 2; do ./og fact 3 $N 100000 /tmp/s.$$ $m >/dev/null; OG_FAST=1 ./og fact 3 $N 100000 /tmp/f.$$ $m >/dev/null; cmp -s /tmp/s.$$ /tmp/f.$$ || bad=$((bad+1)); done; done; echo "mismatches: $bad / 796"
echo "== fixed-modulus engine vs og at N = 500, 1000 (full traces, from fixedmod_*.out)"; for N in 500 1000; do for m in 1 2; do OG_FAST=1 ./og fact 3 $N 100000 /tmp/t.$$ $m >/dev/null; [ "$(cat /tmp/t.$$)" = "$(sed -n 2p out/fixedmod_${N}_${m}.out 2>/dev/null || sed -n 2p fixedmod_${N}_${m}.out)" ] && echo "N=$N m=$m identical" || echo "N=$N m=$m DIFFER"; done; done
echo "== certificates: records + 3000 random fractions + corrupted claims"; $PY certify.py 2086/2381 7734/7829 7990/8111 8328/8581 373/6893 881/937; $PY certify_sample.py
echo "== Brown's coverage table and counts"; $PY brown_cover.py ${KMATH:-../out/kmath478.htm}
echo "== mod-p collapse (covered / fatal / neither at numerator p)"; $PY absorbing.py
rm -f /tmp/*.$$ /tmp/*.$$.c
