#!/usr/bin/env python3
"""Referee (h1m) objection-hunt (c): ROW-LEVEL identification of classes_all.tsv with the authors' H1 inventory.
Authors (Lean, Erdos85OneHighV2CapacityInventory.lean + BranchDeficitSymmetry.lean):
  table T[s][t] = highBranchMissCount = #{a in branch s : N(a) cap branch t = empty}  (== our M[s][t])
  profile a: IE(a,i) = 1 if i even and i//2 < a else 2  -> their pairs 0..a-1 are (1,2) with the EVEN block e=1,
  pairs a..3 are (2,2).  capacity: T[c][j^1] + T[j][c^1] <= 5 over the 24 non-mate pairs (c<j).
Ours, case j = 4-a: pairs 0..j-1 are (2,2), pairs j..3 are (2,1) with the EVEN block e=2.
Relabelling phi (their block -> our block): their (1,2) pair p<a -> our pair j+p FLIPPED (2p -> 2(j+p)+1, 2p+1 -> 2(j+p));
their (2,2) pair p>=a -> our pair p-a unflipped.  phi preserves the pairing and maps their e-pattern onto ours.
Check: phi(their capacity-filtered rows) canonicalised under our case group == our class reps, as SETS, per case;
their 190 capacity-removed rows are exactly the raw orbits failing our M4."""
import itertools, collections
INV = "/tmp/erdos85-1019/repo/proofs/Proofs/Certificates/h1_orbit_inventory.compact"
H1M = "/home/exedev/MathDyad/erdos85/h1m"
PAIRS = [(X, Y) for X in range(8) for Y in range(X + 1, 8) if Y != X ^ 1]
def IE(a, i): return 1 if (i % 2 == 0 and i // 2 < a) else 2
def E_ours(j): return [2 if (p < j or s == 0) else 1 for p in range(4) for s in (0, 1)]
def tomat(flat):
    M = [[0] * 8 for _ in range(8)]
    for (X, Y), v in zip(PAIRS, flat): M[X][Y] = M[Y][X] = v
    return M
def act(g, flat):
    M = tomat(flat); Nn = [[0] * 8 for _ in range(8)]
    for X in range(8):
        for Y in range(8): Nn[g[X]][g[Y]] = M[X][Y]
    return tuple(Nn[X][Y] for X, Y in PAIRS)
rows = collections.defaultdict(list)
for line in open(INV):
    try: v = [int(t) for t in line.split()]
    except ValueError: continue
    if len(v) == 25 and 0 <= v[0] < 5: rows[v[0]].append(tuple(v[1:]))
ours = collections.defaultdict(set)
for l in open(f"{H1M}/classes_all.tsv"):
    f = l.split("\t"); ours[int(f[0])].add(tuple(map(int, f[1].split(","))))
allok = True
for a in range(5):
    j = 4 - a
    phi = [None] * 8
    for p in range(4):
        if p < a: phi[2 * p], phi[2 * p + 1] = 2 * (j + p) + 1, 2 * (j + p)
        else: phi[2 * p], phi[2 * p + 1] = 2 * (p - a), 2 * (p - a) + 1
    assert sorted(phi) == list(range(8)) and all(phi[X ^ 1] == phi[X] ^ 1 for X in range(8))
    assert all(IE(a, X) == E_ours(j)[phi[X]] for X in range(8))
    G = [g for g in itertools.permutations(range(8))
         if all(g[X ^ 1] == g[X] ^ 1 for X in range(8)) and all(E_ours(j)[g[X]] == E_ours(j)[X] for X in range(8))]
    cap = lambda T: all(tomat(T)[c][jj ^ 1] + tomat(T)[jj][c ^ 1] <= 5 for c, jj in PAIRS)        # THEIR form
    m4 = lambda M: all(tomat(M)[X ^ 1][Y] + tomat(M)[X][Y ^ 1] <= 5 for X, Y in PAIRS)           # OUR form
    kept, removed = [], []
    disagree = 0
    for T in rows[a]:
        mapped = act(phi, T)
        if cap(T) != m4(mapped): disagree += 1
        (kept if cap(T) else removed).append(min(act(g, mapped) for g in G))
    same = set(kept) == ours[j] and len(kept) == len(set(kept)) == len(ours[j])
    allok &= same and disagree == 0
    print(f"profile {a} -> case {j}: their rows {len(rows[a])}, capacity kept {len(kept)} removed {len(removed)}; "
          f"capacity==M4 on every row: {disagree == 0}; kept classes == our classes_all (as sets): {same}")
print("ROW-LEVEL MATCH" if allok else "MISMATCH")
