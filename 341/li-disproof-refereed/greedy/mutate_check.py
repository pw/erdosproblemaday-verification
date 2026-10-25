# Mutation controls: the checker must FAIL when Li's formula or the greedy data is perturbed.
import numpy as np, subprocess, sys, re
src=open('check_li.py').read()
muts={
 'drop_B48': src.replace("[3,22,32,40,48]","[3,22,32,40]"),
 'Y0_shift': src.replace("blocks(4,8,q)","blocks(4,9,q)",1),
 'flip_greedy_bit': src.replace("greedy[el]=True","greedy[el]=True; greedy[4999999]=~greedy[4999999]"),
 'shield_drop_P14': src.replace("P={7,14,28}","P={7,28}"),
}
for name,code in muts.items():
    assert code!=src, name
    open('/tmp/erdos2100/_mut.py','w').write(code)
    r=subprocess.run([sys.executable,'/tmp/erdos2100/_mut.py','10000000'],capture_output=True,text=True)
    last=[l for l in r.stdout.strip().split('\n') if l][-1]
    print(f"{name}: rc={r.returncode} verdict={last} :: {[l for l in r.stdout.split(chr(10)) if 'mismatches' in l or 'shield' in l or 'controller' in l][:3]}")
