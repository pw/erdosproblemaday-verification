# #488 reader submission dv8gfk — world report

Seat: separately briefed AI world seat (Claude Opus 5.5, web + gh tools), 20 Nov 2026, fetches 09:03–09:17 UTC.
erdosproblems.com not read (its robots.txt excludes AI agents since 19 Nov 2026); items attributed to that site come
from our own pre-wall dated notes or from Liu's preprint. Downloaded sources are kept privately (third-party papers are
withheld from the public mirror).

Bottom line: neither of the submitter's results is new. Gessel's 5 Sep 2026 counterexample uses essentially the same
proof as Theorem 1; the |A| ≤ 2 case was proved on paper in March 2026 and kernel-checked on Jig on 1 Sep 2026.

## Q1. Where #488 stands, 20 Nov 2026
- Formal Conjectures main (d8d031d, 2026-11-19): 488.lean still `@[category research open, question, AMS 5 11]`,
  byte-identical to the copy we used; last changed 14 Oct (7db2ea3). No `erdos_488.variants.*` (PR #2929, which tried
  to add one, closed unmerged 3 Mar 2026).
- PR #5297: open; labels erdos-problems, awaiting-author, solution found; REVIEW_REQUIRED; CONFLICTING; one commit
  (5 Sep). Toledo, 13 Nov: "What blocks the PR today is the merge conflict with `main`… a `formal_proof` link on a solved
  problem must now point to a Palomar entry (#7631)" (#7631 merged 29 Oct). Gessel, 14 Nov: "Sure, sounds good!… Happy for
  you to proceed". Toledo, 14 Nov: published github.com/carlostoledo1891/erdos-488-lean, "nothing has been submitted to
  Palomar". No other FC issue/PR on 488 since 11 Nov; none by Alicienn.
- teorth/erdosproblems (HEAD 5610470, 2026-11-19): `status: falsifiable`, `last_update: "2026-03-29"`,
  `formal_status: unformalized`.
- Jig 398: "Refuted"; statement 40 kernel-checked, filed 5 Sep 2026 20:25:47 GMT by @declangessel.
- Palomar: no entry for 488.
- aiXiv problem page: "Claimed disproved in aiXiv:2611.02020 (2026-11-19); no independent check recorded on aiXiv."
- Liu: concept DOI 10.5281/zenodo.23287740 lists only v1, v2 (last 2026-10-17).
- New to us: S. Girma, Zenodo 10.5281/zenodo.23977409, 5 Nov 2026, "On an Erdős problem concerning finite unions of
  multiples: counterexamples and positive results": "For y = c = 100 and Y = 10^87, the ratio exceeds 2.27. Two
  independently written programs certify this, one of them in exact integer arithmetic." "I prove it when A has at most
  three generators after removing redundant elements". (Abstract via DataCite; PDF not reachable.)
- arXiv (weak search), MathOverflow, Tao's blog through 14 Nov: nothing new on 488.

## Q2. Is Theorem 2 (|A| ≤ 2) known? Yes, including in Lean.
- P. Chojecki, 20 Mar 2026 (ulam.ai/research/erdos488.pdf): Thm 3.1 (singleton); Thm 3.2 ("Let 2 ≤ a < b and assume
  a ∤ b. Then for every m > n ≥ b, …"); Cor 4.7 ("If the primitive reduction Amin of A has size at most 3, then (1) holds
  for every m > n ≥ max A"); Lemma 2.1 B_A = B_{A_min}. Same reduction as the submitter's (4)/Remark 8; direct, not an
  induction. Singleton/one-tail/dense/union-bound ingredients checked in Lean per the PDF; the two-generator theorem not
  listed, no link. Prints the sharpness example A = {a}, n = 2a − 1, m = 2a.
- L. Ewing, 27 Aug 2026 (github.com/Luew2/erdos-488-size-7-candidate): "candidate exact computer-assisted proof" for
  primitive reductions of size ≤ 7; C++/Python certificates; "not been externally peer reviewed, independently
  reimplemented, or checked in a proof-assistant kernel"; "Eight generators remain open."
- shoal-rat (github.com/shoal-rat/erdos-488-lean): Lean, excess-based: "Every nonempty primitive G ⊆ {2,…,n} with
  E_G(n) ≤ 15 satisfies the original strict inequality"; refutes Chojecki's Conjectures 4.8 and 6.11.
- Jig 398, woshuajolk with Devin, 1 Sep 2026, all kernel-checked: statement 2 (singleton), 4 ("For A = {a, b} with a ≠ b
  positive, every n ≥ max(a, b) and every m > n satisfy n*M(m) < 2*m*M(n)"; TwoGen.lean, 185 lines, no sorry), 7 (every
  primitive set of size three), 11 (every primitive set of size four). In Jig's own wording, not FC's literal text.
- xccElephant/justin-sun-prize-lean (2026-10-17): `Erdos488.erdos_488_pair`, `erdos_488_singleton`,
  `erdos_488_sharpness`, no sorry, standard axioms; FC's filter and ℚ division, not FC's `A.max` form. Not built by us.
- Y. Wang, OSF 10.17605/osf.io/gtzra, 16 Sep 2026: Lean proof for five pairwise-coprime generators.
- Not formal: Asaria (28 Jul 2026), four pairwise-coprime generators; Dunzelman (11 Sep 2026), candidate |A_min| ≤ 4.
- W. Blair: |A| = 2 on the erdosproblems.com forum, 6 Jun 2026 (from our pre-wall notes; Liu: "the case |A| = 2 (W. Blair)").
- Least |A| for a counterexample: open (Liu Problems 18, 19). Lower bounds on |A_min|: ≥ 4 on paper (Chojecki, Girma),
  ≥ 5 kernel-checked (Jig 11), ≥ 8 if Ewing's candidate holds. No source states the smallest |A| of a known
  counterexample; all published ones are astronomical or unstated.

## Q3. The submitter's construction in print?
Mostly yes, as Gessel's proof (gist created 2026-09-05T22:27Z): same 53 odd primes below 257, scale 256 = 2^8, box bound
"H(j) ≤ (8j+1)^53", pigeonhole "There must be an integer k < 4096 satisfying 2H(k+1) ≤ 3H(k)", same lift
c_d = 2^{e(d)}·d ∈ (T, 2T], same exact count of cofactors coprime to Q; "The proof uses finite counting, unique
factorization, and exact integer comparisons"; "no decimal approximations enter the proof." Differences: A restricted to
one dyadic block (essentially Gessel's lifts); m = (2n)!·Q vs 2TQ; constants 6/5 over 3500 vs 3/2 over 4096 (n ≤ 2^28008
vs ≤ 2^32768). A primitive counterexample already in Jiang et al.'s CGM results/erdos_488.md (2026-09-26): "A is a
divisibility antichain (not required, but structurally clean)"; and primitivity is free (B depends only on A_min, max A_min
≤ max A). Jiang's construction (H = 2^16, simplex volume bounds, explicit Mertens bound c > 1/768, m = R^{N+k+1}) is the
closest prior to the (2n)!·Q device. Liu, Girma, Benefield, woshuajolk use smooth bands; Toledo certifies Gessel's proof.

## Q4. aiXiv 2611.02020 and traces
v1 Thu 19 Nov 2026 15:39:06 UTC; v2 15:43:46 UTC ("Metadata only… Paper unchanged"); 0 discussion posts, 0 reproduction
reports. Process notes: "Starting from the smooth-number counterexample reported in arXiv:2610.02945, the agent designed a
fully discrete proof with smoothness bound H = 256." Repo created 2026-11-17 18:57Z, 5 commits 17 Nov, CI green, 0 stars;
formalization.yaml `review: agent-reviewed`, Jiang `author_endorsement: "not-contacted"`. No PR to FC/teorth/Palomar.

## Q5. Jiang et al. (arXiv 2610.02945)
v1 2 Oct 2026 07:38 UTC, v2 6 Nov 2026 17:44 UTC; their write-up file dated 26 Sep 2026; all after Gessel. Claim:
d_A(m)/d_A(n) > 256/67 > 2. v1: "Problem 488… we found, after the Ansatz runs had been completed, that recent proofs had
also been obtained by other groups." v2 drops that sentence, lists "Previously known: Open". Lean status is
author-reported ("These research formalizations were not independently rebuilt for this paper"); their released
manuscript: "Note: verification is by an LLM referee plus numerical calibration, not a formal proof assistant." No public
Lean for their 488 result found.

## Sentences that would be FALSE in our review
1. "The first counterexample is Jiang et al.'s." 2. "Jiang et al.'s counterexample is formalized in Lean." 3. "Theorem 2
is new" / "the first Lean proof of |A| ≤ 2". 4. "The inequality is known to hold only for |A| ≤ 2." 5. "The submitter
gives the first elementary counterexample." 6. "The first counterexample with a primitive A." 7. "The first refutation
formalized against FC's statement." 8. "FC, teorth or Palomar lists #488 as disproved." 9. "The paper appeared on
17 Nov" (repo 17 Nov, paper 19 Nov). 10. "The smallest |A| for a counterexample is known." 11. "Liu has a version newer
than v2."

Side note on our own 11 Nov page: Girma (5 Nov, n = 10^89) and woshuajolk's Jig 41 (6 Sep, 2^392 ≈ 10^118) published
certified explicit instances before our page; any "first explicit counterexample" wording on our side would be false.
(Corrected on the page 20 Nov.)
