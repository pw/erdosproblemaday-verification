# (c) exponent bookkeeping of Section 2, in base-A exponents (A = N^{2/d} = B^2; N = A^{d/2})
from sympy import Rational as R, symbols, binomial, limit, oo, factorial, simplify, floor
print("d | N=A^e  | N^2=A^e | N<=A^(d-1)? | A^(d/2)<=A^(d-2)? (local iso cap, needs d>=4) | s0=d(d-1)/2 | A^(d-1)=N^e | delta(H)/A^(d-1)")
for d in (3, 4, 5, 6):
    eN = R(d, 2)
    print(f"{d} | {eN}    | {2*eN}       | {eN <= d-1} ({eN}<= {d-1}) | {eN <= d-2} ({eN} <= {d-2}) | {R(d*(d-1),2)} | N^{R(2*(d-1),d)} | c3*N^2/(M*A^(d-1)) = c3*A^{d}/(M*A^{d-1}) = c3*A/M -> oo")
print()
print("Prop 2.2, l>=4 branch: fibres O(M^2) many, each bounded by f(d-l); total exponent 2+f vs d/2")
for d in range(3, 9):
    rows = []
    for l in range(1, d+1):
        u = d - l
        if u >= 3: f, why = R(u, 2), f"flat u={u}: C M^(u/2)"
        elif u == 2: f, why = R(1), "circle: 2M"
        else: f, why = R(0), "<=2 points"
        tot = 2 + f
        ok = tot <= R(d, 2)
        rows.append((l, u, why, tot, ok))
    for (l, u, why, tot, ok) in rows:
        tag = "(branch used)" if l >= 4 else "(branch NOT used: l<=3 handled separately)"
        print(f"  d={d} l={l} d-l={u}: fibre {why:22s} total M^{tot} vs M^{R(d,2)}: {'OK' if ok else 'FAILS'} {tag}")
print("  generic identity: 2+(d-l)/2 <= d/2  <=>  l >= 4 :", simplify((2+(symbols('d')-symbols('l'))/2 - symbols('d')/2)), "<= 0")
print()
print("Lemma 2.1 rows (M<=A=B^2): u=1: 2M<=2B^2; u=2: C M log 2M <= C B^2 log(2B^2) = B^{2+o(1)}; u>=3: C M^(u/2) <= C B^u")
for d in (3, 4, 5):
    worst = max(2, d-1)
    print(f"  d={d}: worst proper flat ~ B^{worst} (u={d-1} if >=3 else plane B^{{2+o(1)}}); N B^(-1/2) = B^{R(2*d-1,2)} -> c0=1/2 works: {worst < R(2*d-1,2)}")
print()
print("C(D+s0,s0) vs A^{s0} with D=floor(A): ratio C(D+s0,s0)/A^{s0}")
for d in (3, 4, 5):
    s0 = d*(d-1)//2
    vals = []
    for Aval in (10, 100, 1000, 10**5):
        D = Aval
        vals.append(float(binomial(D+s0, s0))/Aval**s0)
    print(f"  d={d} s0={s0}: A=10,100,1e3,1e5 -> {['%.4g'%v for v in vals]}  limit 1/s0! = {float(1/factorial(s0)):.4g}  (so C4 = 2^{s0}/s0! suffices for A>=s0)")
print()
print("Lemma 2.5 excess dimension: Z-space dim s0, neighbour flat codim d-1, hypersurface dim s0-1 => h = (s0-1)-(s0-d+1) = d-2 = r-1 with r=d-1")
for d in (3,4,5):
    s0 = d*(d-1)//2
    print(f"  d={d}: s0={s0}, neighbour flat dim {s0-(d-1)}, hypersurface dim {s0-1}, h={s0-1-(s0-(d-1))}, r-1={d-2}; bound C*deg*A^(d-2) summed over deg<=A: C*A^{d-1}")
print()
print("Global ambient: skew forms on C^(d+1) = (Z,c): dim s0+d = d(d+1)/2; Lemma 2.4 h ranges 0..d")
for d in (3,4,5):
    print(f"  d={d}: s0+d={d*(d-1)//2+d} = d(d+1)/2={d*(d+1)//2}; total params N^2=A^{d}, iso cap N=A^{R(d,2)} <= A^{d-1}")
print()
print("(2.4)-(2.5): edges 2*sum s_rho^2 >= 2|S|^2/(M-1) >= 2|S|^2/M; prune threshold E0/(2N^2) >= c2 N^2/(2M)")
print("d=3 deletion: sum C(k,2) <= (1/2) sum k^2 <= (K/2) N^4/A ; ratio to N^4/M = (K/2) M/A -> 0")
print("Chernoff: P(Bin < mean/2) <= exp(-mean/8); union over N^2 vertices: N^2 exp(-theta*delta(H)/8) <= N^2 exp(-theta*A^(d-1)/8) -> 0 since A^(d-1)=N^(2(d-1)/d) >> log N")
