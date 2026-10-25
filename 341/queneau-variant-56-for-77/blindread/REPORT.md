# Blind consistency read: #341 Queneau-variant page draft (entry/body.html, title, summary, headline.json)

**Verdict: FIX-FIRST, 22 items.** Items 1–4 are mathematical misstatements in the page's own proof or claims text. Items 5–9 are claims stronger than, or different from, what the logs show. Items 10–17 are wording that a careful reader will stumble on. Items 18–22 are provenance, pre-publish and nit items. The theorem itself, the strict controller, Lemma 2, Lemma 3, Theorem 3 and the no-period argument for rule Q all read consistently with PROOF.md and the logs (see "Checked and consistent" at the end).

Method. I read the page against PROOF.md, every listed log, the scripts, Li's .tex, Green's excerpt, both van Berkel–Bosma texts, the 13 Oct entry in src/index.js and the live snapshot in /tmp/erdos1200/live. I re-ran `gates.py --control` and an FFT check of where the control violations fall, both with `nice` and with no file writes. I did not re-prove the lemmas.

---

## A. Errors in the page's mathematics or claims

**1. "A is a second counterexample to #341 itself" (body l.19) is false.** Li's own paper has an infinite family: §5, Theorem 5.1, "the sets A_p, p ≥ 18, form an infinite family of counterexamples" (7p − 20 elements, modulus 7p). Our 13 Oct entry repeats this ("§5 gives an infinite family A_p"). README_draft.md has the same "second". Suggested wording: "and A is a further counterexample to #341 itself (modulus 49; Li's family A_p uses modulus 7p ≥ 126)".

**2. Rule-D gate shift is backwards (body l.144–145).** The page says the complements "agree with Y1′, Y2′ and **1 + Y0′** on [2, ∞)". PROOF.md Lemma 3′ says: ℕ0∖(Y2′+Y2′) = {1,2} ∪ ⋃_{k≥1}[2·8^k−1, 4·8^k−2], and q−1 lies in it iff q ∈ Y0′. So the complement equals **Y0′ − 1**; equivalently Y0′ = 1 + complement.
- Concretely, the complement is {1,2} ∪ [15,30] ∪ …, while 1 + Y0′ = {1,2,3,4} ∪ [17,32] ∪ ….
- The page itself states the correct direction at l.29 ("Y0 = 1 + ℕ0∖(Y2+Y2)"), so the two passages contradict each other.

**3. The "doubles" sentence closing Lemma 2's proof (body l.78–80) is wrong as stated.** The text is: "The doubles that rule Q removes are exactly the endpoints 2·8^k+2 (recovered through I_0 = {2}), 16·8^k, and 8·8^k — the last two have no other representation and are genuinely absent." This sentence is not in PROOF.md.
- **It omits 4·8^k = 2·(2·8^k)**, the top double of I_k ⊕ I_k. It is genuinely absent from Y0⊕Y0: (S0) stops at 4·8^k − 1. It is the reason J_k can start at 4·8^k.
- The FFT control confirms this. Strict sets under rule D give exactly 7 G1 violations, at q = 4, 32, 256, 2048, 16384, 131072, 1048576 = 4·8^k (k = 0..6). That is the "7" in "7, 7 and 6".
- It also omits the small double 2 = 1+1 in Y1, which is absent from Y1⊕Y1. That is the extra G2 violation at q = 2; the others are at 16·8^k, k = 0..5.
- Among the bottom doubles it names 2·8^k+2 but not 8·8^k (from J_k, recovered via 1 + J_k) or 4·8^k (from K_k, recovered via 0 + K_k).

So "exactly" is false. Either give the full list (absent: 0 and 4·8^k; 2 and 16·8^k; 0 and 8·8^k; the bottoms are recovered), or delete the sentence. The proof does not need it.

**4. "solving for interval endpoints that do close gives 7s = 9, no integer solution" (body l.32–33).**
- The variable *s* is never defined.
- The derivation is nowhere in the bundle. The only trace is a one-line note in README_draft.md: "(Li's geometry, integer offsets) gives 7s = 9". erdos_queue.md says only "the 7s = 9 interval obstruction".
- As written, it contradicts the page's own theorem: the new controller *is* made of interval endpoints that close.

The missing qualifier is "keeping Li's block geometry ([4,8], [16,32], [64,128] per scale) and shifting endpoints by integer constants". Either add that qualifier and put the derivation in PROOF.md, or cut the clause.

## B. Claims stronger than, or different from, what the logs show

