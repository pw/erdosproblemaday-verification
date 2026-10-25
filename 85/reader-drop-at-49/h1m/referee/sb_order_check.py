#!/usr/bin/env python3
"""Referee (h1m), objection-hunt (d): are ALL symmetry-breaking constraints of h1mcell lex-leader constraints
X <=lex X o pi for ONE variable order (sorted(var), row-major) and ONE direction?

1. Transposition SB (h1cube2 lines 126-141, unchanged in h1mcell) is hand-written as row_i <=lex row_j over columns
   c not in {i,j}, c ascending, comparing (x(i,c), x(j,c)) with clause [-eq, -x(i,c), x(j,c)].
   add_perm_sb for the same transposition compares (X_p, X_{pi p}) for p in sorted(var) where they differ.
   We REBUILD both comparison sequences for every transposition of every case and check:
     (S_B = h1cube2 sequence) is a subsequence of (S_A = add_perm_sb sequence), with the same (u, w) orientation, and
     every element of S_A not in S_B is the REVERSAL (w, u) of an element (u, w) of S_B occurring EARLIER in S_A.
   Then the two lex predicates are identical (a reversed pair is equal whenever its earlier original is equal, so
   the first difference in S_A is an S_B element and is also the first difference in S_B).
2. Semantic cross-check on random assignments with long equal prefixes (both predicates evaluated directly).
3. Every pair perm used for a cell (stabiliser filter re-implemented here independently) and every edge-swap perm:
   maps blocks to blocks, preserves the pairing, E, the internal edge set, the free-variable set, and M.
   Plus: the stabiliser computed here (brute force over ALL 8! block permutations commuting with ^1 that preserve E
   and M) equals what h1mcell's filter keeps (re-run of its loop logic) -- reported per sampled cell.
"""
import itertools, random, sys
sys.path.insert(0, "/home/exedev/MathDyad/erdos85/fs")
import fsenc

