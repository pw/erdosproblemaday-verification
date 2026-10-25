# W report — world / novelty / citations seat, OpenAI "A quadratic bound for Jacobsthal's function" (Erdős #970)

STATUS: COMPLETE (2026-10-23 ~03:45Z). All seven questions answered below; every claim carries a URL/commit/date.

## Headline findings (what changes what we may claim)

1. **Bridge priority is NOT ours.** HJ van Veen (@30k30), github.com/30k30/scholia (first commits 2026-10-11T16:01Z), proved
   FC's `erdos_970` right-hand side (`erdos_970_solved`), FC's `Erdos687.erdos_687.parts.ii` (Y(x) = o(x²)) and
   `Green46.green_46.improve_upper` unconditionally from OpenAI's Lean, axioms [propext, Classical.choice, Quot.sound]; FC now links
   his file as the formal proof for 687.parts.ii and green_46.improve_upper (PR #7183 merged 2026-10-19). FC issue #6908 (mo271,
   2026-10-07) first noted the reduction. The only FC statement he did not restate verbatim is `erdos_970.variants.iterated_log`,
   whose bridge is the same one-line `Nat.sInf_le` (OAI's `IsJacobsthalBound` is character-identical to FC's). The files the
   prior W seat saved as `W_work/scholia_*.lean` are 30k30's, not ours.
2. **Replay priority is NOT ours.** Comparator replays of both challenges predate ours: cert-machine (≤2026-10-10, Lean +
   nanoda), 30k30 (10-11, Lean, fake-landrun), mathvet (10-12, Lean, real landrun), nealmcb (10-13 Lean; 10-15 Lean + nanoda);
   plasma-ai built + axiom-checked the quadratic declaration 10-07. Only possible distinction: none reports `leanchecker --fresh`.
3. **No reported error; no independent expert review of the 83-page proof found** (Bloom's 8 Oct blog explicitly disclaims
   review; Tao's blog silent; MO only Sawin's "aligns with conventional wisdom"). No competing proof of h(k) ≪ k².
4. **All checked citations MATCH** (Iwaniec 1978 p. 226 now accessed via Wayback; Vaughan p. 329; HS Thm 1.2; FGKMT §1.1 (1.2)/(1.3);
   Erdős 1962 p. 163 (1)–(3); CW Thm 4.4/§5 in arXiv v2; Ziller §3; BFT §§1.3–1.4). No erratum to the preprint (only commit
   adc7f124, 2026-10-06).
5. **erdosproblems.com/970 is stale and its lower bound is wrong-shaped**: "h(k) ≫ (log k)(log₃k)/(log₂k)²·k due to FGKMT" is
   Rankin's shape minus a log k; FGKMT gives k(log k)²log₃k/log₂k (confirms our July note). The current best (unrefereed,
   Lean-formalized by Alexeev, "more or less convinced this is correct" — Ben Green) is **h(k) ≫ k(log k)²/log log log k**, from
   GPT-5.6's Y(x) ≫ x log x/log₃x (Aug 2026), which OpenAI's paper does not mention. (§7)
6. **The paper also answers #687's "Y(x) = o(x²)?"** (Theorem 1.2 gives Y(z) < z²/(log z)² directly) — not stated in the paper;
   already recorded by 30k30, plasma-ai and FC 687.parts.ii (research solved). erdosproblems #687 page still says Y(x) ≪ x²
   (Iwaniec) is best.
7. Our page must not copy Bloom's blog slips ("contains an integer divisible by some prime in P"; "best previous lower bound
   ... ≪ (k log k)²") or the #970 page's OEIS link as if it were h(k) (A048669 is j(n); h(k) is A395279).


Scope: (1) status of #970/#687 everywhere; (2) prior third-party kernel replays; (3) independent scrutiny / errors /
competing proofs; (4) citation checks in source; (5) OpenAI's own catalogue claims; (6) small known values of h(k), j(P_k).

Reusing previous W seat fetches in /tmp/oaimath/021/seats/W_work/ (fetched ~00:09–00:18Z today); refreshing live pages.

## 1. Status of #970 / #687 (all fetched 2026-10-23 ~03:05Z unless stated)

**erdosproblems.com/970** (via Hetzner, HTTP 200; saved W_work/live1023/ep_970.html). Body text UNCHANGED since the
2025-10-20 revision (history/970 lists only "Current version" and "2025-10-20 00:00:00"). Still says
"Iwaniec [Iw78] proved h(k) ≪ (k log k)^2" and "The best lower bound known is h(k) ≫ (log k)(logloglog k)/(loglog k)^2 · k,
due to [FGKMT18]". No mention of OpenAI. No status label is rendered (site hid statuses ~10-06; the HTML has only the
status-widget JS). "Proof expositions (0)", "Comments (0)", "Proof claims (0)"; /forum/thread/970/proof-claims says
"No proof claims have been submitted yet."; /forum/thread/970 shows no comments and "The ability to post new comments has
been suspended." Formalised statement: Yes; OEIS A048669.