**5. Census overclaims.**
- Body l.37 says "18 show no period at all under rule Q". The headline says "18 of the 27 seeds of this shape never settle". Labels (l.162) says "(18 aperiodic …, to the bounds stated)", but **no bound is stated anywhere on the page**.
- What the logs support: legit27_table.txt, header "0=none ≤8192 on [16384,32768)", gives no period ≤ 8,192 on the quotient window [16,384, 32,768). legit27_runs_Q262144.txt again shows 18 with period=0 at Q = 2^18. PROOF.md states this bound correctly.
- The instrument is weak, which is one more reason the page must carry the bound. census.c tests periods on the suffix [Q/2, Q). For A itself the "no period" verdict rests on one quotient: at q = 16,384, Y1 and Y2 are both on (end of K_4 = start of J_4); after that only Y1 is on. A pattern that is constant except at the window's first point therefore counts as "aperiodic".
- ic=45 (R = {7,14,63,77}) has 30,884 / 33,355 / 25,053 runs on [0, 2^18) and no block structure. It may well be periodic with a period above the cap.
- Suggested wording: "18 show no period ≤ 8,192 in quotient window [16,384, 32,768) (and none to 2^18) under rule Q (25 under rule D)". In the headline: "show no period in the window we ran".

**6. "fail when any one block endpoint is moved by one (every mutation breaks at least one gate)" (l.151–152).** verify_closed_form.py runs exactly **three** mutations: on each rail, the start of block k = 3 moved down by one ("rail i block 3 start −1"). Nothing else was moved: no other k, no end-points, no upward shifts. PROOF.md §"What the computer checked" item 1 and README item 3 ("every endpoint mutation") make the same overclaim. Either reword ("moving the start of one block on any rail down by one breaks a gate") or run the full mutation set.

**7. The greedy-vs-rail-model agreement is rule Q only; the page doesn't say so.**
- `model_vs_greedy.py` hard-codes greedy341 `distinct=1` and `gates.run(…, True, …)`. The legit27_table column header reads "greedy-vs-model mismatches ≤1e6 (**strict**)". mvg_ic27_1e7.log is tagged `ic27_strict`.
- Body l.38–39 ("for all 27 an independent greedy on the integers agrees with the rail model at every integer to 10^6") and route (4) (l.158, "for A and for all 27 seeds") need "under rule Q".
- Consequence: the "25 under rule D" count rests on the rail model alone, with no greedy cross-check for those 27 seeds under D. For A under D, the chain is greedy = S′ to 10^7 (gvc_equal) plus closed form = dynamics to 2^17 (verify log), which is fine.

**8. "Y0′ has runs of 2·8^k members and 4·8^k non-members" (l.146) is wrong.** The gaps between I′_k = [2·8^k, 4·8^k−1] and I′_{k+1} = [16·8^k, 32·8^k−1] are [4·8^k, 16·8^k−1], which is **12·8^k** non-members.
- Recomputed runs: (4,15) len 12, (32,127) len 96, (256,1023) len 768, ….
- verify_closed_form.log agrees: equal Y0 runs (0,3), (16,31), (128,255).
- Same error in PROOF.md l.114. It doesn't break the argument (any unbounded run works), but it is a false statement.

**9. Period-6 explanation and suffix wording (route 3, l.158).**
- "inside one block of 8^k quotients" is the wrong size. The last tenth (gap index ≥ 1,102,058, so t ≳ 9.0·10^6, q ≈ 183,700–204,081) sits in J_5 = [4·8^5, 8·8^5]. The stretch where only the 14-rail is on is (131,072, 262,144], which is 4·8^5 = 2^17 quotients. The live-set explanation (five B-rails plus the 14-rail, giving residues 3, 14, 22, 32, 40, 48 and 6 gaps per 49) is right.
- The last-tenth probe exists **only for rule Q** (mvg_ic27_1e7.log). gvc_equal_1e7.log prints only the half-suffix line. Under rule D the live rail in that window is the **28-rail** (Y2′ ⊇ [131,071, 262,143]; Y0′ and Y1′ are off). The sentence is introduced as "under each rule", so add "(rule Q)".
- "no period up to 612,255": the KMP probe gives the exact smallest period, which here equals the suffix length (612,255 for Q, **612,254 for D**). So the accurate statement is "no period shorter than the suffix itself". The 13 Oct page stated the meaningful bound, "no period up to 306,127" (half). Pick one and give the D length too.

## C. Wording a careful reader will stumble on

