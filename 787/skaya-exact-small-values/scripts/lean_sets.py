import re,sys; sys.path.insert(0,'/tmp/e1125/787work')
from mis import *
src=open(sys.argv[1]).read()
for name,body in re.findall(r'^def (A\d+\w*) : List Int :=\s*\[([^\]]*)\]', src, re.M):
    A=[int(x) for x in body.replace('\n',' ').split(',') if x.strip()]
    claim=re.search(r'HasExactMaxSumAvoiding '+name+r' (\d+)', src)
    a,_=alpha_cpsat(A)
    print(name, len(A), len(set(A)), 'alpha', a, 'lean-claim', claim.group(1) if claim else None, 'OK' if claim and int(claim.group(1))==a else '??')
