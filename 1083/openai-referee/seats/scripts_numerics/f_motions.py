# (f) d=3 rich motions on a small grid P = {0..t-1}^3 (self-motions, both orientations).
# Lattice part: all 48 signed permutation matrices x integer translations (exhaustive for these S).
# Rational part (t<=4): rotations R(q)/|q|^2 from integer quaternions with |q|^2 <= QMAX, plus improper -S; deduplicated.
import numpy as np, itertools, math, sys
QMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 50
def signed_perms():
    out = []
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            M = np.zeros((3, 3), dtype=np.int64)
            for i in range(3): M[i, perm[i]] = signs[i]
            out.append((M, 1))
    return out
def quat_rot(a, b, c, d):
    n = a*a+b*b+c*c+d*d
    M = np.array([[a*a+b*b-c*c-d*d, 2*(b*c-a*d), 2*(b*d+a*c)],
                  [2*(b*c+a*d), a*a-b*b+c*c-d*d, 2*(c*d-a*b)],
                  [2*(b*d-a*c), 2*(c*d+a*b), a*a-b*b-c*c+d*d]], dtype=np.int64)
    g = math.gcd(n, *[int(x) for x in M.flatten()])
    return M//g, n//g
def rational_motions(qmax):
    seen = set(); out = []
    r = math.isqrt(qmax)
    for a, b, c, d in itertools.product(range(-r, r+1), repeat=4):
        n = a*a+b*b+c*c+d*d
        if n == 0 or n > qmax: continue
        M, m = quat_rot(a, b, c, d)
        if m == 1: continue
        for sgn in (1, -1):
            key = (m,) + tuple(int(x) for x in (sgn*M).flatten())
            if key not in seen:
                seen.add(key); out.append((sgn*M, m))
    return out
def match_counts(Pm, motions):
    ks = []
    for M, m in motions:
        img = Pm @ M.T
        H = (m*Pm[None, :, :] - img[:, None, :]).reshape(-1, 3)
        off = H.min(axis=0); span = H.max(axis=0) - off + 1
        key = ((H[:, 0]-off[0])*span[1] + (H[:, 1]-off[1]))*span[2] + (H[:, 2]-off[2])
        _, cnt = np.unique(key, return_counts=True)
        ks.append(cnt)
    return np.concatenate(ks)
lat = signed_perms()
for t in range(3, 8):
    Pm = np.array(list(itertools.product(range(t), repeat=3)), dtype=np.int64); N = len(Pm); A = N**(2/3)
    kl = match_counts(Pm, lat)
    line = f"t={t} N={N:3d} A={A:5.1f} N^(10/3)={N**(10/3):.3e} | lattice: max k={kl.max()}"
    for C in (1, 2):
        S = int((kl[kl >= C*A].astype(np.int64)**2).sum())
        line += f" | C_rich={C}: #motions={(kl>=C*A).sum()}, sum k^2={S}, /N^(10/3)={S/N**(10/3):.4f}"
    print(line)
    if t <= 4:
        q = QMAX if t == 3 else 30
        rat = rational_motions(q)
        kr = match_counts(Pm, rat)
        print(f"      + {len(rat)} rational-rotation motions (quaternion norm <= {q}): max k = {kr.max()}, #with k>=A: {(kr>=A).sum()}, #with k>=4: {(kr>=4).sum()}")
for t in (3, 4, 5, 6, 7):
    Pm = np.array(list(itertools.product(range(t), repeat=3)), dtype=np.int64); N = len(Pm)
    kl = match_counts(Pm, lat).astype(np.int64)
    tot = int((kl**2).sum())
    print(f"t={t}: sum over all lattice motions of k^2 = {tot};  /N^3 = {tot/N**3:.2f};  /N^(10/3) = {tot/N**(10/3):.4f}")
