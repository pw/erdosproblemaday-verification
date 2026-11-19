# #1186, k = 3 — Carlos Toledo's proof claim that δ₃ = 117/2192, refereed

erdosproblemaday.com, 19 November 2026. Page: https://erdosproblemaday.com/day/1186-toledo-delta-3-equals-117-over-2192-refereed

## The claim (not ours)
Carlos Toledo (cert-machine), erdosproblems.com/forum/thread/1186/proof-claims#proof-claim-395, submitted 2026-10-05:
the twelve-block colouring of Parrilo–Robertson–Saracino (2008) is optimal, so the least number of monochromatic
3-term progressions in a 2-colouring of {1..n} is (117/2192 + o(1)) n². Paper: draft v0.2,
https://carlostoledo.co/paper/delta3.pdf ; report https://carlostoledo.co/reports/delta3.html ; repository
https://github.com/carlostoledo1891/cert-machine (read at commit 65e4e42ba121bd20544cb1cae60d8db1527bc566;
certificates and instruments/delta3 unchanged since 2026-10-27). The five certificate files and their sha256 are in
`verify3/cert_sha256.txt`; they equal the hashes in cert-machine's `certs/delta3-ledger.json`.

## What is in this folder
- `verify3/verify3.py` — a third verifier, written here in Python from the paper (§§2–5) and
  `instruments/delta3/CERT-FORMAT.md` only. It does not read or import the claimant's generators, the claimant's
  verifier, or cert-machine's `verify.js`. Exact rationals throughout; cell areas by integrating in a and in b (must
  agree for every ordered pair); positive definiteness by fraction-free (Bareiss) elimination on the integer matrix
  D·(S + εI): every leading principal minor > 0. `python3 verify3.py CERT.json` → exit 0 accepted / 1 refused / 2
  cannot run. `python3 verify3.py --lemma1` → Lemma 1 (Q(φ*) = −5/137, h, its zeros and slopes, ∫h = 5/137).
- `logs/logs_*.txt` — the five runs: all ACCEPTED (inner 32 s; slabs 3 to about 25 min each in pure Python).
- `logs/battery/` — 16 mutations. Refused (14): inner radius doubled; a negative multiplier (inner, slab);
  half the λ multipliers dropped (linear identity fails on 54 cells); one bathtub constant a₁ raised by 10⁻⁹ in the
  inner certificate (linear identity fails); the first edge removed from the grid (inner, slab); slab bound B raised
  by 10⁻⁶ (S + εI not PD); ε = 0 (not PD); every θ = 1 (not PD); slab widened by 1/100 (not PD); R mirrored for a slab
  (θ misaligned, not PD); triangle forms removed (not PD); one triangle with s₁s₂s₃ = −1 (refused by the sign rule).
  Accepted (2), both expected: mirroring R in the inner certificate leaves the quadratic form unchanged (Q is
  symmetric under (a,b) ↔ (b,a)); raising a₁ by 10⁻⁹ in a slab is absorbed by the slab's margin — so the soundness of
  the bathtub constants is established by Lemma 2's own test (below), not by the certificate check.
- `verify3/bathtub_test.py`, `logs/bathtub_test.txt` — Lemma 2 tested exactly: on all 276 cells of the two grids, at
  85 values of the cell average, the exact bathtub minimum (lowest levels of h filled) is ≥ a y + b y²: 0 failures in
  23,460 tests; with m′ read as the largest single piece instead of the sum, 1,782 failures (the control).
  `beta_check.py` checks the exact bathtub minimum against a numerical rearrangement (agreement to 3.5 × 10⁻¹⁶).
- `logs/their_verify_js_rerun.txt`, `logs/their_battery_rerun.txt` — cert-machine's verifier and its 79-check
  forgery battery, re-run here: VERIFIED, BATTERY GREEN.
- `referee/` — the hostile referee instance's scripts and logs (Claude, Opus 5.5, briefed to refute): t1 Lemma 1
  by two routes; t2 bathtub constants and areas by different routes (0 mismatches vs verify.js over 276 cells and
  38,216 ordered pairs); t3 the adversarial search for E − L < 0 (3,183 constructions + 15 descents on a 1/2192
  grid; minimum exactly 0); t4/t6 positive definiteness of every S + εI and of the inner P (Bareiss minors, own
  dyadic Cholesky); t5 every certificate rebuilt; t7 exact counts of the twelve-block colouring; t8 2,090 descents on
  Q. Verdict HOLDS WITH FIXES.
- `numerics/` — the compute seat's code (C + Python), logs and gzipped run records: about 4,100 searches on step
  functions at 1,096 and 2,192 cells and 91 continuous descents over block edges, none below −5/137 (best: φ*
  exactly); exact first/second-order check that φ* is a strict local minimiser (kkt.py); controls with a planted better optimum
  (found); 244 annealing/tabu runs on colourings of [n] for n = 300, 600, 1,096, 2,192 (all end at the twelve-block
  shape; exact at 1,096 and 2,192); small-n check against exhaustive enumeration.

## Reproduce
    git clone https://github.com/carlostoledo1891/cert-machine && cd cert-machine
    python3 /path/to/verify3.py certs/delta3/inner-r20-g24_4_8.json      # and the four slab-*.json
    python3 /path/to/verify3.py --lemma1
    (cd /path/to/verify3 && python3 bathtub_test.py)   # expects ../repo/certs/delta3/*.json; edit the glob

## Not done here
No human mathematician read any of this. Every seat was a Claude instance, as were Toledo's own verifiers and
Quana Labs' formalisation, so a misreading shared by all of them is not excluded.
