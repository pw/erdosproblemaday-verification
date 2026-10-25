# Referee A — hostile review of Li, "Counterexamples to Erdős Problem 341"

Reviewer seat A, 2026-10-13. Scratch + every script/log cited below: `/tmp/erdos2100/seats/A/`.
Numbering follows the compiled PDF (`Erdos341.pdf`, created 2026-08-20), which is one off from the
numbering in my brief: brief "Lemma 2.3" = PDF **Lemma 2.2** (Y0 aperiodic); brief "Lemma 3.2" = PDF
**Lemma 3.1** (finite shield); brief "Theorem 3.3" = PDF **Theorem 3.2** (exact recurrence); the
controller identities are PDF **Lemma 2.1**, eqs. (9)–(11).

## VERDICT: HOLDS AS READ

I tried to refute it and could not. Every lemma of Sections 1–5 survived both a line-by-line read and
independent recomputation; the Lean final theorem negates the problem as Erdős–Graham, erdosproblems.com
and Formal Conjectures state it (I machine-checked the bridge to the FC statement myself; nobody had);
and two independently written greedy programs reproduce Li's explicit set exactly. Nothing below is FATAL,
and nothing is a GAP in the logical sense. What remains is exposition plus two scope facts the paper
should state: the result is specific to Dickson's equal-summands rule (under Queneau's `i<j` rule the
same seed is numerically periodic), and the seed is far from sum-free, so the Cameron/Calkin–Finch
sum-free version is untouched.

---

## Objections

**1. [EXPOSITION] Controller identities rest on an unshown computation.**
> "Proof. A direct interval calculation gives" (Lemma 2.1, before eqs. (12)–(14))

The cross-scale terms are never mentioned. Examples are `[4·8^i, 8·8^i−1] + [4·8^j, 8·8^j−1]` for i<j, which
must land inside `[4·8^j, 16·8^j−2]`, and the small pieces `[1,3]`, `[0,1]∪[7,15]` added to every
scale. All three displayed unions are **true**:
- **Brute force** (`shield_ctrl.py`, FFT sumsets of the indicators on [0, 263 144)): gate01, gate12
  and gate20 hold with 0 mismatches. The run-lists match (12)–(14) exactly, including k=0:
  - Y0+Y0 = {0}∪[4,14]∪[32,126]∪[256,1022]…
  - Y1+Y1 = [2,6]∪[16,62]∪[128,510]…
  - Y2+Y2 = [0,2]∪[7,30]∪[63,254]∪[511,2046]…
- **Lean:** the formalization proves them for all n (`pairSum_y0_iff` etc., with an explicit
  `le_total i j` cross-scale case).

A referee would still require the three-line cross-scale bound in the text.

**2. [EXPOSITION] D, B, P change meaning silently, and the type classification relies on an unstated disjointness.**
> "The six possible pair-sum types are D + D, D + B, D + P, B + B, B + P, P + P." (Thm 3.2)

In Lemma 3.1, D, B and P are residue sets in Z/49Z. Here they mean sets of integers: the finite set D,
the B-rails, and the *present* elements of the P-rails. For the six types to be exhaustive and
exclusive, the residue sets D, B, P must be pairwise disjoint. They are (checked: D∩B = D∩P = B∩P = ∅),
and every element of S then lies in exactly one class. The paper never says so. The same unstated
fact is used in "49q+14 ∈ S+S ⟺ q ∈ Y0+Y0": the ⟹ direction needs residue-7 elements of S to be exactly
{49a+7 : a ∈ Y0}, i.e. no element of D is ≡ 7 (mod 49).

**3. [EXPOSITION; scope] The cutoff hides that the seed is far from sum-free.**
> "A D + D sum is at most 94 < t." (Thm 3.2)

