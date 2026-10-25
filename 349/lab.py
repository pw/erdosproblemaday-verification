#!/usr/bin/env python3
"""Erdős #349 — completeness of floor(t*alpha^n), 0-indexed vs 1-indexed.

The formally-posed problem (DeepMind Lean) is 0-indexed: s_n = floor(t*alpha^n), n=0,1,2,...
van Doorn's paper + the Pro result are 1-indexed (n>=1). The only difference is the
leading floor(t) term. This lab measures how completeness behaves on the 0-indexed
sequence and how far it reaches beyond the 1-indexed frontier.

Three independent lenses, each exact rational arithmetic (fractions.Fraction):
  1. greedy_entire   — decisive test for ENTIRE completeness (every positive integer
                       representable): process terms ascending, extend [0,C]; a term
                       s>C+1 is a PERMANENT gap (all later terms >= s).
  2. lemma5_cert     — for 1<alpha<phi, a contiguous interval of subset sums of the
                       first r+1 terms of length >= s_{r+1} is a genuine PROOF of
                       (cofinite) completeness (van Doorn Lemma 5 propagation).
  3. gap_to_N        — empirical: subset-sum bitset to cap N; report max gap + covered
                       tail. "no gap to N", NOT a proof, unless lens 2 fires.
"""
from fractions import Fraction
import math

PHI = (1 + math.sqrt(5)) / 2  # golden ratio ~1.6180339887


def floors(t, alpha, n_terms=None, max_val=None, start=0):
    """[floor(t*alpha^n) for n = start, start+1, ...]. Exact for Fraction t,alpha.
    Iterates the power (val *= alpha) instead of recomputing alpha**n each term."""
    out = []
    val = t * (alpha ** start)  # exact Fraction = t*alpha^start
    n = start
    while True:
        f = val.numerator // val.denominator  # floor of a positive Fraction
        out.append(f)
        if n_terms is not None and len(out) >= n_terms:
            break
        if max_val is not None and f > max_val:
            break
        if alpha <= 1 and max_val is not None:
            break  # avoid non-termination for alpha<=1
        val *= alpha
        n += 1
    return out


def subsetsum_bits(terms, cap):
    """Bitset (python int): bit v set iff v is a subset sum of distinct `terms`, v<=cap."""
    mask = (1 << (cap + 1)) - 1
    bits = 1  # empty sum = 0
    for s in terms:
        if s <= 0 or s > cap:
            continue
        bits |= (bits << s)
        bits &= mask
    return bits


def longest_run_length(bits):
    """Length of the longest run of consecutive SET bits. C-level: bin() + split('0').
    Robust even when the longest run is very long (near-complete sets)."""
    if bits <= 0:
        return 0
    return max((len(run) for run in bin(bits)[2:].split("0")), default=0)


def longest_run(bits, cap=None):
    """(length, start_bit) of a longest run of consecutive SET bits.
    Length via C-level split; start found with a C-level str.find on success."""
    if bits <= 0:
        return 0, 0
    s = bin(bits)[2:]  # MSB-first; bit position of s[i] is (len(s)-1-i)
    L = max((len(run) for run in s.split("0")), default=0)
    if L == 0:
        return 0, 0
    idx = s.find("1" * L)  # MSB-first index of the (first) run of length L
    start_bit = (len(s) - 1) - (idx + L - 1)  # lowest bit position of that run
    return L, start_bit


def gap_stats(bits, cap):
    """(max_gap_len, gap_start, tail_start) over [1, cap].
    tail_start = smallest X with [X, cap] fully covered; cap+1 if cap itself uncovered."""
    max_gap = 0
    gap_start = None
    i = 1
    while i <= cap:
        if not ((bits >> i) & 1):
            j = i
            while j <= cap and not ((bits >> j) & 1):
                j += 1
            if j - i > max_gap:
                max_gap = j - i
                gap_start = i
            i = j
        else:
            i += 1
    if not ((bits >> cap) & 1):
        tail_start = cap + 1
    else:
        x = cap
        while x >= 1 and ((bits >> x) & 1):
            x -= 1
        tail_start = x + 1
    return max_gap, gap_start, tail_start


def greedy_entire(t, alpha, n_terms=80, start=0):
    """Greedy no-gap-from-1 test on the `start`-indexed sequence.
    Process terms ascending, extend covered interval [0,C]; a term s>C+1 is a PERMANENT
    gap (all later terms >= s). Returns entire=False with the gap, or entire=True meaning
    'no gap through n_terms terms and C reached >=1' (a PROOF of entire-completeness only
    when paired with the analytic sustainment bound — see entire_cert_0indexed)."""
    terms = floors(t, alpha, n_terms=n_terms, start=start)
    C = 0
    for r, s in enumerate(terms):  # already nondecreasing for alpha>1
        if s == 0:
            continue
        if s > C + 1:
            return {"entire": False, "gap_at": C + 1, "at_index": r, "term": s, "C": C,
                    "start": start}
        C += s
    if C < 1:  # never covered the integer 1 (e.g. all-zero sequence) -> gap at 1
        return {"entire": False, "gap_at": 1, "at_index": None, "term": None, "C": 0,
                "start": start, "note": "no positive term <= 1 ever appeared"}
    return {"entire": True, "C": C, "n_terms": n_terms, "start": start}


