#!/usr/bin/env python3
"""Erdős #188 lower-bound apparatus.

Build a finite point set P in the plane = union of patches of the unit triangular lattice Z[w]
under a finite set of isometries (rotations about lattice points by angles that move a point at
distance d by exactly 1, i.e. 2 d sin(theta/2) = 1).  Emit a CNF:
    red_i  (true = red, false = blue)
    for every pair at unit distance:            (-red_i v -red_j)
    for every unit-spaced collinear k-run:      (red_1 v ... v red_k)
UNSAT  =>  every red/blue colouring of the plane with no red unit pair has a blue l_k
       =>  the #188 answer satisfies  k_188 >= k+1.
Screening uses double precision with a 1e-9 tolerance; soundness comes from exact re-verification
of the UNSAT core (verify_core.py), never from this file.
"""
import sys, math, itertools, argparse, json
import numpy as np
from scipy.spatial import cKDTree

SQ3 = math.sqrt(3.0)

def lattice_points(R):
    """Z[w] points within distance R of the origin: a + b*w, w = (-1+sqrt3 i)/2."""
    pts = []
    A = int(R*2)+2
    for a in range(-A, A+1):
        for b in range(-A, A+1):
            x = a - b/2.0; y = b*SQ3/2.0
            if x*x + y*y <= R*R + 1e-9:
                pts.append((x, y))
    return pts

def rot_angle(d):
    """rotation angle theta with 2 d sin(theta/2) = 1 (moves a point at distance d by exactly 1)."""
    return 2.0*math.asin(1.0/(2.0*d))

def apply(iso, p):
    c, s, tx, ty = iso
    x, y = p
    return (c*x - s*y + tx, s*x + c*y + ty)

def rotation_about(center, theta):
    c, s = math.cos(theta), math.sin(theta)
    cx, cy = center
    # z -> center + e^{i theta}(z - center)
    tx = cx - (c*cx - s*cy); ty = cy - (s*cx + c*cy)
    return (c, s, tx, ty)

def compose(g, h):
    """g o h"""
    c1, s1, t1x, t1y = g; c2, s2, t2x, t2y = h
    c = c1*c2 - s1*s2; s = s1*c2 + c1*s2
    tx = c1*t2x - s1*t2y + t1x; ty = s1*t2x + c1*t2y + t1y
    return (c, s, tx, ty)

def build(R, centers, ds, words=1, extra_isos=None, rot_radius=None):
    """Point set = union over isometries g (words of length <= `words` in the generators
    rotations about `centers` by +-theta_d, d in ds) of g(lattice patch of radius R)."""
    gens = []; gen_desc = []
    for cen in centers:
        for d in ds:
            th = rot_angle(d)
            gens.append(rotation_about(cen, th)); gen_desc.append((cen, d, +1))
            gens.append(rotation_about(cen, -th)); gen_desc.append((cen, d, -1))
    ident = (1.0, 0.0, 0.0, 0.0)
    isos = {ident}; words_of = {tuple(round(v, 9) for v in ident): []}
    frontier = [ident]
    for _ in range(words):
        new = []
        for g in frontier:
            gw = words_of[tuple(round(v, 9) for v in g)]
            for hi, h in enumerate(gens):
                k = compose(h, g)
                key = tuple(round(v, 9) for v in k)
                if key not in words_of:
                    isos.add(k); new.append(k); words_of[key] = [hi] + gw
        frontier = new
    build.gen_desc = gen_desc; build.words_of = words_of
    base = lattice_points_ab(R)
    pts = {}
    tags = {}
    for gi, g in enumerate(sorted(isos)):
        is_id = abs(g[0]-1) < 1e-12 and abs(g[1]) < 1e-12 and abs(g[2]) < 1e-12 and abs(g[3]) < 1e-12
        cen = None
        if rot_radius is not None and not is_id:
            # rotation centre = fixed point of g: solve (I - M) c = t
            c, s_, tx, ty = g
            det = (1-c)**2 + s_**2
            cen = (((1-c)*tx - s_*ty)/det, (s_*tx + (1-c)*ty)/det)
        for (a, b) in base:
            p = (a - b/2.0, b*SQ3/2.0)
            if cen is not None and (p[0]-cen[0])**2 + (p[1]-cen[1])**2 > rot_radius**2 + 1e-9:
                continue
            q = apply(g, p)
            key = (round(q[0], 7), round(q[1], 7))
            if key not in pts:
                pts[key] = q; tags[key] = (gi, a, b)
    P = list(pts.values())
    T = [tags[k] for k in pts.keys()]
    return P, T, sorted(isos)

def lattice_points_ab(R):
    out = []
    A = int(R*2)+2
    for a in range(-A, A+1):
        for b in range(-A, A+1):
            x = a - b/2.0; y = b*SQ3/2.0
            if x*x + y*y <= R*R + 1e-9:
                out.append((a, b))
    return out

