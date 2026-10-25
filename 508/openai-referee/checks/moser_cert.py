#!/usr/bin/env python3
"""Independent exact check of the paper's seven-point certificate (Lemma 8.9): the placed Moser spindle z_g = ((35+12i)/37)·(g + (−290+149i)/250),
g ∈ G = {0, A, B, T, uA, uB, uT}, A = (√3+i)/2, B = (√3−i)/2, T = √3, u = (5+i√11)/6 (eq. 8.5–8.6).
Checks, all in exact algebra over Q(√3, √11) via sympy: (1) |u| = 1 and the multiplier (35+12i)/37 has modulus 1; (2) the eleven
drawn edges 0A,0B,AB,AT,BT, (rotated copies) 0uA,0uB,uAuB,uAuT,uBuT, and T–uT all have squared length exactly 1 and the placement
preserves them; (3) every vertex satisfies 0 < l < 4 and P < P' of (8.4) with l = ξ²+υ², P = υ²(3ξ²−υ²)², P' = l³(1−l/4)(l−1)²
(decided exactly by sympy's real algebraic comparison, and reported numerically at 50 digits); (4) CONTROLS: the points z = i/2 and z = 1 (outside the region) and
a non-unit edge are rejected. Exit 0 iff all certificate checks pass AND the control fails."""
import sympy as sp
s3, s11, I = sp.sqrt(3), sp.sqrt(11), sp.I
A=(s3+I)/2; B=(s3-I)/2; T=s3; u=(5+I*s11)/6
G={'0':sp.Integer(0),'A':A,'B':B,'T':T,'uA':u*A,'uB':u*B,'uT':u*T}
mult=(35+12*I)/37; shift=(-290+149*I)/250
def n2(z): z=sp.expand(z); return sp.simplify(sp.re(z)**2+sp.im(z)**2)
ok=True
print("|u|^2 =", n2(u), " |mult|^2 =", n2(mult)); ok &= (n2(u)==1 and n2(mult)==1)
edges=[('0','A'),('0','B'),('A','B'),('A','T'),('B','T'),('0','uA'),('0','uB'),('uA','uB'),('uA','uT'),('uB','uT'),('T','uT')]
Z={g:sp.expand(mult*(G[g]+shift)) for g in G}   # (8.6): z_g = ((35+12i)/37)·(g + (−290+149i)/250) — shift INSIDE, read from the rendered PDF p.57 (pdftotext had flattened the parentheses)
for a,b in edges:
    d0=n2(G[a]-G[b]); d1=n2(Z[a]-Z[b]); print(f"edge {a}-{b}: |g-h|^2 = {d0}, placed |z-w|^2 = {d1}"); ok &= (d0==1 and d1==1)
def region(z):
    xi,up=sp.re(z),sp.im(z); l=sp.expand(xi**2+up**2); P=sp.expand(up**2*(3*xi**2-up**2)**2); Pp=sp.expand(l**3*(1-l/4)*(l-1)**2)
    c1=sp.simplify(l)>0; c2=sp.simplify(l-4)<0; c3=sp.simplify(Pp-P)>0   # exact real-algebraic comparisons
    return bool(c1),bool(c2),bool(c3),sp.N(xi,20),sp.N(up,20),sp.N(l,20),sp.N(P,20),sp.N(Pp,20)
for g in G:
    c1,c2,c3,xi,up,l,P,Pp=region(Z[g]); print(f"vertex {g:>2}: xi={xi} up={up} l={l} 0<l:{c1} l<4:{c2} P={P} P'={Pp} P<P':{c3}"); ok &= (c1 and c2 and c3)
# controls
c=region(sp.I/2); print("CONTROL z = i/2 (P = 1/64 > P' = 27/3276.8):", c[:3], "-> expected a False:", not all(c[:3])); ctrl1 = not all(c[:3])
c=region(sp.Integer(1)); print("CONTROL z = 1 (radius one, P' = 0):", c[:3], "-> expected a False:", not all(c[:3])); ctrl1 = ctrl1 and not all(c[:3])
c=region(Z['uT']+sp.Rational(1,2)); print("NOTE uT shifted by +1/2 stays inside:", c[:3], "(not a control)")
bad_edge = n2(Z['0']-Z['T']); print("CONTROL non-edge 0-T squared length:", bad_edge, "-> expected ≠ 1:", bad_edge!=1); ctrl2 = (bad_edge!=1)
# CONTROL (the trap in the text extraction): the LITERAL reading of pdftotext's flattened (8.6), rotate·g + shift (the prose on p. 57 also says
# "a rotation followed by a translation"), must put vertices OUTSIDE the region — it does, at 0, uB and uT — while Table 1 and the rendered
# formula (translate, then rotate) put every vertex inside. This is the run that first failed on 2026-10-14 before the PDF page was read.
Zlit={g:sp.expand(mult*G[g]+shift) for g in G}; outside=[g for g in G if not all(region(Zlit[g])[:3])]
print("CONTROL literal rotate·g+shift reading: vertices outside the region =", outside, "-> expected non-empty:", bool(outside))
ctrl3 = bool(outside)
print("CERTIFICATE", "PASS" if ok else "FAIL", "| CONTROLS", "FAIL-AS-EXPECTED" if (ctrl1 and ctrl2) else "DID NOT FAIL")
raise SystemExit(0 if (ok and ctrl1 and ctrl2 and ctrl3) else 1)
