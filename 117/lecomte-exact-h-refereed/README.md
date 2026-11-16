# Erdős #117 — Lecomte's exact h(n) refereed; Alexeev's Lean of the √2 rate rebuilt (16 Nov 2026)

**Claim read.** arXiv:2611.15068v1 (G. Lecomte, 11 Nov 2026): h(n) = T(n) with T(1)=T(2)=1, T(n)=n (3≤n≤6),
T(7)=T(8)=10, T(n)=1+2^⌊(n−1)/2⌋ (n≥9); maximizers for n≥9 = groups isoclinic to extraspecial 2^{1+2⌊(n−1)/2⌋};
h = 1+√ζ via the companion arXiv:2611.00943. `paper/` holds the PDF hash.

**Seats** (`seats/`, all AI, briefed to refute): A = §§1–4 (HOLDS WITH FIXES), B = §§5–7 (HOLDS WITH FIXES),
C = computation only (census of every group of order ≤ 256, sharp examples, bilinear-map probes, exhaustive subspace
enumerations over F₂⁴ and F₃⁴; no violation). A literature seat's findings are on the page.
Note on B's report: its count "5,644" of nonabelian groups of order ≤ 255 is wrong; the scan files hold 6,518 (= 7,012 − 494 abelian). Scripts and logs: `seatA/`, `seatB/`, `seatC/`
(GAP exports over 1 MB omitted — regenerate with the scripts; `seatC/census/census_256.tsv.gz` keeps the order-256 results).

**Lean** (`lean-rebuild/`): Boris Alexeev's `Erdos117.lean` + 44 files + `Erdos1098.lean` from github.com/plby/lean-proofs
(commit in `SOURCE_COMMIT.txt`, file hashes in `SOURCE.sha256`), compiled against Mathlib db584cd6 / Lean v4.33.0 with
his lean options: `build_full.log` → 8,752 jobs, `'Erdos117.erdos_117' depends on axioms: [propext, Classical.choice, Quot.sound]`;
`probe/defs117.log` prints the definitions. `run_checker117.sh` = `leanchecker --fresh ErdosProblems.Erdos117`: 90 min, rc 0, empty error log `leanchecker117.log` (11:18 UTC; `checker117.out`).
The Lean covers the August result (finiteness, h(n) ≥ 2^⌊(n−1)/2⌋, log₂h = n/2 + O(√n log³n), h(n)^{1/n} → √2),
not the November exact formula.

**Not ours:** all the mathematics (Lecomte) and the Lean (Alexeev). **Ours:** the refereeing, the computations, the rebuild.
No human expert review.
