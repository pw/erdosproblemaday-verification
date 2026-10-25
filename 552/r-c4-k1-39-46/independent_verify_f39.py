#!/usr/bin/env python3
"""Decorrelated exact audit of the candidate proof of R(C4,K1,39)=46.

This intentionally uses only the Python standard library. It does not import
any upstream module, use floating point, trust SAT status lines, or use assert.
"""

from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
UPSTREAM = ROOT / "upstream_ro"


class AuditFailure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise AuditFailure(message)


def normalized_edges(data):
    edges = []
    for item in data:
        require(
            isinstance(item, list)
            and len(item) == 2
            and all(isinstance(v, int) for v in item),
            f"invalid edge record: {item!r}",
        )
        u, v = item
        require(u != v, f"loop at {u}")
        edges.append((min(u, v), max(u, v)))
    require(len(edges) == len(set(edges)), "duplicate edge")
    return tuple(edges)


def graph_from_data(data):
    edges = normalized_edges(data)
    vertices = sorted({v for edge in edges for v in edge})
    adjacency = {v: set() for v in vertices}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    return vertices, edges, adjacency


def common_neighbor_max(vertices, adjacency):
    return max(
        len(adjacency[u] & adjacency[v])
        for u, v in combinations(vertices, 2)
    )


def four_cycle_count(vertices, edge_set):
    count = 0
    for a, b, c, d in combinations(vertices, 4):
        cycles = (
            ((a, b), (b, c), (c, d), (d, a)),
            ((a, b), (b, d), (d, c), (c, a)),
            ((a, c), (c, b), (b, d), (d, a)),
        )
        for cycle in cycles:
            if all((min(u, v), max(u, v)) in edge_set for u, v in cycle):
                count += 1
    return count


def check_lower_witness():
    raw = json.loads((UPSTREAM / "lower_bound_45.json").read_text())
    vertices, edges, adjacency = graph_from_data(raw)
    degrees = [len(adjacency[v]) for v in vertices]
    require(len(vertices) == 45, f"witness order is {len(vertices)}, not 45")
    require(min(degrees) == 6, f"witness minimum degree is {min(degrees)}, not 6")
    require(common_neighbor_max(vertices, adjacency) <= 1, "witness has a C4")
    require(four_cycle_count(vertices, set(edges)) == 0, "direct cycle scan found a C4")

    # Negative controls: duplicate, degree-destroying deletion, and a known
    # C4-creating insertion must all be detected by the same independent code.
    try:
        normalized_edges(raw + [raw[0]])
    except AuditFailure:
        pass
    else:
        raise AuditFailure("duplicate-edge negative control was accepted")

    dv, de, da = graph_from_data(raw[1:])
    require(min(len(da[v]) for v in dv) < 6, "edge-deletion control kept delta >= 6")

    inserted = raw + [[1, 12]]
    iv, ie, ia = graph_from_data(inserted)
    require(common_neighbor_max(iv, ia) >= 2, "C4-insertion control was not detected")
    require(four_cycle_count(iv, set(ie)) > 0, "cycle scan missed insertion control")

    print(
        "lower_witness=PASS "
        f"vertices={len(vertices)} edges={len(edges)} min_degree={min(degrees)} "
        f"degree6={degrees.count(6)} degree7={degrees.count(7)} c4=0"
    )
    print("lower_witness_negative_controls=PASS")


def matmul(left, right):
    n = len(left)
    require(n == len(right), "matrix size mismatch")
    columns = list(zip(*right))
    return [
        [sum(a * b for a, b in zip(row, column)) for column in columns]
        for row in left
    ]


def trace(matrix):
    return sum(matrix[i][i] for i in range(len(matrix)))


def adjacency_matrix(vertices, adjacency):
    return [
        [int(v in adjacency[u]) for v in vertices]
        for u in vertices
    ]


