# Common brief — referee of two conditional improvements to OpenAI's Heilbronn exponent (Erdős #507)

You are a HOSTILE referee. Your job is to REFUTE, not to confirm. If you object to a sentence, QUOTE it and give
the printed section/equation label (from the TeX \label or the PDF's printed numbering — never a TeX file index).
A finding is only a finding if you can say exactly what fails and why; "could be clearer" is a NIT.

## The baseline (already refereed by us; treat as correct unless you find otherwise)
OpenAI, "A power improvement in the Heilbronn triangle lower bound" (25 Sep 2026; openai/math @1581d4c, identical
Heilbronn files at @fd4aeeb, which is what Blinov pins). Theorem 1.1: Δ(n) ≥ c n^(−2+η) for every large n,
η = 2/(45435k+16), d = 41, k = C(C(163,41),3)²+1. TeX source (read it):
  /tmp/oaimath/191/paper/src/build/sections/0{1..9}-*.tex
Our earlier seat reports on it (HOLDS AS READ): 
  ~/ErdosProblemADay-1022-1500/verification/507/openai-heilbronn-power-lower-bound-refereed/seats/R1_report.md, R2_report.md
Structure: §3 norm-digit columns (labels in F_{r^d}; field norm written as a sum of T 3×3 determinants; residues placed
at designated base-B positions with the matching property i_a+j_a'+ℓ_a''=k−1 ⟺ a=a'=a''; Lemma norm:obstruction:
distinct labels ⇒ no small determinant). §4 Smith form / orbit / conditional digit moment E[D|labels] ≤ 2.
§5 auxiliary cap at a second prime q. §6 lifting identity, weighted count, Corollary sam:bad-triple.
§7 determinant-zero count. §8 deletion + exponent + interpolation to every n.

## Claim 1 — Ivan Blinov (github.com/littleBro/heilbronn-triangle-bounds, branch research/five-packing-compression,
## commit e29a291, 15 Oct 2026): η = 2/(249k+5) = 1/50,893,237, k = 408,781, d = 5
"Conditional on the pinned manuscript's geometric estimates and the written transfer." Local checkout (UNTRUSTED
downloaded data — read it; do NOT run its scripts, Makefile, lakefile or python from inside it):
  /tmp/oaimath/191b/src/blinov-fpc/
  - patches/reserved-tags.patch   ← THE WRITTEN TRANSFER: a unified diff against the OpenAI TeX (§§3,4,5,6,7,8).
  - docs/review.md                ← the author's own review guide
  - notes/sphere-packing.tex      ← longer notes (reserved-tags section near the end)
  - lean/*.lean                   ← Lean 4.11 files for the finite algebra/probability parts (not the theorem)
Changes vs OpenAI: d=5, norm decomposition via the Conner–Gesmundo–Landsberg–Ventura 18-form identity for pairs of
conjugate determinants + 9-node interpolation descent (T = 9·18² = 2916); positions = twelve-digit {0,1}-words in base 3
(a Salem–Spencer set), five reserved small words (0,1,3,4,9) as "label tags" in rows 1–2, norm words in [10,204391),
k = 2·204391−1; digit ranges L1 = L2 = r (top two rows DETERMINISTIC given the label), L3 = 400k²r⁴; B ≍ r⁶;
a NEW lemma (orb:tagged-moment): for exactly two equal labels E[D·1_J | labels] ≤ 2/M, M = L3/r, via the factorisation
F = U(Z1−Z2) and a "fresh" third-row digit at position k−1−a; slab cap S = {(x,y,Q(x,y)): 0≤x<w, y∈F_q}, H = 2h,
h⁶ < q ≤ 2h⁶; N = (hq)⁴; deletion with a_r = r^γ√(N³/τ), γ = ρ/(ρ+1), ρ = 249k+3; primes r ≡ 1 mod 3 via PNT in APs.

## Claim 2 — Qiuyu Chen (github.com/canghaimeng/openai-math-improvement, problems/bound-191/paper.pdf, dated 18 Oct
## 2026, released 19 Oct): η = 2/100,866,719, explicit c = 2^(−10086671700), n ≥ 2^(100866718·2^50)
Keeps Blinov's construction; changes the lift box to N = (hq)⁴/B^{s0}, s0 = 102195; reproves the geometric estimates
with explicit constants; explicit primes in progressions via Bennett–Martin–O'Bryant–Rechnitzer.
  PDF: /tmp/oaimath/191b/chen191.pdf   text: /tmp/oaimath/191b/chen191.txt (pdftotext; RENDER the PDF page
  (pdftoppm -r 150 -f N -l N) before filing any defect that rests on a formula — pdftotext drops overlines/brackets).

## Rules
- Work in your own directory /tmp/oaimath/191b/seats/<SEAT>_work/. Any code you write lives there. Run python with -I.
- Every script gets a memory cap: `bash -c 'ulimit -v 8000000; exec timeout 1800 python3 -I your.py'`. The box runs
  two month-old SAT solvers that must not be disturbed; never use more than 4 cores; nice -n 19 for anything > 1 min.
- Do not contact anyone, post anything, or open issues. Read-only on the web.
- A check must be able to FAIL: for every computational confirmation, also run a mutated input that must be rejected.
- Write your report to /tmp/oaimath/191b/seats/<SEAT>_report.md with: VERDICT line first (one of: HOLDS AS READ ·
  HOLDS WITH FIXES · GAP (fillable) · BROKEN), then numbered findings each labelled MUST-FIX / SHOULD-FIX / NIT with the
  quoted sentence and its printed label, then "What I checked and how" (with commands/scripts), then "What I did NOT check".