def entire_cert_0indexed(t, alpha, n_check=5000):
    """Rigorous entire-completeness PROOF for the 0-INDEXED sequence, 1<alpha<2, t>=1.

    Claim: if the greedy has no gap through term M, and the analytic sustainment bound
        n*(alpha-1) + t  <=  t*alpha^(n+1)*(2-alpha)        (*)
    holds for every n >= M, then the sequence is entirely complete (every positive
    integer is a subset sum).

    Proof: by induction the covered interval is [0, C_n], C_n = sum_{k<=n} s_k, as long as
    each s_{n+1} <= C_n + 1. s_{n+1}=floor(t*alpha^(n+1)) <= t*alpha^(n+1), and
    C_n = sum_{k<=n} floor(t*alpha^k) >= t*(alpha^(n+1)-1)/(alpha-1) - (n+1). So s_{n+1}<=C_n+1
    is forced once t*alpha^(n+1) <= t*(alpha^(n+1)-1)/(alpha-1) - n, which rearranges to (*).
    For t>=1 the difference f(n+1)-f(n) = (alpha-1)*(t*alpha^(n+1)*(2-alpha)-1) >= (alpha-1)*(t-1)
    >= 0 whenever f(n)>=0 (since then t*alpha^(n+1)*(2-alpha) >= n(alpha-1)+t >= t >= 1). So f,
    once nonnegative, is nondecreasing — hence (*) holds for ALL n past the FIRST n where f>=0.
    We find that first crossing M (incremental powers, exact Fraction), verify the greedy has no
    gap through term M, and conclude [0,C_n] is covered for all n with C_n -> infinity.
    """
    if not (1 < float(alpha) < 2):
        return {"proven": False, "reason": "analytic bound requires 1<alpha<2"}
    if not (float(t) >= 1):
        return {"proven": False, "reason": "monotonicity argument requires t>=1"}
    two = Fraction(2)
    c = two - alpha            # (2-alpha) > 0
    am1 = alpha - 1            # (alpha-1) > 0
    # find first n with f(n) = t*alpha^(n+1)*(2-alpha) - n*(alpha-1) - t >= 0
    p = alpha                  # alpha^(n+1), starting at n=0 -> alpha^1
    M = None
    fM = None
    for n in range(0, n_check + 1):
        fn = t * p * c - Fraction(n) * am1 - t
        if fn >= 0:
            M = n
            fM = fn
            break
        p *= alpha
    if M is None:
        return {"proven": False, "reason": f"sustainment crossover not found within n_check={n_check}"}
    # verify the greedy has no gap through term M (terms s_0..s_M), reaching C>=1
    g = greedy_entire(t, alpha, n_terms=M + 1, start=0)
    if not g["entire"]:
        return {"proven": False, "reason": f"early gap at {g['gap_at']} (term index {g['at_index']})"}
    return {"proven": True, "t": str(t), "alpha": str(alpha), "M": M,
            "greedy_C_at_M": g["C"], "f(M)": str(fM), "s0": int(t),
            "note": "entire-completeness proved for all positive integers"}


def lemma5_cert(t, alpha, max_r=34, start=0):
    """Search r (on `start`-indexed seq) with a contiguous subset-sum interval of length
    >= next term. Valid completeness PROOF for 1<alpha<phi only. Returns dict or None."""
    terms = floors(t, alpha, n_terms=max_r + 2, start=start)
    bits = 1
    for r in range(0, max_r + 1):
        cur_cap = sum(terms[:r + 1])
        mask = (1 << (cur_cap + 1)) - 1
        bits &= mask
        s_r = terms[r]
        if 0 < s_r <= cur_cap:
            bits |= (bits << s_r)
            bits &= mask
        s_next = terms[r + 1]
        if cur_cap > 4_000_000:  # bitset horizon guard
            return {"r": r, "status": "horizon", "note": "cap exceeded before trigger"}
        L = longest_run_length(bits)  # fast length-only check (no start scan)
        if L >= s_next:
            _, X = longest_run(bits, cur_cap)  # find start only on success
            return {"r": r, "X": X, "interval_len": L, "s_next": s_next, "start": start,
                    "alpha<phi": float(alpha) < PHI}
    return None


