# Independent exact scorer for Erdos #36 step-function witnesses.
# h = a_i/D on n equal cells of [0,2]; g = 1-h on [0,2], both zero outside.
# overlap at shift k cells = (2/(n D^2)) * sum_i a_i (D - a_{i+k}); affine between grid shifts.
import json, sys
from fractions import Fraction
def score(a, D):
    n = len(a)
    assert all(0 <= x <= D for x in a), "box"
    assert 2 * sum(a) == n * D, ("mass", sum(a), n * D // 2)
    b = (n * D * D).bit_length() + 2
    P = 0
    for i in reversed(range(n)):
        P = (P << b) | a[i]
    Q = 0
    for i in reversed(range(n)):
        Q = (Q << b) | (D - a[n - 1 - i])
    R = P * Q
    mask = (1 << b) - 1
    best, arg = -1, None
    m = 0
    while R:
        c = R & mask
        if c > best:
            best, arg = c, m
        R >>= b; m += 1
    # coefficient m: sum_{i} a_i (D - a_{n-1-(m-i)}) ; shift k = i' - i with i' = n-1-m+i => k = n-1-m
    k = n - 1 - arg
    # direct recheck of this shift
    direct = sum(a[i] * (D - a[i + k]) for i in range(n) if 0 <= i + k < n)
    assert direct == best, ("direct mismatch", direct, best)
    return Fraction(2 * best, n * D * D), k, best
if __name__ == "__main__":
    for path in sys.argv[1:]:
        d = json.load(open(path))
        if "heights_int" in d:
            a = [int(x) for x in d["heights_int"]]; D = int(d["D"])
        else:
            raise SystemExit("unknown format: " + ",".join(d.keys()))
        fr, k, best = score(a, D)
        print(path, "n", len(a), "D", D, "max shift k", k, "exact", fr.numerator, "/", fr.denominator, "=", "%.20f" % (fr.numerator / fr.denominator))
        print("   decimal 25dp:", (fr.numerator * 10**25) // fr.denominator)
