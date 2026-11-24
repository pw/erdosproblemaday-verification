"""Independent exact Erdos 1034 certificate verifier; standard library only."""

import argparse
import gzip
import json
import math
import os
import sys
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, permutations, product
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


class Q:
    """a + b*sqrt(3), with rational coordinates and the positive embedding."""

    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a = a if isinstance(a, Fraction) else Fraction(a)
        self.b = b if isinstance(b, Fraction) else Fraction(b)

    def __add__(self, other):
        other = other if isinstance(other, Q) else Q(other)
        return Q(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return Q(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-other if isinstance(other, Q) else -Q(other))

    def __mul__(self, other):
        if not isinstance(other, Q):
            return Q(self.a * other, self.b * other)
        return Q(self.a * other.a + 3 * self.b * other.b,
                 self.a * other.b + self.b * other.a)

    __rmul__ = __mul__

    def __truediv__(self, other):
        if not isinstance(other, Q):
            return Q(self.a / other, self.b / other)
        norm = other.a * other.a - 3 * other.b * other.b
        return Q((self.a * other.a - 3 * self.b * other.b) / norm,
                 (self.b * other.a - self.a * other.b) / norm)

    def __bool__(self):
        return bool(self.a or self.b)

    def __eq__(self, other):
        other = other if isinstance(other, Q) else Q(other)
        return self.a == other.a and self.b == other.b

    def sign(self):
        # Clear positive denominators; opposite signs are decided by squares.
        a = self.a.numerator * self.b.denominator
        b = self.b.numerator * self.a.denominator
        return sign_pair(a, b)

    def __str__(self):
        return "(%s) + (%s)*sqrt(3)" % (self.a, self.b)


def sign_pair(a, b):
    if not a:
        return (b > 0) - (b < 0)
    if not b or (a > 0) == (b > 0):
        return (a > 0) - (a < 0)
    difference = a * a - 3 * b * b
    return ((difference > 0) - (difference < 0)) * ((a > 0) - (a < 0))


def exact_number(pair):
    require(isinstance(pair, list) and len(pair) == 2
            and all(isinstance(x, str) for x in pair), "Invalid exact field element")
    return Q(*pair)


def check_psd(matrix):
    """Exact symmetric elimination: each positive pivot is an LDL pivot.

    A zero pivot must have an entirely zero remaining column. The Schur
    complement is then equivalent by congruence to the original matrix.
    No stored PSD report or numerical eigenvalue is used.
    """
    n = len(matrix)
    require(all(len(row) == n for row in matrix), "Nonsquare matrix")
    require(all(matrix[i][j] == matrix[j][i] for i in range(n) for j in range(i)),
            "Nonsymmetric matrix")
    work = [row[:] for row in matrix]
    for k in range(n):
        pivot = work[k][k]
        require(pivot.sign() >= 0, "Negative LDL pivot at coordinate %d" % k)
        if not pivot:
            require(all(not work[i][k] for i in range(k + 1, n)),
                    "Zero LDL pivot with nonzero column at coordinate %d" % k)
            continue
        ratios = {i: work[i][k] / pivot for i in range(k + 1, n) if work[i][k]}
        for i in ratios:
            for j in ratios:
                if j <= i:
                    work[i][j] = work[i][j] - work[i][k] * ratios[j]


def _check_psd_block(item):
    index, matrix = item
    try:
        check_psd(matrix)
    except ValueError as error:
        raise ValueError("PSD block %d: %s" % (index, error)) from error
    return index


def check_psd_blocks(matrices, workers=1):
    """Run the same exact elimination serially or in separate processes."""
    require(type(workers) is int and workers > 0,
            "Worker count must be a positive integer")
    items = list(enumerate(matrices))
    if workers == 1 or len(items) <= 1:
        for completed, item in enumerate(items, 1):
            _check_psd_block(item)
            if completed % 8 == 0:
                print("PSD progress: %d/%d" % (completed, len(items)), flush=True)
    else:
        with ProcessPoolExecutor(max_workers=min(workers, len(items))) as executor:
            for completed, _ in enumerate(executor.map(_check_psd_block, items), 1):
                if completed % 8 == 0:
                    print("PSD progress: %d/%d" % (completed, len(items)), flush=True)


@lru_cache(None)
def pairs(n):
    return tuple(combinations(range(n), 2))


def adjacency(n, mask):
    require(type(mask) is int and 0 <= mask < (1 << (n * (n - 1) // 2)),
            "Invalid graph bitmask")
    rows = [0] * n
    for bit, (i, j) in enumerate(pairs(n)):
        if (mask >> bit) & 1:
            rows[i] |= 1 << j
            rows[j] |= 1 << i
    return tuple(rows)


def induced(rows, vertices):
    result = 0
    for bit, (i, j) in enumerate(pairs(len(vertices))):
        if (rows[vertices[i]] >> vertices[j]) & 1:
            result |= 1 << bit
    return result


@lru_cache(None)
def canonical(n, k, mask):
    """Only unlabelled vertices move; root labels remain fixed."""
    if n - k <= 1:
        return mask
    rows = adjacency(n, mask)
    roots = tuple(range(k))
    return min(induced(rows, roots + free) for free in permutations(range(k, n)))


def allocations(vertices, sizes):
    """Ordered, disjoint, uniformly chosen subsets, allowing unused vertices."""
    if not sizes:
        yield ()
        return
    for subset in combinations(vertices, sizes[0]):
        remaining = tuple(v for v in vertices if v not in subset)
        for tail in allocations(remaining, sizes[1:]):
            yield (subset,) + tail


@lru_cache(None)
def root_samples(n, k):
    return tuple((roots, tuple(v for v in range(n) if v not in roots))
                 for roots in permutations(range(n), k))


@lru_cache(None)
def subset_samples(free_count, sizes):
    return tuple(allocations(tuple(range(free_count)), sizes))


def check_graph_basis(n, masks):
    """Check distinct isomorphism classes and completeness by orbit sizes.

    Degrees restrict the permutations considered without changing the result.
    Distinct classes whose labelled orbit sizes sum to 2^(n choose 2) exhaust
    all graphs; no external graph enumeration or table is needed.
    """
    seen, labelled_count = set(), 0
    for mask in masks:
        rows = adjacency(n, mask)
        cells = defaultdict(list)
        for v, row in enumerate(rows):
            cells[bin(row).count("1")].append(v)
        cells = [cells[d] for d in sorted(cells)]
        best, automorphisms = None, 0
        for parts in product(*(permutations(cell) for cell in cells)):
            vertices = tuple(v for part in parts for v in part)
            candidate = induced(rows, vertices)
            if best is None or candidate < best:
                best, automorphisms = candidate, 1
            elif candidate == best:
                automorphisms += 1
        require(best not in seen, "Duplicate graph isomorphism class")
        seen.add(best)
        require(math.factorial(n) % automorphisms == 0, "Invalid graph orbit size")
        labelled_count += math.factorial(n) // automorphisms
    require(labelled_count == 1 << (n * (n - 1) // 2), "Graph basis is incomplete")


def polynomial(n, sigma, terms):
    k, type_mask = sigma
    coefficients = defaultdict(Fraction)
    for mask, coefficient in terms:
        rows = adjacency(n, mask)
        require(induced(rows, tuple(range(k))) == type_mask, "Flag does not match its type")
        require(isinstance(coefficient, str), "Flag coefficient must be an exact rational string")
        coefficients[canonical(n, k, mask)] += Fraction(coefficient)
    return {mask: q for mask, q in coefficients.items() if q}


def quadratic_weights(block, matrix):
    """Expand v^T Q v symbolically in raw flags, before graph sampling."""
    basis = [polynomial(block["flag_order"], block["type"], terms)
             for terms in block["basis"]]
    weights = defaultdict(Q)
    for i, left in enumerate(basis):
        for j in range(i + 1):
            q = matrix[i][j] * (1 if i == j else 2)
            if q:
                for a, ca in left.items():
                    for b, cb in basis[j].items():
                        weights[tuple(sorted((a, b)))] += q * (ca * cb)
    # Sampling below merges the two ordered events (a,b) and (b,a).
    # For distinct flags each event has half the merged probability.
    return {key: q / (1 if key[0] == key[1] else 2)
            for key, q in weights.items() if q}


class Model:
    def __init__(self, model, matrices, scalars):
        require(model["format_version"] == 1 and model["target_order"] == 7,
                "Expected the order-7 model, format version 1")
        require(model["field"] == {"radicand": 3, "embedding": "positive"},
                "Expected Q(sqrt(3)) with the positive embedding")
        require(len(model["matrix_blocks"]) == len(matrices) == 82, "Expected 82 matrix blocks")
        require(len(model["scalar_generators"]) == len(scalars) == 819, "Expected 819 scalars")
        require(len(model["graph_slack_flags"]) == 1044, "Expected 1044 graph descriptors")
        descriptors = model["scalar_generators"]
        require(descriptors[816:] == [["bollobas"], ["constant", "1"], ["constant", "-1"]],
                "Wrong mapping of scalar coordinates 816, 817, 818")
        definitions = model["definitions"]
        self.n = model["target_order"]
        self.masks = model["graph_slack_flags"]
        self.tau = definitions["triangle_type"]
        require(self.tau == [3, 7], "Expected the fully labelled triangle type")
        self.c = exact_number(definitions["c_star"])
        require(self.c == Q("6/11", "-5/66"), "Unexpected c_star for the fixed certificate")
        require(Fraction(model["target_bound"]) == Fraction(1, 4), "Unexpected target bound")
        require(scalars[817] - scalars[818] == -Q(model["target_bound"]),
                "Split constant coordinates do not give minus the target bound")
        require(definitions["D"]["flag_order"] == 4, "Expected a one-vertex triangle localizer")
        self.D = polynomial(4, self.tau, definitions["D"]["terms"])
        # Independently confirm D is exactly the event of >=2 triangle neighbours.
        for neighbours in range(8):
            rows = list(adjacency(3, 7)) + [0]
            for root in range(3):
                if (neighbours >> root) & 1:
                    rows[root] |= 1 << 3
                    rows[3] |= 1 << root
            mask = induced(rows, (0, 1, 2, 3))
            require(self.D.get(mask, 0) == int(bin(neighbours).count("1") >= 2),
                    "D is not the stated triangle-neighbour indicator")
        self.rho = definitions["rho"]
        require(self.rho == {"flag": [2, 1], "coefficient": "1/2"}, "Unexpected objective rho")
        self.bollobas = definitions["bollobas"]
        # This fixes the precise nonnegative Bollobas polynomial being invoked,
        # not its expansion. All its densities are reconstructed below.
        require(self.bollobas == {
            "type": [4, 62], "sector_roots": [0, 1],
            "indicators": {"X": [1, 0], "E": [2, 1], "T": [3, 3], "P3": [3, 2]},
            "terms": [["1", ["X", "X", "X"]], ["-11", ["X", "E"]],
                      ["30", ["T"]], ["15", ["P3"]]]
        }, "Unexpected rooted Bollobas definition")
        self.groups = defaultdict(dict)
        self.local = defaultdict(Q)
        for index, (block, matrix) in enumerate(zip(model["matrix_blocks"], matrices)):
            require(len(block["basis"]) == len(matrix), "Matrix/basis dimension mismatch at block %d" % index)
            k, sigma = block["type"]
            n = block["flag_order"]
            adjacency(k, sigma)
            weights = quadratic_weights(block, matrix)
            if block["kind"] == "triangle_localizer_psd":
                require(index == 0 and block["type"] == self.tau and n == 4,
                        "Unsupported localizer block descriptor")
                for key, value in weights.items():
                    self.local[key] += value
            else:
                require(block["kind"] == "flag_psd" and k in (1, 3, 5) and 2 * n - k == 7,
                        "Unsupported flag PSD descriptor")
                group = self.groups[k].setdefault(sigma, {"order": n, "weights": defaultdict(Q)})
                require(group["order"] == n, "Inconsistent flag orders for one type")
                for key, value in weights.items():
                    group["weights"][key] += value
        require(model["matrix_blocks"][0]["kind"] == "triangle_localizer_psd",
                "Missing triangle localizer PSD block")
        self.scalar_flags = {}
        for descriptor, multiplier in zip(descriptors[:816], scalars[:816]):
            require(len(descriptor) == 3 and descriptor[:2] == ["P_flag", 6],
                    "Unsupported scalar localizer descriptor")
            mask = next(iter(polynomial(6, self.tau, [[descriptor[2], "1"]])))
            require(mask not in self.scalar_flags, "Duplicate scalar flag descriptor")
            self.scalar_flags[mask] = multiplier
        self.beta = scalars[816]
        self.constant = scalars[817] - scalars[818]

    def P(self, mask):
        return self.c - self.D.get(mask, 0)

    def flag_quadratics(self, rows):
        result = Q()
        for k, groups in self.groups.items():
            counts = defaultdict(Counter)
            for roots, free in root_samples(self.n, k):
                sigma = induced(rows, roots)
                if sigma not in groups:
                    continue
                n = groups[sigma]["order"]
                for left, right in subset_samples(len(free), (n - k, n - k)):
                    a = canonical(n, k, induced(rows, roots + tuple(free[i] for i in left)))
                    b = canonical(n, k, induced(rows, roots + tuple(free[i] for i in right)))
                    counts[sigma][tuple(sorted((a, b)))] += 1
            for sigma, count in counts.items():
                group = groups[sigma]
                denominator = len(root_samples(self.n, k)) * len(subset_samples(self.n - k,
                                  (group["order"] - k,) * 2))
                result += sum((group["weights"].get(key, Q()) * multiplicity
                               for key, multiplicity in count.items()), Q()) / denominator
        return result

    def localizers(self, rows):
        quadratic, scalar = Counter(), Counter()
        for roots, free in root_samples(self.n, 3):
            if induced(rows, roots) != self.tau[1]:
                continue
            vertex_flags = {v: induced(rows, roots + (v,)) for v in free}
            for left, right, extra in permutations(free, 3):
                a, b = sorted((vertex_flags[left], vertex_flags[right]))
                quadratic[a, b, vertex_flags[extra]] += 1
            for extra in free:
                others = tuple(v for v in free if v != extra)
                mask = canonical(6, 3, induced(rows, roots + others))
                scalar[mask, vertex_flags[extra]] += 1
        root_count = len(root_samples(self.n, 3))
        q_den = root_count * len(subset_samples(self.n - 3, (1, 1, 1)))
        s_den = root_count * len(subset_samples(self.n - 3, (1, 3)))
        q = sum((self.local.get((a, b), Q()) * self.P(p) * count
                 for (a, b, p), count in quadratic.items()), Q()) / q_den
        s = sum((self.scalar_flags.get(mask, Q()) * self.P(p) * count
                 for (mask, p), count in scalar.items()), Q()) / s_den
        return q + s

    def bollobas_density(self, rows):
        definition = self.bollobas
        k, sigma = definition["type"]
        terms = []
        for coefficient, factors in definition["terms"]:
            indicators = [definition["indicators"][name] for name in factors]
            samples = subset_samples(self.n - k, tuple(f for f, _ in indicators))
            terms.append((Fraction(coefficient), indicators, samples))
        counts = [0] * len(terms)
        for roots, free in root_samples(self.n, k):
            if induced(rows, roots) != sigma:
                continue
            for t, (_, indicators, samples) in enumerate(terms):
                for subsets in samples:
                    valid = True
                    for subset, (_, edges) in zip(subsets, indicators):
                        vertices = tuple(free[i] for i in subset)
                        in_B = all((rows[v] >> roots[r]) & 1 for v in vertices
                                   for r in definition["sector_roots"])
                        edge_count = sum((rows[a] >> b) & 1 for a, b in combinations(vertices, 2))
                        if not in_B or edge_count != edges:
                            valid = False
                            break
                    counts[t] += int(valid)
        root_count = len(root_samples(self.n, k))
        return sum((coefficient * Fraction(count, root_count * len(samples))
                    for count, (coefficient, _, samples) in zip(counts, terms)), Fraction())

    def objective(self, rows):
        n, mask = self.rho["flag"]
        count = sum(canonical(n, 0, induced(rows, subset)) == canonical(n, 0, mask)
                    for subset in combinations(range(self.n), n))
        return Fraction(self.rho["coefficient"]) * Fraction(count, math.comb(self.n, n))

    def residual(self, mask, slack):
        rows = adjacency(self.n, mask)
        return (self.objective(rows) + self.flag_quadratics(rows) + self.localizers(rows)
                + self.beta * self.bollobas_density(rows) + self.constant + slack)


def read_json(path):
    def reject_float(value):
        raise ValueError("Floating-point JSON values are forbidden: " + value)

    raw = Path(path).read_bytes()
    if str(path).endswith(".gz"):
        raw = gzip.decompress(raw)
    return json.loads(raw, parse_float=reject_float, parse_constant=reject_float)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", help="neutral exact witness, certificate.json.gz")
    parser.add_argument("model", help="verification_model.json")
    parser.add_argument("--workers", type=int, default=min(8, os.cpu_count() or 1),
                        help="exact PSD worker processes (default: up to 8; 1 for serial)")
    args = parser.parse_args()
    require(args.workers > 0, "Worker count must be a positive integer")
    witness, model = read_json(args.certificate), read_json(args.model)
    require(set(witness) == {"format_version", "source_sha256", "matrices",
                             "graph_slacks", "scalar_multipliers"}, "Unexpected neutral witness fields")
    require(witness["format_version"] == 1, "Unsupported neutral witness version")
    require(witness["source_sha256"] == model["certificate_sha256"] ==
            "541baf0f1bf03c803c268a65c9bf008127bd5839b3a4103f1cdba75f7a5933dc",
            "Wrong fixed certificate provenance")
    matrices = [[[exact_number(x) for x in row] for row in matrix] for matrix in witness["matrices"]]
    scalars = [exact_number(x) for x in witness["scalar_multipliers"]]
    slacks = [exact_number(x) for x in witness["graph_slacks"]]
    require(len(slacks) == 1044, "Expected 1044 graph slack coefficients")
    expressions = Model(model, matrices, scalars)
    check_graph_basis(expressions.n, expressions.masks)
    print("1044 graph descriptors form the complete order-7 basis", flush=True)
    check_psd_blocks(matrices, args.workers)
    print("82 PSD blocks verified exactly", flush=True)
    for i, scalar in enumerate(scalars):
        require(scalar.sign() >= 0, "Negative scalar multiplier at index %d" % i)
    print("819 scalar generators checked", flush=True)
    for i, slack in enumerate(slacks):
        require(slack.sign() >= 0, "Negative graph slack at index %d" % i)
    print("1044 graph slacks checked", flush=True)
    for i, (mask, slack) in enumerate(zip(expressions.masks, slacks)):
        residual = expressions.residual(mask, slack)
        require(not residual, "Nonzero identity coefficient for graph %d (mask %d): %s" %
                (i, mask, residual))
        if (i + 1) % 128 == 0:
            print("Identity progress: %d/1044" % (i + 1), flush=True)
    print("1044/1044 identity coefficients exactly zero")
    print("CERTIFICATE VERIFIED")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, TypeError, ZeroDivisionError, OSError) as error:
        print("VERIFICATION FAILED: " + str(error), file=sys.stderr)
        sys.exit(1)