**teorth/erdosproblems** data/problems.yaml at HEAD (last commit to the file 9ca52af356, 2026-10-22T23:20:58Z, bot
"Auto-update formalization status from formal-conjectures"): entry 970 = `status: open (last_update 2025-08-31)`,
`informal_status: open`, `formal_status: unformalized`, `formalized: yes (2026-09-07)`, comments "Jacobsthal's function".
Entry 687 = `status: open (2025-08-31)`, prize $1000, `formalized: yes (2026-10-17)`. No issue/PR in teorth/erdosproblems
mentions 970, 687 or Jacobsthal (gh search, today).

**Formal Conjectures** `FormalConjectures/ErdosProblems/970.lean` at HEAD (repo HEAD c83a94d785, 2026-10-22T20:28Z; file last
touched 7db2ea3b91, 2026-10-14). `erdos_970` : `∃ C > 0, ∀ k > 0, (jacobsthalFunction k : ℝ) ≤ C * k^2` tagged
`@[category research solved, question, AMS 11, formal_proof using lean4 at ".../openai/math/blob/adc7f124.../Conclusions/QuadraticBound.lean#L13"]`;
`erdos_970.variants.iterated_log` tagged `research solved` with formal_proof link to IteratedLogBound.lean#L59. **Both
bodies are still `sorry`** (FC's convention: the external proof is linked, not imported). Docstring: "The bound h(k) ≪ k^2
was proved by an internal OpenAI model in September 2026 [OAI26a] ... The order of magnitude of h(k) remains open."
History of the file: 3dfd999dfe 2026-10-11 "mark problems solved in the OpenAI math release and link formal proofs" (PR #6898
by mo271, opened 10-07, merged 10-11); 75a6d3d52d 10-14 (question attribute); 7db2ea3b91 10-14 (remove Prop-valued answer).
FC issue #1045 (2025-10-12, closed) = original statement. No open FC PR touches 970.

**BRIDGE PRIORITY — ALREADY DONE BY A THIRD PARTY.** HJ van Veen (@30k30), repo github.com/30k30/scholia (created
2026-10-11T15:58Z; commits 70d96a4f9a 2026-10-11T16:01Z "Add proof for Erdős 687 and Green's Open Problem 46" … b072c89c3e
2026-10-16T18:10Z), folder `erdos-687/`:
- `bridge/Erdos687/Bridge.lean` (Mathlib only, hypothesis = the comparator statement written out) proves `Erdos687.little_o`,
  `Green46.improve_upper` and **`FC970.erdos_970_rhs` — "the right-hand side of formal-conjectures' erdos_970, from the
  quadratic bound"** against FC's definitions copied verbatim;
- `glue/JacobsthalTo687.lean` imports `OAI.NumberTheory.Jacobsthal.Main`, plugs in `erdos_970_quadratic` /
  `erdos_970_iterated_log`, and proves them unconditionally; `logs/bridge.log`: "'erdos_970_solved' depends on axioms:
  [propext, Classical.choice, Quot.sound]" and likewise `erdos_687_little_o`, `green_46_improve_upper`,
  `Green46.green_46.improve_upper`, `Erdos687.erdos_687.parts.ii`. README: statements were checked `rfl`-equal to FC's
  inside a copy of FC main. Built against openai/math fd4aeeb2 ("9,785 build jobs with 0 errors"). Prior W seat had saved
  these as W_work/scholia_Bridge.lean / scholia_glue.lean without recording provenance — they are 30k30's, not ours.
- FC links 30k30's glue as the formal proof of `erdos_687.parts.ii` (687.lean, "The linked Lean proof is by 30k30",
  JacobsthalTo687.lean#L325) and `green_46.improve_upper` (46.lean, #L319); FC PR #7183 (30k30, opened 10-11, merged
  2026-10-19T15:06Z); FC issue #6908 (mo271, 2026-10-07, closed 10-19) first flagged that the OpenAI bound answers
  green_46.improve_upper and that "the reduction from maxY to h ... is not part of the linked Lean proof".
