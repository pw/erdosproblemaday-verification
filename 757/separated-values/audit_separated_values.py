#!/usr/bin/env python3
"""Independent definition-level audit of four exact finite values for #757.

The coordinate sets and their partitions are hardcoded.  This implementation
does not import the construction/verifier module and does not reconstruct the
sets using its scale-separation routine.
"""

from itertools import combinations
from math import comb


CASES = {
    17: {
        "split": 14,
        "expected_h": 10,
        "points": (
            0,136,200,243,246,249,272,286,298,323,400,528,596,1056,
            195057,292057,389057,
        ),
        "witness": (
            0,136,200,243,246,298,323,528,195057,292057,
        ),
    },
    24: {
        "split": 12,
        "expected_h": 14,
        "points": (
            0,97,161,194,227,322,374,454,521,534,547,720,
            720721,817721,881721,914721,947721,1042721,1094721,
            1174721,1241721,1254721,1267721,1440721,
        ),
        "witness": (
            0,97,161,227,374,534,547,720721,817721,881721,947721,
            1094721,1254721,1267721,
        ),
    },
    26: {
        "split": 14,
        "expected_h": 15,
        "points": (
            0,136,200,243,246,249,272,286,298,323,400,528,596,1056,
            721057,818057,882057,915057,948057,1043057,1095057,
            1175057,1242057,1255057,1268057,1441057,
        ),
        "witness": (
            0,136,200,243,246,298,323,528,721057,818057,882057,
            948057,1095057,1255057,1268057,
        ),
    },
    28: {
        "split": 14,
        "expected_h": 16,
        "points": (
            0,136,200,243,246,249,272,286,298,323,400,528,596,1056,
            1057057,1193057,1257057,1300057,1303057,1306057,1329057,
            1343057,1355057,1380057,1457057,1585057,1653057,2113057,
        ),
        "witness": (
            0,136,200,243,246,298,323,528,1057057,1193057,1257057,
            1300057,1303057,1355057,1380057,1585057,
        ),
    },
}


def literal_difference_count(block):
    return len({x-y for x in block for y in block})


def direct_sidon(block):
    sums = [block[i]+block[j]
            for i in range(len(block)) for j in range(i, len(block))]
    return len(sums) == len(set(sums))


def direct_weak_sidon(block):
    sums = [x+y for x,y in combinations(block,2)]
    return len(sums) == len(set(sums))


def exhaustive_h(block):
    for size in range(len(block), -1, -1):
        for subset in combinations(block, size):
            if direct_sidon(subset):
                return size, subset
    raise AssertionError


def complete_ap_list(block):
    return tuple(t for t in combinations(block,3) if t[0]+t[2] == 2*t[1])


def audit(n, data):
    points = data["points"]
    split = data["split"]
    expected_h = data["expected_h"]
    witness = data["witness"]
    assert len(points) == n == len(set(points))
    assert tuple(sorted(points)) == points
    left, right = points[:split], points[split:]

    # Literal live statement on every quadruple, no equivalence lemma used.
    histogram = {}
    checked = 0
    for quad in combinations(points,4):
        checked += 1
        count = literal_difference_count(quad)
        histogram[count] = histogram.get(count,0)+1
        assert count >= 11, quad
    assert checked == comb(n,4)

    # Pair-sum and complete AP audits.  Every triple is visited, and every AP
    # is required to remain wholly within one of the two declared blocks.
    assert direct_weak_sidon(points)
    pair_sum_count = len({x+y for x,y in combinations(points,2)})
    assert pair_sum_count == comb(n,2)
    aps = complete_ap_list(points)
    mixed_aps = tuple(e for e in aps
                      if not (set(e) <= set(left) or set(e) <= set(right)))
    assert mixed_aps == ()
    assert all(len(set(e)&set(f)) <= 1 for e,f in combinations(aps,2))

    # Exhaust the two actual coordinate components independently.  For any
    # Sidon S in the union, S∩left and S∩right are Sidon, hence
    # |S| <= h(left)+h(right).  The hardcoded witness is tested by every
    # unordered pair sum (including diagonals), so it proves equality.
    h_left, left_witness = exhaustive_h(left)
    h_right, right_witness = exhaustive_h(right)
    component_upper = h_left+h_right
    assert component_upper == expected_h
    assert len(witness) == expected_h and set(witness) <= set(points)
    assert direct_sidon(witness)
    witness_sum_count = len({witness[i]+witness[j]
                             for i in range(len(witness))
                             for j in range(i,len(witness))})
    assert witness_sum_count == expected_h*(expected_h+1)//2

    # Full exhaustive union check is feasible at n=17 and is performed as a
    # further independent confirmation of the component upper proof.
    full_h = None
    if n == 17:
        full_h, full_witness = exhaustive_h(points)
        assert full_h == expected_h and direct_sidon(full_witness)

    # Full integer arithmetic for the published-theorem lower corollary.
    m_bound = n-2
    numerator = 5*n+3*m_bound
    tau_bound = numerator//17
    assert 17*tau_bound <= numerator < 17*(tau_bound+1)
    lower = n-tau_bound
    assert lower == expected_h

    return {
        "n": n,
        "points": points,
        "split": split,
        "quadruples": checked,
        "difference_histogram": dict(sorted(histogram.items())),
        "pair_sums": pair_sum_count,
        "aps": aps,
        "mixed_aps": mixed_aps,
        "component_h": (h_left,h_right),
        "component_witnesses": (left_witness,right_witness),
        "witness": witness,
        "witness_sums": witness_sum_count,
        "full_h": full_h,
        "m_bound": m_bound,
        "numerator": numerator,
        "tau_bound": tau_bound,
        "lower": lower,
    }


def main():
    for n,data in CASES.items():
        result = audit(n,data)
        print("n =",n)
        print("  coordinates =",result["points"])
        print("  partition index =",result["split"])
        print("  quadruples / live histogram =",result["quadruples"],
              result["difference_histogram"])
        print("  distinct-element pair sums =",result["pair_sums"])
        print("  complete AP list =",result["aps"])
        print("  mixed APs =",result["mixed_aps"])
        print("  exact component h =",result["component_h"])
        print("  direct Sidon witness / sum count =",result["witness"],
              result["witness_sums"])
        print("  full exhaustive union h =",result["full_h"])
        print("  lower arithmetic: m<=%d, 5n+3m<=%d, tau<=%d, h>=%d" %
              (result["m_bound"],result["numerator"],
               result["tau_bound"],result["lower"]))
    print("INDEPENDENT AUDIT PASSED: f(17)=10, f(24)=14, f(26)=15, f(28)=16")


if __name__ == "__main__":
    main()
