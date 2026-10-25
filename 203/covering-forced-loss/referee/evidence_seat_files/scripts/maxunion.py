# Exact max over all coset choices of |C_p1 u ... u C_pr| on the torus (Z/T)^2, T = lcm(e_p).
# C_p(c) = {(k,l): a_p k + b_p l == c (mod e_p)} (forms derived+verified in cosets.py).
import sys, itertools, math
from fractions import Fraction
import numpy as np
sys.path.insert(0, "/tmp/evidence203/scripts")
from cosets import lattice_form
def run(primes, fix_first):
    forms = [lattice_form(p) for p in primes]
    T = 1
    for e, *_ in forms: T = T * e // math.gcd(T, e)
    k, l = np.meshgrid(np.arange(T), np.arange(T), indexing="ij")
    idx = [((a * k + b * l) % e).ravel() for e, g, a, b in forms]
    masks = [[idx[i] == c for c in range(forms[i][0])] for i in range(len(primes))]
    ranges = [range(1) if (fix_first and i == 0) else range(forms[i][0]) for i in range(len(primes))]
    # nested loop with partial unions to keep it cheap
    best, arg, nchoices = -1, None, 0
    from collections import Counter
    hist = Counter()
    def rec(i, acc, choice):
        nonlocal best, arg, nchoices
        if i == len(primes):
            n = int(acc.sum()); nchoices += 1; hist[n] += 1
            if n > best: best, arg = n, tuple(choice)
            return
        for c in ranges[i]:
            rec(i + 1, masks[i][c] if acc is None else (acc | masks[i][c]), choice + [c])
    rec(0, None, [])
    return T, best, arg, nchoices, hist
if __name__ == "__main__":
    for primes, fix in [((5, 7, 11, 13), False), ((5, 7, 11, 13, 17), True), ((5, 7, 11, 13, 17), False)]:
        T, best, arg, nch, hist = run(primes, fix)
        print(f"primes={primes} torus=(Z/{T})^2 ({T*T} pts), choices enumerated={nch}{' (c_5 fixed =0)' if fix else ''}")
        print(f"   max covered = {best}  density = {Fraction(best, T*T)}  ~{best/(T*T):.6f}  argmax c={arg}")
        print(f"   min covered = {min(hist)}  ({Fraction(min(hist),T*T)});  #choices attaining max = {hist[best]}")
        print(f"   union bound sum 1/e_p = {sum(Fraction(1, lattice_form(p)[0]) for p in primes)}")