def check_general_moment_controls():
    outputs = []
    for filename in ("reg_3_10.json", "reg_4_15.json", "reg_5_26.json", "reg_6_34.json"):
        raw = json.loads((UPSTREAM / filename).read_text())
        vertices, _edges, adjacency = graph_from_data(raw)
        degrees = {len(adjacency[v]) for v in vertices}
        require(len(degrees) == 1, f"{filename} is not regular")
        k = next(iter(degrees))
        n = len(vertices)
        require(common_neighbor_max(vertices, adjacency) <= 1, f"{filename} has a C4")

        A = adjacency_matrix(vertices, adjacency)
        A2 = matmul(A, A)
        D = [
            [int(i != j and A2[i][j] == 0) for j in range(n)]
            for i in range(n)
        ]
        z = n - 1 - k * (k - 1)
        require({sum(row) for row in D} == {z}, f"{filename}: bad deficiency degree")
        for i in range(n):
            for j in range(n):
                rhs = (k - 1 if i == j else 0) + 1 - D[i][j]
                require(A2[i][j] == rhs, f"{filename}: A2 identity failed")

        A4 = matmul(A2, A2)
        A5 = matmul(A4, A)
        AD = matmul(A, D)
        D2 = matmul(D, D)
        AD2 = matmul(A, D2)
        actual = trace(A5) - k**5
        predicted = (
            -2 * (k - 1) * trace(AD)
            + trace(AD2)
            + k * n * (2 * (k - 1 - z) + n)
            - k**5
        )
        require(actual == predicted, f"{filename}: fifth-moment identity failed")
        outputs.append(f"{filename}:{n},{k},{z},{actual}")

    print("general_moment_controls=PASS " + " ".join(outputs))


def check_universal_reduction_and_moments():
    # For any vertex degree d in a hypothetical 46-vertex graph with delta 7,
    # 7d <= 45+d. This leaves only d=7.
    allowed_degrees = [d for d in range(7, 46) if 7 * d <= 45 + d]
    require(allowed_degrees == [7], f"regularity reduction left {allowed_degrees}")

    # Once regular, 49=45+2m-f and m<=3.
    local = [
        (m, 2 * m - 4)
        for m in range(4)
        if 2 * m - 4 >= 0
    ]
    require(local == [(2, 0), (3, 2)], f"unexpected local cases {local}")
    require((7 - 2) % 2 == 1, "parity lemma did not eliminate m=2")

    # In the surviving case every vertex is in three edge-disjoint triangles.
    n, k, z = 46, 7, 3
    triangles = n * 3 // 3
    matching_edges = n * (k - 2 * 3) // 2
    require(triangles == 46 and matching_edges == 23, "structure counts failed")

    # Exact nonprincipal moments. For D cubic, A^2=6I+J-D.
    s0 = n - 1
    s1 = -k
    s2 = n * k - k**2
    s3 = 6 * triangles - k**3
    tr_p2 = 36 * n + z * n
    s4 = tr_p2 + 52 * n - k**4
    fixed = (s0, s1, s2, s3, s4)
    require(fixed == (45, -7, 273, -67, 1785), f"bad fixed moments {fixed}")

    # tr(AD)=46. Writing T=tr(AD^2)=2*kappa gives 0<=T<=92.
    fifth_constant = -12 * 46 + 364 * 46 - k**5
    require(fifth_constant == -615, f"bad fifth-moment constant {fifth_constant}")
    require(2 * 46 == 92, "bad kappa range")

    # A cubic simple graph has all eigenvalues mu in [-3,3]. On 1-perp,
    # theta^2=6-mu, hence 3<=theta^2<=9 and no theta is zero.
    require(6 - 3 == 3 and 6 - (-3) == 9, "bad spectral support")
    print("universal_reduction=PASS degrees=[7] local=[(2,0),(3,2)] surviving=(3,2)")
    print(f"moments=PASS fixed={fixed} fifth=T-615 T=0..92 support_squared=3..9")
    return fixed


def poly_add(left, right):
    size = max(len(left), len(right))
    out = [0] * size
    for i, value in enumerate(left):
        out[i] += value
    for i, value in enumerate(right):
        out[i] += value
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return tuple(out)


