# Seat W (world / novelty) — reader submission 8gfcew, Erdős #1188 (Pedro Martins)
(Opus seat, 2026-11-02 ~09:03–09:22Z. Saved by the host from the seat's final message; harness blocked .md writes.
Supporting files referee/W/scratch/: snyder_zip/, gh/, papers/, claims1189.html, forum1189.html, history1188.html.)
Host re-checked W2 and W3 against the PDFs (js.pdf Lemma 7 + proof; dt_jis.pdf Cor 8) — quotes confirmed.

VERDICT (scope = prior art / novelty): HOLDS WITH NOTES. Headline (log F ≍ x log x; explicit x/2 − 3x/log x for x ≥ 40;
the 1 − log 2 upper constant) is new as far as these searches reach.

1. Snyder (Star Fleet Math, GPT-5.6 custom harness), proof-claims tab, 2026-07-15 01:59, 0 comments: log log F/log x → 1,
   Lean (`erdos1188_loglog_ratio_tendsto_one`). Zip read not built. Its F = page's F (Basic.lean: ValidClass 2 ≤ n, a < n;
   Int.emod; Covers; HasDistinctModuli; minimal ∀T ⊂ S, ¬Covers T; moduli in Icc 2 x). Key lemma
   `explicit_sparse_coarse_lower`: 2^(x/(2048·D·(log₂(x+1)+1)^4)) ≤ coveringCount x, D ≈ e^{3·10^7} (product of the first
   2^21−1 primes ×…), so log F ≥ c·x/(log x)^4, effective only for x beyond ~e^{3·10^7}; upper bound trivial (x+2)^{x+1}.
   Snyder's referee note: "sharper asymptotics such as the constant in log F ≍ x log x remain open."
   Martins strictly stronger both sides; Martins does NOT cite Snyder (grep snyder/starfleet/lean/formal: nothing) though
   p.4 says Thms 1.2+1.5 "give a short, elementary and fully explicit proof that log log F(x)/log x tends to 1".
2. teorth/erdosproblems HEAD b5867d6: status open (last_update 2026-04-04), formal_status unformalized, formalized yes (bot
   2026-08-07). FC 1188.lean: `@[category research solved, … formal_proof … starfleet/erdos-1188/Research/SparseAsymptotic.lean]`
   theorem erdos_1188 : Tendsto (log log F / log x) atTop (𝓝 1) — added PR #4578 (2026-08-07); open issue #4808 (status mismatch).
   Martins's Cor 1.6 implies FC's theorem. JustinSunPrize awards PR #673 formalised only the non-minimal remark.
3. Literature (coverage claims): arXiv title/abstract queries (0 for "minimal covering systems" in titles; "number of covering
   systems" 0), 39 covering-systems titles incl. Chen 2610.35139, FKK 2610.34541; author "Pedro Martins" 98 hits none relevant;
   5 web searches; OpenAI CONTENTS none. Controls found FKK, BBMST, other Martins papers. Not reached: Scholar, MathSciNet.
   Preprint on Zenodo only (23406127 15 Oct; 23427851 16 Oct; md5 bb78757936c6ac05bea41d6c6a2fbed4 both = our PDF); "v3" not public.
   chenhaoyu (thread, 3 Sep) G(24) = 5 irreducible sets = exactly Martins's five moduli sets for F(24) = 216.
4. FKK 2610.34541 exists; Cor 1: N < 10 (families of covering systems with pairwise disjoint moduli) — submission's sentence accurate.
   Dalton–Trifonov JIS 25 (2022) 22.9.1: Lemma 6, Cor 7 (accurately cited by Martins); Cor 8 (Krukenberg): "If p is a prime and a
   is a positive integer such that p^a(p+1) > d, then we can discard all congruences whose moduli are multiples of p^a" — a = 1
   gives P⁺(n)(P⁺(n)+1) ≤ x, i.e. Martins's Cor 1.4, slightly sharper; not cited. Jenkin–Simpson, Integers 3 (2003) A13 (= his [17]):
   Lemma 7 (sets of moduli, "unhelpful"), j = 1, same CRT argument (x_k ≡ x mod L, x_k ≡ x + k p^{j−1} mod p^α) gives the
   projection + Σ p^{−v} ≥ 1 of Thm 1.3. Agrawal et al. 2208.09720 (Integers 24A 2024): six-moduli classes + "24 technically
   different" systems on {2,3,4,6,12} — consistent with Table 1. BBMST frame credited.
5. Er80 p.95 (rendered, read): "Determine or estimate the maximum number j_x of covering systems … where all the n's are distinct
   and less than x … I expect that j_x tends to infinity very slowly." So "very slowly" is about j_x (bounded: Hough; < 10 FKK),
   not F. Page kept F on purpose (Bloom 17 Apr); no status label shown (site stopped 6 Oct).
6. Our site: tracker_data "1188" s:open, fz:1; statements_data shows FC "research solved"; ledger SKIP 2026-07-29 citing Snyder;
   index.js entry 489-394-starfleet (2026-07-25): "#336 and #1188 remain unverified by us … covering-system canonicalization for
   #1188". No /report/1188. Basic.lean settles the July canonicalization worry; we have still not BUILT Snyder's Lean.

Findings: W1 gap (attribution) — Snyder uncited; Thm 1.2 "improves (log x)^{3−o(1)}" should say it improves exp(x^{1−o(1)}).
W2 gap (attribution) — Thm 1.3 = Jenkin–Simpson 2003 Lemma 7 (j = 1); cite it. W3 gap (attribution) — Cor 1.4 = Krukenberg /
DT Cor 8 (sharper). W4 exposition — intro "irreducible covering systems with largest modulus x" should be "all moduli ≤ x";
"Erdős expected F(x) to grow very slowly" repeats the site's misattribution (Er80 says it of j_x). W5 exposition — Remark 5.2
attributes n_k ≤ 2^{k−1} to Simpson [23], who does not state it (BitterLemma, #1189 thread); Remark 6.5's derivation correct.
New in Martins: Thm 1.1 (log F ≍ x log x, c1 = 0.0672, 1 − log 2), Thm 1.2 (explicit, x ≥ 40), split construction / splitting
trees / Dickman constants, explicit upper bound + 1.5x all x ≥ 2, Thm 1.7 (k(x) ≍ x), Thm 1.8 / Cor 1.9 / anchor lemma, exact
F(x) for x ≤ 24 and k(x) for several x ≤ 48.
