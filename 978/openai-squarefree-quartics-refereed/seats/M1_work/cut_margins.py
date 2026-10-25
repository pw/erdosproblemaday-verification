import cert_v2 as C
from fractions import Fraction as F
for d in range(4, 9):
    k = d-2
    H, Ha, Hb = C.H_polys(d)
    gv = [(t, C.ev(H,t), C.ev(Ha,t), C.ev(Hb,t)) for t in [F(i,50) for i in range(1,500)]]
    worst1 = worst2 = None
    z = C.K0
    while True:
        eL, eH = F(z, C.K0), F(z+1, C.K0)
        if eL*(1-k*eL/d) < C.STOP: break
        bH = d - k*eL
        fe, fb = float(eH), float(bH)
        t, Ht, Hat, Hbt = min(gv, key=lambda r: (fe+fb*float(r[0]))**d/float(r[1]))
        x = ((d+1)*(eH+bH*t)/d**2)**d / Ht
        r = C.iroot((x.numerator*100000**(d-1))//x.denominator, d-1)
        while F(r,100000)**(d-1) <= x: r += 1
        w = F(r, 100000)
        c1 = w**(d-1)*Ht / ((d+1)*(eH+bH*t)/d**2)**d - 1
        c2 = w**(d-2)*min(Hat,Hbt) / ((eH+bH*t)/(d-1))**(d-1) - 1
        if worst1 is None or c1 < worst1[0]: worst1 = (c1, z)
        if worst2 is None or c2 < worst2[0]: worst2 = (c2, z)
        z += 1
    print(f"d={d}: min(cut1 ratio-1)={float(worst1[0]):.3e} at z={worst1[1]}; min(cut2 ratio-1)={float(worst2[0]):.3e} at z={worst2[1]}")
