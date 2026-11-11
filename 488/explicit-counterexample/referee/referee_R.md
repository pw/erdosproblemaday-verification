# Referee R: Gessel's counterexample to Erdős #488 (multiples version)

Hostile referee report, 2026-11-11. Scope: the proof note (`MathDyad/erdos488/src/gessel/proof-note.md`), the README, the Lean source `Erdos488.lean` (gist d8e15e5f, sha256 f2a7dcfd…; the PR-pinned revision 034be67 and every later gist revision carry this same file), and the Formal Conjectures statement (FC main, cached checkout 2f91d251, 2026-11-09, body identical to `/tmp/e488/lean/fc_488_main.lean`). Every number below was re-run by this seat (`bash -c 'ulimit -v 4000000; exec timeout 900 python3 X.py'`). Scripts and outputs are in `/tmp/e488/referee_R/`.

## Verdict: HOLDS WITH FIXES

I tried to break every step and could not. The mathematics is correct, and the counterexample satisfies every hypothesis of the erdosproblems.com statement and of FC's `erdos_488` (A finite, nonempty, 0 ∉ A, 1 ∉ A, m > n ≥ max A, ℚ densities). The kernel replay is clean. None of the fixes touches the mathematics; they are prose overstatements plus one context residual on the FC bridge. The construction is also more explicit than the note claims: the smallest slow index is **k = 111**, and k = 110 is not slow. Both facts are certified in exact integer arithmetic (and also by floats with a rigorous error envelope). So an explicit counterexample is

> A = {P-smooth a : 2^888 < a ≤ 2^896}, n = 2^896, m = 2^889·Q (k = 111), or the same with 896/904/897 (k = 112),

with P = primes < 257 and Q = ∏ of the odd primes < 257.

## Objections

No MUST-level objection survives.

**O1 (SHOULD), proof note, Verification status:** "The server also checked that this is the exact negation of the original statement."
The Lean theorem `proof` (line 497) negates a *reformulation*: cross-multiplied ℕ inequality, `∀ a ∈ A, a ≤ n` in place of `A.max ≤ n`, and **no `1 ∉ A` hypothesis**. Dropping a hypothesis makes the universal statement stronger, so its negation is *weaker* than the negation of FC's statement. Jig's "exact negation" check therefore does not by itself refute FC's `erdos_488`. What refutes FC is the gist's own adapter (`Erdos488ExactAdapter.refutation`), which derives 1 ∉ A and clears the ℚ denominators. Fix: say "exact negation of Jig's root statement" and point to the adapter for FC.

**O2 (SHOULD), proof note:** "the original root is marked **refuted**, and the problem is **closed**."
This is Jig's internal status. In the files fetched today, FC PR #5297 ("solve(ErdosProblems): link formal refutation of 488") is still OPEN, and the erdosproblems.com page shows no accepted resolution. Fix: "closed on Jig".

**O3 (SHOULD), README:** "The declaration `Erdos488ExactAdapter.refutation : ¬ Erdos488ExactAdapter.proposition` matches the full right side of the collection's `erdos_488`."
It matches *textually*: our `stmt_match.py` shows the bodies identical after removing FC's one `--` comment, and our Bridge proves `fc_statement ↔ proposition := Iff.rfl` with rc 0. But both elaborations happen in the standalone file's import context (13 Mathlib modules). FC elaborates the same text under `public import FormalConjecturesUtil` (all of Mathlib plus FormalConjecturesForMathlib). No artifact compiles the refutation against FC's own elaborated term. The PR's `lake --wfail build` checks only the statement file.
Residual risk is low. I scanned FormalConjecturesForMathlib and FormalConjecturesUtil:
- The only global notations are `≫`, `≪` (Asymptotics), `∗` (sumConv), `→g` and `turing_machine%`. None of these tokens occurs in the statement.
- There is no global `open Classical`.
- The `binop%` ℚ elaboration and `Finset.max : Finset ℕ → WithBot ℕ` are core/Mathlib and the same in both contexts.
- The one thing that could differ is the `DecidablePred (· ∈ B)` instance picked for `Finset.filter`. Under full Mathlib it could differ, which would break `Iff.rfl`, but not the meaning (`Finset.filter_congr_decidable`).

