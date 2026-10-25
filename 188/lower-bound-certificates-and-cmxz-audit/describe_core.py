#!/usr/bin/env python3
"""Canonical description of a core: which points are Eisenstein integers (base lattice), which rotations
(centre, sign, d) carry genuinely rotated points, diameter, and an exact-coordinate listing."""
import sys, json, math, collections
import sympy as sp
c = json.load(open(sys.argv[1]))
pts = {int(k): v for k, v in c['points'].items()}; tags = {int(k): v for k, v in c['tags'].items()}
words = c['iso_words']; gd = c['gen_desc']
W = sp.Rational(-1,2) + sp.I*sp.sqrt(3)/2
def exact(i):
    gi, a, b = tags[i]
    z = a + b*W
    for h in words[gi][::-1]:   # apply rightmost (first) generator first
        cen, d, sign = gd[h]
        bb = round(cen[1]/math.sqrt(3)*2); aa = round(cen[0] + bb/2)
        cz = aa + bb*W
        dd = sp.sqrt(round(d*d))
        cth = 1 - 1/(2*dd**2); sth = sign*sp.sqrt(4*dd**2 - 1)/(2*dd**2)
        z = cz + (cth + sp.I*sth)*(z - cz)
    return sp.expand(z)
def is_eisenstein(z):
    # z in Z[w]  <=>  z = a + b w with integers: a = re + im/sqrt3, b = 2 im/sqrt3
    re, im = sp.re(z), sp.im(z)
    b = sp.nsimplify(2*im/sp.sqrt(3)); a = sp.nsimplify(re + im/sp.sqrt(3))
    return a.is_integer and b.is_integer, (a, b)
base = 0; rot = collections.Counter(); listing = []
for i in sorted(pts):
    z = exact(i); ok, ab = is_eisenstein(z)
    if ok:
        base += 1; listing.append((i, "lattice", ab))
    else:
        gi = tags[i][0]; h = words[gi][0]
        cen, d, sign = gd[h]
        key = (round(cen[0],3), round(cen[1],3), ("+" if sign>0 else "-")+f"theta_sqrt{round(d*d)}")
        rot[key] += 1; listing.append((i, "rotated", key, sp.simplify(z)))
print(f"points {len(pts)}: {base} Eisenstein integers + {len(pts)-base} rotated points from {len(rot)} rotations:")
for k, n in sorted(rot.items()):
    print("   ", k, n, "points")
used_d2 = sorted({round(gd[words[tags[i][0]][0]][1]**2) for i in pts if words[tags[i][0]]})
print("rotation angles actually used: d^2 in", used_d2, "-> e^{i theta_d} = (2d^2-1 + sqrt(1-4d^2))/(2d^2); real coordinates lie in Q(sqrt3, sqrt(4d^2-1))")
print("diameter from origin: %.4f" % max(math.hypot(*p) for p in pts.values()))
json.dump({"n": len(pts), "base_lattice_points": base, "rotations": [[list(k), n] for k, n in sorted(rot.items())],
           "listing": [[str(x) for x in row] for row in listing]}, open(sys.argv[1].replace('.core.json', '.core.describe.json'), 'w'), indent=0)
