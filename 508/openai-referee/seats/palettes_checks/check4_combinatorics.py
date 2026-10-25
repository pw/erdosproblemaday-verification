# Check 4: the finite combinatorics of Section 6 (Theorem 6.5) and the four-cycle velocity formula.
#  (a) palette classifications used for triangles / four-cycles / five-cycles (all palettes of size 1..2 on 5 labels);
#  (b) five-cycle support-list contradiction (Sec 6.3.4) by brute force over all 31^6 list assignments
#      (via a compatibility-graph search).  CONTROL: drop the Lemma 6.7 step bans -> solutions must appear.
#  (c) V_H(a;b) = -H.Ja - (H.a) cot(arg b - arg a) for the first output angle of T_h (finite differences).
#      CONTROL: the sign-flipped formula.
#  (d) test (B): the same palette arithmetic with SIX labels (what breaks).
import itertools, numpy as np
L = range(5)
pal = [frozenset(p) for k in (1, 2) for p in itertools.combinations(L, k)]
def edges_of_cycle(cyc): return [frozenset((cyc[i], cyc[(i+1) % len(cyc)])) for i in range(len(cyc))]
def admissible(P, cyc): return not any(P <= e for e in edges_of_cycle(cyc))     # (6.2) for each cycle edge
ok = True
for cyc in itertools.permutations(L, 3):
    out = frozenset(L) - set(cyc)
    ok &= all(P & out for P in pal if admissible(P, cyc))
print("(a) triangle: every admissible palette (|P|<=2) meets the outside pair:", ok)
ok = True
for cyc in itertools.permutations(L, 4):
    X = (set(L) - set(cyc)).pop(); U = frozenset((cyc[0], cyc[2])); V = frozenset((cyc[1], cyc[3]))
    ok &= all((X in P) or P == U or P == V for P in pal if admissible(P, cyc))
print("    four-cycle: admissible palette contains X or is exactly a diagonal:", ok)
cyc = (0, 1, 2, 3, 4); D = [frozenset((i, (i+2) % 5)) for i in L]
print("    five-cycle: admissible palettes == the five diagonals:", set(P for P in pal if admissible(P, cyc)) == set(D))
print("    D_i ∩ D_j = ∅  <=>  j = i±1:", all((not (D[i] & D[j])) == ((j-i) % 5 in (1, 4)) for i in L for j in L if i != j))
print("    label outside D_i ∪ D_{i+1} is unique (= i+4):", all(set(L) - D[i] - D[(i+1) % 5] == {(i+4) % 5} for i in L))

# (b) five-cycle support lists.  Lists S^(r), r in Z/6, nonempty subsets of Z/5 (bitmasks 1..31).
subsets = list(range(1, 32))
mem = lambda m: [i for i in L if m >> i & 1]
def nbr_ok(A, B):            # every i in A has an adjacent index in B
    return all((B >> ((i+1) % 5) & 1) or (B >> ((i-1) % 5) & 1) for i in mem(A))
compat = {(A, B): (A & B) == 0 and nbr_ok(A, B) and nbr_ok(B, A) for A in subsets for B in subsets}
def diag_meet_empty(A):
    inter = set(L)
    for i in mem(A): inter &= D[i]
    return len(inter) == 0
def bans(A):                 # Lemma 6.7: i,i+1 both in the list => steps i<->i+1 banned everywhere
    return {frozenset((i, (i+1) % 5)) for i in L if (A >> i & 1) and (A >> ((i+1) % 5) & 1)}
def step_ok(j, banned):      # state j must have an unbanned step j -> j±1 (R maps state j into states j±1)
    return frozenset((j, (j+1) % 5)) not in banned or frozenset((j, (j-1) % 5)) not in banned
def solve(use_bans, bans_on="S0"):
    sols = []
    S0S3 = [(a, b) for a in subsets for b in subsets if diag_meet_empty(a) and diag_meet_empty(b)]
    for S0, S3 in S0S3:
        banned = bans(S0) | bans(S3) if use_bans else set()
        chk = [S0] if bans_on == "S0" else None
        if use_bans and not all(step_ok(j, banned) for j in mem(S0)): continue
        mids1 = [(S1, S2) for S1 in subsets for S2 in subsets if compat[S0, S1] and compat[S1, S2] and compat[S2, S3]]
        mids2 = [(S4, S5) for S4 in subsets for S5 in subsets if compat[S3, S4] and compat[S4, S5] and compat[S5, S0]]
        if mids1 and mids2: sols.append((mem(S0), mem(mids1[0][0]), mem(mids1[0][1]), mem(S3), mem(mids2[0][0]), mem(mids2[0][1])))
    return sols
s_paper = solve(True)
s_ctrl = solve(False)
print("(b) five-cycle lists with constraints of Sec 6.3.4 + Lemma 6.7 bans: #(S0,S3) admitting a full assignment =", len(s_paper))
print("    CONTROL without Lemma 6.7 bans: #(S0,S3) admitting a full assignment =", len(s_ctrl), "; example (S0..S5):", s_ctrl[0] if s_ctrl else None)

# (c) velocity of the first output angle of T_h(a,b): c+d = a+b-h
def first_output(alpha, beta, h):
    w = np.exp(1j*alpha) + np.exp(1j*beta) - h
    Th = np.angle(w); ac = np.arccos(np.abs(w)/2)
    c1, c2 = Th + ac, Th - ac           # pick the branch whose first output is near alpha
    cand = np.array([c1, c2]); k = np.argmin(np.abs(np.angle(np.exp(1j*(cand - alpha)))))
    return alpha + np.angle(np.exp(1j*(cand[k] - alpha)))
rng = np.random.default_rng(7); worst = 0; worst_c = 0
for _ in range(2000):
    al, be, ph = rng.uniform(0, 2*np.pi, 3)
    if abs(np.sin(be - al)) < 0.2: continue
    H = np.exp(1j*ph); a = np.exp(1j*al); b = np.exp(1j*be); Ja = 1j*a
    dot = lambda u, v: (u*np.conj(v)).real
    VH = -dot(H, Ja) - dot(H, a)/np.tan(be - al)
    eps = 1e-6
    num = (first_output(al, be, eps*H) - first_output(al, be, -eps*H))/(2*eps)
    worst = max(worst, abs(num - VH)); worst_c = max(worst_c, abs(num - (dot(H, Ja) + dot(H, a)/np.tan(be - al))))
print(f"(c) max |finite-difference velocity - V_H formula| = {worst:.2e};  CONTROL sign-flipped formula: {worst_c:.2f}")

# (d) test (B): six labels
L6 = range(6)
pal6 = [frozenset(p) for k in (1, 2, 3) for p in itertools.combinations(L6, k)]
tri = (0, 1, 2); out6 = frozenset(L6) - set(tri)
adm = [P for P in pal6 if not any(P <= e for e in edges_of_cycle(tri)) and len(P) <= 2]
print("(d) SIX labels: complement of a palette triple has size", 6-3, "(Prop 5.6 needs 2); triangle outside set has size", len(out6),
      "; admissible |P|<=2 palettes all meet ONE fixed pair?", any(all(P & frozenset(pr) for P in adm) for pr in itertools.combinations(out6, 2)))