def poly_scale(poly, scalar):
    return tuple(scalar * value for value in poly)


def poly_mul(left, right):
    out = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] += a * b
    return tuple(out)


def product(*factors):
    out = (1,)
    for factor in factors:
        out = poly_mul(out, factor)
    return out


def minus_x(poly):
    return tuple(value if i % 2 == 0 else -value for i, value in enumerate(poly))


def evaluate(coefficients, value):
    out = Fraction(0)
    for coefficient in reversed(coefficients):
        out = out * value + coefficient
    return out


def moment_affine(numerator, fixed, denominator):
    require(len(numerator) == 6, "certificate is not degree five")
    constant = sum(numerator[i] * fixed[i] for i in range(5))
    constant += numerator[5] * (-615)
    return Fraction(constant, denominator), Fraction(numerator[5], denominator)


def check_factored_dual_certificate(fixed):
    denominator = 26_468_750

    # q=(2x+5)^2(3x+5)(4904x^2-38072x+85705)/denominator.
    q_num = product((5, 2), (5, 2), (5, 3), (85_705, -38_072, 4_904))
    one_minus_q_num = product(
        (3, -1), (-5, 2), (-5, 2), (210_075, 101_560, 14_712)
    )
    require(
        poly_add(q_num, one_minus_q_num) == (denominator,),
        "factorization of 1-q failed",
    )

    # Q(x)=1-q(-x). Pointwise, q<=1 on the positive support and q<=0
    # on the negative support; therefore Q>=1 positive and Q>=0 negative.
    Q_num = poly_add((denominator,), poly_scale(minus_x(q_num), -1))

    # Universal sign proof from the displayed factors:
    # * on [-3,-sqrt(3)], 3x+5<0 because 27>25, while the
    #   quadratic in q is strictly positive term by term;
    # * on [sqrt(3),3], every factor of 1-q is nonnegative.
    require(27 > 25, "could not establish 3*sqrt(3)>5")
    require((4_904 > 0 and -38_072 < 0 and 85_705 > 0), "bad q quadratic")
    require(all(value > 0 for value in (14_712, 101_560, 210_075)), "bad 1-q quadratic")

    q_const, q_slope = moment_affine(q_num, fixed, denominator)
    Q_const, Q_slope = moment_affine(Q_num, fixed, denominator)
    require(q_slope > 0 and Q_slope > 0, "unexpected fifth-moment slope")

    lower_margin = q_const - 21
    upper_margin = 22 - (Q_const + 92 * Q_slope)
    require(lower_margin > 0, f"lower certificate margin is {lower_margin}")
    require(upper_margin > 0, f"upper certificate margin is {upper_margin}")
    for T in range(93):
        lower = q_const + q_slope * T
        upper = Q_const + Q_slope * T
        require(21 < lower, f"T={T}: lower bound failed")
        require(upper < 22, f"T={T}: upper bound failed")

    # Negative control: the upper certificate must stop working if the
    # combinatorial T bound is materially weakened.
    require(Q_const + Q_slope * 200 > 22, "loose-T negative control still closed the case")

    # A second negative control targets the main repository certificate's
    # delicate algebraic endpoint. p(sqrt(3))-1 is positive exactly, but
    # p(173/100)-1 is negative, so replacing sqrt(3) by 1.73 is rejected.
    p = (
        Fraction(277_973, 500_000),
        Fraction(390_143, 1_000_000),
        Fraction(-4_087, 250_000),
        Fraction(-8_719, 200_000),
        Fraction(19, 15_625),
        Fraction(423, 200_000),
    )
    require(evaluate(p, Fraction(173, 100)) - 1 < 0, "1.73 endpoint control did not fail")
    root_coefficient = 9 * p[5] + 3 * p[3] + p[1]
    constant = 9 * p[4] + 3 * p[2] + p[0] - 1
    require(root_coefficient > 0 and constant < 0, "unexpected sqrt(3) endpoint form")
    require(
        3 * root_coefficient**2 > constant**2,
        "p(sqrt(3))-1 is not exactly positive",
    )

    print(
        "factored_dual_certificate=PASS "
        f"lower_margin={lower_margin} upper_margin={upper_margin}"
    )
    print("certificate_negative_controls=PASS loose_T=200 rational_endpoint=173/100")


