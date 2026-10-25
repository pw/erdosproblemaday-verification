from math import log
from fractions import Fraction as F
def e1(p): return 3+0.5*(4*log(p))/(log(27*p))          # Cor 1.4 via (1)
def e2(k,p):                                            # Cor 1.5 via (2)
    L=k*k/4; r=(k-1)**(L-1)*p
    return k-1+(L*log(p)/log(r))/(k-1)
print("Cor1.4: e(p)=3+2logp/(logp+log27)")
for p in [5,101,10**4+7,10**8+7,10**30]: print(f"  p={p:.3g} e={e1(p):.4f}")
for k in [4,6,8,10]:
    lim=k-1+ (k*k/4)/(k-1); lim2=k+(k-2)**2/(4*(k-1))
    L=k*k/4
    # threshold: L logp > (k-1)[(L-1)log(k-1)+logp]
    thr=(k-1)*(L-1)*log(k-1)/(L-(k-1))
    print(f"k={k}: limit {lim:.6f} == k+(k-2)^2/(4(k-1)) {lim2:.6f}; exceeds k iff log p > {thr:.3f} i.e. p > {2.718281828**thr:.4g}")
    for p in [k+1 if k+1 in (5,7,11) else 11, 10**6+3, 10**12+39, 10**40]:
        print(f"    p={p:.3g} e2={e2(k,p):.4f}")
print("DTZ local-lemma colouring r~M^(2/k) through (2): k-1+(k/2)/(k-1)")
for k in [4,6,8]: print(f"  k={k}: {k-1+(k/2)/(k-1):.4f}  vs k={k}")
print("k=4 Shi-Dong colouring (log_r M -> 4) reused for k-APs through (2): k-1+4/(k-1)")
for k in [4,6,8]: print(f"  k={k}: {k-1+4/(k-1):.4f}  vs k={k}")
print("Itabe 1/3 colouring (log_r M->3) via (1): 3+3/2 =",3+1.5," via (2) k=4:",3+3/3)
print("DTZ Z/22 3-colouring via (2): k-1+log_3(22)/(k-1):",[round(k-1+log(22)/log(3)/(k-1),4) for k in (4,6,8)])
print("Conditional: if beta_6=3 (DTZ conj beta_k=k/2), k=4 SD colouring via proof exponent k-1+log_rM/beta_k:",5+4/3)
