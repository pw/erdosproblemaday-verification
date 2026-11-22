# Erdős #1109 — a 67-element squarefree-sumset set inside {1, …, 3569} (submission 2wvfme, Nguyen Trong Nhan, 21 Nov 2026)

f(N) = largest size of A ⊆ {1,…,N} with every a + b (a, b ∈ A, a = b allowed) squarefree.

**Claim:** the 67-element set in `erdos1109_witness_67_candidate_3569.txt` (largest element 3569) has all 2,278 sums
squarefree, so f(3569) ≥ 67, i.e. the least N with f(N) = 67 (OEIS A392165, a(67)) is at most 3569. Minimality is not
claimed.

**Verdict: VERIFIED** (22 Nov 2026).

**Checks.** `python3 check1109.py erdos1109_witness_67_candidate_3569.txt` → `check1109.out`: 67 distinct elements in
[1, 3569]; all 67·68/2 = 2,278 sums a + b (a ≤ b) are squarefree by full factorisation (sympy) and by a separate p²
sieve. Negative control: adding 1 to one element creates 15 non-squarefree sums, found by both routes. We also report
that no single x ≤ 3569 extends the set to 68 elements (not a claim about f).

**Context.** OEIS A392165's b-file (Kevin Russell; terms 1..65 from Leandre Jack) runs to a(66) = 3065, so
3067 ≤ a(67) ≤ 3569 after this witness (a(67) is odd, like every term). Leandre Jack's computations
(github.com/leandrejack-afk/erdos-computations, e1109) give f(N) exactly for N ≤ 3000. Our own exact table on
/day/1109-squarefree-sumset stops at 2000.

**Not checked:** the submitter's PDF write-up beyond the witness; his second C++ file (the Drive link served a
confirmation page instead of the file).

`submission_2wvfme_frozen.json` is the submission as received (contact details removed).