Correct, and it is the only place the cutoff 97 matters. But D+D *does* hit Q residues:
1+2=3, 2+5=7, 1+13=14, 1+27=28, 5+27=32, 13+27=40, 1+47=48 (`shield_ctrl.py`: D+D ∩ Q =
{3,7,14,28,32,40,48}). Consequently 12 of the 21 seed elements are sums of two earlier seed elements:
2=1+1, 3=1+2, 5=2+3, 7=2+5, 27=5+22, 28=1+27, 32=5+27, 40=13+27, 47=7+40, 48=1+47, 52=5+47, 63=27+36.

Erdős–Graham ("Given a set of integers A_k") and erdosproblems.com ("a finite set of positive integers")
impose no condition on the seed, so this is legitimate for #341. However, S ∩ (S+S) ≠ ∅, so S is not a
sum-free set, and the construction says nothing about Cameron's question as studied by Calkin–Finch
(is a complete sum-free set generated from a finite sum-free seed ultimately periodic?).

Calkin–Finch's Conjecture 4.2 is exactly that sum-free statement, and all of their "apparently
aperiodic" examples (Table 3) have sum-free bases. The paper cites Calkin–Finch and Calkin–Erdős as
"related" without telling the reader this. It should say it explicitly.

**4. [EXPOSITION; scope] The result is convention-specific and the paper does not say so.**
> "We answer the arbitrary finite-seed question negatively." (§1)

This is true for Dickson's rule (i, j ≤ n, equal indices allowed). That is the rule in Erdős–Graham p.53 —
contrast the very next paragraph (Ulam), which writes "i ≠ j" explicitly — and the rule on
erdosproblems.com and in Green's list.

Green's Problem 7 comment, however, lists Queneau's variant (i < j) as **equally open**. Under that rule
the *same seed* is numerically eventually periodic:
- `literal_greedy_dump 3000000 1` (my own scan-based program): gap period **693** (period sum 5733 =
  117·49) from gap index 421 (a_422 = 3364), holding through a = 2 999 998.
- Our earlier `greedy341.c` distinct-mode run agrees through 10^7 (`li_dist_1e7.log`: smallest period 693
  on every suffix tested).

The diagonal gates (7+7, 14+14, 28+28 on equal residues, and Y_i+Y_i sumsets that contain 2y) depend on
equal summands being allowed. The title and abstract are accurate for #341, but the paper should state
that Queneau's variant is not addressed. Recent work (van Berkel–Bosma, arXiv:2609.16843 and
2609.18522) conjectures ultimate periodicity for the strict variant, which is consistent with this
observation.

**5. [EXPOSITION] Lemma 1.2's induction compresses the min-formulation into a scan.**
> "Scan the integers t > N in order. Inductively, immediately before testing t, the selected set is S ∩ [1,t−1]." (Lemma 1.2)

Definition (1) is a *min* over t > a_n with A_n fixed. The proof uses a *scan* in which the selected set is
re-read before every t. They agree because A_n does not change between a_n and the next selected element,
but that step is not written.

The lemma itself is correct and needs no greedy condition inside [1,N]: the seed is prescribed,
exactly as in (1) "for n ≥ k". It also *must not* have one — the greedy rule fails inside this seed
(e.g. 2 = 1+1). The Lean is correctly restricted to `∀ j ≥ i` with `enumeration i = 97`.

Notation clash: N is both ℕ (`\N`) and the cutoff element "N ∈ S".

**6. [EXPOSITION] "Hence" in (21) skips a step.**
> "Hence S ∩ [1,97]_Z = D ∪ B ∪ (49+B) ∪ {7,28,63,77} = A." (eq. 21)

This needs Y0∩{0,1}={0}, Y1∩{0,1}={1}, Y2⊇{0,1}, which are not stated. The equality itself is right:
21 elements, matching the listed seed. Checked by `fft_recurrence.py`'s assert and `literal_greedy.c`;
Lean `seed_prefix` is `interval_cases`-checked.