Fix: compile `refutation` inside an FC checkout, or reword to "textually identical, with an `Iff.rfl` bridge in the standalone context".

**O4 (SHOULD, missed strengthening), proof note:** "**The proof establishes the existence of k in the finite range 0≤k<4096; it does not compute its value.**"
The value can be computed (see "Slow index" below). Smallest slow k = 111, and both 111 and 112 have exact-integer certificates; k = 110 is certified not slow. The note and paper should state the explicit counterexample. The Lean proof stays non-constructive: putting k = 111 in Lean would need a formal certificate for H(112) and H(111), which are about 10^50 and far beyond `decide`. That is fine; the non-constructive existence is fully proved.

**O5 (NIT), proof note:** "Then $c$ is positive and less than 257."
In fact c = j/a < 256T/T = 256. Both are true and the argument only needs c < 257, but the tighter bound is the one that explains why the band ratio is 256.

**O6 (NIT), README:** "It excludes generators0 and1": missing spaces.

**O7 (NIT), Lean replay log:** `Erdos488.lean:139:2: warning: exponent 4096 exceeds the threshold 256, exponentiation operation was not evaluated`.
This comes from the elaborator's guarded `Nat.pow` fast path, not from the kernel. `decide` at line 139 still closed `endpoint_gap` (no error at 139, compile rc 0, clean axioms), and the kernel rechecks `decide … = true`. The statement itself is independently true by exact Python integers with a 1601-bit margin. The warning is benign. It should not be read as "not checked".

**O8 (NIT), Lean replay controls, first round:** `controls.sh` logged `rc=$?` *after* a `$(date …)` substitution, so the first-round control rows in `steps.tsv` ("NegConst rc=0", "NegBridge rc=0") always read 0 and are void. The earlier seat caught this and re-ran the controls as `ctl2_*` with a correct rc. Only the ctl2 rows should be cited.

## Mathematics, step by step (attempted breaks)

- **(a) Covered set up to n equals A.** If a ∈ A and a | j ≤ 256T, then c = j/a < 256, so every prime factor of c is < 257. That makes j P-smooth, and T < a ≤ j ≤ 256T puts j in A. The converse is a | a. **Holds.**
  - Control: real P, every T in 1..64 plus 256, 40 random T up to 4096, and T = 4096, gives an exact equality of covered set and band (106/106).
  - Negative control: widen the band to (T, 258T] so cofactor 257 is possible. The check fails at T = 257 with witness 66306 = 258·257 (also at T = 300 and 1000). In the small analogue (T, 18T] with primes < 17 it fails at T = 17, witness 306.
- **(b) a ↦ (d, e mod 8) is injective and |A| ≤ 8H(k+1).** If e ≡ f (mod 8) and f > e, then 2^f·d ≥ 256·2^e·d > 256T. Also d ≤ a ≤ 256T = 256^{k+1}, so d is counted by H(k+1). **Holds.**
  - Control: 0 collisions in 106 real-parameter cases. The bound is loose: |A|/(8·H) = 0.32 at T = 4096.
  - Negative control: residues mod 3 with base 16 collide at T = 1 (2 and 16 both map to (1,1)).