def gap_to_N(t, alpha, N=200_000, start=0):
    """Empirical subset-sum coverage of the `start`-indexed sequence up to cap N."""
    terms = floors(t, alpha, max_val=N, start=start)
    bits = subsetsum_bits(terms, N)
    mg, gs, tail = gap_stats(bits, N)
    return {"N": N, "n_terms_used": len(terms), "max_gap": mg, "first_max_gap_at": gs,
            "covered_tail_from": tail, "start": start}


def F(x):
    """Coerce to Fraction (accepts int, str like '3/2', float)."""
    return Fraction(x)


if __name__ == "__main__":
    print("=" * 78)
    print("VALIDATION BATTERY — reproduce the live site entry's known facts")
    print("=" * 78)

    # --- alpha = 1 (0-indexed): complete iff t in [1,2) ---
    print("\n[alpha=1, 0-indexed] complete iff t in [1,2):")
    for ts in ["1/2", "1", "3/2", "2", "5/2"]:
        t = F(ts)
        g = greedy_entire(t, F(1), n_terms=10, start=0)
        s0 = floors(t, F(1), n_terms=3, start=0)
        verdict = "ENTIRE" if g["entire"] else f"gap at {g['gap_at']}"
        print(f"  t={ts:>5} seq0={s0} -> {verdict}")

    # --- alpha = 2 (0-indexed): complete iff t = 1/2^j, j>=0 ---
    print("\n[alpha=2, 0-indexed] complete iff t=1/2^j (j>=0):")
    for ts in ["1/4", "1/2", "1", "3/4", "3/2", "2"]:
        t = F(ts)
        g = greedy_entire(t, F(2), n_terms=40, start=0)
        s0 = floors(t, F(2), n_terms=6, start=0)
        verdict = "ENTIRE" if g["entire"] else f"gap at {g['gap_at']}"
        print(f"  t={ts:>5} seq0={s0} -> {verdict}")

    # --- reproduce entry's alpha=1.65 threshold via gap_to_N (1-indexed):
    #     entry: "t=1.80, 1.818 clean to 60,000; t=1.82 gaps at 2" ---
    a = F("1.65")
    thr = min(F(2), F(3) / a, F(5) / (a * a))
    print(f"\n[1-indexed alpha=1.65] entry: t=1.80,1.818 clean to 60k; t=1.82 gaps at 2.")
    print(f"  (van Doorn entire-complete threshold min(2,3/a,5/a^2) = {float(thr):.4f})")
    for ts in ["1.80", "1.818", "1.82", "1.83"]:
        t = F(ts)
        r1 = gap_to_N(t, a, N=60_000, start=1)
        print(f"  1-indexed t={ts:>6}: max_gap={r1['max_gap']:>6} first@{str(r1['first_max_gap_at']):>6} "
              f"covered_tail_from={r1['covered_tail_from']:>6} seq1[0:3]={floors(t,a,n_terms=3,start=1)}")

    # --- entire_cert_0indexed: rigorous proof test, cross-validated with gap_to_N ---
    print("\n[entire_cert_0indexed] rigorous entire-completeness proof (1<alpha<2):")
    pts = [("1", "1.8"), ("1", "3/2"), ("1", "1.7"), ("1", "1.9"), ("1", "1.95"),
           ("3/2", "1.8"), ("1", "1.618")]
    for ts, als in pts:
        t, al = F(ts), F(als)
        c = entire_cert_0indexed(t, al)
        if c["proven"]:
            # cross-validate: gap_to_N to a large N must show no gap
            gv = gap_to_N(t, al, N=300_000, start=0)
            print(f"  t={ts:>4} a={als:>6}: PROVEN entire (M={c['M']}, C_M={c['greedy_C_at_M']}) "
                  f"| cross-check gap_to_300k: max_gap={gv['max_gap']} tail_from={gv['covered_tail_from']}")
        else:
            print(f"  t={ts:>4} a={als:>6}: not proven ({c['reason']})")

    # --- the contrast point made rigorous: (t=1, alpha=1.8) ---
    print("\n[contrast] (t=1, alpha=1.8) — 0-indexed vs 1-indexed:")
    c0 = entire_cert_0indexed(F(1), F("1.8"))
    print(f"  0-indexed: {c0}")
    g1 = greedy_entire(F(1), F("1.8"), n_terms=30, start=1)
    r1 = gap_to_N(F(1), F("1.8"), N=200_000, start=1)
    print(f"  1-indexed: greedy -> {'ENTIRE' if g1['entire'] else 'gap@%s (term %s)'%(g1['gap_at'],g1['at_index'])}"
          f" | gap_to_200k: max_gap={r1['max_gap']} tail_from={r1['covered_tail_from']}")