**10. "Li's construction uses the coincidence: his three residue rails talk to each other through the sums 7 + 7, 14 + 14, 28 + 28" (l.11–12).** Those residue-level sums survive under rule Q; Theorem 3 on this very page uses them with u ≠ v. What rule Q removes is the **integer doubles 2y at Li's block ends**. For example, Li's Y1 block starts at 16·8^k − 1, right after 16·8^k − 2 = 2·(8·8^k − 1), which is in Y0+Y0 only as a double. Reword to say that Li's identities are tight at doubles.

**11. "Theorems 1 and 2 are (a) elementary: every sumset identity is proved by hand above" (l.160).** The rule-D sumsets and gates are only stated and sketched on the page ("each: the block plus …"); the proof is in PROOF.md. Say "above (rule Q) and in PROOF.md (rule D)". The same point applies to the summary's "every identity checked by hand", which is true for rule Q.

**12. "So Queneau's variant of #341 has a negative answer for general seeds" (l.18–19).** This can be read as "for a generic seed", which nothing supports: 9 of the 27 census seeds are periodic under Q, and van Berkel–Bosma conjecture periodicity for all two-term starts. Say "has a negative answer: not every seed gives eventually periodic gaps".

**13. "So the variant was genuinely open." (l.13).** This doesn't follow from Li's seed being periodic. Green says it "appears to be open"; Li's seed being periodic only shows his counterexample doesn't settle it. Say exactly that.

**14. "Under rule D this forces Y1 = …, Y2 = …, Y0 = 1 + … from the second block on, and Li's blocks of quotients [4·8^k, 8·8^k − 1] satisfy these exactly" (l.26–30).**
- "Second block" is undefined; it means q ≥ 2 (t > 97).
- [4·8^k, 8·8^k − 1] lists only Li's Y0 blocks, while "Li's blocks" reads as all of them.
- Li's identities (his Lemma 2.1) hold for every q, with the {0} ∪ exception for Y0, which is more than q ≥ 2.
- Suggested wording: "for q ≥ 2; Li's Y0 = {0} ∪ ⋃[4·8^k, 8·8^k−1] and the two sets it generates satisfy these (in fact for all q)".

**15. "the 20-element R = {7, 14, 28} is aperiodic by the dynamics" (l.173).** R has 3 elements; the seed has 20. "Aperiodic" here is the same bounded census observation as in item 5. Say "the 20-element seed with R = {7,14,28} shows no period in the dynamics to 2^18".

**16. Summary "gives a greedy extension whose gaps are never periodic"; title "non-periodic gaps".** The page itself reports a local period 6, so "never periodic" invites the objection. Use "not eventually periodic" in the summary at least. The headline's "never settle" is acceptable colloquially.

**17. Green citation (l.6–7, also summary and headline).** Green's Problem 7 is Ulam's sequence; the Dickson/Queneau question is in its *Comments*, per the excerpt. The 13 Oct entry said "discussed in the comments to Problem 7". Write "(comments to Problem 7, list dated 30 Jan 2026)". The quotation itself matches Green verbatim, and the 30 Jan date is supported by the 13 Oct world_search.md (PDF Last-Modified / CreationDate 2026-01-30).

## D. Provenance, pre-publish checks and nits

**18. "Queneau (1972) and Finch (1992) likewise treat two-term bases" (l.171).** Queneau is supported: van Berkel–Bosma say he "considered many explicit cases S_{f,g}". **Finch (1992) appears in no source file.** The only Finch in either paper is Calkin–Finch, *Exp. Math.* 5:2 (**1996**), which concerns non-strict sum-free sets via Cameron's bijection, not two-term bases. Add the intended 1992 reference to lit/ and check it, or drop it.

**19. "nothing there or in the Formal Conjectures repository concerns rule Q" (l.172).**
- The FC half is supported only by the 13 Oct snapshot of FC's 341 file (`live/fc341.lean`: one theorem `erdos_341`, Dickson's sumset). Nothing on disk shows a 14 Oct whole-repository search.
- Narrow it to "FC's erdos_341 states only Dickson's rule (as of 13 Oct)", or do the search and bank it.
- The erdosproblems half matches /tmp/erdos1200/live/341-claims.html: one proof claim, Li's. The file mtimes are 12:08 against "12:09Z" in the text, which is immaterial.

