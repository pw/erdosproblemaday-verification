# Explicit congruence form of L_p: H_p cyclic of order e; pick generator g of H_p, 2=g^a, 3=g^b;
# then 2^k 3^l = g^(ak+bl), so L_p = {(k,l): a k + b l == 0 mod e} and cosets are a k + b l == c.
import math
from sympy import n_order
def lattice_form(p):
    a2, a3 = n_order(2, p), n_order(3, p); e = a2 * a3 // math.gcd(a2, a3)
    H = {pow(2, k, p) * pow(3, l, p) % p for k in range(a2) for l in range(a3)}
    assert len(H) == e
    for g in sorted(H):
        if n_order(g, p) == e:
            dl = {pow(g, i, p): i for i in range(e)}
            return e, g, dl[2], dl[3]
def verify(p, T):
    e, g, a, b = lattice_form(p)
    for k in range(T):
        for l in range(T):
            assert ((pow(2, k, p) * pow(3, l, p)) % p == 1) == ((a * k + b * l) % e == 0)
    return e, g, a, b
if __name__ == "__main__":
    for p in (5, 7, 11, 13, 17):
        e, g, a, b = verify(p, 48)
        print(f"p={p}: e_p={e}, generator g={g}, 2=g^{a}, 3=g^{b};  L_{p} = {{(k,l): {a}k + {b}l == 0 (mod {e})}}  [verified on 48x48 box]")
    # Prop 4: every pair of cosets of L_5, L_7 meets; intersection density 1/24.
    e5, _, a5, b5 = lattice_form(5); e7, _, a7, b7 = lattice_form(7)
    T = 12  # lcm(4,6): both coset systems are 12-periodic in k and l
    counts = {}
    for c5 in range(e5):
        for c7 in range(e7):
            cnt = sum(1 for k in range(T) for l in range(T)
                      if (a5*k + b5*l) % e5 == c5 and (a7*k + b7*l) % e7 == c7)
            counts[(c5, c7)] = cnt
    print("intersection counts on (Z/12)^2 for all 24 (c5,c7):", sorted(set(counts.values())), "out of", T*T,
          "-> density", f"{min(counts.values())}/{T*T}")
    # also directly from the definition (no parametrisation): cosets = fibres of (k,l) -> (2^k3^l mod 5, mod 7)
    fib = {}
    for k in range(T):
        for l in range(T):
            key = (pow(2,k,5)*pow(3,l,5)%5, pow(2,k,7)*pow(3,l,7)%7)
            fib[key] = fib.get(key, 0) + 1
    print("direct: #distinct (r5,r7) pairs hit =", len(fib), " sizes =", sorted(set(fib.values())))
