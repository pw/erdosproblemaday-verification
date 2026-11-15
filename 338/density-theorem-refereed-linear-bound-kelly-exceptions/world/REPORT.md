# Literature / state-of-the-world seat (Opus instance) — Erdős #338, 2026-11-15
Saved by the 09Z erdos seat from the seat's reply (it could not write .md files itself). Sources it fetched are under
world/src/ (not in the public bundle: third-party papers and web captures).

## Main finding: close prior art that neither Veljjanoski's note nor our first draft cited
P. Erdős, M. B. Nathanson, A. Sárközy, "Sumsets containing infinite arithmetic progressions", J. Number Theory 28 (1988)
159–166 (renyi.hu/~p_erdos/1988-33.pdf; full scan read, pp. 161–162 checked by eye).
- The same Kneser form (p. 161): "either (i) d_L(hA) ≥ h·d_L(A) or (ii) there exists a minimal integer g ≥ 1 such that
  hA ∼ hA^(g) and d_L(hA) ≥ h·d_L(A) − (h−1)/g."
- Lemmas 1–2 turn repeated summands into distinct ones (Szemerédi: elements in the middle of long progressions inside A
  have full density; sums of h such elements are sums of h distinct elements of A).
- Theorem 1: d_L(A) = w ≤ 1/2, k = ⌈1/w⌉ ⇒ sums of k+1 distinct elements contain an infinite progression with difference
  ≤ k² − k; sums of k² − k distinct elements one with difference ≤ k + 1. The proof works for every s ≥ 1 with
  1 < g ≤ k + (k² − 2k)/s and in fact shows the sumset contains all large integers of a residue class mod g.
- Theorem 3 fixes a residue class with one extra distinct element.
- Lacks: bases, restricted order, robustness, the residue-generation step.
- Not stated by ENS, derived by us: with the residue-fixing elements set aside first, restricted order ≤ about 4⌈1/δ⌉
  for δ ≤ 1/2 (CLAIMS.md Theorem C).

## Q1. Theorem 1 / Theorem A in the literature? NOT FOUND as stated; ENS 1988 comes very close (above).
- HHP 2007 (two author versions read in full; journal version not reached). Plagne's copy (Sept 2006) uses the numbering
  Veljjanoski cites: Thm 1 (order-2 gaps; h ≥ 3 unbounded gaps), Conjecture 2 (k(h) finite), Thm 3 k(h) ≥ 2^{h−2}+h−1,
  Thm 4 f(h) ≥ 2^{h−2}+h−1 with restricted order exactly that, Prop 5, Conjecture 6, Prop 7, Thms 8–9 (Thm 9's proof uses
  the Erdős–Rado sunflower lemma = the disjoint-representation step), Thm 10 (conditional on Conjecture 2: if hA has
  density ≥ β, sums of a bounded number of distinct elements have bounded gaps). The hegyvari.web.elte.hu/artEB4.pdf
  version (Oct 2005) numbers things differently (no Theorem 9/10). Nothing there gives "positive density ⇒ restricted
  order" or a bound in terms of density.
- Kelly 1957 (paper not reached; zbMATH review Zbl 0077.26304): restricted order ≤ 4 for CLASSICAL bases of order 2
  (every non-negative integer a sum of two elements); ≤ 3 for asymptotic bases of order 2 with counting function
  ≥ Cx/log log x. Order 2 only.
- HHP 2003: abstract only (positive density of sums of distinct elements; #339). Chen–Li 2026: abstract.
  Chen–Yu 2023, Fang–Cheng 2025, Chen–Fang 2014: blocked by a captcha today, not re-read.
- Searches (OpenAlex, Semantic Scholar forward citations, arXiv last 12 months and last 30 days, MathOverflow): nothing new.

## Q2. Hennecart 2005: the paper itself was NOT reached.
Abstract: "any asymptotic basis of order 2 has a restricted order at most equal to 4. We also provide an example of an
additive basis of order 2 whose restricted order is 4." Reference list: Erdős–Graham 1980, Kelly 1957, Roth 1953.
Whether his construction is the same as, a variant of, or different from the ternary set, and whether he describes the
exception set: UNKNOWN.

## Q3. Kneser's theorem, s-fold: Kneser 1953 p. 463 and Halberstam–Roth Thm I.17′ p. 57 as quoted in a MathOverflow
answer (question 484732); ENS's form; HHP's; Jin 2010; Griesmer arXiv 2602.19014. No 0 ∈ A hypothesis in any.
The note's Step 2 is consistent with all of them.

## Q4. GitHub
- formal-conjectures #7788 (Kelly disproof): merged 2026-11-08T23:18Z by Paul-Lez; build and all checks green. The Lean
  set includes 0. It proves only that restricted order 3 fails.
- #6793: the problem file, merged 2026-10-19. #7620 (linrock): links an external Lean proof of the HHP variant; open, approved.
- #7779 (Veljjanoski): OPEN, approved 2026-11-04: adds the positive-density variant as an existence-only statement, with
  a Lean proof registered on Palomar (PALOMAR-2026-11-03-000016, repo veljjanoski/erdos338-palomar at a699263d);
  machine-checked; review by another AI agent, no human sign-off.
- #7783 (Bateman) and #7784 ("Kelly ≤ 4"): open, approved. #6868 (AItoBit): open; says it includes Lean proofs of our
  order-3 / restricted-order-6 example (Lean not checked by the seat).
- veljjanoski/erdos338: one commit 9429d6f (1 Oct). bitterlemma/erdos-338: one commit 2026-08-17.
- No earlier FORMAL disproof of Kelly's conjecture found.

## Q5. Discussion since 1 Oct: none found (forum thread 4 comments, last 1 Oct; commenting suspended; page unchanged since Sept 2025).

## What we may say
SAFE: Kelly's two theorems as in the zbMATH review; Hennecart's abstract; HHP's lower bounds and that their density
theorem is conditional and about gaps; Kneser's s-fold form; ENS 1988 as the closest prior work; the Palomar Lean proof
of the existence part and #7779 open/approved; #7788 merged 8 Nov 2026.
DO NOT SAY: that Theorem 1 or A is new/first without the ENS caveat; "HHP Theorem 9/10, Conjecture 2" pointing at the
artEB4.pdf version; that Kelly's ≤ 4 was for asymptotic bases; anything about what Hennecart's example is; that the Lean
proves restricted order exactly 4; that anyone has refereed or discussed the density theorem.
UNKNOWN: full texts of Hennecart, Kelly, HHP 2003, the HHP 2007 journal version; Chen–Yu, Fang–Cheng, Chen–Fang today;
Halberstam–Roth and Kneser 1953 in the original; papers citing ENS 1988 (titles only); MathSciNet reviews.
