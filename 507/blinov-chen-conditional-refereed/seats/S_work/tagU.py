# Seat S: tag-minor check for the tagged-moment lemma, with the real position layout of a packing.
# For random label pairs (lam != mu) over F_r^5, build the deterministic row-1/row-2 digit polynomials
# (L1=L2=r: residue 0 -> digit r, residue x -> x), compute U = A_lam*Q_mu - A_mu*Q_lam on low degrees,
# and assert: U_j = 0 for j < a, U_a = Q_mu[a]-Q_lam[a] != 0, |U_a| < r, where a = t_s, s = first differing coord.
# Usage: python3 -I tagU.py <setfile|bt163> [tagabovenorm]
import sys, random
exec(open("/tmp/oaimath/191b/seats/S_work/claim2.py").read().split("def main")[0])
S = sorted(load(sys.argv[1] if sys.argv[1] == "bt163" else "file:" + sys.argv[1]))
mut = sys.argv[2] if len(sys.argv) > 2 else "none"
tags, norm = S[:5], S[5:]
if mut == "tagabovenorm":
    tags = S[:4] + [S[6]]; norm = [x for x in S if x not in tags]
r = 37
rng = random.Random(20261022)
top = max(tags) + 1                      # degrees we need: 0..a <= max tag
normset = set(norm)
def digit(res): return r if res % r == 0 else res % r
def rows(lab, normres):
    A = [0] * top; Q = [0] * top
    for p in range(top):
        A[p] = 1 if p == 0 else (digit(normres[("A", p)]) if p in normset else r)
        if p in tags: Q[p] = digit(lab[tags.index(p)])
        elif p in normset: Q[p] = digit(normres[("Q", p)])
        else: Q[p] = r
    return A, Q
viol = 0; trials = 0; amax = 0
for _ in range(20000):
    # force every first-differing coordinate s in 0..4 equally often (uniform labels almost never reach s>=2)
    s0 = rng.randrange(5)
    lam = [rng.randrange(r) for _ in range(5)]; mu = lam[:s0] + [(lam[s0] + rng.randrange(1, r)) % r] + [rng.randrange(r) for _ in range(4 - s0)]
    # norm residues depend on the label: model as independent random values per label
    nl = {(t, p): rng.randrange(r) for t in "AQ" for p in range(top)}
    nm = {(t, p): rng.randrange(r) for t in "AQ" for p in range(top)}
    Al, Ql = rows(lam, nl); Am, Qm = rows(mu, nm)
    s = next(i for i in range(5) if lam[i] != mu[i]); a = tags[s]; amax = max(amax, a)
    U = [sum(Al[i] * Qm[j - i] - Am[i] * Ql[j - i] for i in range(j + 1)) for j in range(a + 1)]
    ok = all(U[j] == 0 for j in range(a)) and U[a] == Qm[a] - Ql[a] and U[a] != 0 and abs(U[a]) < r
    trials += 1; viol += (not ok)
seen_a = None
print(f"set={sys.argv[1]} mut={mut} tags={tags} first_norm={min(norm)} trials={trials} max a seen={amax} violations={viol}")
sys.exit(1 if viol else 0)
