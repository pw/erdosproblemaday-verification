#!/usr/bin/env python3
"""Enumerate the block-level MISS MATRICES of H1 (k = 7), per e-pattern case j, up to the case's block group.
Derivation (label (a), see README.md here): for distinct non-paired blocks X, Y let M[X][Y] = #{z in X : z misses Y}.
Every z in X has <= 1 neighbour in Y and has one iff Y != mu(z), so the H-edges between X and Y form a matching of
size N[X][Y] = 5 - M[X][Y]. N is symmetric => M is symmetric. A matched z in X misses one block outside {X, X'}; an
unmatched z misses X itself => row sum of M over the non-paired others = #matched in X = 2 e(X).
Lemma D: q(X,Y) = N[X'][Y] + N[X][Y'] - 5 = 5 - M[X'][Y] - M[X][Y'] >= 0 for non-paired X != Y.
Blocks 0..7, pairs (0,1),(2,3),(4,5),(6,7). Case j: pairs 0..j-1 have e = (2,2), the rest (2,1).
Output: one line per class: 'j<TAB>flat upper-triangle entries of the canonical rep<TAB>orbit size<TAB>|stab|'."""
import itertools, sys

def case_E(j):
    E = []
    for p in range(4):
        E += [2, 2] if p < j else [2, 1]
    return E

def group(j):
    """block maps of the case group: permute (2,2) pairs with optional swap, permute (2,1) pairs (orientation fixed)."""
    E = case_E(j)
    full = [p for p in range(4) if E[2*p] == E[2*p+1]]
    half = [p for p in range(4) if E[2*p] != E[2*p+1]]
    G = []
    for pf in itertools.permutations(full):
        for flips in itertools.product((0, 1), repeat=len(full)):
            for ph in itertools.permutations(half):
                b = [None]*8
                for s, t, f in zip(full, pf, flips):
                    b[2*s] = 2*t + f; b[2*s+1] = 2*t + 1 - f
                for s, t in zip(half, ph):
                    b[2*s] = 2*t; b[2*s+1] = 2*t + 1
                assert all(E[b[X]] == E[X] for X in range(8)) and all(b[X ^ 1] == b[X] ^ 1 for X in range(8))
                G.append(tuple(b))
    assert len(set(G)) == len(G) == (2**len(full)) * len(list(itertools.permutations(full))) * len(list(itertools.permutations(half)))
    return G

PAIRS = [(X, Y) for X in range(8) for Y in range(X + 1, 8) if Y != X ^ 1]   # 24 free entries

def enum(j):
    E = case_E(j)
    R = [2 * e for e in E]
    out = []
    M = [[0]*8 for _ in range(8)]
    rem = R[:]
    def rec(i):
        if i == len(PAIRS):
            if any(rem):
                return
            for X, Y in PAIRS:   # Lemma D (both orientations of the unordered non-paired pair)
                if M[X ^ 1][Y] + M[X][Y ^ 1] > 5:
                    return
            out.append(tuple(M[X][Y] for X, Y in PAIRS))
            return
        X, Y = PAIRS[i]
        # remaining capacity check: X must be finishable using later entries of row X
        for v in range(min(rem[X], rem[Y]) + 1):
            M[X][Y] = M[Y][X] = v; rem[X] -= v; rem[Y] -= v
            # prune: when the last free entry of row X is passed, rem[X] must be 0
            ok = True
            for Z in (X,):
                later = [p for p in PAIRS[i+1:] if Z in p]
                if not later and rem[Z]:
                    ok = False
            if ok:
                rec(i + 1)
            M[X][Y] = M[Y][X] = 0; rem[X] += v; rem[Y] += v
    rec(0)
    return out

def act(b, flat):
    M = [[0]*8 for _ in range(8)]
    for (X, Y), v in zip(PAIRS, flat):
        M[X][Y] = M[Y][X] = v
    N = [[0]*8 for _ in range(8)]
    for X in range(8):
        for Y in range(8):
            N[b[X]][b[Y]] = M[X][Y]
    return tuple(N[X][Y] for X, Y in PAIRS)

if __name__ == "__main__":
    tot = 0
    for j in ([int(a) for a in sys.argv[1:]] or range(5)):
        G = group(j)
        allM = enum(j)
        S = set(allM)
        reps = {}
        seen = set()
        for m in allM:
            if m in seen:
                continue              # orbit already recorded (each orbit computed once)
            orb = {act(b, m) for b in G}
            assert orb <= S, "enumeration not closed under the group"
            seen |= orb
            c = min(orb)
            stab = sum(1 for b in G if act(b, c) == c)
            reps[c] = (len(orb), stab)
            assert len(orb) * stab == len(G)
        assert sum(o for o, s in reps.values()) == len(allM)
        print(f"# case j={j}: |G|={len(G)} matrices={len(allM)} classes={len(reps)}", file=sys.stderr)
        tot += len(reps)
        for c in sorted(reps):
            o, s = reps[c]
            print(f"{j}\t{','.join(map(str, c))}\t{o}\t{s}")
    print(f"# total classes {tot}", file=sys.stderr)
