# Exhaustive check of Lemma outer:lll (finite asymmetric LLL) on random small
# product spaces of fair bits, exact Fraction arithmetic. For every instance whose
# z-weights satisfy (outer:lll-condition) for the "share a variable" dependency graph,
# verify the induction invariant (outer:conditional) for EVERY T subset of the family and
# every E not in T (this exercises the T1/T2 split and "independence from T_2"), hence
# P(intersection of complements) > 0.  Also checks the double-counting step
#   sum_{F in Gamma(E)} z_F <= |S(E)| * max_beta sum_{F uses beta} z_F.
# CONTROLS run through the SAME verifier with a mutant (too sparse) dependency graph.
import random, itertools, sys
from fractions import Fraction as Fr

def build(n, m, rng):
    outcomes = list(itertools.product((0,1), repeat=n))
    events = []
    for _ in range(m):
        s = sorted(rng.sample(range(n), rng.randint(1, min(4, n))))
        pats = list(itertools.product((0,1), repeat=len(s)))
        bad = set(rng.sample(pats, rng.randint(1, max(1, len(pats)//3))))
        events.append((s, frozenset(i for i,w in enumerate(outcomes) if tuple(w[j] for j in s) in bad)))
    return len(outcomes), events

def share_graph(events):
    m = len(events)
    return [[f for f in range(m) if f != e and set(events[e][0]) & set(events[f][0])] for e in range(m)]

def criterion(N, events, nb, z):
    for e in range(len(events)):
        prod = Fr(1)
        for f in nb[e]: prod *= (1 - z[f])
        if not Fr(len(events[e][1]), N) <= z[e]*prod: return False
    return True

def invariant(N, events, z):
    """returns None if (outer:conditional) holds for all T, else a witness"""
    m = len(events); allw = frozenset(range(N))
    for r in range(m+1):
        for T in itertools.combinations(range(m), r):
            A = allw
            for f in T: A = A - events[f][1]
            if not len(A) > 0: return ('P(A_T)=0', T)
            for e in range(m):
                if e in T: continue
                if not Fr(len(events[e][1] & A), len(A)) <= z[e]: return ('P(E|A_T)>z_E', T, e)
    return None

def choose_z(N, events, nb):
    for mult in (Fr(3,2), Fr(2), Fr(3)):
        z = [min(Fr(9,10), mult*Fr(len(ev[1]), N) + Fr(1,1000)) for ev in events]
        if criterion(N, events, nb, z): return z
    return None

def main():
    rng = random.Random(1)
    held = nocrit = 0
    for it in range(1500):
        N, events = build(rng.randint(3, 8), rng.randint(2, 6), rng)
        nb = share_graph(events)
        z = choose_z(N, events, nb)
        if z is None: nocrit += 1; continue
        w = invariant(N, events, z)
        if w is not None: print('LEMMA VIOLATION', w); return 1
        n = 1 + max(max(ev[0]) for ev in events)
        B = max(sum((z[f] for f in range(len(events)) if b in events[f][0]), Fr(0)) for b in range(n))
        for e in range(len(events)):
            if not sum((z[f] for f in nb[e]), Fr(0)) <= len(events[e][0])*B:
                print('DOUBLE-COUNT VIOLATION', e); return 1
        held += 1
    print(f'correct graph: {held} instances satisfied the criterion, invariant held in all; {nocrit} had no admissible z')
    # CONTROL A (must FAIL): same verifier, MUTANT graph with all edges deleted
    # (independence hypothesis of outer:lll is then false).
    rng = random.Random(2); fails = tried = 0; first = None
    for it in range(3000):
        N, events = build(rng.randint(2, 5), rng.randint(2, 6), rng)
        nb0 = [[] for _ in events]
        z = choose_z(N, events, nb0)
        if z is None: continue
        tried += 1
        w = invariant(N, events, z)
        if w is not None:
            fails += 1
            if first is None: first = (w, [(ev[0], sorted(ev[1])) for ev in events])
    print(f'CONTROL A (edgeless mutant graph): criterion held in {tried} instances, invariant/conclusion FAILED in {fails}')
    print('  first failing instance:', first)
    # CONTROL B (must FAIL): the textbook two-point example through the same verifier.
    events = [([0], frozenset([0])), ([0], frozenset([1]))]   # Omega={0,1}: E={0}, F={1}
    z = [Fr(3,5), Fr(3,5)]
    print('CONTROL B: mutant graph criterion', criterion(2, events, [[],[]], z),
          '| invariant witness', invariant(2, events, z),
          '| true graph criterion', criterion(2, events, share_graph(events), z))
    return 0
sys.exit(main())