- So: a Lean proof of FC's `erdos_970` statement (its RHS, sInf form) from OpenAI's Lean exists publicly since 2026-10-11
  (`erdos_970_solved` in 30k30's glue). Whether 30k30 also covered `erdos_970.variants.iterated_log` verbatim: the README
  lists only `erdos_970_rhs` (quadratic); not separately stated. Either way the FC→OAI bridge for 970 is a one-line
  `Nat.sInf_le` (the OAI comparator predicate `IsJacobsthalBound` is character-identical to FC's) — **not new, not ours.**
- Second, later party: AItoBit (github.com/AItoBit/erdos-687-quantitative-bound and AItoBit/jacobsthal-lean435, both created
  2026-10-18) — Lean 4.35 port of OpenAI's 819-module closure + an independent CRT transfer to Y(x) = O((x/log x)^2);
  README: "conditional transfer verified; unconditional solution pending", credits 30k30 as "prior formalization". Draft FC
  PR #7442 (open, 2026-10-18) "record a quantitative upper bound for Erdos 687", no formal_proof claim attached.

**#687** (erdosproblems.com/687, last edited 31 Aug 2026; history 2026-08-31 revision is the latest): still says "The best
known upper bound is due to Iwaniec [Iw78], Y(x) ≪ x^2"; best lower bound "due to GPT 5.6 Pro (see [4]) Y(x) ≫ x log x/logloglog x";
no mention of the OpenAI Jacobsthal paper; "Proof claims (0)", 1 comment (BorisAlexeev 2025-12-04, Er80 reference). The
question "can one prove that Y(x)=o(x^2) or even Y(x) ≪ x^{1+o(1)}?" — **the paper does settle the first sub-question**:
Theorem 1.2 directly gives Y(z) < ⌊z^2/(log z)^2⌋ for z ≥ z0 (any classes a_p, p ≤ z, leave ≥ cYV0/B^2 > 0 survivors in
[1, Y]), and Theorem 1.1 with Y(x)+1 = j(P(x)) ≤ h(π(x)) gives Y(x) ≪ x^2/((log x)^2 (loglog x)^2). The paper itself never
names Y(x) or #687 (grep of all sections: no "687"); the deduction is in 30k30's README ("Answer. Y(x) ≪ x^2/((log x)^2(loglog x)^2)")
and plasma-ai/erdos E0687 claim page (created 2026-10-07, status "claimed", scope partial, reads Theorem 1.2 directly).
Y(x) ≪ x^{1+o(1)}, Maier–Pomerance, and Erdős's o(y/log y) variant remain open. FC 687.lean: parts.ii (o(x^2)) =
`research solved` linked to 30k30; parts.i (Θ-order) and parts.iii (x^{1+ε}) `research open`.

**#4** page (fetched): the GPT 5.6 Pro prime-gap improvement and Bloom's 31 Aug 2026 exposition concern LOWER bounds for
Y(x); not related to this paper's upper bound.
## 2. Prior third-party kernel replays (searched by challenge name `Jacobsthal` / `JacobsthalImproved`, 2026-10-23)

All replays below are of openai/math's comparator configs `ComparatorChallenges/Jacobsthal.json` and
`ComparatorChallenges/JacobsthalImproved.json` (solution module `OAI.NumberTheory.Jacobsthal.Main`, 819 in-repo modules),
Lean 4.34.1, verdict "Lean default kernel accepts the solution" unless stated. Chronological:

| Who | Where (receipt) | When | Kernels | Notes |
|---|---|---|---|---|
| plasma-ai/erdos | wiki/problems/integer_sequences/E0970/claims/2026_09_25_openai.md (created 2026-10-07T05:29Z) | "verification of 2026-10-07" | Lean build + `#print axioms` (propext, Classical.choice, Quot.sound) + "pinned comparator fingerprint identical" | built `erdos_970_quadratic` at pinned revision; status `accepted` for the quadratic bound only; iterated-log "axioms checked 2026-10-07 but has not accepted it". Not a comparator/export replay as far as the page says. |
| carlostoledo1891/cert-machine | corpus/openai-math/kernel-runs/38019899278/{Jacobsthal,JacobsthalImproved}.json, commit d93dd5b48e 2026-10-10T08:34:51Z | ≤ 2026-10-10 | **Lean default kernel AND nanoda** ("nanoda kernel accepts the solution") | exit 0, okay true, 2852 s / 3296 s, build jobs 8924+9776, maxRSS ~8.7 GB, Azure runner with landlock. **Earliest dual-kernel replay found.** |
| 30k30/scholia (HJ van Veen) | erdos-687/logs/comparator_Jacobsthal.log, comparator_JacobsthalImproved.log, commit a2a8478b9f/ccac010ab2 2026-10-11T16:05Z | 2026-10-11 | Lean default kernel | `leanprover/comparator` d03acab, lean4export v4.34.0; **ran with a fake-landrun no-sandbox shim** ("WARNING: THIS IS NOT REAL LANDRUN!"). Plus the glue axiom check (bridge.log). |
| mathvet/mathvet | reviews/openai-math/evidence/cloud/Jacobsthal.comparator.txt ("comparator exit=0 end 2026-10-12T18:45:27Z"), JacobsthalImproved (end 18:55:52Z); commit ee7aa0603d 2026-10-15T06:57Z | 2026-10-12 | Lean default kernel, real landrun 0.1.17 (Landlock ABI v8) | fidelity-table verdict for 021: "full"; note "both the quadratic and the (log log 3k)^-2 improved bound are stated with elementary definitions". |
| nealmcb/openai-math-lean-tooling | results/cmp-all/configs.csv (commit 1e30e04692 2026-10-13T21:01Z "all 416 configs accepted"): Jacobsthal / JacobsthalImproved `accepted`, started 2026-10-13T08:42:15Z, nanoda False; results/kernel-pair-sweep.jsonl: started 2026-10-15T08:34Z / 08:59Z | 2026-10-13 (Lean), 2026-10-15 (Lean + nanoda) | Lean kernel ("replay 316103 ms" / "311348 ms") **and nanoda** (rc 0, 134,298 / 134,312 decls) | export 1.50 GB each. |
| korbonits | public/assets/data/2026-10-19-openai-math-audit.tsv (commit c308a2f1c9 2026-10-20) | 2026-10-19 | none — statement/coverage audit only | row 021: coverage MAIN → FC ErdosProblems/970.lean, "Already stated with OAI reference". |
| AItoBit/jacobsthal-lean435 | created 2026-10-18 | — | none claimed | Lean 4.35.0-rc2 port of the 819-module closure; README "candidate port; not yet verified on this toolchain". |

**Replay priority: ours is at best the 5th–6th independent replay.** Dual-kernel (Lean + nanoda) replays predate ours:
cert-machine (≤10-10) and nealmcb (10-15). Our `leanchecker --fresh` run may be the first *leanchecker* replay of this
closure (none of the above report leanchecker; cert-machine/nealmcb use comparator's export + Lean/nanoda kernels) — that
is the only distinguishing feature I can see, and it is a method difference, not priority.
## 3. Independent mathematical scrutiny / reported errors / competing proofs (searched 2026-10-23)

**No independent expert assessment of the Jacobsthal proof found, and no reported error.**
- Thomas Bloom, "Erdős problems in the OpenAI proofs", erdosproblems.com/forum/thread/blog:10, 8 Oct 2026 (re-fetched today;
  last comment 10 Oct, none on 970): lists [970] among 25 problems, "This PDF claims a proof ... This proof has been formalised.
  The PDF is 83 pages long." Explicit disclaimer: "I have not yet looked at in any serious way any of the proofs in this release
  ... I have also not ... checked myself that the formalisation compiles or that the statement in the challenge file accurately
  captures the problem. This post should not be read as any kind of endorsement". ⚠ His summary contains two slips our page must
  not copy: "every interval of length h(k) contains an integer divisible by some prime in P" (should be: coprime to every prime
  in P) and "The best previous lower bound known was h(k) ≪ (k log k)²" (that is the Iwaniec UPPER bound). He also notes [970]
  is on the FrontierMath Erdős list (Epoch FME: 68 problems open as of Aug 2026; FME table row "Erdos970 Jacobsthal’s function
  satisfies h(k) ≪ k²").
- Terence Tao's blog: site search "Jacobsthal" returns only 2014 and 2024 posts; Oct 2026 feed (to 22 Oct) has no Jacobsthal
  post. (6 Oct 2026 guest post by Bloom = site-changes announcement.)
- MathOverflow: only hit is Will Sawin's answer (2026-10-09, q/515849 "How many of the results released by OpenAI went against
  the conventional mathematical wisdom?") placing "021 (bounds for Jacobsthal's function)" among results that "align with
  conventional wisdom" — no correctness comment. MSE: nothing relevant.
- X: recent-search (7-day window only, API limit) "Jacobsthal": two arXiv-bot posts about Jacobsthal *numbers*; nothing on this
  paper. Older X history not searchable from our API tier → NOT FULLY CHECKED.
- Hacker News (Algolia, prior seat's fetch hn_jacobsthal.txt): no relevant hit.
- Third-party reading pages: plasma-ai/erdos E0970 claim (created 2026-10-07): accepts the *Lean* quadratic statement; "The prose
  proof of the manuscript was read for its structure only and is not reviewed here ... no outside reviewer is known here to have
  examined the result." 30k30 README: "Not covered: The paper's prose." mathvet fidelity verdict "full" = statement fidelity, not
  proof review. Nobody has published a line-by-line review of the 83-page argument.
- arXiv (API via Hetzner today; queries abs:"Jacobsthal function", abs:"Jacobsthal's function", abs:Jacobsthal AND cat:math.NT):
  no 2026 paper on upper bounds for h(k) or j(P_k). Hits are Jacobsthal *numbers*/sums, Jaffe 2610.17267 (Frobenius problem;
  cites Hajdu–Saradha and Costello–Watts only), Kalmynin–Konyagin 2302.00459 (polynomial analogue, 2023). The OpenAI manuscript
  itself has no arXiv version.
- **Earlier/simultaneous independent proof of h(k) ≪ k²: none found.** Last human upper-bound improvement remains Iwaniec 1978;
  the AItoBit/30k30 work is downstream of OpenAI's.
## 4. Citations checked in their sources (paper reference numbers per its printed bibliography: [2] CW, [3] Erdős 1962, [11] HS, [15] Iwaniec 1978, [25] Vaughan)

| Paper's claim (printed locator) | Source accessed | Verdict |
|---|---|---|
| "Iwaniec's shifted-sieve argument removed two logarithmic factors and established h(k) ≪ k² log² k for arbitrary prime sets [15, Theorem and Corollary, p. 226]" (§1, p. 3) | Iwaniec, Demonstratio Math. 11 (1978) 225–231, Wayback copy of the De Gruyter PDF (web.archive.org/web/20241110235611/https://www.degruyter.com/document/doi/10.1515/dema-1978-0121/pdf), W_work/cited/iwaniec1978.pdf, rendered p. 226 | **MATCH.** p. 226: "Theorem. There exists an absolute constant c > 0 such that for arbitrarily chosen primes q₁,…,q_r, r > 1 each interval of the length c(1−1/q₁)⁻¹…(1−1/q_r)⁻¹ r² log r contains at least r² integer numbers coprime to q₁…q_r. Corollary. We have C(r) ≪ r² log² r." |
| "Iwaniec's work on the error term in the linear sieve gave an estimate of order k² log² k when the prime divisors are the first k primes [Iwaniec1971]; this primorial case is distinguished explicitly in [25, p. 329] and [15, pp. 225–226]" | Iwaniec 1978 pp. 225–226; Vaughan p. 329 | **MATCH.** Iwaniec 1978 p. 226: "let C₀(r) be the maximal length ... each divisible by one of the first r primes ... while in [3] it is proved (1) C₀(r) ≪ r² log² r", [3] = "On the error term in the linear sieve, Acta Arith. 19 (1971) 1–30" (p. 231). Vaughan p. 329: "Iwaniec (2, Theorem 2) has shown this [C arbitrarily close to 2] in the special case when n is the product of the first r primes". Iwaniec 1971 itself NOT ACCESSED. |
| "Vaughan then proved the uniform estimate j(n) ≪ ω(n)²(log 2ω(n))⁴ (n>1) [25, Theorem, p. 329]" | Vaughan, Proc. Edinburgh Math. Soc. 20 (1977) 329–331, Cambridge Core open-access PDF (doi 10.1017/S0013091500026560), W_work/cited/vaughan1977.pdf, rendered p. 329 | **MATCH.** "Theorem. Suppose that n > 1. Then g(n) ≪ ω(n)²(log 2ω(n))⁴." (Vaughan's g = paper's j.) |
| "Vaughan explained the exponent 2 through the one-dimensional sieve's restriction to moduli near the square root of the interval length [25, p. 329]" | same | **MATCH.** "That 2 is the best that can be done by the method below is due to the usual inability of the one dimensional sieve to handle moduli larger than about the square root of the length of the interval under examination." |
| "Vaughan suggested the stronger possible estimate j(n) ≪_ε ω(n)^{1+ε} [25, p. 329]" (p. 3) | same | **MATCH.** "It is probably true that g(n) ≪ ω(n)^{1+ε} (3)". |
| "Hajdu and Saradha proved equality for k ≤ 23, but found j(P₂₄) = 234 < 236 = h(24) [11, Theorem 1.2]" (p. 3) | HS author PDF (math.unideb.hu/.../jacobsrevsaradha.pdf = the bib's url), W_work/cited/hajdu_saradha.txt; Math. Comp. version NOT ACCESSED (AMS page returned HTML) | **MATCH (notation swapped correctly).** "Theorem 1.2. We have H(r) = h(r) for r ≤ 23 ... Further, 236 = H(24) > h(24) = 234", where HS's h(r) = j(p₁…p_r) and H(r) = max_{ω(n)=r} j(n) (= the paper's h). |
| "see also [11, Lemma 2.1]" for classes ⇔ translates (p. 4) | same | **MATCH.** Lemma 2.1: j(n) = k+1 with k the largest such that {1,…,k} is covered by the prime divisors of n. |
| FGKMT: "j(P_k) ≫ k(log k)² log₃k/log₂k (1.1) [FGKMT, Section 1.1]. Indeed, their covered-interval bound at prime cutoff x is ≫ x log x log₃x/log₂x; take x = p_k" (p. 3) | arXiv:1412.5029v3 (W_work/src), §1.1; published JAMS version not separately accessed | **MATCH.** §1.1 eq. (1.2) "Y(x) ≫ x log x log₃x/log₂x" and (1.3) "Y(x) = j(P(x)) − 1"; x = p_k, p_k ~ k log k gives (1.1). (FGKMT §1.1 also says "The best upper bound known is Y(x) ≪ x², which comes from Iwaniec's work".) |
| erdosproblems.com/970's stated lower bound "h(k) ≫ (log k)(log log log k)/(log log k)² · k, due to FGKMT" | — | **WEAKER THAN, AND MISATTRIBUTED.** It is not FGKMT's form; it is Rankin's shape c₁r(log r)²log₃r/(log₂r)² (as quoted by Erdős 1962 eq. (2) and HS p. 2) with one factor log k dropped. FGKMT + x = p_k gives k(log k)² log₃k/log₂k (= the paper's (1.1)) — **confirms our July report.** It is a true but non-best bound. Current best (unrefereed) is k(log k)²/log₃k — see §7. |
| "Erdős subsequently recorded Jacobsthal's question whether h(k) ≪ k² [3, p. 163, equations (1) and (3)]. In Erdős's notation, C(k)+1 is the maximum of j(n) over integers with exactly k distinct prime divisors"; "Brun's method gives h(k) ≪ k^{C₀} [3, p. 163]"; "Rankin's lower-bound construction beside Brun's polynomial upper bound [3, p. 163, equation (2)]" | Erdős, Math. Scand. 10 (1962) 163–170, W_work/cited/erdos1962.pdf rendered p. 163 | **MATCH** on all three. (1) "max g(n) = C(r)+1" over ν(n) = r; (2) "c₁r(log r)² logloglog r/(loglog r)² < C(r) < c₂r^{c₃}. The left hand side of (2) is a result of Rankin [8] and the right hand side follows easily from Brun's method."; "Jacobsthal asked (in a letter) if (3) C(r) < c₄r² is true." |
| "Costello and Watts obtained recursive lower bounds for the minimum number of integers coprime to P_k in an interval, and used them to compute upper bounds for j(P_k) [2, Theorem 4.4 and Section 5]" (p. 3) | arXiv:1208.5342v2 (14 Sep 2012) only; published Math. Comp. 84 (2015) version NOT ACCESSED (AMS returned HTML) | **MATCH in arXiv v2**: §4 "A lower bound on ϕ_min(m,k)", Theorem 4.4 (recursive lower bound for ϕ_min(m,k)); §5 "Computations" gives b(k) with h(k) ≤ b(k) ≤ 0.27749612254 k² log k for 50 ≤ k ≤ 10000 (their h(k) = j(P_k)). Numbering in the journal version unverified. |
| "Ziller computed the maximum over arbitrary prime sets through 43 prime factors [Ziller, Section 3]" (p. 3) | arXiv:1903.11973v2 | **MATCH.** Abstract: "computed the maximum Jacobsthal function for the product of k primes up to k = 43"; §3 "Results", Table 2 (k = 20…43). |
| "the interval-sieve quantity studied by Banks, Ford and Tao [Sections 1.3–1.4]. They minimize the survivor count over all choices of forbidden classes at primes up to (y/log y)^{1/2} in an interval of length y. At that cutoff a classical lower sieve gives a bound of order y log log y/(log y)²" (p. 4) | arXiv:1908.08613v3 (2025, the "corrected version" the bib names) | **MATCH.** §1.3 defines S_z (1.9); §1.4 (1.11) W_y := min #([0,y] ∩ S_{(y/log y)^{1/2}}) over all classes; (1.12) "(4+o(1)) y log₂y/log²y ≤ W_y ≤ y/log y + O(y log₂y/log²y), the lower bound being a consequence of Iwaniec's theory ... of the linear sieve". |
| linear-sieve functions f, F [MontgomeryVaughanII, Section 21.2.2] | MV II author draft (W_work/cited/mv2.txt) | **MATCH** (TOC: "21.2.2 The differential delay equations", in §21.2 "The Rosser–Iwaniec sieve"). Content not re-derived here. |
| Jacobsthal 1960 [17]; Iwaniec 1971 | — | NOT ACCESSED. |
## 5. OpenAI's own catalogue (github.com/openai/math, HEAD 1581d4cbdd 2026-10-12T21:55Z)

- CONTENTS.md, family 021: "**021. A quadratic bound for Jacobsthal’s function.** Answers Jacobsthal's quadratic-bound
  question: every interval of Ck^2 consecutive integers contains an integer coprime to any prescribed positive integer with
  at most k distinct prime divisors, for an absolute constant C. The bound is uniform over prime sets and interval positions
  and removes the classical logarithmic loss." Paper blurb: "We prove h(k) ≪ k^2/(log log(3k))^2, giving an affirmative
  answer to Jacobsthal's quadratic-bound question."
- lean/docs/021.md (unchanged since adc7f124 Initial commit 2026-10-06): "The formalization proves the paper's strengthened
  Jacobsthal bound h(k) ≤ Ck^2/(log log(3k))^2 for one absolute C>0 and every k≥1. Intervals may begin at any signed
  integer. The earlier quadratic bound is also retained as a separate statement; the optimal order of growth is not
  determined." Comparator links: Jacobsthal.lean (`OAI.Erdos970.Erdos970Final.erdos_970_quadratic :
  JacobsthalQuadratic`) and JacobsthalImproved.lean (`erdos_970_iterated_log : JacobsthalIteratedLog`), both stated with
  only Mathlib definitions (`IsJacobsthalBound k m := ∀ n>0, n.primeFactors.card ≤ k → ∀ a : ℤ, ∃ i < m, (a+i).natAbs.Coprime n`).
  Jacobsthal.json: permitted_axioms [propext, Quot.sound, Classical.choice], definition_names [], enable_nanoda false.
  So the claim is the WHOLE theorem with no extra hypotheses/axioms. lean/formalization.yaml lists only the quadratic
  declaration as the article's formal result (QuadraticBound.lean), though the iterated-log comparator also exists.
  External Lean packages in the cone (mathvet fidelity-table): AbsorptionCutoff, PrimeNumberTheoremAnd, StrongPNT.
- Errata / revisions: commits touching `preprints/A-quadratic-bound-for-Jacobsthals-function-September-25-2026` = only
  adc7f1241b (2026-10-06, Initial commit); same for lean/OAI/NumberTheory/Jacobsthal and lean/docs/021.md. history.md
  (Oct 7 update: 3 withdrawals, 14 revisions) does not mention Jacobsthal/021. Our local paper.pdf git-blob hash
  869f5902d50e… = the repo blob at HEAD. **No erratum or revision of this preprint.**
- README generic caveat: "This collection includes results at different stages of verification ... Some of the
  unformalized results could have issues." (021 is formalized.)
## 6. Small known values (for the page's data panel)

Sources (fetched 2026-10-23 via Hetzner, OEIS JSON + b-file):
- **h(k) = max_{ω(n)≤k} j(n)** (the paper's h; = H(k) of HS/Ziller since j is monotone under adjoining primes): OEIS
  **A395279** (Jeffrey Shallit, created 2026-04-19, "Jacobsthal's function H(n)"), terms n = 1..43, from Hajdu–Saradha 2012
  (Table 1, r ≤ 24) and Ziller 2019 (Tables 1–2, k ≤ 43). **Largest k known exactly: 43, h(43) = 610.**
  2,4,6,10,14,22,26,34,40,46,58,66,74,90,100,106,118,132,152,174,190,200,216,**236**,258,264,284,300,312,332,354,378,390,420,
  438,462,482,500,520,544,566,588,610 (k = 1..43). Cross-checked: HS Table 1 (r ≤ 24) and Ziller Table 2 (k = 20..43) agree
  term by term with A395279.
- **j(P_k)** (primorial): OEIS **A048670**, b-file "Table of n, a(n) for n = 1..64" by Andrzej Bozek ("Computation of
  a(62)-a(64) was supported by Google Cloud", 2021); a(1..57) Gerbicz table; Hagedorn 2009 (k < 50). **Largest k known: 64,
  j(P₆₄) = 1110.** Values k = 44..64: 616, 642, 660, 686, 718, 742, 762, 798, 810, 834, 858, 876, 908, 926, 954, 978, 1002, 1030,
  1058, 1098, 1110. (A058989 = A048670 − 1 = Y(p_k).)
- h(k) ≠ j(P_k) first at k = 24 (236 vs 234); per Ziller §3.1 equality also holds only at k = 25, 26, 28, 29, 31, 32 in 25..43.
- ⚠ The OEIS id on erdosproblems.com/970 is **A048669 = j(n) for every n** (not h(k)); the h(k) sequence is A395279.
- Computed upper bounds beyond the exact range (primorial only): Costello–Watts b(k) ≤ 0.27749612254 k² log k for 50 ≤ k ≤ 10000.

Ratio table (pure arithmetic on the above; natural logs):

| k | h(k) | j(P_k) | h/k² | h/(k²/(log log 3k)²) | h/(k² log² k) |
|---|---|---|---|---|---|
| 10 | 46 | 46 | 0.460 | 0.689 | 0.087 |
| 20 | 174 | 174 | 0.435 | 0.864 | 0.049 |
| 24 | 236 | 234 | 0.410 | 0.865 | 0.041 |
| 30 | 332 | 330 | 0.369 | 0.834 | 0.032 |
| 40 | 544 | 538 | 0.340 | 0.834 | 0.025 |
| 43 | 610 | 600 | 0.330 | 0.825 | 0.023 |
| 64 | — | 1110 | 0.271 | 0.746 (j(P_k)) | 0.016 |

Caveat for the page: at k ≤ 64, log log 3k ∈ [0.1, 1.67], so these ratios say nothing about the asymptotic constant C (which
is not explicit and, by the paper's use of Siegel–Walfisz, ineffective per 30k30's README); h(k)/k² is visibly *decreasing*,
consistent with any of the conjectured shapes (h(k) ≈ k log²k-ish), so the data cannot distinguish k² from k²/(loglog)².

## 7. The GPT-5.6 lower bound Y(x) ≫ x log x / log log log x (coordinator's added question; fetched 2026-10-23 ~03:30Z)

**(a) What is claimed, where, and its standing.**
- erdosproblems.com/687 (last edited 31 Aug 2026): "The best lower bound is due to GPT 5.6 Pro (see [4]) Y(x) ≫ (log x/logloglog x)·x,
  improving on a previous bound of [FGKMT18]." erdosproblems.com/4 (last edited 31 Aug 2026): gap bound improved "to
  ≫ (log log n/log log log log n) log n by GPT 5.6 Pro (prompted by DottedCalculator)".
- /forum/thread/4/proof-claims: "There are 2 proof claims (partial or full)" with the site's standard disclaimer ("Appearing on this
  page is no guarantee of proof correctness, and does not mean that anyone associated with this site has examined any part of the
  proof").
  1. "claimed by GPT 5.6 Pro (using GPT 5.6 Pro)", submitted 2026-08-26 01:55:32 by DottedCalculator; external link
     github.com/DottedCalculator/ai-math/blob/main/Erdos_4_GPT_5.6_Sol.pdf (single commit 9ed1cea565, 2026-08-26T01:30Z). The PDF
     is titled "A Tilted Residue-Class Construction for Long Prime-Free Intervals", author line **"GPT 5.6 Sol"**, dated 25 August
     2026; abstract: "Y(X) ≫ X log X/log₃ X, G(T) ≫ log T log₂ T/log₄ T". Uses "two precisely stated results of FGKMT" as
     external inputs. (Model naming is inconsistent: the site says "GPT 5.6 Pro", the PDF says "GPT 5.6 Sol".)
  2. "claimed by OpenAI (using GPT-6 Astra)", submitted 2026-09-04 by BorisAlexeev: G(X) ≫ log X (log₂X)² log₄X/(log₃X)², via
     a "short translates" proposition — this improves only the step from Y to G, **not Y(x) itself** (comment by Xiao Hu
     2026-09-04: "This improves only over the trivial inequality G(P+Y+x)≥Y, without touching Y"; Bloom 2026-09-04 calls it a
     "99% Jacobsthal function" idea). Paper: openai/LongGapsBetweenPrimes (created 2026-09-02) / cdn.openai.com long_gaps.pdf. **Irrelevant to h(k).**
- Comments on claim 1 (thread /forum/proof-claims/224/comments, 31 comments): Ben Green (2026-08-26 14:59) "survives an initial
  plausibility check ... the exposition is truly horrible ... verifying/understanding the argument will take a bit of time";
  **Ben Green (2026-08-27 18:55): "Following a few hours thought and some conversations with Terry Tao and James Maynard I became
  more or less convinced this is correct. ... a lean formalisation exists so we know it's correct, and experts closest to the area
  basically understand informally what the key ideas are"** (6 likes); Green (08-28): "some subset of [FGKMT] (including G) will be
  doing exactly this [a human write-up] ... on a human timescale which I would anticipate being O(1) months". Boris Alexeev
  (2026-08-27 17:19): "This result has been formalized unconditionally in Lean" → github.com/plby/lean-proofs
  src/latest/ComparatorChallenges/ErdosProblems/Erdos4.lean. Bloom (08-27): the claim "should be partial".
- Bloom's exposition on #4 ("last edited 31 Aug 2026"): "The new GPT argument improves this further to Y(X) ≫ (1/L₃) X L₁"
  (L_k = k-fold iterated log); he sketches only the weaker Y(X) ≫ X L₁/(L₂L₃) and says the further L₂ "combines these ideas with
  the existing work of [FGKMT18]"; "heuristic sketch ... some of the omitted technicalities are quite substantial".
- **Lean**: plby/lean-proofs (Boris Alexeev). The comparator challenge Erdos4.json pins `Erdos4.erdos_4`, `Erdos4.fgkmt18`,
  `Erdos4.Tilted.all_endpoint_consecutive_prime_gaps` (the **gap** bound G(X) ≫ log X log₂X/log₄X), permitted axioms the standard
  three, `enable_nanoda: true`. The **covering bound itself** is proved in-repo as `Erdos4.Tilted.covering_theorem :
  ∃ c X₀ > 0, ∀ X ≥ X₀, c·X·log X/log log log X ≤ maximumCoverLength X` (src/latest/ErdosProblems/Erdos4Tilted.lean, commit
  20b8b276b5 2026-08-27T17:10Z), where `maximumCoverLength X = Nat.findGreatest (BoundedCover ⌊X⌋) (primorial ⌊X⌋)` and
  `ResidueCover y` = one residue per prime in a finite prime set covering every 1 ≤ i ≤ y — i.e. Y(⌊X⌋). **It is not one of the
  comparator-pinned theorem names**, so a comparator run certifies the gap statement, and the Y statement only as an
  intermediate declaration (we did not replay it).
- Refereed/published: **no**. No arXiv version (searched arXiv API today: ti "gaps between primes", au Ford/Green — nothing
  after 2026-06 except Stadlmann 2608.31126 "Bounded gaps", unrelated); no journal. FC `ErdosProblems/4.lean` has no
  formal_proof link for it; FC 687.lean still lists only `erdos_687.variants.fgkmt` as the lower-bound variant.

**(b) Does OpenAI's paper mention it?** No. grep of all section .tex + references.bib for GPT, DottedCalculator, tilted,
erdosproblems: no hits; the only 2026 dates in the bib are "Accessed September 25, 2026" URL notes. §1 (p. 3) presents
FGKMT as "The later construction of Ford, Green, Konyagin, Maynard and Tao gives j(P_k) ≫ k(log k)² log₃k/log₂k (1.1)" and
says "The gap between (1.1) and our upper bound remains substantial" — it does not call (1.1) the best known bound, so this is
an **omission, not a misstatement**, by a manuscript dated a month after the claim.

**(c) Exact form for our page.** With (1.3) of FGKMT, Y(x) = j(P(x)) − 1, take x = p_k (P(p_k) = P_k, p_k ~ k log k, so
x log x ~ k(log k)², log₃x ~ log₃k):
  h(k) ≥ j(P_k) = Y(p_k) + 1 ≫ p_k log p_k / log log log p_k ≍ **k (log k)² / log log log k**.
This beats the FGKMT-derived k(log k)² log₃k/log₂k by a factor log₂k/(log₃k)², and beats the #970 page's stated form by
(log k)(log₂k)²/(log₃k)². Honest wording: "the best lower bound known is h(k) ≫ k(log k)²/log log log k, from the covering bound
Y(x) ≫ x log x/log log log x of a GPT-5.6 manuscript (Aug 2026; posted to erdosproblems #4 by DottedCalculator), Lean-formalized by
B. Alexeev, judged 'more or less ... correct' by Ben Green, not yet refereed; the best refereed bound is FGKMT's
k(log k)² log₃k/log₂k." The h(k) conversion is ours (trivial, not in anyone's Lean).
