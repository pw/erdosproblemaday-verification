"""Referee: setwise stabilizer of the q=11 witness(es) in PGL(3,11) by frame-image enumeration,
group identification, involution centres/axes, commuting criterion, projective equivalence of witnesses."""
import json, os, sys, itertools, time
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rpg
p = 11
HERE = os.path.dirname(os.path.abspath(__file__)); RUNS = os.path.join(HERE, '..', 'runs')
pts, idx, lines, inc = rpg.plane(p)
W = json.load(open(os.path.join(RUNS, 'witnesses_q11_c4.json')))
extra = {k: json.load(open(os.path.join(RUNS, f'witness_q11_c4_{k}.json'))) for k in ('orbit_perm', 'orbit_singer7')}
sets = {k: [rpg.norm(P, p) for P in v] for k, v in list(W.items()) + list(extra.items())}

# ---- negative controls on the checker: deleting a point must create an empty line; adding one must create a 5-line or change spectrum
S0 = [idx[P] for P in sets['cadical']]
for k in range(3):
    sp = rpg.spectrum(S0[:k] + S0[k + 1:], inc); assert 0 in sp, sp
others = [i for i in range(len(pts)) if i not in S0]
sp = rpg.spectrum(S0 + [others[0]], inc); assert sp != rpg.spectrum(S0, inc)
print("checker negative controls: delete-a-point gives an empty line (x3); add-a-point changes spectrum: OK")

def find_frame(Sv):
    for quad in itertools.combinations(Sv, 4):
        if rpg.general_position(list(quad), p): return list(quad)

def maps_between(Sa, Sb):
    """all projectivities g with g(Sa) = Sb (as sets)"""
    F = find_frame(Sa); Sbset = set(Sb); out = []
    for quad in itertools.permutations(Sb, 4):
        if not rpg.general_position(list(quad), p): continue
        g = rpg.proj_from_frames(F, list(quad), p)
        if all(rpg.norm(rpg.matvec(g, P, p), p) in Sbset for P in Sa):
            out.append(g)
    return out

t = time.time()
S = sets['cadical']
G = maps_between(S, S)
print(f"stabilizer of cadical witness: order {len(G)}  ({time.time()-t:.1f}s; frame enumeration over ordered 4-tuples of S)")
I = rpg.mnorm(((1,0,0),(0,1,0),(0,0,1)), p)
Gs = set(G); assert I in Gs and len(Gs) == len(G)
mul = lambda a, b: rpg.mnorm(rpg.matmul(a, b, p), p)
# closure
assert all(mul(a, b) in Gs for a in G for b in G), "not closed"
inverse = {g: rpg.mnorm(rpg.inv(g, p), p) for g in G}
assert all(inverse[g] in Gs for g in G)
def order(g):
    k, h = 1, g
    while h != I: h = mul(h, g); k += 1
    return k
ords = {g: order(g) for g in G}
print("element-order census:", dict(sorted(Counter(ords.values()).items())))
# conjugacy classes
seen = set(); classes = []
for g in G:
    if g in seen: continue
    cl = {mul(mul(h, g), inverse[h]) for h in G}; seen |= cl; classes.append(cl)
print("classes (size, order):", sorted((len(c), ords[next(iter(c))]) for c in classes))
def gen_closure(gens):
    H = {I}; frontier = [I]
    while frontier:
        new = []
        for a in frontier:
            for b in gens:
                c = mul(a, b)
                if c not in H: H.add(c); new.append(c)
        frontier = new
    return H
nc = [len(gen_closure(list(c))) for c in classes if I not in c]
print("normal closures of the nontrivial classes:", nc, "-> simple:", all(n == len(G) for n in nc))
# derived subgroup (perfectness) as an independent check
comms = {mul(mul(a, b), mul(inverse[a], inverse[b])) for a in G for b in G}
print("derived subgroup order:", len(gen_closure(list(comms))))
# Sylow-7 count
syl7 = {frozenset(gen_closure([g])) for g in G if ords[g] == 7}
print("number of Sylow 7-subgroups:", len(syl7))

# ---- involutions: fixed points, centre, axis
Sset = set(S)
invs = [g for g in G if ords[g] == 2]
info = {}
for g in invs:
    fixed = [P for P in pts if rpg.norm(rpg.matvec(g, P, p), p) == P]
    fixidx = {idx[P] for P in fixed}
    axes = [li for li, l in enumerate(inc) if l <= fixidx]
    assert len(fixed) == p + 2 and len(axes) == 1, (len(fixed), axes)
    ax = axes[0]
    centre = [P for P in fixed if idx[P] not in inc[ax]]
    assert len(centre) == 1
    info[g] = (centre[0], ax)
centres = [info[g][0] for g in invs]
print(f"involutions: {len(invs)}; each fixes exactly {p+2} points = one line pointwise + one isolated point (homology)")
print("distinct centres:", len(set(centres)), " centres == S:", set(centres) == Sset)
S_idx = {idx[P] for P in S}
four = sorted(li for li, l in enumerate(inc) if len(l & S_idx) == 4)
three = sorted(li for li, l in enumerate(inc) if len(l & S_idx) == 3)
axes = sorted(info[g][1] for g in invs)
print("axes distinct:", len(set(axes)), " axes == the 4-secants:", axes == four)
print("centre on its own axis for some involution:", any(idx[info[g][0]] in inc[info[g][1]] for g in invs))
bad = 0; inc_count = 0
for s_, t_ in itertools.permutations(invs, 2):
    on = idx[info[s_][0]] in inc[info[t_][1]]
    comm = mul(s_, t_) == mul(t_, s_)
    inc_count += on
    bad += (on != comm)
print(f"centre(s) in axis(t) <=> st=ts over {len(invs)*(len(invs)-1)} ordered pairs: mismatches={bad}; incidences={inc_count}")
# 3-secants: every pair of S on exactly one 3- or 4-secant?
pair_cover = Counter()
for li in three + four:
    for a, b in itertools.combinations(sorted(inc[li] & S_idx), 2): pair_cover[(a, b)] += 1
print("pairs of S covered by 3/4-secants:", len(pair_cover), "of", 21 * 20 // 2, " max multiplicity", max(pair_cover.values()))
# orbits of G on S, on the 3-secants, on 4-secants
def img_line(g, li):
    # image of a line = set image of its points
    return frozenset(idx[rpg.norm(rpg.matvec(g, pts[i], p), p)] for i in inc[li])
line_of = {l: li for li, l in enumerate(inc)}
orb3 = {line_of[img_line(g, three[0])] for g in G}; orb4 = {line_of[img_line(g, four[0])] for g in G}
orbS = {rpg.norm(rpg.matvec(g, S[0], p), p) for g in G}
print(f"G-orbit sizes: on S {len(orbS)}, on 3-secants {len(orb3)} (of {len(three)}), on 4-secants {len(orb4)} (of {len(four)})")

# ---- projective equivalence of every witness with the cadical one
for k, T in sets.items():
    if k == 'cadical': continue
    t = time.time(); m = maps_between(S, T)
    print(f"projectivities cadical -> {k}: {len(m)}  ({time.time()-t:.1f}s)")
json.dump({'G': [list(map(list, g)) for g in G]}, open(os.path.join(HERE, 'stabilizer_q11.json'), 'w'))