**7. [EXPOSITION] Section 5 ports Theorem 3.2 "verbatim", but two facts change.**
> "The argument is the same as in the proof of Theorem 3.2, with M, Q_p, P_p, B_p, D_p, S_p replacing 49, Q, P, B, D, S respectively" (Thm 5.3)

Two facts used in Thm 3.2 do not port literally:
- **D+D bound:** it becomes D_p ⊆ [1, M−4] (since M−3, M−2, M−1 ∈ F_p), so D_p+D_p ≤ 2M−8 < 2M ≤ t.
- **Rail disjointness:** D_p ∩ Q_p = ∅ holds because Q_p ⊆ F_p.

Both are true but unstated. The cover also changes shape: only D_p+B_p is used, with no e_14 = 63
trick. The paper does flag that change.

**8. [EXPOSITION] The threshold p ≥ 18 is sufficient, not sharp; and Theorem 5.1's cardinality is not formalized.**
> "Fix an integer p ≥ 18" / "the seed A_p in (25) has 7p − 20 elements" (Thm 5.1)

`pfamily.py` checks, for every p in [18,400], each of the following — 0 failures:
- the explicit 30-term F_p list (30) equals Q_p ∪ (Q_p−B_p) ∪ (Q_p−P_p), with 30 distinct representatives
  and 0 ∉ D_p;
- (26)–(28) and the diagonal-pair claim (29);
- every internal claim of the Lemma 5.2 proof: G_p ⊆ F_p, f∈G_p ⇒ f−1∈Q_p,
  f∈F_p∖(G_p∪E_p) ⇒ f+2∉F_p, and all five E_p representations having their D-summand in D_p;
- |A_p| = 7p − 20.

The same checks **also pass for p ∈ {12,14,15,16,17}**: for those p, `fft_pfamily.py` finds 0 recurrence
violations to 4.19·10^6. They **fail at p = 13** (cover fails; 18 719 recurrence violations). That is
harmless, since the paper claims only sufficiency. The main 49-seed is *not* a member of the family:
p = 7 fails the family shield.

The README is honest that `|A_p| = 7p−20` is outside the Lean. The paper's one-line proof (disjointness
of the four pieces in (33)) is correct.

**9. [EXPOSITION] Dickson is never cited.**
> "Erdős and Graham asked whether, for every finite initial set A, ..." (§1)

