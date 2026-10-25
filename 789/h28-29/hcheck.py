#!/usr/bin/env python3
"""Exact H(A) (largest admissible subset) for explicit integer sets A (page definition: integers, 0 allowed).
Admissible: for all nonempty S,T ⊆ B, sum(S)=sum(T) ⇒ |S|=|T|. Checked literally over all nonempty subset pairs
(no positivity shortcut), so 0 and negatives are handled exactly as the page states."""
import sys, itertools
def admissible(B):
    seen = {}
    for r in range(1, len(B) + 1):
        for S in itertools.combinations(B, r):
            s = sum(S)
            if s in seen and seen[s] != r: return False
            seen.setdefault(s, r)
    return True
def H(A, kmax=None):
    A = sorted(A); best = 0
    for k in range(1, (kmax or len(A)) + 1):
        if any(admissible(S) for S in itertools.combinations(A, k)): best = k
        else: break
    return best
def main():
    cands = {
      "[-10,10] (21)": list(range(-10, 11)),
      "{-10}∪[-8,8]∪{10} (19, report's)": [-10] + list(range(-8, 9)) + [10],
      "[-9,9] (19)": list(range(-9, 10)),
      "{-10}∪[-8,8]∪{10,12} (20)": [-10] + list(range(-8, 9)) + [10, 12],
      "{-12,-10}∪[-8,8]∪{10,12} (21)": [-12, -10] + list(range(-8, 9)) + [10, 12],
      "{-10}∪[-8,8]∪{10,11} (20)": [-10] + list(range(-8, 9)) + [10, 11],
      "{-11,-10}∪[-8,8]∪{10} (20)": [-11, -10] + list(range(-8, 9)) + [10],
      "{-10}∪[-8,8]∪{10,16} (20)": [-10] + list(range(-8, 9)) + [10, 16],
      "{-10}∪[-8,8]∪{10,20} (20)": [-10] + list(range(-8, 9)) + [10, 20],
      "{-10}∪[-8,8]∪{10,9} (20)": [-10] + list(range(-8, 10)) + [10],
    }
    for name, A in cands.items():
        print(f"{name:40s} n={len(A):2d}  H={H(A, 6)}", flush=True)
if __name__ == "__main__": main()
