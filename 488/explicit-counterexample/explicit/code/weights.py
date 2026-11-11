# Certified integer weights w_p = floor(R * ln p), R = 2^RB, for primes p <= YMAX (60-digit Decimal; asserts the
# fractional part is far from 0 and 1 so the floor is unambiguous). Writes weights_RB.txt: "p w_p".
import sys
from decimal import Decimal, getcontext
getcontext().prec=60
RB=int(sys.argv[1]); YMAX=int(sys.argv[2]); R=Decimal(2)**RB
def primes_upto(y):
    s=bytearray([1])*(y+1); s[0]=s[1]=0
    for i in range(2,int(y**.5)+1):
        if s[i]: s[i*i::i]=bytearray(len(s[i*i::i]))
    return [i for i in range(y+1) if s[i]]
P=primes_upto(YMAX)
with open(f'weights_{RB}.txt','w') as f:
    mind=1
    for p in P:
        v=R*Decimal(p).ln(); w=int(v); fr=v-w; mind=min(mind,fr,1-fr)
        f.write(f"{p} {w}\n")
print(len(P),"primes, min distance of R ln p to an integer:",mind)
assert mind>Decimal('1e-40')
