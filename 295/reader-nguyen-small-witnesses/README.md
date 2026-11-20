# Erdős #295 — reader certificates with small denominators (submission amryba, 19 Nov 2026)

**Claim (Nguyen Trong Nhan):** a 34-term expansion of 1 into distinct unit fractions with all denominators ≥ 18
(largest denominator 107,805,600) and a 36-term one with all denominators ≥ 19 (largest 239,154,300).
So k(18) ≤ 34 and k(19) ≤ 36.

**Verdict: VERIFIED** (20 Nov 2026). Both sums equal 1 exactly. Neither bound is new: k(18) ≤ 34 and k(19) ≤ 36
were Kyunghan Bae's (certificates of 11 Oct 2026; see /day/295-k17-exact). The new thing is the size of the
witnesses: largest denominators 107,805,600 and 239,154,300 against 10,457,416,992 in both of Bae's; least common
multiples 144,403,552,893,600 and 1,010,824,870,255,200 against Bae's 6,209,352,774,424,800.

**Checks.** `python3 verify.py certs.json` → `verify_py.log`: strictly increasing, distinct, min ≥ N, exact
`Fraction` sum = 1, integer sum Σ L/n_i = L over the lcm L. `gp -q check.gp` → `verify_gp.log` (PARI/GP, third route).
Controls (in verify.py): deleting any one term never leaves a sum of 1 (34 + 36 deletions), and adding 1 to the
largest denominator breaks the sum.

**Not checked:** the submitter's C++ search (not submitted). This does not decide k(18) ∈ {33, 34}.

`submission_amryba_frozen.json` is the submission as received (contact details removed).
