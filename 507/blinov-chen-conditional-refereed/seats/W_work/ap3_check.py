"""Seat W: reconstruct and check a 2,921-element 3-AP-free set in [1, 137693]
from Wroblewski's 'Theorem N' (N=216, P=3889) + a(14)=36, and compare with the
binary-digit ternary set Blinov uses ([0, 204390]).

Reads (as data only) the m(216) and a(14) witnesses copied from
raw/oeis/jwr_DATABASE.TXT.  Writes witness files next to this script.
Run: python3 -I ap3_check.py raw/oeis/jwr_DATABASE.TXT
"""
import sys, re


def is_3ap_free(S):
    """True iff no x<y<z in S with x+z=2y (integers)."""
    s = sorted(set(S))
    if len(s) != len(S):
        raise ValueError("duplicates")
    ss = set(s)
    n = len(s)
    for i in range(n):
        x = s[i]
        for j in range(i + 1, n):
            z = s[j]
            t = x + z
            if t % 2 == 0 and (t // 2) in ss:
                return False, (x, t // 2, z)
    return True, None


def is_3ap_free_mod(K, P):
    """True iff no x,y,z in K, not all equal, with x+z = 2y mod P (P odd)."""
    Ks = set(k % P for k in K)
    L = sorted(Ks)
    for x in L:
        for z in L:
            if x == z:
                continue  # x=z forces y=x when P is odd
            y2 = (x + z) % P
            y = (y2 * pow(2, -1, P)) % P
            if y in Ks:
                return False, (x, y, z)
    return True, None


def main():
    db = open(sys.argv[1]).read()
    m = re.search(r"^m\(216\)<=3889 ([0-9 ]+)\(", db, re.M)
    K = [int(t) for t in m.group(1).split()]
    a14 = [int(t) for t in re.search(r"^a\(14\)=36 ([0-9 ]+)\(", db, re.M).group(1).split()]
    P = 3889
    print("m(216) witness size", len(K), "max", max(K), "| a(14) witness", a14)
    assert len(K) == 216 and len(a14) == 14 and max(a14) == 36
    print("P prime:", all(P % d for d in range(2, int(P ** 0.5) + 1)))
    ok, w = is_3ap_free_mod(K, P); print("K 3-AP-free mod 3889:", ok, w)
    ok14, w14 = is_3ap_free(a14); print("a(14) set 3-AP-free:", ok14, w14)
    # Is K the subgroup of 18th powers (216th roots of unity)?
    print("K == {x: x^216 = 1 mod P}:", set(K) == {x for x in range(1, P) if pow(x, 216, P) == 1})
    # Theorem N: a(N(q-1)+r) <= P(a(q)-1) + k_r over affine images c*K+d (mod P, reps in 1..P).
    N, n_target = 216, 2921
    q = (n_target - 1) // N + 1
    r = n_target - N * (q - 1)
    print("q =", q, "r =", r)
    best = None
    # multiplying a subgroup by c only permutes cosets; 18 coset reps suffice
    g = next(x for x in range(2, P) if all(pow(x, (P - 1) // p, P) != 1 for p in (2, 3)))
    reps = [pow(g, i, P) for i in range(18)]
    for c in reps:
        cK = [(c * k) % P for k in K]
        for d in range(P):
            T = sorted(((x + d) % P) or P for x in cK)
            kr = T[r - 1]
            if best is None or kr < best[0]:
                best = (kr, c, d, T)
    kr, c, d, T = best
    bound = P * (max(a14) - 1) + kr
    print("best k_r =", kr, "via c =", c, "d =", d, "-> bound a(2921) <=", bound)
    blocks = sorted(a14)
    A = [P * (b - 1) + t for b in blocks[:-1] for t in T] + [P * (blocks[-1] - 1) + t for t in T[:r]]
    print("constructed |A| =", len(A), "min", min(A), "max", max(A))
    okA, wA = is_3ap_free(A); print("A 3-AP-free:", okA, wA)
    open("witness_2921_in_1_137693.txt", "w").write(" ".join(map(str, sorted(A))) + "\n")
    # ternary {0,1}-digit set, first 2921 elements
    tern = [int(bin(i)[2:], 3) for i in range(2921)]
    okT, wT = is_3ap_free(tern); print("ternary first 2921: max", max(tern), "3-AP-free:", okT, wT)
    # ----- negative controls (each must be REJECTED) -----
    print("NEG1 {1,2,3}:", is_3ap_free([1, 2, 3])[0] is False)
    Kbad = K[:-1] + [(2 * K[1] - K[0]) % P] if (2 * K[1] - K[0]) % P not in K else K
    print("NEG2 K with x,y,2y-x mod P:", is_3ap_free_mod(Kbad, P)[0] is False)
    Abad = sorted(A); x, y = Abad[0], Abad[1]; Abad = Abad[:-1] + [2 * y - x] if (2 * y - x) not in A else Abad
    print("NEG3 A with an AP completion:", is_3ap_free(Abad)[0] is False)
    T2 = sorted(((x + 1) % P) or P for x in range(216))  # an interval: not 3-AP-free mod P
    print("NEG4 interval as modular set:", is_3ap_free_mod(T2, P)[0] is False)
    tern_bad = tern[:-1] + [2 * tern[5] - tern[3]] if (2 * tern[5] - tern[3]) not in tern else tern
    print("NEG5 ternary with AP completion:", is_3ap_free(tern_bad)[0] is False)


if __name__ == "__main__":
    main()
