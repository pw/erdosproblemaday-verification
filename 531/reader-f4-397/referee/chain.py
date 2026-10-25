import sys, glob, os
sys.path.insert(0,'/tmp/ref531')
from bitcheck import count
for f in sorted(glob.glob('/home/exedev/MathDyad/subs-1022/531/untrusted/repo/witnesses/w*.txt')):
    raw = open(f,'rb').read(); s = bytes(c for c in raw if c in b'01').decode()
    N, tot, per, first = count(s)
    print(os.path.basename(f), N, tot, first)
