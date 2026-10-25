# exact bookkeeping for the coordinator's proposed parameter choice (seat G's sharpened pair bound + a better packing)
from fractions import Fraction as F
def best_u(k):
    # pair term exponent in powers of B (B ~ r^6): 20.5k + 0.5 + gamma/6 - 1.5u must be < 0 for every gamma<1
    # u integer: need 1.5u >= 20.5k + 0.5 + 1/6 (sup over gamma<1), i.e. 3u > 41k + 1 + 1/3  -> 3u >= 41k + 2
    u = -(-(41*k + 2) // 3)
    return u
for name, k in [("Blinov packing (Erdos-Turan base-3 set)", 408781), ("our product set", 356155), ("Wroblewski Theorem-216 set", 275385)]:
    u = best_u(k)
    assert 3*u >= 41*k + 2 and 3*(u-1) < 41*k + 1 + F(1,3)        # u-1 fails for gamma near 1
    beta = F(20*k + 3*u + 1, 2)                                    # sqrt(N^3/tau) ~ B^beta,  N = h q B^u, q ~ h^6, tau ~ B^(k-1)
    X = 6*beta                                                     # n_r ~ r^(gamma + X)
    assert X == 60*k + 9*u + 3
    gamma = F(X, X+1); eta = 2*gamma/(gamma + X); assert eta == F(2, X+2)
    pair_exp_B = F(41,2)*k + F(1,2) + gamma/6 - F(3,2)*u           # B-exponent of the first deletion term
    print(f"{name}: k={k} u={u} N=h*q*B^u  X={X}  eta=2/{X+2} = {float(eta):.5e}  pair-term B-exponent={float(pair_exp_B):.4f}  sup 2/(183k+8)=2/{183*k+8}")
print("Chen 2/100866719 =", 2/100866719)