**20. Logs the page cites that are not on disk; bundle not yet in place.**
- Li positive control ("0 mismatches to 32,768", l.156): there is no log in runs/. I re-ran `gates.py --control` and it reproduces: [0,0,0] at Q = 32,768; strict classify (69, 117); the mutated IC gives nonzero mismatches. Save that output to runs/.
- The 2^20 run (l.155) is census.c on ic27, **rule Q only**. It is a run listing, not a programmatic comparison. I checked the listing and it matches I_k, J_k, K_k exactly. The rule-D closed form is checked against the dynamics only to 2^17, so "reproduce the closed forms … to 2^17 and 2^20" overstates for D.
- The page says "the bundle has every file" and "the bundle's PROOF.md", but `ErdosProblemADay-main/verification/341/queneau-variant-56-for-77` (apply.py's link) does not exist yet.
- README_draft refers to `live/` and `lit/`, which currently sit in /tmp/erdos1200, not in the bundle.

**21. Headline and status consistency.** The tag says "HOSTILE REFEREE HOLDS", but referee/ holds no verdict or report yet (REFEREE_SENTENCE is pending), so make the tag match the actual verdict. headline.json has `kind: "solved"` while apply.py writes `status: "partial"` (a valid STATUS key, badge PARTIAL); confirm the mismatch is intended.

**22. Nits.**
- l.145 uses the curly "Li’s"; the other 13 instances use "Li's".
- "Q" means both the residue set P ∪ B and "rule Q", including inside Theorem 3's proof ("If r ∈ Q" right next to rule-Q talk).
- The page numbers Lemma 2, Lemma 3 and Theorem 3, but there is no Lemma 1 on the page (it is cited as Li's Lemma 1.2).
- "(the cover step of the shield needs a representative on each rail)" is sufficient, not necessary. mvg_1e6.log shows ic=44 (seed has neither 7 nor 56) still matches the greedy to 10^6. Only residue 29 needs the 7-rail, via 7 + 22, and a q = 2 representative serves. Say "the cover step as written uses a representative on each rail at q ≤ 1".
- "each interval sumset shrinks by one at both ends" means the *self*-sums X ⊕ X; cross sums don't shrink.

---

## Checked and consistent (no action)
- **Logs.**
  - 1,224,510 (Q) and 1,224,509 (D) elements, 0 mismatches against S and S′ to 10^7 (gvc_*).
  - 612,255 is the half-suffix length for Q.
  - 8^7 = 2,097,152; gate violations [0,0,0] under the claimed rule; [7,7,6] under the other rule, for both rules.
  - S ∩ [1,97] = A; shield cover, avoid, PP and diagonal-only all hold.
  - Strict cover pairs: 2,378 checked (41 residues × 58 quotients), 0 without a pair.
  - Closed form = dynamics on [0, 2^17) for both rules.
  - ic27 runs to 2^20 equal I_k / J_k / K_k exactly.
- **Census.** 27 = 3^3 seeds; 18 / 25; Li's R = {7,28,63,77} has period 117 under Q. The ic encoding maps correctly (ic27 = {7,56,63,28}, ic57 = Li's). The 9 periodic seeds match between the table and the 2^18 rerun.
- **Li references.** Lemma 1.2, Lemma 3.1, Theorem 3.2 and Lemma 4.1 all match his numbering (section-numbered theorem counter). His blocks [4·8^k, 8·8^k−1], [16·8^k−1, 32·8^k−1], [64·8^k−1, 128·8^k−1] are right (the page omits his small pieces [1,3], [7,15], which is fine as "blocks"). e_7 = 7, e_14 = 63, e_28 = 28 match.
- **13 Oct facts.** Membership period 5,733 = 49·117, certified; Li (Aug 2026, GPT-5.6 Sol, Lean 4); Erdős–Graham 1980 p. 53; greedy341.c is the same source (sha256 match between MathDyad/erdos341 and the 13 Oct bundle).
- **van Berkel–Bosma.** 2609.16843v1 dated 15 Sep and 2609.18522v1 dated 16 Sep. Their conjectures are for strict sequences from two-term starts S_{f,g} (Conj. 2; Conj. 1 of 18522) and t-term starts (Conj. 4 for t = 3; the informal "all t-sumfree"). A 21-term seed is outside that scope, so "does not touch" is right.
- **The page's proof text against PROOF.md.**
  - Strict controller; (S0)–(S2) including every interval endpoint and separation inequality; (G1)–(G3) complements.
  - Theorem 3: residues 21, 35, 42; D+D ≤ 94; the distinct-summand argument (≥ 49 + b).
  - The no-period argument (8^k members, 6·8^k non-members, period 49h).
  - The rule-D sets Y0′, Y1′, Y2′ and their three sumsets.
  - All agree, apart from items 2, 3 and 8.
- **#342.** It is Ulam's problem (live snapshot).
- **HTML.** The body is tag-balanced with no nested `<p>`. There is no backtick or `${` in the body.
