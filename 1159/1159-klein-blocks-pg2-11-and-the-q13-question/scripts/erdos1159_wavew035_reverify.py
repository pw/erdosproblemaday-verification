#!/usr/bin/env python3
"""
Independent finite-field/projective-plane checker for the Erdős #1159 report.

No solver or third-party package is used.  The script:
  * implements the finite fields used below from polynomial quotients;
  * checks the projective-plane incidence axioms directly;
  * checks every displayed blocking-set witness and its secant histogram;
  * checks the elementary discriminant obstructions to C <= 2 and, for q >= 5,
    C <= 3;
  * checks the Bruen--Fisher cubic construction in PG(2,9) and PG(2,27).
"""

from collections import Counter
from itertools import combinations, product
from math import comb


class FiniteField:
    """F_p[x]/(modulus), with elements encoded as base-p coefficient vectors."""

    def __init__(self, p, modulus):
        self.p = p
        self.modulus = tuple(c % p for c in modulus)
        self.degree = len(self.modulus) - 1
        assert self.degree >= 1
        assert self.modulus[-1] == 1
        assert self._irreducible(), (p, modulus)
        self.q = p**self.degree
        # A direct sanity check, independent of the irreducibility test.
        for a in range(1, self.q):
            assert self.mul(a, self.pow(a, self.q - 2)) == 1

    def coeffs(self, a):
        out = []
        for _ in range(self.degree):
            out.append(a % self.p)
            a //= self.p
        return out

    def encode(self, coeffs):
        ans = 0
        place = 1
        for c in coeffs[: self.degree]:
            ans += (c % self.p) * place
            place *= self.p
        return ans

    def add(self, a, b):
        return self.encode(
            [(x + y) % self.p for x, y in zip(self.coeffs(a), self.coeffs(b))]
        )

    def neg(self, a):
        return self.encode([(-x) % self.p for x in self.coeffs(a)])

    def sub(self, a, b):
        return self.add(a, self.neg(b))

    def mul(self, a, b):
        aa, bb = self.coeffs(a), self.coeffs(b)
        tmp = [0] * (2 * self.degree - 1)
        for i, x in enumerate(aa):
            for j, y in enumerate(bb):
                tmp[i + j] = (tmp[i + j] + x * y) % self.p
        # The modulus is monic, so x^d = -sum_{j<d} modulus[j] x^j.
        for k in range(len(tmp) - 1, self.degree - 1, -1):
            c = tmp[k] % self.p
            if c:
                for j in range(self.degree):
                    tmp[k - self.degree + j] = (
                        tmp[k - self.degree + j] - c * self.modulus[j]
                    ) % self.p
        return self.encode(tmp)

    def pow(self, a, exponent):
        ans = 1
        while exponent:
            if exponent & 1:
                ans = self.mul(ans, a)
            a = self.mul(a, a)
            exponent >>= 1
        return ans

    def inv(self, a):
        assert a != 0
        ans = self.pow(a, self.q - 2)
        assert self.mul(a, ans) == 1
        return ans

    @staticmethod
    def _poly_remainder(f, g, p):
        f = [x % p for x in f]
        while len(f) >= len(g):
            c = f[-1]  # g is monic
            shift = len(f) - len(g)
            if c:
                for j, x in enumerate(g):
                    f[shift + j] = (f[shift + j] - c * x) % p
            while f and f[-1] == 0:
                f.pop()
        return f

    def _irreducible(self):
        # A reducible degree-d polynomial has a monic factor of degree <= d/2.
        d = self.degree
        for e in range(1, d // 2 + 1):
            for low_coeffs in product(range(self.p), repeat=e):
                divisor = list(low_coeffs) + [1]
                if not self._poly_remainder(self.modulus, divisor, self.p):
                    return False
        return True


def prime_field(p):
    return FiniteField(p, [0, 1])


def normalize(field, vector):
    for c in vector:
        if c:
            scale = field.inv(c)
            return tuple(field.mul(x, scale) for x in vector)
    raise AssertionError("zero vector has no projective normalization")


def projective_points(field):
    q = field.q
    return (
        [(1, a, b) for a in range(q) for b in range(q)]
        + [(0, 1, a) for a in range(q)]
        + [(0, 0, 1)]
    )


def dot(field, u, v):
    ans = 0
    for x, y in zip(u, v):
        ans = field.add(ans, field.mul(x, y))
    return ans


def incidence(field):
    points = projective_points(field)
    # The same canonical triples parameterize the lines ax+by+cz=0.
    rows = [
        tuple(i for i, point in enumerate(points) if dot(field, point, line) == 0)
        for line in points
    ]
    return points, rows


def verify_plane(field):
    points, rows = incidence(field)
    q = field.q
    v = q * q + q + 1
    assert len(points) == len(set(points)) == v
    assert len(rows) == v
    assert all(len(row) == q + 1 for row in rows)
    assert all(sum(p in row for row in rows) == q + 1 for p in range(v))

    # Every point-pair is on exactly one line.  Since dot product is symmetric
    # and points/lines use the same index set, this also checks the dual axiom.
    seen = set()
    for row in rows:
        for i, j in combinations(row, 2):
            key = i * v + j
            assert key not in seen
            seen.add(key)
    assert len(seen) == comb(v, 2)
    return points, rows


def verify_witness(field, witness, expected_histogram, label):
    points, rows = verify_plane(field)
    point_index = {point: i for i, point in enumerate(points)}
    assert len(witness) == len(set(witness))
    assert all(point in point_index for point in witness)
    selected = {point_index[point] for point in witness}
    intersections = [sum(i in selected for i in row) for row in rows]
    histogram = dict(sorted(Counter(intersections).items()))
    assert histogram == expected_histogram, (label, histogram)
    assert min(intersections) >= 1

    # Three independent global counts: lines, incidences, and selected pairs.
    q = field.q
    assert sum(histogram.values()) == q * q + q + 1
    assert sum(i * n for i, n in histogram.items()) == len(witness) * (q + 1)
    assert sum(comb(i, 2) * n for i, n in histogram.items()) == comb(
        len(witness), 2
    )
    print(
        f"{label}: q={q}, |S|={len(witness)}, "
        f"max={max(intersections)}, histogram={histogram}"
    )


def bruen_fisher_witness(field):
    """A={(x,x^3)}, B={(x,t*x^3)}, plus the vertical point at infinity."""
    q = field.q
    assert field.p == 3 and field.degree >= 2
    t = next(
        a for a in range(1, q) if field.pow(a, (q - 1) // 2) != 1
    )
    assert field.pow(t, (q - 1) // 2) == field.neg(1)
    witness = set()
    for x in range(q):
        x3 = field.pow(x, 3)
        witness.add(normalize(field, (x, x3, 1)))
        witness.add(normalize(field, (x, field.mul(t, x3), 1)))
    witness.add((0, 1, 0))
    assert len(witness) == 2 * q
    return sorted(witness)


def verify_symbolic_obstructions():
    # If all line intersections are 1 or 2, double counting yields
    # s^2-(2q+3)s+2(q^2+q+1)=0, whose discriminant is below.
    for q in range(2, 1000):
        discriminant_c2 = -4 * q * q + 4 * q + 1
        assert discriminant_c2 < 0

    # If all line intersections are 1,2,3, then
    # n_2 = -s^2+(3q+4)s-3(q^2+q+1).  For q>=5 this
    # concave quadratic has negative discriminant, hence n_2<0.
    for q in range(5, 1000):
        discriminant_c3 = -3 * q * q + 12 * q + 4
        assert discriminant_c3 < 0
    # Direct integer cross-check across all possible |S| for many small q
    # (the preceding discriminant check is the uniform proof).
    for q in range(5, 50):
        for s in range(q * q + q + 2):
            n2 = -s * s + (3 * q + 4) * s - 3 * (q * q + q + 1)
            assert n2 < 0
    print("symbolic obstructions: C>=3 for q>=2; C>=4 for q>=5")


def main():
    verify_symbolic_obstructions()

    witnesses = [
        (
            prime_field(2),
            [(1, 0, 0), (1, 1, 0), (0, 1, 0)],
            {1: 6, 3: 1},
            "PG(2,2) line",
        ),
        (
            prime_field(3),
            [
                (1, 0, 0),
                (1, 0, 2),
                (1, 1, 0),
                (1, 1, 2),
                (1, 2, 1),
                (0, 1, 0),
            ],
            {1: 6, 2: 3, 3: 4},
            "PG(2,3)",
        ),
        (
            FiniteField(2, [1, 1, 1]),  # x^2+x+1
            [
                (1, 0, 0),
                (1, 0, 1),
                (1, 1, 0),
                (1, 1, 1),
                (0, 1, 0),
                (0, 1, 1),
                (0, 0, 1),
            ],
            {1: 14, 3: 7},
            "PG(2,4) Baer subplane PG(2,2)",
        ),
        (
            prime_field(5),
            [
                (1, 0, 0),
                (1, 0, 2),
                (1, 0, 3),
                (1, 0, 4),
                (1, 1, 3),
                (1, 2, 4),
                (1, 3, 0),
                (1, 4, 0),
                (0, 1, 0),
            ],
            {1: 18, 2: 6, 3: 4, 4: 3},
            "PG(2,5)",
        ),
        (
            prime_field(7),
            [
                (0, 1, 0),
                (1, 0, 0),
                (1, 0, 3),
                (1, 0, 4),
                (1, 0, 6),
                (1, 1, 1),
                (1, 1, 3),
                (1, 1, 4),
                (1, 1, 5),
                (1, 2, 2),
                (1, 2, 3),
                (1, 2, 4),
                (1, 2, 6),
                (1, 3, 1),
                (1, 4, 1),
                (1, 5, 0),
                (1, 6, 0),
            ],
            {1: 20, 2: 10, 3: 12, 4: 15},
            "PG(2,7)",
        ),
        (
            prime_field(11),
            [
                (0, 0, 1),
                (1, 0, 6),
                (1, 0, 7),
                (1, 0, 9),
                (1, 0, 10),
                (1, 1, 4),
                (1, 1, 6),
                (1, 1, 7),
                (1, 1, 8),
                (1, 2, 1),
                (1, 2, 4),
                (1, 2, 6),
                (1, 2, 7),
                (1, 3, 2),
                (1, 3, 8),
                (1, 4, 3),
                (1, 4, 4),
                (1, 5, 5),
                (1, 6, 3),
                (1, 7, 0),
                (1, 7, 7),
                (1, 8, 7),
                (1, 8, 9),
                (1, 9, 3),
                (1, 9, 6),
                (1, 10, 3),
                (1, 10, 6),
                (1, 10, 10),
            ],
            {1: 40, 2: 31, 3: 31, 4: 14, 5: 17},
            "PG(2,11) upper-bound witness",
        ),
    ]
    for args in witnesses:
        verify_witness(*args)

    gf9 = FiniteField(3, [1, 0, 1])  # x^2+1
    verify_witness(
        gf9,
        bruen_fisher_witness(gf9),
        {1: 50, 2: 9, 3: 16, 4: 16},
        "Bruen--Fisher cubic construction in PG(2,9)",
    )

    gf27 = FiniteField(3, [1, 2, 0, 1])  # x^3+2x+1
    verify_witness(
        gf27,
        bruen_fisher_witness(gf27),
        {1: 470, 2: 27, 3: 52, 4: 208},
        "Bruen--Fisher cubic construction in PG(2,27)",
    )
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