def unit_pairs(P, tol=1e-9):
    arr = np.array(P)
    tree = cKDTree(arr)
    pairs = tree.query_pairs(1.0 + tol)
    out = []
    for i, j in pairs:
        d2 = ((arr[i]-arr[j])**2).sum()
        if abs(d2 - 1.0) < 2*tol:
            out.append((i, j))
    return out

def runs(P, pairs, k, tol=1e-9):
    """all collinear unit-spaced runs of length k: p, p+u, ..., p+(k-1)u with every point in P."""
    arr = np.array(P)
    index = {(round(x, 7), round(y, 7)): i for i, (x, y) in enumerate(P)}
    def find(q):
        return index.get((round(q[0], 7), round(q[1], 7)))
    out = set()
    for i, j in pairs:
        for a, b in ((i, j), (j, i)):
            u = arr[b] - arr[a]
            chain = [a, b]
            cur = arr[b]
            ok = True
            for _ in range(k-2):
                cur = cur + u
                t = find(cur)
                if t is None: ok = False; break
                # guard against rounding: exact-ish position check
                if abs(arr[t][0]-cur[0]) > tol or abs(arr[t][1]-cur[1]) > tol: ok = False; break
                chain.append(t)
            if ok:
                out.add(tuple(chain) if chain[0] < chain[-1] else tuple(reversed(chain)))
    return sorted(out)

def write_cnf(path, n, pairs, krun):
    with open(path, 'w') as f:
        f.write(f"p cnf {n} {len(pairs)+len(krun)}\n")
        for i, j in pairs:
            f.write(f"-{i+1} -{j+1} 0\n")
        for ch in krun:
            f.write(" ".join(str(v+1) for v in ch) + " 0\n")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=float, default=8)
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--ds", type=str, default="sqrt3,3,5", help="comma list; use sqrtN for sqrt(N)")
    ap.add_argument("--centers", type=float, default=0.0, help="use all lattice points within this radius as rotation centres")
    ap.add_argument("--words", type=int, default=1)
    ap.add_argument("--rot-radius", type=float, default=None, help="for rotated copies keep only lattice points within this distance of the rotation centre")
    ap.add_argument("--out", type=str, required=True)
    ap.add_argument("--origin-red", action="store_true", help="add the unit clause 'origin is red' (WLOG: a valid colouring has a red point; translate it to the origin)")
    ap.add_argument("--blue", type=str, default="", help="lattice coords a,b of a BASE-lattice point forced blue (WLOG by a rotation about the red origin when its theta_d partner is at unit distance; one such assumption only)")
    args = ap.parse_args()
    ds = []
    for t in args.ds.split(","):
        t = t.strip()
        if not t: continue
        ds.append(math.sqrt(float(t[4:])) if t.startswith("sqrt") else float(t))
    centers = lattice_points(args.centers) if args.centers > 0 else [(0.0, 0.0)]
    P, T, isos = build(args.R, centers, ds, words=args.words, rot_radius=args.rot_radius)
    pairs = unit_pairs(P)
    kr = runs(P, pairs, args.k)
    extra = []
    if args.origin_red:
        o = [i for i, p in enumerate(P) if abs(p[0]) < 1e-9 and abs(p[1]) < 1e-9]
        assert len(o) == 1, o
        extra = [(o[0],)]
    blue_idx = None
    if args.blue:
        a, b = (int(t) for t in args.blue.split(","))
        q = (a - b/2.0, b*SQ3/2.0)
        cand = [i for i, p in enumerate(P) if abs(p[0]-q[0]) < 1e-9 and abs(p[1]-q[1]) < 1e-9]
        assert len(cand) == 1, cand
        blue_idx = cand[0]
    with open(args.out + ".cnf", "w") as f:
        f.write(f"p cnf {len(P)} {len(pairs)+len(kr)+len(extra)+(1 if blue_idx is not None else 0)}\n")
        for i, j in pairs: f.write(f"-{i+1} -{j+1} 0\n")
        for ch in kr: f.write(" ".join(str(v+1) for v in ch) + " 0\n")
        for ch in extra: f.write(" ".join(str(v+1) for v in ch) + " 0\n")
        if blue_idx is not None: f.write(f"-{blue_idx+1} 0\n")
    json.dump({"R": args.R, "origin_red": args.origin_red, "blue": args.blue, "rot_radius": args.rot_radius, "k": args.k, "ds": ds, "centers": centers, "words": args.words,
               "n_points": len(P), "n_unit_pairs": len(pairs), "n_runs": len(kr),
               "isos": isos, "iso_words": [build.words_of[tuple(round(v, 9) for v in g)] for g in isos],
               "gen_desc": build.gen_desc, "points": P, "tags": T, "pairs": pairs, "runs": kr},
              open(args.out + ".json", "w"))
    print(f"points={len(P)} isometries={len(isos)} unit_pairs={len(pairs)} l{args.k}_runs={len(kr)} -> {args.out}.cnf")