Erdős–Graham attribute the problem to Dickson [Dic (34)] ("The following old problem of Dickson … is
still wide open"), and erdosproblems.com calls it "An old problem of Dickson". The paper's bibliography
omits Dickson 1934 (Bull. AMS 40, 711–714) and Guy E32/C9. Dickson's paper defines the greedy rule
(construction I, equal summands allowed) but never poses the periodicity question; Calkin–Erdős 1996
footnote 1 says the same. So crediting Erdős–Graham for the *question* is defensible. Bibliographic only.

**10. [EXPOSITION; statement-match, closed by me] The Lean final theorem does not state the community's statement.**
> `theorem erdos_341_negative : GreedyExtension Seed S 97 ∧ (∃ i, enumeration i = 97 ∧ ∀ j ≥ i, LeastGreedyStep enumeration j) ∧ ¬ EventuallyPeriodic gap`

This is Li's own vocabulary. It is not a proof of FC's `erdos_341`, whose file still ends in `sorry` and
whose docstring only *asserts* that casting gives a counterexample. It is also not plby's `not_erdos_341`,
yet another restatement, which I did not compile.

**I closed this.** `/tmp/erdos2100/seats/A/bridge/Bridge.lean` states FC's theorem **verbatim**, with
`answer(False)` replaced by `False`; FC's `answer()` elaborator just elaborates its argument plus an mdata
annotation (`FormalConjecturesUtil/Answer.lean`, fetched to `dl/`). It proves the statement from
`Erdos341.least_next_rule_after_fixed_seed` and `Erdos341.gap_not_eventuallyPeriodic`:
- It compiles against Li's built oleans (Lean v4.33.0-rc1), read-only via LEAN_PATH.
- `#print axioms` = [propext, Classical.choice, Quot.sound].
- Negative control 1: replacing the appeal to `gap_not_eventuallyPeriodic` with `sorry` puts `sorryAx` in
  the axioms.
- Negative control 2: mutating FC's sumset to Queneau's `i<j` makes the proof fail to typecheck.

The elaborated FC set is `{x | ∃ i ≤ n, ∃ j ≤ n, a i + a j = x}`, i.e. equal indices allowed, as required.

---

## What I ran

All under `/tmp/erdos2100/seats/A/`.

| check | instrument | result |
|---|---|---|
| Lemma 3.1, all four assertions | `shield_ctrl.py` (sets from scratch) | all true; D∩B=D∩P=B∩P=∅ |
| Lemma 2.1 (9)–(11) incl. k=0 and initial pieces | `shield_ctrl.py`, FFT sumsets on [0,263144) | 0 mismatches; runs = (12)–(14) |
| Thm 3.2 recurrence `t∈S ⟺ t∉S+S`, t>97 | `fft_recurrence.py 27` | **0 violations for 97 < t ≤ 134 217 727**, i.e. q ≤ 2 739 137 (see below) |
| ↳ controls | same script, perturbed S | dropping 49·4·8^6+7 → 2 violations; adding 49·16+28 → 3 violations (the check can fail) |
| greedy from the seed vs Li's S | `literal_greedy.c` (scan algorithm, independent of `greedy341.c`) | **N=10^7: 1 224 508 elements, 0 mismatches** (count equals `greedy341.c`'s) |
| Queneau `i<j` from the same seed | `literal_greedy_dump 3000000 1` | period 693 from a_422=3364 (objection 4) |
| §5, p=18 and p=19 directly | `literal_pgreedy.c` (greedy from A_p built from the paper's definition) | N=3·10^6: 0 mismatches vs S_p; \|A_18\|=106, \|A_19\|=113 = 7p−20 |
| §5 recurrence | `fft_pfamily.py` p ∈ {18,19,23,40}, N=2^24 | 0 violations; rail-p ≡ Y0 |
| §5 shield + seed size | `pfamily.py` p ∈ [18,400] | 0 failures |
| FC statement ⇐ Li's Lean | `bridge/Bridge.lean` | compiles, standard axioms, both negative controls fail as they should |

The 2^27 window (q ≤ 2 739 137) covers the whole k=6 block of Y0, [1 048 576, 2 097 151], both ends;
the k=5 block of Y1, [524 287, 1 048 575]; the k=4 block of Y2, [262 143, 524 287]; and the start of
Y2's k=5 block at 2 097 151. That is every controller transition up to there.

Math read line by line, with no defect found in:
- Lemma 1.2;
- Lemma 2.2 — note m = 4a−h > 3a since h < a;
- Thm 3.2, both cases. For r∈B: D+D by size, the four mixed types by (17), and P+P by (18) since
  B∩P=∅. For r∈P: forward via (17)–(19) and quotient bookkeeping u+v=q (resp. q−1); converse via the
  displayed representations. For r∉Q: the e_x construction, with u_x, c ≤ 1 and q ≥ 2;
- Lemma 4.1, including the "unique m" step and H>0;
- the proof of Thm 1.1 (49h is an ultimate period).

Seed elements lying on rails (3, 22, 32, 40, 48, 52, 71, 81, 89, 97 on B; 7, 28, 63, 77 on P) are
correctly typed by residue. No sum type is missed.

---

## Statement-match table

| item | Erdős–Graham 1980 p.53 | erdosproblems.com/341 | FC `erdos_341` | Li paper | Li Lean `erdos_341_negative` |
|---|---|---|---|---|---|
| seed | "a set of integers A_k={a_1<…<a_k}" | "finite set of **positive** integers" | prefix of any `a : ℕ → ℤ` (not required increasing or positive) | A⊆ℕ finite, nonempty | `Seed` = exactly the 21 listed integers; `GreedyExtension` conj. 1 pins S∩[0,97]=Seed |
| rule starts | "for n ⩾ k" (page image; OCR misreads "n >k") | n ≥ k | `∀ᶠ n in atTop` (only eventually) | n ≥ k | `∀ j ≥ i` with `enumeration i = 97` ⇒ i=20=k−1 (0-indexed; see note) |
| next term | least integer > a_n not of form a_i+a_j, i,j ≤ n | same | `IsLeast {x : ℤ \| a n < x ∧ x ∉ {a i + a j \| (i ≤ n) (j ≤ n)}} (a (n+1))` | min{t>a_n : t ∉ A_n+A_n}, equal summands explicitly allowed | `LeastGreedyStep`: a i < a(i+1), ¬PrefixPairSum (j,k ≤ i, j=k allowed), every t strictly between is a PrefixPairSum |
| equal summands | allowed (contrast Ulam "i ≠ j" next paragraph) | allowed | allowed (elaborates to `∃ i ≤ n, ∃ j ≤ n`) | allowed ("Equal summands are allowed in every sumset") | allowed (`PairSum`, `PrefixPairSum`) |
| conclusion negated | "differences a_{n+1}−a_n eventually periodic" | same | `∃ p > 0, ∀ᶠ m, d (m+p) = d m`, d i = a(i+1)−a i in ℤ | ∀K≥1 ∀h≥1 ∃m≥K d_{m+h}≠d_m | `¬ ∃ N p, 0<p ∧ ∀ n≥N, gap(n+p)=gap n`, gap = ℕ-subtraction of a strictly monotone `Nat.nth S` (no truncation) |
| bridge | — | — | — | — | **FC statement ⇐ Li's theorem: machine-checked by Referee A (`Bridge.lean`)** |

Notes:
- **i = 20.** Lean never states `i = 20`. It follows from conjunct 1: S∩[0,97] = Seed has 21 elements and
  `Nat.nth S` is the strictly increasing enumeration of S, so `enumeration i = 97` forces i = 20. In
  1-indexed terms, a_21 = 97 and the rule applies for n ≥ k = 21.
- **The Lean statement is not vacuous.**
  - S is proved infinite (`S_infinite`, via the 3-rail). `Nat.nth` is classical but needs no
    decidability.
  - `decide` is used only on `Finset (Fin 49)` certificates; no `native_decide`.
  - Our replay built all 8663 jobs, with standard axioms (`/tmp/erdos2100/lean-build/build.log`, `audit.log`).
  - The definitions printed in `audit.log` (`Seed`, `S`, `PairSum`, `LeastGreedyStep`,
    `EventuallyPeriodic`, `gapOf`) match the paper.
  - Paper Y1 = [1,3]∪⋃[16·8^k−1, 32·8^k−1] ⟺ Lean `16*8^k ≤ n+1 ∧ n < 32*8^k`; likewise for Y2 and Y0.
- **FC is broader than Erdős–Graham:** ℤ-valued, arbitrary non-monotone prefix, rule only eventually.
  So FC's `answer(False)` is a strictly **weaker** proposition than "#341 has answer no". Li's witness
  lies in the narrow class (strictly increasing, positive, rule from index 20), so it refutes both. The
  FC "research solved" tag alone would not certify #341.
- **plby's `not_erdos_341`** (ℕ-valued, StrictMono, positive, ∃k ∀n≥k greedy, non-periodic gaps) is the
  most faithful single statement of the erdosproblems wording. It is discharged by Li's lemmas in plby's
  file. Per the world seat, those lemmas are byte-identical to Li's (import paths aside), and they were
  rebuilt by the FC PR #6070 author. I did not compile plby's file.

---

## Convention (item 3)

- **Equal summands allowed (Dickson / E–G / erdosproblems / Green):** a counterexample. Proved, Lean-checked.
- **Distinct summands i<j (Queneau):** **not** a counterexample for this seed — numerically periodic
  (objection 4). The paper does not address this variant.
- **Seed required sum-free (Cameron / Calkin–Finch reading):** this seed is not sum-free (objection 3).
  No such requirement appears in E–G or on erdosproblems.com.
- **Seed size ≥ 2 vs 1:** irrelevant (k=21).
- **"Eventually periodic":** standard meaning; the paper, the Lean and FC agree.
- **E–G's own illustration is internally inconsistent with both conventions.** E–G write: "Even a
  starting set as small as {1,4,9,16,25} requires thousands of terms before periodicity eventually
  occurs." Under i≤j that seed has gap period 224 from a_87 = 440, i.e. periodic after ~310 terms (our
  `sq_eq_2e6.log`, matching Kitamura's comment on the thread). Under i<j it has period 10 almost
  immediately (`sq_dist_2e6.log`). So the remark cannot be used to argue that E–G meant a different
  rule; the rule text itself is unambiguous.
- **Dickson's 1934 definition:** construction I is the greedy rule with equal summands allowed and 0 in the set. Adding 0 to Li's seed changes nothing (x+0 ≤ a_n < t). Dickson never posed the periodicity question at all (see World findings).

---

## World findings

Full notes with every query and URL: `/tmp/erdos2100/seats/A/world_search.md`. Raw fetches: `/tmp/erdos2100/seats/A/raw/`. All read 2026-10-13.

**Nobody has disputed it, nobody found an error, and nobody authoritative has accepted it.**

**erdosproblems.com/341** (https://www.erdosproblems.com/341; history https://www.erdosproblems.com/history/341)
- The page was last edited 2026-01-20 and shows no solved/disproved marker.
- Proof-claims tab (https://www.erdosproblems.com/forum/thread/341/proof-claims): one claim (#200) by Z_Li, submitted 2026-08-09 15:32:18. It carries the disclaimer "Appearing on this page is no guarantee of proof correctness…" and has 0 comments.
- Posting comments and proof claims is paused site-wide, so the silence is partly structural.
- The only thread comment (https://www.erdosproblems.com/forum/thread/341) is KentaKitamura, 2026-07-08. It concerns the {1,4,9,16,25} side remark (period 224 from a_87), not Li.

**teorth/erdosproblems** (https://github.com/teorth/erdosproblems/blob/main/data/problems.yaml at HEAD 2026-10-13): #341 is still `status: open`, last_update 2025-08-31.

**Formal Conjectures** — the only institutional uptake.
- Issue https://github.com/google-deepmind/formal-conjectures/issues/6069 and PR https://github.com/google-deepmind/formal-conjectures/pull/6070 were merged 2026-09-18 (commit a8d29337). The PR was approved by mo271 with "Thanks, LGTM!" and no other discussion.
- The merge set `answer(False)` and `research solved` and linked plby's wrapper.
- The FC theorem body is still `sorry`. The PR's ℕ→ℤ/IsLeast bridge was "verified locally, not part of this PR". My `Bridge.lean` is an independent machine check of exactly that bridge.

**plby/lean-proofs** (https://github.com/plby/lean-proofs/commit/faeedb63f1c9d991c943baf17304e48daa111d19, 2026-08-26, Boris Alexeev)
- It re-hosts Li's Lean files byte-identically (import paths aside), adds `not_erdos_341`, and adds a Comparator challenge. It is a re-host, not an independent proof.

**Ben Green's list** (https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf): the PDF is dated 2026-01-30, before the claim. Problem 7 poses both the Dickson (i,j ≤ n) and Queneau (i<j) variants as open.

**Searched, nothing about Li's claim found:**
- arXiv API, 7 queries; the positive control returned hits. Li's paper is not on arXiv.
- OpenAlex.
- MathOverflow / Math.SE.
- Tao's blog (search "erdős 341").
- Hacker News.
- Mathstodon (#erdosproblems, #erdos).
- GitHub code/issue search for "Zhiheng", "LiAlreadyExists", "erdos_341".

**Not searchable:** X/Twitter, Reddit, Lean Zulip, Discord.

**Two closed or stale items that are NOT verdicts:**
- TheJustinSunPrize/awards PR #4260 was closed with boilerplate and is mis-mapped: its JSP-000341 is a different problem.
- grandchallenge/MATH-PROGRAMME#1611 is an automated audit built on stale pins and never saw the claim.

**Li's repo and Zenodo** (https://github.com/LiAlreadyExists/Erdos-341, https://zenodo.org/records/22030511)
- The repo has 1 star and 0 issues.
- The DOI cited in the paper is the **v2.0.1** snapshot. The latest is v2.1.0 (record 22030579). Lean files are byte-identical across versions and since the first upload; `Erdos341g.lean` is identical at v2.0.1 and v2.1.0.
- Provenance nit: the since-deleted `BUILD_VERIFIED.md` recorded a sha256 for `Erdos341.lean` (`e95e8a49…`) that does not match the committed file (`75c56c1e…`). That is a self-reported record. Our replay built the committed file, so this is not a soundness issue.

**Prior literature: no earlier proof or counterexample.**
- **Dickson 1934**, Bull. AMS 40, 711–714 (https://www.ams.org/journals/bull/1934-40-10/S0002-9904-1934-05951-2/), read in full.
  - It concerns additive bases ("universal k-sets", containing 0). Construction I is the greedy rule with **equal summands allowed**: "least integer which is not a sum of any two of the first n−1 elements … 0 and all positive odd integers".
  - It **never asks the periodicity question**. Calkin–Erdős 1996, footnote 1: "the problem as stated by Guy doesn't appear in the reference cited."
  - Dickson's seeds contain 0. Adding 0 to Li's seed changes nothing, because x+0 ≤ a_n < t.
  - So there is no reading of Dickson under which Li's example fails, beyond the i<j and sum-free variants discussed above.
- **Calkin–Finch 1996** (Exp. Math. 5, 131–137; https://emis.de/ft/51959): Table 3 lists 19 "apparently aperiodic" complete sum-free sets, all from **sum-free bases** and checked to 10^7. They state "no method is known that will show that a sum-free set is not ultimately periodic from … finitely many elements." Their Conjecture 4.2 (Cameron) concerns sum-free sets.
- **Calkin–Erdős 1996** (https://www.math.clemson.edu/~calkin/Papers/calkin_erdos.pdf): {1,3,8,20,26,…} and {2,15,16,23,27,…} are "not known to be ultimately periodic … no way to show that these sets are aperiodic".
- **Calkin–Finch–Flowers 2005** (INTEGERS 5(2) A03): more evidence, no proof.
- **Finch's 2020 addenda** (arXiv 2001.00578) and **Wen–Zhang–Wu 2015** (arXiv 1405.6493, "This question is still open"): no resolution.
- So Li's is, to everything found, the **first proved** aperiodic example. It is for arbitrary seeds; the sum-free-base version remains open (objection 3).
- **2026 work on the strict i<j variant**: van Berkel–Bosma arXiv:2609.16843 and 2609.18522 conjecture ultimate periodicity there, which is consistent with my period-693 observation for Li's seed under i<j. Shtrezi arXiv:2606.17447. None mentions Li.

**Erdős–Graham p.53, checked against the page image `pg-049.png`:** "for n ⩾ k" (not "n > k" as in the OCR), and "a_i + a_j, i, j ⩽ n". This confirms the statement-match table.

---

## Our instruments (item 5)

**What a BAD result would look like:**
- a single n ≤ N where Li's S and the greedy disagree;
- a single t > 97 violating `t∈S ⟺ t∉S+S`;
- a residue-shield or controller identity failing on its finite range.

All three are producible by the instruments: the `mutate_check.py` mutations FAIL, and so do my FFT
controls (2 and 3 violations). So the zeros are informative within the window.

**Shared-misreading risk.** `greedy341.c` and `check_li.py` were written in the same session, and both
implement the equal-summands rule. If the true rule were i<j, both would pass together on the wrong
problem. Three things mitigate this:
- (a) The rule text is unambiguous (above).
- (b) `greedy341.c`'s distinct mode and my `literal_greedy` mode 1 show the instruments *can* tell the
  conventions apart, and that the claim is convention-specific.
- (c) My `literal_greedy.c` is an independent algorithm (pair scan, not bitset shift-or) and reproduces
  `greedy341.c` exactly: 1 224 508 elements to 10^7.

**What they structurally cannot see:**
- **Anything beyond the window.** `check_li.py` stops at 10^7 (q ≤ 204 081, which reaches only the
  *start* of Y0's k=5 block at 131 072). My FFT check stops at 1.34·10^8 (q ≤ 2.74·10^6). A set agreeing
  with the greedy on the window and diverging later would pass both. The infinite statement rests on the
  proof and the Lean.
- **Non-periodicity, which no finite computation can certify.** Worse, the periodicity probe built into
  `greedy341.c` reports, on the true sequence, "suffix from gap index 918380 … smallest period **6**
  (PERIODIC-COMPATIBLE)" and the same for the last 10%. That is because for q ∈ [131 072, 204 081] the
  controller sits inside one block (Y0=1, Y1=Y2=0), so the window's tail genuinely is periodic. Read
  naively, our own instrument "says" the gaps are periodic — the opposite of the theorem. That reading
  is meaningless: aperiodicity lives at the scale transitions 8^k, which a 10^7 window sees only once
  (the 50% suffix reports "no period ≤ half"). This probe must never be cited for or against the claim.
- **Transcription.** `check_li.py` tests Li's S as transcribed from the *Lean* definitions. Had paper and
  Lean disagreed, it would have certified the Lean set only. I checked by hand that the paper's
  (5)–(7), (20) and the Lean `Y0/Y1/Y2/S` define the same sets.
- **Coverage.** `check_li.py` does not touch Section 5 at all. I covered p = 18 and 19 directly, and
  p ∈ {18,19,23,40} by recurrence.

---

## What I did NOT check

- **A from-scratch kernel replay** (`leanchecker --fresh`). The replay's `leanchecker_fresh` step died on
  a usage error ("--fresh flag is only valid when specifying a single module"). A
  `leanchecker_fresh2.sh` that targets the single module `LeanProject` exists in `/tmp/erdos2100/scripts/`.
  I left that to the lean-build seat as instructed. The non-fresh leanchecker passed (exit 0) and the
  build passed. My Bridge compiled against those oleans and adds no kernel re-check of Mathlib.
- **plby's wrapper** `/tmp/erdos2100/plby/Erdos341.lean`: read, not compiled.
- **Dickson 1934:** read by my world-search subagent (pdf at `raw/lit/dickson1934.pdf`); I did not read it myself.
- **Guy UPINT, Queneau 1972, Finch 1992 Monthly:** not retrievable (borrow-only or Cloudflare-challenged); characterised from secondary sources only.
- **§5 beyond the sampled p.** The Lean `theorem_5_1_nonperiodicity` covers all p ≥ 18; I did not
  independently re-derive its symbolic proof line by line. I read its statement, its `Seed`/`F`/`D`
  definitions, and `F_iff_semanticF`, which ties the explicit 30-term list to the set definition.
- **Zenodo files myself.** The world seat reports the Lean is byte-identical across Zenodo v2.0.1/v2.1.0 and GitHub; I reviewed the GitHub copy at commit c1d9121.
