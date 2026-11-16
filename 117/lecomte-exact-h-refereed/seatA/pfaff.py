"""[10, Lemma 3] as used in Sec 4.3 (j=2): a subspace of alternating 4x4 forms over F_p whose nonzero members are all
nondegenerate has dimension <= 2.  Exhaustive over F_3 (and F_2 as a second field): search for 3-dim anisotropic
subspaces of the Pfaffian quadratic form on Alt_4 (6 coordinates m12,m13,m14,m23,m24,m34).
Positive control: 2-dim anisotropic subspaces DO exist (so the search can find things)."""
import itertools
def pf(m, p): return (m[0]*m[5] - m[1]*m[4] + m[2]*m[3]) % p
def run(p):
    vecs = [v for v in itertools.product(range(p), repeat=6) if any(v)]
    aniso = [v for v in vecs if pf(v, p)]
    S = set(aniso)
    def span_ok(basis):
        for c in itertools.product(range(p), repeat=len(basis)):
            if not any(c): continue
            w = tuple(sum(ci*b[k] for ci, b in zip(c, basis)) % p for k in range(6))
            if not any(w): return False  # dependent
            if w not in S: return False
        return True
    two = 0; three = 0
    for a in aniso:
        for b in aniso:
            if b <= a: continue
            if span_ok([a, b]):
                two += 1
                if three == 0:
                    for c in aniso:
                        if c > b and span_ok([a, b, c]): three += 1; break
    print(f"p={p}: anisotropic vectors {len(aniso)}, anisotropic 2-dim spans found {two} (>0 expected), 3-dim found {three} (0 expected)")
    assert two > 0 and three == 0
run(2); run(3)
