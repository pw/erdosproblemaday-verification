
## 7. Citation table (scope)

§5 cites no external source. Its only citations are internal: setup:dilation, mesh:width, mesh:neighbors, count:eligible, outer:coloring, outer:pullback, and its own lemmas. Each was checked at the statement level in §5 of this report. The nearby Fox–Hunter remark on least-common-multiple dilations is in §2, outside this scope.

| cited result | claimed | actual | verdict |
|---|---|---|---|
| — (no external citation in 05-dichotomy.tex) | — | — | n/a |

## 8. Lean cross-reference (read as text, not built)

- `ShortPeriodLift.lean`, `short_period_affine_lift` (l. 59) and `AdaptiveMesh.short_period_cyclic_lift` (l. 125).
  - Hypotheses: `hmotion : k*|w i| < 1/2`, `halpha : M.alpha ≤ 1/q^D`, `hsmall : 2*H*(k+1) < 1`, and one repeated label pair `hsame`.
  - The cut is taken on a closed segment, 0 ≤ t ≤ k. This is the paper's short-period argument.
  - It confirms that a single repeated pair, not heaviness, is what the cut step uses.
- `LongPeriodEligibility.lean`, `heavy_long_block_eligible` (l. 74).
  - Hypotheses: `hD : 3 ≤ D`, `hsmall : 2*M/k ≤ 1/16`, `hnear : |v i| < 1/(1000 D)` for rotating i, `hperiod : D^2 < h/gcd(h, λ t_i)`, and `hheavy` (stationary |v_i| ≤ (2M/k)·width at the anchor).
  - These are exactly I9, I11, I8 and Lemma 5.4 at the heavy anchor. The formalization needed the same binding constants that §3 identifies.
- `HeavyIntervalWidth.lean`, `heavy_fiber_relative_width` (l. 48).
  - Hypotheses: `hscale : 2*M ≤ k`, `hsmall : 2H + 4MH/h < 1`, `hdrift : |v i| ≤ 4MH/k`. These are I1 and I5.

## 9. Verdict

**HOLDS AS READ.** I checked every step of Lemmas 5.1–5.4 and Theorem 5.5 line by line, with every large-k inequality given an explicit threshold (k ≥ 1056 suffices for all of §5). I found no hole in the human-readable proof. The two points the brief singled out are correct as written:
- **The short-period cut argument.** It uses the lattice w_i ∈ q^{−i}Z, the bound |w_i| ≥ α, and the fact that a crossing forces every V-width in that coordinate below |w_i|.
- **Lemma 5.4 in the longer-period eligibility (iii).** It is applied at a heavy index whose label may differ from the one that defined h; this is valid because there is only one global (h,t,u,v).

The finite model with the paper's own constants at k = 1056 confirms every intermediate claim, including block eligibility. Controls show that the model detects violations and that each failure lands at the step the proof says depends on the changed ingredient. The only defects are cosmetic: C1–C5.

---

## Appendix A. Scripts (verbatim)