k = 7; d, bs, nb = 6, 5, 8; N = 40
blk = [v // bs for v in range(N)]
blocks = [list(range(X * bs, (X + 1) * bs)) for X in range(nb)]
partner = lambda X: X ^ 1

def setup(j):
    E = []
    for p in range(4):
        E += [2, 2] if p < j else [2, 1]
    internal = set()
    for X in range(nb):
        for t in range(E[X]):
            internal.add((blocks[X][2 * t], blocks[X][2 * t + 1]))
    var = {}
    for a, b in itertools.combinations(range(N), 2):
        if blk[a] == blk[b] or blk[b] == partner(blk[a]):
            continue
        var[(a, b)] = len(var) + 1
    trans = []
    for X in range(nb):
        L = blocks[X]
        trans += [(L[2 * t], L[2 * t + 1]) for t in range(E[X])]
        trans += list(itertools.combinations(L[2 * E[X]:], 2))
    return E, internal, var, trans

def x(var, a, b):
    return var.get((min(a, b), max(a, b)))

def seq_h1cube2(var, i, jj):
    out = []
    for c in range(N):
        if c in (i, jj):
            continue
        a, b = x(var, i, c), x(var, jj, c)
        if a is None and b is None:
            continue
        assert a is not None and b is not None
        out.append((a, b))
    return out

def seq_addperm(var, pi):
    out = []
    for (a, b) in sorted(var):
        u, w = x(var, a, b), x(var, pi[a], pi[b])
        assert w is not None
        if u != w:
            out.append((u, w))
    return out

def lexle(assign, seq):
    for u, w in seq:
        if assign[u] != assign[w]:
            return assign[u] < assign[w]
    return True

def check_structural(SA, SB):
    pos = 0; seenB = set()
    for e in SA:
        if pos < len(SB) and e == SB[pos]:
            seenB.add(e); pos += 1
        elif (e[1], e[0]) in seenB:
            continue
        else:
            return False
    return pos == len(SB)

ok_all = True
rng = random.Random(1)
for j in range(5):
    E, internal, var, trans = setup(j)
    nv = len(var)
    bad = 0
    for i, jj in trans:
        pi = list(range(N)); pi[i], pi[jj] = jj, i
        SA, SB = seq_addperm(var, pi), seq_h1cube2(var, i, jj)
        if not check_structural(SA, SB):
            bad += 1
        # semantic: random assignments with forced long equal prefix along SB
        for _ in range(200):
            asg = [None] + [rng.randint(0, 1) for _ in range(nv)]
            L = rng.randint(0, len(SB))
            for u, w in SB[:L]:
                asg[w] = asg[u]
            if lexle(asg, SA) != lexle(asg, SB):
                bad += 1
    print(f"case j={j}: {len(trans)} transpositions, structural/semantic mismatches vs add_perm_sb order: {bad}")
    ok_all &= bad == 0
print("TRANSPOSITION SB == add_perm_sb lex-leader (same order, same direction):", ok_all)

# ---- negative controls: the check above must FAIL on a wrong order or a wrong direction ----
for name, mut in (("descending columns", lambda S: S[::-1]), ("flipped direction", lambda S: [(w, u) for u, w in S]),
                  ("odd-even column order", lambda S: S[1::2] + S[0::2])):
    E, internal, var, trans = setup(4)
    nv = len(var); bad = 0
    for i, jj in trans:
        pi = list(range(N)); pi[i], pi[jj] = jj, i
        SA, SB = seq_addperm(var, pi), mut(seq_h1cube2(var, i, jj))
        for _ in range(200):
            asg = [None] + [rng.randint(0, 1) for _ in range(nv)]
            if lexle(asg, SA) != lexle(asg, SB):
                bad += 1
    print(f"NEGATIVE CONTROL ({name}): semantic mismatches {bad} (must be > 0)")

# ---- step 3: every perm used by h1mcell for a cell preserves the cell; stabiliser filter re-derived ----
import importlib.util
PAIRS = [(X, Y) for X in range(8) for Y in range(X + 1, 8) if Y != X ^ 1]
def stab_bruteforce(E, MM):
    S = []
    for g in itertools.permutations(range(8)):
        if all(g[X ^ 1] == g[X] ^ 1 for X in range(8)) and all(E[g[X]] == E[X] for X in range(8)) \
           and all(MM[g[X]][g[Y]] == MM[X][Y] for X in range(8) for Y in range(8)):
            S.append(g)
    return S
def h1mcell_pairperms(E, MM):
    """re-run of h1mcell's loop (lines ~322-342) as a function"""
    full = [p for p in range(4) if E[2 * p] == E[2 * p + 1]]
    half = [p for p in range(4) if E[2 * p] != E[2 * p + 1]]
    out = []
    for pf in itertools.permutations(full):
        for flips in itertools.product((0, 1), repeat=len(full)):
            for ph in itertools.permutations(half):
                bmap = {}
                for src, dst, fl in zip(full, pf, flips):
                    bmap[2 * src] = 2 * dst + fl; bmap[2 * src + 1] = 2 * dst + (1 - fl)
                for src, dst in zip(half, ph):
                    bmap[2 * src] = 2 * dst; bmap[2 * src + 1] = 2 * dst + 1
                if all(bmap[X] == X for X in range(nb)):
                    continue
                if any(MM[bmap[X]][bmap[Y]] != MM[X][Y] for X in range(nb) for Y in range(nb)):
                    continue
                out.append(tuple(bmap[X] for X in range(8)))
    return out
def preserves(pi, E, internal, var, MM):
    # blocks -> blocks
    bmap = {}
    for v in range(N):
        if bmap.setdefault(blk[v], blk[pi[v]]) != blk[pi[v]]:
            return "block"
    if sorted(pi) != list(range(N)): return "not a perm"
    if any(bmap[X ^ 1] != bmap[X] ^ 1 for X in range(8)): return "pairing"
    if any(E[bmap[X]] != E[X] for X in range(8)): return "E"
    if {(min(pi[a], pi[b]), max(pi[a], pi[b])) for a, b in internal} != internal: return "internal"
    if {(min(pi[a], pi[b]), max(pi[a], pi[b])) for a, b in var} != set(var): return "freevars"
    if any(MM[bmap[X]][bmap[Y]] != MM[X][Y] for X in range(8) for Y in range(8)): return "M"
    return None
cls = [l.rstrip("\n").split("\t") for l in open("/home/exedev/MathDyad/erdos85/h1m/classes_all.tsv")]
rng2 = random.Random(7)
# sample: all cells with the largest stabilisers per case + random ones
bycase = {}
for r in cls: bycase.setdefault(int(r[0]), []).append(r)
probs = 0; nchk = 0
for j in range(5):
    E, internal, var, trans = setup(j)
    rows = sorted(bycase[j], key=lambda r: -int(r[3]))[:15] + rng2.sample(bycase[j], 25)
    for r in rows:
        flat = [int(t) for t in r[1].split(",")]
        MM = [[0] * 8 for _ in range(8)]
        for (X, Y), v in zip(PAIRS, flat): MM[X][Y] = MM[Y][X] = v
        S = stab_bruteforce(E, MM)
        H = h1mcell_pairperms(E, MM)
        if len(S) != int(r[3]) or set(H) != {g for g in S if g != tuple(range(8))}:
            probs += 1; print("STAB MISMATCH", j, r[1], len(S), r[3], len(H))
        perms = []
        for b in H:
            perms.append([b[blk[v]] * bs + (v - blk[v] * bs) for v in range(N)])
        for X in range(nb):
            if E[X] == 2:
                pi = list(range(N)); L = blocks[X]
                pi[L[0]], pi[L[2]], pi[L[1]], pi[L[3]] = L[2], L[0], L[3], L[1]
                perms.append(pi)
        for i, jj in trans:
            pi = list(range(N)); pi[i], pi[jj] = jj, i; perms.append(pi)
        for pi in perms:
            why = preserves(pi, E, internal, var, MM); nchk += 1
            if why: probs += 1; print("PERM DOES NOT PRESERVE CELL:", j, r[1], why)
print(f"step 3: {nchk} perms checked over 200 cells (incl. the 15 largest stabilisers per case): problems {probs}")
