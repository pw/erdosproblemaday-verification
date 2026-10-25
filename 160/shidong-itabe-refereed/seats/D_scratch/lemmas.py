#!/usr/bin/env python3
"""Referee seat D: exhaustive checks of Itabe's residue lemmas as STATED, plus controls.
Each check prints counts; a lemma 'holds' when violations == 0 and its control (weakened hypothesis) fires."""
import itertools, math, sys

def lemma41(P, mod, weights=((1,1),(2,1),(1,2))):
    """Lemma 4.1: alpha x + beta y = (alpha+beta) z (i.e. P | E) and rx=ry=rz mod `mod` => E == 0."""
    viol=0; tested=0
    for (a,b) in weights:
        for rx in range(P):
            for ry in range(rx%mod, P, mod):
                s=a*rx+b*ry
                for rz in range(rx%mod, P, mod):
                    E=s-(a+b)*rz
                    if E%P==0:
                        tested+=1
                        if E!=0: viol+=1
    return viol, tested

def abab_residue(P, mod):
    """ABAB no-wrap: residues with congruent steps mod P, r0=r2, r1=r3 mod `mod` => exact AP."""
    viol=0; tested=0
    for r0 in range(P):
        for r1 in range(P):
            for r2 in range(r0%mod, P, mod):
                if (2*r1-r0-r2)%P: continue
                r3=(2*r2-r1)%P
                if (r3-r1)%mod: continue
                tested+=1
                if not (r1-r0==r2-r1==r3-r2): viol+=1
    return viol, tested

def beta(r): return (r+1).bit_length()-1  # floor(log2(r+1))

def lemma51(B, bucket=beta):
    viol=0; tested=0
    for r0 in range(B):
        for r1 in range(B):
            if bucket(r0)!=bucket(r1): continue
            for r2 in range(B):
                if (2*r1-r0-r2)%B: continue
                r3=(2*r2-r1)%B
                if bucket(r2)!=bucket(r3): continue
                tested+=1
                if not (r1-r0==r2-r1==r3-r2): viol+=1
    return viol, tested

def tau(r,p):
    return 0 if 3*r<p else (1 if 3*r<2*p else 2)

def lemma71(p, t=tau):
    viol=0; tested=0
    for r0 in range(p):
        for r1 in range(p):
            for r2 in range(p):
                if (2*r1-r0-r2)%p: continue
                r3=(2*r2-r1)%p
                if t(r0,p)!=t(r3,p) or t(r1,p)!=t(r2,p): continue
                tested+=1
                if not (r1-r0==r2-r1==r3-r2): viol+=1
    return viol, tested

def classification():
    bad=0
    for c in itertools.product(range(4),repeat=4):
        if len(set(c))>2: continue
        three=any(c[i]==c[j]==c[k] for i,j,k in itertools.combinations(range(4),3))
        abab=c[0]==c[2] and c[1]==c[3]
        aabb=c[0]==c[1] and c[2]==c[3]
        if three or abab or aabb: continue
        if not (c[0]==c[3] and c[1]==c[2] and c[0]!=c[1]): bad+=1
    return bad

rc=0
print("§2 classification: tuples with <=2 values, no three-equal, no ABAB, no AABB, not proper ABBA:", classification())
print("\n-- Lemma 4.1 (weights (1,1),(2,1),(1,2)) as stated (mod 24) and with smaller moduli --")
for P in [25,49,73,97,121]:
    v,t=lemma41(P,24); print(f"  P={P} mod 24: violations {v} / {t} tested"); rc|= (v>0)
for (P,mod) in [(5,4),(9,4),(13,4),(7,6),(13,6),(7,3),(10,3),(5,2),(9,2),(7,2)]:
    v,t=lemma41(P,mod); print(f"  [generalisation] P={P} mod {mod}: violations {v} / {t}")
print("\n-- ABAB residue no-wrap (4.10)-(4.11) --")
for P in [25,49,73]:
    v,t=abab_residue(P,24); print(f"  P={P} mod 24: violations {v} / {t}"); rc|=(v>0)
for (P,mod) in [(5,4),(9,4),(7,6),(5,2),(7,3),(10,3),(4,3),(9,3)]:
    v,t=abab_residue(P,mod); print(f"  [generalisation/control] P={P} mod {mod}: violations {v} / {t}")
print("\n-- Lemma 5.1 dyadic no-wrap, ALL bases B=1..72 and B=128 --")
tot=0; worst=[]
for B in list(range(1,73))+[128]:
    v,t=lemma51(B); tot+=v
    if v: worst.append(B)
print(f"  violations total {tot}; bases with violations {worst}"); rc|=(tot>0)
# control: replace the dyadic bucket with a 'ratio-3' bucket floor(log3(r+1)) -> should fail
def b3(r):
    k=0; x=r+1
    while x>=3: x//=3; k+=1
    return k
fails=[B for B in range(2,40) if lemma51(B,b3)[0]]
print(f"  control floor(log3(r+1)) buckets: bases with violations {fails[:10]}... (>0 expected)")
print("\n-- Lemma 7.1 thirds no-wrap, ALL integers p=2..60 (primality not used) --")
tot=0; badp=[]
for p in range(2,61):
    v,t=lemma71(p); tot+=v
    if v: badp.append(p)
print(f"  violations total {tot}; p with violations {badp}"); rc|=(tot>0)
# control: halves instead of thirds should fail
def half(r,p): return 0 if 2*r<p else 1
fh=[p for p in range(3,40) if lemma71(p,half)[0]]
print(f"  control (halves instead of thirds): p with violations {fh[:10]} (>0 expected)")
# control: drop the inner equality (only tau(r0)=tau(r3))
def lemma71_outer_only(p):
    v=0
    for r0 in range(p):
        for r1 in range(p):
            for r2 in range(p):
                if (2*r1-r0-r2)%p: continue
                r3=(2*r2-r1)%p
                if tau(r0,p)!=tau(r3,p): continue
                if not (r1-r0==r2-r1==r3-r2): v+=1
    return v
print(f"  control (outer equality only) p=11: violations {lemma71_outer_only(11)} (>0 expected)")
print("RC",rc)