- **(c) Far-count injection.**
  - c_d ∈ (T, 2T] by minimality (and d ≤ T forces e(d) ≥ 1), so c_d ∈ A.
  - r ∈ R gives r ≥ 1, because gcd(0, Q) = Q > 1. So c_d·r ≤ 2T(Q−1) < m, and the product is covered.
  - Injectivity uses only gcd(d, 2^{e'}·r') = 1 (d is odd and S-smooth, r' is coprime to Q). It never needs r odd, so even r is fine.
  - **Holds.** Control: real P, truncated R (4546 residues, 2337 of them even), T up to 4096 (5.3M pairs): 0 collisions, every c_d in the band.
  - Negative controls: dropping coprimality, allowing even d, or taking c_d one dyadic step too low each fail as they should.
- **(d) Pigeonhole and H(j) ≤ (8j+1)^53.** Exponents satisfy 2^e ≤ p^e ≤ 2^{8j}. If every step were fast, H(4096) > (3/2)^4096, which contradicts the margin in (2). The note's "≤" is weaker than the available strict "<", which is fine.
  - Exact H(0..4) = 1, 128, 9537, 397421, 10913534, all within the bound.
  - The same pigeonhole on the small analogue {3,5,7,11,13} finds its first slow step at k = 11, below its own N = 70.
- **(e) Final chain.**
  - 2m·M(n) ≤ 2·2TQ·12h = 48TQh. Since 3Q < 16φ, 48TQh < 256Tφh. And 256Tφh = n·hφ ≤ n·M(m).
  - T, h > 0, so the strictness is real. The direction is the strict reverse of the conjecture (the conjecture is n·M(m) < 2m·M(n)).
  - Implied density ratio ≥ (32/3)(φ/Q) = 2.1409 > 2. **Holds.**
- **(f) m > n** ⟺ Q > 128, and Q has 101 digits. **Holds.**
- **(g) k = 0 (T = 1).** Never selected: 2H(1) = 256 > 3 = 3H(0). Even if it were selected, every lemma is uniform in T ≥ 1, as Lean shows: `far_bound` needs only 0 < T, and `near_bound` and `band_nonempty_pow` hold for every k. Slow steps start at k = 111, so T ≥ 2^888. **No issue.**
- **Hypotheses of the problem.** A ⊂ (T, 256T] with T ≥ 1, so 0, 1 ∉ A. 2T ∈ A, so A is nonempty. max A = 256T = n, since 2^{8k+8} is in the band.

Note that the small analogue (primes < 17, band ratio 16) cannot close: its density ratio stays below 2 (0.86 to 0.97 at T = 1..256). The constants close only from band ratio 2^8 upward, because b = 8 is the least b with φ/Q > 6b/2^b. So no end-to-end brute-force instance exists. The lemma-level positive and negative controls above are the strongest available.

## Recomputed constants (`constants.py`, re-run, rc 0)

| quantity | value |
|---|---|
| \|P\|, \|S\|, max P | 54, 53, 251 |
| Q | 101 digits; Q > 128 |
| φ/Q | 0.2007065925246908562710268… |
| 16φ/(3Q) (needs > 1) | 1.0704351601316845667788… |
| (32/3)(φ/Q), the density-ratio floor (needs > 2) | 2.1408703202633691335576… |
| ∏_{p<257}(1−1/p) | 0.1003532962623454… (Mertens estimate 0.101252) |
| 2^4096·32769^53 < 3^4096 | True. Margin 1601.0 bits (1109.7 nats); bit lengths 4892 vs 6493 |
| smallest N with 2^N(8N+1)^53 < 3^N | 1199 (so 4096 has ample slack) |

## Slow index k (item 2)

**How the brackets are built.** S-smooth d ≤ 2^{8j} correspond one-to-one with exponent vectors satisfying Σ e_p·log2 p ≤ 8j. Using floored weights Wf_p ≤ R·log2 p can only admit more vectors, so Cf[8jR] ≥ H(j). Ceiled weights Wc_p ≥ R·log2 p can only admit fewer, so Cc[8jR] ≤ H(j). These hold by construction.

**Could this go wrong?**
- The weights were computed in floating point. `weights_exact.py` re-checks every one with exact integers (2^Wf ≤ p^R < 2^{Wf+1}, and Wc = Wf + 1) for R ∈ {256, 2048, 8192, 32768, 65536}: 0 violations. Its negative control (bumping the weight for p = 3) is caught.
- The DP is an unbounded-knapsack column cumsum. Positive control: the exact H(0..4) lie inside the brackets at R = 256 and at R = 2048 (also in float mode at R = 32768).
- Slow certification is 2·Hf(k+1) ≤ 3·Hc(k). Fast certification is 2·Hc(k+1) > 3·Hf(k). Both directions are correct.

**Results.**
- **Exact integers, R = 2048** (`slowk.py`, re-run, output byte-identical to the previous seat's apart from timing): certified fast for every k in 0..109; certified slow at **k = 112**:
  - 19663756308570290306837490615260075346157744638482 ≤ H(112) ≤ 19741959316398740655319416052621348910058319709095
  - 29358925658528546454237452718394053975124129342927 ≤ H(113) ≤ 29475817255257223914252285401859861991526186093434
  - 2·Hf(113) ≤ 3·Hc(112), so H(113)/H(112) ≤ 1.49899.
  - At this resolution k = 110 and 111 are undecided.
- **Floats with a rigorous a-priori envelope** (`slowk_float.py`):
  - Each pass is a recursive sum of nonnegative terms, so its relative error is at most γ_{K−1}. Errors compound as (1+ε)(1+γ), and the final cumsum adds γ_B. The envelope is ε = 3.35e-9 at R = 32768.
  - Validation: at R = 2048 the float values match the exact-integer run to 5.6e-15, against an envelope of 2.1e-10.
  - At **R = 32768**: certified fast for every k in 0..**110**, with H(111)/H(110) ∈ [1.50198, 1.50273]. Certified **slow at k = 111**, with H(112)/H(111) ∈ [1.49729, 1.49803]. Also slow at 112, 113 and 114.
- **Exact integers, R = 32768, by CRT** (`slowk_crt.py`):
  - The same DP is run modulo 8 primes just below 2^31 in int64. Overflow is ruled out by asserts (column sums < K·p < 2^63, final cumsum < (B+1)·p < 2^63).
  - The values are reconstructed by CRT from 7 moduli (product 2^216) and checked against the 8th.
  - Pipeline control: at R = 2048 the CRT output equals the object-int run exactly at j = 112 and 113.
  - Negative control (`crt_negctl.py`): corrupting one residue gives a 216-bit value and a failed 8th-modulus check.
  - Result: **fast (exact) for every k in 0..110; slow (exact) at k = 111 and 112.** The certificates:
    - k = 111: 2·Hf(112) = 39410360591540098718370042313028444795763055170406 ≤ 3·Hc(111) = 39462195293478174903254292422925002409644040614352
    - k = 112: 2·Hf(113) = 58841679874000150892623604895634073637014163864478 ≤ 3·Hc(112) = 59100877750480131439357408413857860371376896482982
    - Brackets: 13154065097826058301084764140975000803214680204784 ≤ H(111) ≤ 13157324965832306298340155879560221723747742638459, and 19700292583493377146452469471285953457125632160994 ≤ H(112) ≤ 19705180295770049359185021156514222397881527585203.
  - Consistency: these brackets nest inside the R = 2048 brackets, as they must. Finer floor weights can only lower the upper bound, and finer ceiling weights can only raise the lower bound.
  - A first attempt at exact object-int arithmetic at R = 8192 was stopped at the harness's 10-minute background limit with no output. It is superseded by the CRT run.

**Answer to item 2.** k = 110 is *not* slow: exact, H(111)/H(110) ∈ [1.50198, 1.50273]. **k = 111 is slow and is the smallest slow index**: exact, H(112)/H(111) ∈ [1.49729, 1.49803]. The ratio decreases steadily: k = 111 and 112 are certified slow in exact arithmetic, and 113 and 114 by the float envelope.

## Controls

**Python** (re-run; each output is byte-identical to the previous seat's):
- `controls.py`, rc 0.
  - Positive: near-count lemmas at real P (106 cases pass); far injection at real P (6 values of T, 0 collisions); small analogue near and far (43 cases pass).
  - Negative, all FAIL as expected: N1 (cofactor 17), N1' (cofactor 257), N2 (residues mod 3), N3 (coprimality dropped), N4 (even d allowed), N5 (c_d below the band).
  - Each negative control breaks exactly one hypothesis, and the per-check counts show it is the intended check that fails (for example N1 gives (174, 0, 0)). So the checkers can fail.
- `pigeonhole.py`, rc 0.
- `weights_exact.py`, rc 0, with its own negative control.
- `slowk_float.py`, cross-checked against the exact run.

**Lean** (replay already done; I read the logs and did not run Lean):
- Main compile: rc 0. `#print axioms` for both `proof` and `refutation` gives [propext, Classical.choice, Quot.sound].
- Bridge (`ctl2_Bridge`): rc 0, 0 errors. `FCBridge.fc_statement_false` has the same three axioms.
- **NegConst** (16 → 14 in `constant_ratio`): `decide` reports "proved that the proposition 3 * Q < 14 * phiOdd is false", rc 1, and sorryAx propagates into both audits. *Meaningful*: `decide` really evaluates the 53-prime products. The false variant is genuinely false, since 14φ/(3Q) = 0.937.
- **NegSorry** (`Q_large` proved by `sorry`): **rc 0**, but both audits list sorryAx. *Meaningful, with a lesson*: rc 0 is not a pass. The gate must be the axiom line, and the replay's gate used the axiom line.
- **NegBridge** (2 → 3 in the pasted FC body): `Iff.rfl` type mismatch, rc 1. *Meaningful but coarse*: it shows the bridge distinguishes a changed constant. It does not probe elaboration-level differences such as ℕ versus ℚ division. In any case it lives in the standalone context (see O3).
- No negative control exists for `endpoint_gap`'s `decide`. Its truth is covered independently by exact Python (1601-bit margin).

## Statement match

The adapter `proposition` is literally FC's body. After deleting FC's single `--` comment line and collapsing whitespace, the strings are identical (`stmt_match.py`, 0 opcodes). The FC body in the cached checkout 2f91d251 (2026-11-09) also equals `fc_488_main.lean` and `/tmp/e488/w/fc488_main.lean`. Item by item:
- Binders: `∀ᵉ (n : ℕ) (m > n)`.
- `letI B := {n ≥ 1 | ∃ a ∈ A, a ∣ n}`: a Set builder, since there is no expected type.
- `A.max ≤ n` in `WithBot ℕ`. The adapter produces it via `Finset.max_le_iff` and `WithBot.coe_le_coe`.
- ℚ division with casts at the leaves. The adapter applies `div_lt_div_iff₀` with (0:ℚ) < m and (0:ℚ) < n, which typechecks only for ℚ division.
- `0 ∉ A` and `1 ∉ A`: the adapter derives 1 ∉ A from the strict reverse inequality. The concrete A sits in (T, 256T] with T ≥ 1 anyway.

The erdosproblems.com statement fetched today, "Let A be a finite set and B = {n ≥ 1 : a | n for some a ∈ A} … for every m > n ≥ max(A)", agrees. The note correctly scopes itself to the multiples version, not the [Er61] non-multiples typo version.

FC context: see O3. The tokens and instances that could change meaning were scanned and none apply. The decidability instance is the only conceivable definitional difference, and it does not change meaning.

## Lean scan (read only)

- **Absent:** `sorry`, `native_decide`, `axiom`, `implemented_by`, `extern`, `unsafe`, `debug.skipKernelTC`, `ofReduceBool`, `trustCompiler`, `opaque`, `csimp`, `macro`/`syntax`/`notation`/`elab`/`infix`, `instance`, `attribute`, `open Classical`, `@[…]` attributes.
- **Options:** `set_option maxRecDepth` at 10000 (×3) and 20000, and `maxHeartbeats 0`. These affect resources only, not soundness.
- **`decide` sites (7):**
  - L46 `2 ∈ Nat.primesBelow 257`
  - L61 `oddPrimes.card = 53`
  - L139 `2^4096 * (8*4096+1)^53 < 3^4096` (see O7)
  - L449 `128 < Q`
  - L452 `3 * Q < 16 * phiOdd`
  - L470 `0 < 256`
  - L473 `1 ≤ 1` (membership of 1 in `Icc 1 T`)
- **Definitions match the note:**
  - `primes = Nat.primesBelow 257` (p < 257)
  - `oddPrimes = primes.erase 2`
  - `H k = |{d ∈ [1, 256^k] : d ∈ factoredNumbers oddPrimes}|`
  - `band T = (T, 256T] ∩ factoredNumbers primes`
  - `far_bound` counts `S ×ˢ {r < Q : Q.Coprime r}` with `Nat.totient_eq_card_coprime`
  - `exists_slow_H` uses the pigeonhole with `H_polynomial_bound 4096` and `H_zero_pos`.
- **Two statements differ by design:** the Jig-form `proof` (no 1 ∉ A; see O1) and the FC-form `refutation`.

## Files

`/tmp/e488/referee_R/`:
- constants.py
- controls.py and controls_rerun.out
- pigeonhole.py and pigeonhole_rerun.out
- weights_exact.py
- slowk.py and slowk_exact_rerun.out
- slowk_float.py, slowk_float_2048.out and slowk_float_32768.out
- slowk_crt.py, slowk_crt_2048.out and slowk_crt_32768.out
- crt_negctl.py and crt_negctl.out
- stmt_match.py
