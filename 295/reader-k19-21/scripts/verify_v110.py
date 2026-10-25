#!/usr/bin/env python3
"""Independent check of Kyunghan Bae's v1.1.0 certificates for Erdős #295: k(19)<=36, k(20)<=38, k(21)<=39.
Definition (erdosproblems.com/295): k(N) = least k with N <= n1 < ... < nk, sum 1/ni = 1.
Routes: (1) exact Fraction sum, (2) integer LCM sum. Plus the replacement identities he states, the
harmonic lower bound, and NEGATIVE controls (one denominator perturbed) that must be rejected by both routes.
Exit 0 all pass / 1 a positive check failed / 2 a negative control was NOT rejected. Imports nothing from the submission.
Optional argv[1]: path to his certificates-extension.json, cross-checked as data only (json.load)."""
import sys, json
from fractions import Fraction as F
from math import gcd

C = {
19: [19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,38,39,40,42,43,44,45,46,48,50,52,54,55,66,70,275,14143068,10457416992],
20: [20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,48,50,51,52,53,54,72,9512,316569706,745735753538714400,755732875917998385],
21: [21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,44,45,46,48,49,50,52,53,54,55,56,57,58,64,3162192,13244735025984,60692489317197426150],
}
CLAIM = {19:36, 20:38, 21:39}
K18 = [18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,38,39,40,43,44,45,46,48,50,52,54,63,275,14143068,10457416992]
# botnet grind-35 2026-09-24 comparison witnesses (N=20,21), copied from botnet.com artifact c1db3093...
B20 = [20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,48,50,51,52,53,54,72,9512,316569706,375350516580963408,268924701510638515898654784499874429,2261038874563113922933823915885193677838991607590224593926139941626578400]
B21 = [21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,44,45,46,48,49,50,52,53,54,55,56,57,58,64,3162192,13244732135627,1695054869316863708008507383,2891995144170939944129341268302440926803000814274542400]

def lcm(xs):
    L = 1
    for x in xs: L = L * x // gcd(L, x)
    return L
def r1(D): return sum((F(1, d) for d in D), F(0)) == 1
def r2(D):
    L = lcm(D); return sum(L // d for d in D) == L
def shape(D, N): return len(set(D)) == len(D) and D == sorted(D) and min(D) >= N and all(isinstance(d,int) and d>0 for d in D)

ok = True
def rep(name, cond):
    global ok
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}"); ok = ok and bool(cond)

for N, D in C.items():
    print(f"N={N}")
    rep(f"{len(D)} terms == claimed {CLAIM[N]}", len(D) == CLAIM[N])
    rep("distinct, increasing, min >= N, contains N (so also A192881-admissible)", shape(D, N) and D[0] == N)
    rep("route 1 exact Fraction sum == 1", r1(D))
    rep(f"route 2 integer LCM sum == L (L={lcm(D)}, bits(max)={max(D).bit_length()})", r2(D))
    # harmonic lower bound: fewest consecutive N,N+1,... whose reciprocals reach 1
    s, k = F(0), 0
    while s < 1: s += F(1, N + k); k += 1
    print(f"  harmonic lower bound k >= {k}")

print("stated constructions")
rep("1/18+1/63 == 1/14 == 1/42+1/55+1/66+1/70", F(1,18)+F(1,63) == F(1,14) == F(1,42)+F(1,55)+F(1,66)+F(1,70))
rep("N=19 set == (k18 set - {18,63}) + {42,55,66,70}", sorted((set(K18)-{18,63})|{42,55,66,70}) == C[19] and not ({42,55,66,70} & (set(K18)-{18,63})))
rep("botnet N=20 witness sums to 1 (39 terms)", len(B20)==39 and r1(B20) and r2(B20))
rep("botnet N=21 witness sums to 1 (40 terms)", len(B21)==40 and r1(B21) and r2(B21))
rep("N=20 = first 36 of botnet N=20 + two new", C[20][:36] == B20[:36])
rep("N=21 = first 37 of botnet N=21 + two new", C[21][:37] == B21[:37])
res20 = 1 - sum((F(1,d) for d in B20[:36]), F(0)); res21 = 1 - sum((F(1,d) for d in B21[:37]), F(0))
rep(f"N=20 residual {res20} == 1/745735753538714400 + 1/755732875917998385", res20 == F(151817,56984589375772121632800) == F(1,745735753538714400)+F(1,755732875917998385))
rep(f"N=21 residual {res21} == 1/13244735025984 + 1/60692489317197426150", res21 == F(35558057,470956940228352916800) == F(1,13244735025984)+F(1,60692489317197426150))

if len(sys.argv) > 1:
    J = json.load(open(sys.argv[1]))
    recs = {r['minimum']: [int(x) for x in r['denominators']] for r in J['records']}
    rep("his JSON denominators == the sets checked here (N=18..21)", all(recs.get(N) == D for N, D in C.items()) and recs.get(18) == K18)

print("negative controls (each must be REJECTED by both routes)")
neg_ok = True
for N, D in C.items():
    for i in (0, len(D)//2, len(D)-1):
        B = list(D); B[i] += 1
        rejected = (not r1(B)) and (not r2(B))
        print(f"  [{'PASS' if rejected else 'FAIL'}] N={N} denominator #{i} +1 rejected")
        neg_ok = neg_ok and rejected
    B = D[:-1]; rej = (not r1(B)) and (not r2(B)); print(f"  [{'PASS' if rej else 'FAIL'}] N={N} last term dropped rejected"); neg_ok &= rej
if not neg_ok: print("RESULT: NEGATIVE CONTROL NOT REJECTED — checker untrusted"); sys.exit(2)
print("RESULT:", "VERIFIED k(19)<=36, k(20)<=38, k(21)<=39" if ok else "FAILED"); sys.exit(0 if ok else 1)