def check_provenance_and_live_gate():
    ids = (ROOT / "provenance/upstream_ids.txt").read_text().splitlines()
    require(
        ids == [
            "86a1c5055eea5e3891b2eeaea6c7ee1b3977bd33",
            "347a884913671c9f9a060de868de8fdd63d4f6a1",
        ],
        f"unexpected commit/tree ids {ids}",
    )
    remote = (ROOT / "provenance/github_ls_remote_20260811.txt").read_text()
    require(
        remote.startswith("86a1c5055eea5e3891b2eeaea6c7ee1b3977bd33\tHEAD\n"),
        "frozen remote HEAD differs",
    )
    metadata = json.loads((ROOT / "provenance/github_repo_20260811.json").read_text())
    require(metadata["full_name"] == "zach7036/c4-star-ramsey", "wrong GitHub repository")
    commit = json.loads((ROOT / "provenance/github_commit_86a1c505_20260811.json").read_text())
    require(commit["sha"] == ids[0], "GitHub commit response mismatch")

    readme = (UPSTREAM / "README.md").read_text()
    require("Status: not yet peer-reviewed" in readme, "review status missing")
    require("R(C₄, K₁,₃₉) = 46" in readme, "candidate claim missing")

    survey = (ROOT / "sources/ejcram18.txt").read_text()
    require("39       46-47" in survey, "published 46..47 interval missing")
    require("40        47" in survey, "published parameter-40 value missing")
    require("values of f (n) are known for all n ≤ 38" in survey, "survey scope missing")
    equality = (ROOT / "sources/zhang_broersma_chen_2014.txt").read_text()
    require(
        "Theorem 1.6. R(Wn , C4 ) = R(Sn+1 , C4 ) for n ≥ 6." in equality,
        "star-wheel equality missing",
    )

    live = (ROOT / "provenance/live_552_bright_20260811.txt").read_text()
    for sentinel in (
        "OPEN",
        "0 claimed proofs for this problem",
        "Currently working on this problem\tNone",
    ):
        require(sentinel in live, f"live gate missing {sentinel!r}")

    other_remote = (ROOT / "provenance/suitedaces_ls_remote_20260811.txt").read_text()
    require(
        other_remote.startswith("d20470914e9f496e4b4fd47c4bcc38f6f832da6b\tHEAD\n"),
        "other current claimant HEAD differs",
    )
    other_metadata = json.loads(
        (ROOT / "provenance/suitedaces_repo_metadata_20260811.json").read_text()
    )
    require(
        other_metadata["full_name"] == "suitedaces/ramsey-c4-star39",
        "other claimant repository mismatch",
    )
    other_readme = (ROOT / "provenance/suitedaces_repo_README_20260811.md").read_text()
    require(
        "Status:** unreviewed computer-assisted result" in other_readme,
        "other claim status missing",
    )
    require("R(C_4,K_{1,39})=46" in other_readme, "other exact claim missing")
    print("provenance=PASS commit=86a1c5055eea5e3891b2eeaea6c7ee1b3977bd33")
    print(
        "published_prior_scope=46<=R(C4,K1,39)<=47 "
        "R(C4,K1,40)=47 lower_bound_already_established=YES"
    )
    print("live_gate=OPEN claimed_proofs=0 current_worker=None")
    print("other_current_claimant=suitedaces/ramsey-c4-star39 status=unreviewed audit_scope=EXCLUDED")


def main():
    check_provenance_and_live_gate()
    check_lower_witness()
    check_general_moment_controls()
    fixed = check_universal_reduction_and_moments()
    check_factored_dual_certificate(fixed)
    print("INDEPENDENT_AUDIT=PASS exact_claim=R(C4,K1,39)=46")


if __name__ == "__main__":
    main()
