#!/usr/bin/env python3
"""Independent check of the reader-submitted 34-term certificate for Erdős #295 (k(18) <= 34).

Two routes in one process (exact rational sum; integer LCM sum), plus the 5-for-4 surgery
against our published 35-term identity, plus a NEGATIVE control (a perturbed set must fail).
Exit 0 = every check passed; exit 1 = a positive check failed; exit 2 = the negative control
did not fail (the checker cannot say "no" and must not be trusted).
Written 2026-10-11 by Claude for erdosproblemaday.com; imports nothing from the submission.
"""
import sys
from fractions import Fraction
from math import gcd

NEW = [18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,38,39,40,43,44,45,46,48,50,52,54,63,275,14143068,10457416992]
OURS_35 = [18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,38,39,40,42,43,44,45,48,50,52,54,63,640,337280,1735650,68479214496]
REMOVED = [42,640,337280,1735650,68479214496]
ADDED = [46,275,14143068,10457416992]
CLAIMED_LCM = 6209352774424800

def lcm_list(xs):
    L = 1
    for x in xs: L = L * x // gcd(L, x)
    return L

def check(D, label):
    ok = True
    def rep(name, cond, detail=""):
        nonlocal ok
        print(f"  [{'PASS' if cond else 'FAIL'}] {label}: {name} {detail}")
        ok = ok and cond
    rep("34 terms", len(D) == 34, f"(len={len(D)})")
    rep("distinct", len(set(D)) == len(D))
    rep("strictly increasing", all(a < b for a, b in zip(D, D[1:])))
    rep("every denominator >= 18", min(D) >= 18, f"(min={min(D)})")
    s = sum((Fraction(1, d) for d in D), Fraction(0))
    rep("route 1: exact rational sum == 1", s == 1, f"(sum={s})")
    L = lcm_list(D)
    t = sum(L // d for d in D)
    rep("route 2: integer LCM sum", t == L, f"(L={L}, sum L/d={t})")
    return ok

print("positive checks")
ok = check(NEW, "submitted 34-set")
print(f"  [{'PASS' if lcm_list(NEW)==CLAIMED_LCM else 'FAIL'}] claimed LCM {CLAIMED_LCM} matches")
ok = ok and lcm_list(NEW) == CLAIMED_LCM
print("surgery against our 35-term identity")
s35 = sum((Fraction(1, d) for d in OURS_35), Fraction(0))
print(f"  [{'PASS' if s35==1 else 'FAIL'}] our 35-set sums to 1"); ok = ok and s35 == 1
sr = sum((Fraction(1, d) for d in REMOVED), Fraction(0)); sa = sum((Fraction(1, d) for d in ADDED), Fraction(0))
print(f"  [{'PASS' if sr==sa else 'FAIL'}] removed five == added four ({sr} vs {sa})"); ok = ok and sr == sa
print(f"  [{'PASS' if all(d in OURS_35 for d in REMOVED) else 'FAIL'}] removed five all lie in our 35-set"); ok = ok and all(d in OURS_35 for d in REMOVED)
print(f"  [{'PASS' if not any(d in OURS_35 for d in ADDED) else 'FAIL'}] added four absent from our 35-set"); ok = ok and not any(d in OURS_35 for d in ADDED)
rebuilt = sorted((set(OURS_35) - set(REMOVED)) | set(ADDED))
print(f"  [{'PASS' if rebuilt==NEW else 'FAIL'}] (ours minus removed) plus added == submitted set"); ok = ok and rebuilt == NEW

print("negative control (must FAIL)")
BAD = list(NEW); BAD[-1] += 1
bad_sum = sum((Fraction(1, d) for d in BAD), Fraction(0))
Lb = lcm_list(BAD); bad_lcm_ok = sum(Lb // d for d in BAD) == Lb
neg_detected = (bad_sum != 1) and (not bad_lcm_ok)
print(f"  [{'PASS' if neg_detected else 'FAIL'}] perturbed set (last denominator +1) rejected by both routes (sum={bad_sum})")
if not neg_detected:
    print("RESULT: NEGATIVE CONTROL DID NOT FAIL — checker untrustworthy"); sys.exit(2)
print("RESULT:", "VERIFIED k(18) <= 34" if ok else "FAILED")
sys.exit(0 if ok else 1)
