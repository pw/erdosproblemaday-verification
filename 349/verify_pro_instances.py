#!/usr/bin/env python3
"""Cross-check GPT-5 Pro's exact machine-checkable instances for the #349 closed form
t0(alpha)=min_k (2^k+1)/alpha^k against lab.py. Per alpha confirms: the boundary prefix and
permanent gap at t0; the shelf [L,T) entirely-complete; the top component extending below L;
the (1.9,1) counterexample (gap 12); and the alpha=1.95 disconnected set (island entire, hole
not). Run from this dir: python3 verify_pro_instances.py"""
import lab
from fractions import Fraction
def F(x): return Fraction(x)
fails=0
def check(c,label):
    global fails
    print(("  OK   " if c else " FAIL ")+label)
    if not c: fails+=1
cases=[
 (F('8/5'),1,F('25/16'),F(1),None),
 (F('9/5'),2,F('14/10'),F('11/10'),None),
 (F('19/10'),4,F('126/100'),F('11/10'),('cx',F(1),12)),
 (F('39/20'),5,F('115/100'),None,('hi',F('1027/1000'),F('104/100'))),
]
for a,k,smid,bL,ex in cases:
    T=F(2**k+1)/a**k; L=F(2**k)/a**k
    print("== alpha=%s (%.4f) k=%d T=%.6f L=%.6f =="%(a,float(a),k,float(T),float(L)))
    pref=lab.floors(T,a,n_terms=k+1,start=0); exp=[2**j for j in range(k)]+[2**k+1]
    check(pref==exp,"boundary prefix %s == %s"%(pref,exp))
    C=sum(pref[:k]); check(pref[k]==2**k+1 and C+1==2**k,"permanent gap at %d (C_{k-1}+1=%d, a_k=%d)"%(2**k,C+1,pref[k]))
    check(lab.entire_cert_0indexed(smid,a)['proven'],"shelf mid t=%.4f entire (proven)"%float(smid))
    if bL is not None: check(lab.entire_cert_0indexed(bL,a)['proven'],"below-shelf t=%.4f entire (top component below L)"%float(bL))
    if ex and ex[0]=='cx':
        _,ct,cg=ex; g=lab.greedy_entire(ct,a,n_terms=20,start=0)
        check((not g['entire']) and g['gap_at']==cg,"counterexample t=%.4f NOT entire, gap@%s (expect %d)"%(float(ct),g.get('gap_at'),cg))
    if ex and ex[0]=='hi':
        _,isl,hole=ex
        check(lab.entire_cert_0indexed(isl,a)['proven'],"island t=%.4f entire"%float(isl))
        check(not lab.entire_cert_0indexed(hole,a)['proven'],"hole t=%.4f NOT entire (disconnected)"%float(hole))
print(); print("ALL PASS" if fails==0 else "%d FAILURES"%fails); sys_exit=fails
import sys; sys.exit(1 if fails else 0)
