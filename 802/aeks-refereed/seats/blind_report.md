# Blind read — #802 /day/ entry (802-openai-aeks-independence-refereed), 2026-10-21

Read: entry_rendered.txt (title, header, body) + the `summary:` field from src/index.js (the /day page does not render it), the HEADLINE card (values.json),
paper §§1–6 .tex, bundle README, Bridge802.lean, FC_802.lean, O/T/L/W reports, T_work/ and O_work/ scripts, replay/ and bridge/ logs, live/ snapshots.
Quotes are copied from entry_rendered.txt, where superscripts are flattened (e.g. "e√x" = e^√x, "ex" = e^x).

Version note: values.json (03:39) already differs from what src/index.js and entry_rendered.txt carry in two places. Its READING says "the solution of (2.1) that
is constant on each side puts weight about…" and its WORLD adds "two primary sources … were checked through secondary sources only". Neither change is in the
rendered page. Items 25 and 27 below are about the rendered text, and item 27 still applies to the values.json wording.

Tags: FACT = the paper or our record does not support the sentence · OVERCLAIM = a universal, or a sentence that reads stronger than the evidence ·
CONSISTENCY = title, summary and body (or entry and bundle) disagree · STYLE = plain-English problems.

---

1. **Title** — "#802: every K_r-free graph with n vertices and average degree d ≥ 2 has an independent set of size c_r·n·log d/d — the Ajtai–Erdős–Komlós–Szemerédi conjecture of 1981, by OpenAI's 21-page proof: read line by line here, its Lean proof kernel-replayed on our machine, and carried by a kernel-checked bridge of ours to Formal Conjectures' statement, which asks for every r and every average degree and is still marked open"
   → About 75 words. It is also the browser `<title>`. It works as a summary, not as a title.
   → "#802: every K_r-free graph of average degree d ≥ 2 has an independent set of size c_r·n·log d/d — OpenAI's proof of the 1981 Ajtai–Erdős–Komlós–Szemerédi conjecture, refereed here, its Lean replayed, and bridged to Formal Conjectures' still-open statement". **STYLE**

2. **Summary** — "…an independent set of size at least c_r·n·log t/t, the order they had just proved for triangle-free graphs; this is Erdős problem #802."
   → "They" means all four authors. The triangle-free result is Ajtai–Komlós–Szemerédi (AKS80), without Erdős: AEKS p. 314 attributes Theorem 1 to AKS [2],[3], and the
   body says "The case r = 3 is Ajtai–Komlós–Szemerédi". The sentence is also 43 words long.
   → "In 1981 Ajtai, Erdős, Komlós and Szemerédi asked whether every K_r-free graph with n vertices and average degree t has an independent set of size at least c_r·n·log t/t. Ajtai, Komlós and Szemerédi had just proved this for triangle-free graphs. This is Erdős problem #802." **FACT**

3. **Summary** — "Clique exclusion enters once, through random multipliers that keep each weight in expectation. They give a bound on the weighted edge mass between any two vertex sets, …"
   → The multipliers alone give no cross-mass bound. The bound comes from feeding them into the maximizer's variational inequality (Lemma 2.3, global
   maximality), and it covers only sets of weight ≤ e^x. "They" is also ambiguous.
   → "…keep each weight in expectation. Fed into the maximizer's variational inequality, they bound the weighted edge mass between any two vertex sets of weight at most e^x, and a separate theorem…" **FACT**

4. **Summary vs body vs reports** — Summary: "Hostile AI referee seats on §2 with §6, on §§3–5, on the Lean against the paper, and on the sources agreed, with eight exposition notes between them." Body: "Seat L mapped the Lean to the paper. Between them they made eight exposition notes and found no gap."
   → The reports list O: 4 EXPOSITION (E4 is a pdftotext artefact), T: 5, L: 2, W: 2, for 13 in all. "Eight" fits only O(E1–E3) + T(E1–E5). The summary applies it to
   four seats, and the body places it after seat L, so "them" reads as O, T and L, which gives 11.
   → Summary: "…agreed; seats O and T logged eight exposition notes on the mathematics, seat L two on the Lean and seat W two on wording." Body: "Seats O and T made eight exposition notes between them and found no gap." **CONSISTENCY**

5. **Problem paragraph** — "\"Is it true … many vertices?\" The page records that Ajtai, Erdős, Komlós and Szemerédi proved (log log(t+1)/t)·n, that Shearer [Sh95] improved this to …, that Ajtai, Komlós and Szemerédi [AKS80] had the conjectured bound for r = 3, and that Alon [Al96b] proved it under the stronger assumption that every neighbourhood induces a graph of chromatic number at most r − 2."
   → The second sentence is about 60 words with four "that" clauses.
   → Split it: "The page records three partial results. Ajtai, Erdős, Komlós and Szemerédi proved (log log(t+1)/t)·n, and Shearer [Sh95] improved this to (log t/(t·log log(t+1)))·n. Ajtai, Komlós and Szemerédi [AKS80] had the conjectured bound for r = 3, and Alon [Al96b] proved it when every neighbourhood induces a graph of chromatic number at most r − 2." **STYLE**

6. **Header chips** — "CLOSEDOCT 21, 2026" sits beside "Community database OPENas of 2025-08-31".
   → A reader sees CLOSED and OPEN together. "as of 2025-08-31" is the database row's last-update date, but it reads as the date of our check, while the body says
   we checked on 21 October 2026.
   → Chip: "Community database: OPEN (row last updated 2025-08-31; checked 21 Oct 2026)". Also give the CLOSED badge a one-line gloss on this page ("closed by OpenAI's proof, refereed here"). **CONSISTENCY**

7. **The claim** — "The order is best possible already for triangle-free graphs."
   → Without a qualifier this is false. Tightness holds only in the sparse range (AEKS p. 315: 10 < t′ < n′^{1/3}). When d is of order n, a triangle-free graph has
   α ≥ Δ ≥ d. The entry contradicts itself later: "Two wording notes: the order n log d/d is best possible in the sparse range (… t < n1/3)".
   → "In the sparse range (d up to about n^{1/3}) the order is best possible already for triangle-free graphs." **FACT**

8. **The claim** — "The case r = 3 is Ajtai–Komlós–Szemerédi, and with r ≥ 4 open since 1981 the theorem is the conjecture as Ajtai, Erdős, Komlós and Szemerédi wrote it (their Equation (3), average valency, every fixed clique size)."
   → AEKS (3) assumes t ≥ 1 and uses log x = max{1, ln x} (W §1a). Theorem 1.1 needs d ≥ 2, so the two match only up to the range 1 ≤ t < 2, which is Turán's
   bound. The bridge paragraph then says "the real gap is 1 < t < 2, where Theorem 1.1 says nothing", which makes the "is the conjecture" claim look loose. The
   sentence is also 37 words.
   → "The case r = 3 is Ajtai–Komlós–Szemerédi, and r ≥ 4 had been open since 1981. For r ≥ 4 the theorem is the conjecture as Ajtai, Erdős, Komlós and Szemerédi wrote it (their Equation (3): average valency, every fixed clique size). The only exception is 1 ≤ t < 2, where their convention log x = max{1, ln x} makes (3) a consequence of Turán's bound." **FACT**

9. **The claim (companion)** — "Since the chromatic number is at least n/α, it implies Theorem 1.1 on its own, but it shares the argument of §§3–5, so a flaw there would likely reach both; it is not an independent check."
   → (a) The companion's Theorem 1.1 bounds χ_DP by C_r Δ/log Δ for **maximum** degree Δ ≥ Δ_r. Reaching the average-degree Theorem 1.1 also needs the deletion of
   vertices of degree above 2d, plus Turán's bound for bounded d. A graph theorist will notice the jump from maximum to average degree.
   (b) The companion says it develops "the multiplier and entropy-splitting methods of the companion manuscript … [22, Sections 2–5]". That is §§2–5, not §§3–5.
   (c) The first "it" follows "the chromatic number", so it reads as if the chromatic number were the subject.
   → "The companion's bound χ ≤ C_rΔ/log Δ, for maximum degree Δ, gives α ≥ n/χ. Deleting the vertices of degree above 2d then yields Theorem 1.1 without citing it. But the companion re-develops the method of §§2–5 (its own words: '[22, Sections 2–5]'), so a flaw there would likely reach both. It is not an independent check." **FACT**

10. **The argument** — "Fed into the maximizer's variational inequality, they bound the weighted edge mass between any two vertex sets of weight at most ex by 16r²·w(S)(x + log⁺(1/w(S)))."
    → S is never introduced. The bounded quantity is the *directed* mass from S to D, which counts an edge inside S∩D twice. The bound holds for x ≥ 1.
    → "…they bound the directed edge mass e_w(S, D) between vertex sets S and D, both of weight at most e^x (x ≥ 1), by 16r²·w(S)(x + log⁺(1/w(S)))." **STYLE**

11. **The argument** — "Sampling all of them jointly by shared rejection sampling groups each vertex's edges, so the vertex can be split into copies whose neighbourhoods weigh at most e√x; a triangle survives the split unless its corner samples disagree or a reversed transition probability is too small."
    → The "so" gives the wrong reason. The sampling alone does not cap a group's weight at e^√x. The cap comes from discarding incidences whose reversed transition
    probability K_u(y,v) is below w_v e^{−√x} ((5.1)–(5.2)). The sentence is also 45 words.
    → "Sampling all of them jointly by shared rejection sampling groups each vertex's edges. Discarding edges whose reversed transition probability is too small caps every group's weight at e^√x, and the vertex is split into one copy per group. A triangle survives unless its corner samples disagree or one of its six edges was discarded." **FACT**

12. **The argument** — "The losses are summable as x → √x → x1/4 → …, and once every neighbourhood weighs at most a constant, T ≤ (L/3)·M."
    → L is never defined. The constant is e^X.
    → "…and once every neighbourhood weighs at most e^X, T ≤ (e^X/3)·M." **STYLE**

13. **The argument** — "If TG(w) ≤ Br·MG(w), some vertex costs at most Dr log Δ; a constant test weight gives F ≥ n(log Δ)²/(4Δ); and induction on n, with the maximum degree Δ held fixed, gives α ≥ n log Δ/(4DrΔ)."
    → B_r, D_r and (later) C△ are used before they are defined. Δ ≥ 3 is not stated. The sentence is 38 words.
    → "Write B_r and D_r = 3 + 3B_r/2 for constants depending only on r. If T_G(w) ≤ B_r·M_G(w), some vertex costs at most D_r log Δ (for maximum degree Δ ≥ 3). A constant test weight gives F ≥ n(log Δ)²/(4Δ), and induction on n with Δ held fixed gives α ≥ n log Δ/(4D_rΔ)." **STYLE**

14. **Lean vs paper** — "Every constant is the printed one: Cr = 16r², EC, AC, BC, aC, C△ = 2(1 + eX/3), Dr = 3 + 3Br/2 and cr = 1/(16Dr)."
    → "Every" goes beyond what seat L reports (§5.2–5.3). The listed constants match, but inside Lemma 2.3 the Lean has its own A_r (5 + 10k + k², with k = r − 2,
    against the paper's 4 + 8(r−2) + (1+r(r−2))log 2). Its Lemma 2.2 also ends at (ε/2)s² rather than (3/4)εs². Separately, a reader can confuse A_C (§4) with §2's A_r.
    → "Every named constant on the way to the theorem is the printed one: …. Inside Lemmas 2.2–2.3 the Lean's bookkeeping differs (its A_r is 5 + 10k + k² with k = r − 2), and it reaches the same C_r = 16r²." **OVERCLAIM**

15. **Lean vs paper** — "The paper steps without a Lean counterpart are not load-bearing: the triangle-count clause of Lemma 3.2, the converse half of Lemma 5.3, and the almost-sure stopping of the rejection sampler, which the Lean replaces by a finite construction."
    → The list reads as complete, but seat L also lists Lemma 3.2's "preserved under any finite composition" clause (L §2, §5.5). The sentence is 38 words.
    → "Four paper steps have no Lean counterpart, and none is load-bearing: Lemma 3.2's triangle-count clause and its finite-composition clause, the converse half of Lemma 5.3, and the almost-sure stopping of the rejection sampler. The Lean replaces the sampler by a finite construction." **FACT**

16. **Lean vs paper** — "The per-vertex walks are one walk on oriented edges."
    → This reads as if the Lean used a different random process. Per seat L, it is the same family of walks packed into one block-diagonal kernel on oriented edges.
    → "The per-vertex walks are packaged as one block-diagonal kernel on oriented edges." **STYLE**

17. **Bridge** — "Under Lean's conventions log 0 = 0 and x/0 = 0, so t = 0 is trivial, and for 0 < t ≤ 1 the left side is not positive; the real gap is 1 < t < 2, where Theorem 1.1 says nothing."
    → To a graph theorist, 1 < t < 2 is not a "real gap". Turán/Caro–Wei gives α ≥ n/(t+1) > n/3 there (W Part 3). The gap is formal only: per W, Mathlib has no
    Caro–Wei lemma, which is why the bridge uses OpenAI's maximum-degree lemma. Also, the bridge's case split is 0 < t < 2, not 1 < t < 2. The sentence is 44 words.
    → "Under Lean's conventions log 0 = 0 and x/0 = 0, so t = 0 is trivial, and for 0 < t ≤ 1 the left side is not positive. On paper the range 1 < t < 2 is Turán's bound, α ≥ n/(t+1). Mathlib has no such lemma, so the bridge treats all 0 < t < 2 with OpenAI's own maximum-degree lemma." **FACT**

18. **Bridge** — "…maximum_degree_independence with Δ = 4 gives α ≥ n·log 4/(32Dr), and log t/t < 1, so c = min(cr, log 4/(32Dr)) works."
    → In Bridge802.lean the first argument of `min` is `c1`, the constant OpenAI's theorem supplies behind ∃, which need not be 1/(16D_r). D is 3 + 3B/2 for the B
    that `exists_optimizer_triangle_bound` supplies, not the printed B_r. Calling them c_r and D_r suggests the printed constants.
    → "…gives α ≥ n·log 4/(32D), where D = 3 + 3B/2 for the triangle constant B the library supplies. Since log t/t ≤ 1, c = min(c₁, log 4/(32D)) works, where c₁ is the constant of OpenAI's theorem." **FACT**

19. **Bridge** — "…our script checks those three statements and the definition against FC's text, which is the same FC commit we cite below."
    → The Sources link is `…/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/802.lean`, which is the moving `main` branch, not a commit. The bridge
    pins 90d18f666eb98adec4eee4d12f1d37e30b4eb204. Also, the copies live in namespace `Bridge802.Erdos802`, not `Erdos802`. The statements are verbatim but the names
    are not.
    → "…against FC's text at commit 90d18f66 (20 October), the commit our link below pins. The copies sit in namespace Bridge802." Pin the URL to `blob/90d18f666eb98adec4eee4d12f1d37e30b4eb204/…`. **CONSISTENCY**

20. **The reading** — "Two hostile AI referee seats on the mathematics agreed, each told to refute and to quote what it objected to."
    → "Agreed" leaves open what they agreed with. It also reads as independent confirmation, but every seat and the main session ran on the same model, Claude Opus 5.5
    (MODEL_RECEIPTS). They are correlated readers, not independent ones.
    → "Two hostile AI referee seats on the mathematics, each told to refute and to quote what it objected to, also found no gap. They run on the same model as the main seat, so they are not independent readers." **OVERCLAIM**

21. **The reading (seat O)** — "…3,708 times on K3-, K4- and K5-free graphs with ε down to 10⁻⁶; the bounds came within a factor 1.013 of tight and never failed."
    → Only one step came within 1.013 of tight: p_i > ε/8 (min p_i/(ε/8) = 1.013). For the other bounds, max m_v reached 0.969·b_r(ε). E M reached only 0.125·εs²,
    against εs² in the statement and (3/4)εs² in the proof. The ε down to 10⁻⁶ applies to the 860 random runs; the 2,848 adversarial runs went down to 10⁻⁴.
    → "…3,708 times on K3-, K4- and K5-free graphs (ε down to 10⁻⁶), and no property ever failed. The tightest step, p_i > ε/8, came within a factor 1.013." **FACT**

22. **The reading (seat O)** — "…and confirmed (6.2) and (6.3) as exact identities on 300 graphs."
    → (6.3) is an inequality, and seat O checked its first line as an exact rational identity. (6.2) holds only at a maximizer. O checked it exactly after
    substituting (2.1), and numerically (error ≤ 2.7·10⁻¹⁵) at 60 true maximizers.
    → "…confirmed the identity in the first line of (6.3) exactly on 300 graphs, and (6.2) exactly given (2.1) and to 10⁻¹⁴ at 60 computed maximizers." **FACT**

23. **The reading (seat O)** — "It also reported that its own brute-force test of the cross-mass bound (2.5) could not have failed on any graph small enough to compute, since stationarity alone keeps the ratio below about log n/log log n; the evidence for Lemma 2.3 is the hand check."
    → 45 words. The bound is max{e, log n/log log n}, which stays below 256 unless log n ≳ 1900.
    → "It also reported that its brute-force test of the cross-mass bound (2.5) could not have failed. On any graph small enough to compute, stationarity alone keeps the ratio below about log n/log log n, far under 256. So the evidence for Lemma 2.3 is the hand check." **STYLE**

24. **The reading (seat T)** — "It re-derived every displayed identity and inequality with the printed constants, and checked the mechanical ones numerically, each beside a control that fails: reversibility, the density bound, the monotone entropies, the entropy-increment identity, the exact passage to the ordered triangle law, Lemma 5.2's E ℓ = Hj, the survival rule of Lemma 5.3, and the fact that splitting never raises the best cross-mass constant."
    → T_work contains a deliberately failing control for five of the eight checks: NC3 (reversibility against the uniform measure), NC1 (increment identity from a
    uniform start), NC4 (μP/μQ passage with lazy weight 1/3), NC2 (E ℓ with a non-reversible start), and the K_{5,5} blow-up (cross-mass constant). For the density
    bound, the monotone entropies and the survival rule there is no planted-failure control in negctl.py, mech.py or split.py. The survival check compares predicted
    with actual survivors in both directions, which is a real check but not a failing control. The sentence is also 64 words.
    → "It re-derived every displayed identity and inequality with the printed constants, and checked the mechanical ones numerically. Five were checked beside a control built to fail: reversibility, the entropy-increment identity, the passage to the ordered triangle law, Lemma 5.2's E ℓ = H_j, and the fact that splitting never raises the best cross-mass constant. The density bound, the monotone entropies and the survival rule of Lemma 5.3 were checked without one." **FACT**

25. **The reading (example)** — "On the triangle-free graph Km,k with m ≈ e3000 and k ≈ 3000e, take weight e−3000 on each vertex of the large side and e−1 on each of the small side. That solves (2.1) but is not a maximizer: … above the paper's constant 16·4² = 256."
    → (a) With integer m and k these weights solve (2.1) only approximately. Seat O solved the part-constant stationary point numerically (w(S) = 1.00002).
    values.json already rewords this; the rendered page does not have the fix yet.
    (b) The graph is triangle-free, so the paper's constant for it is C_3 = 16·3² = 144. Quoting 256 (r = 4) makes a graph theorist ask why r = 4. Since 374.7 exceeds
    both, 144 is the stronger comparison.
    → "…the solution of (2.1) that is constant on each side puts weight about e^−3000 on each vertex of the large side and about e^−1 on each of the small side… the ratio in (2.5) is about 374.7, above 16·3² = 144, the paper's constant for triangle-free graphs (and above 16·4² = 256 too)." **FACT**

26. **The constant** — "…the threshold X(C) of (5.6) is about 8.3·10¹⁸…"
    → (5.6) is a condition ("choose X so large that…"), not a definition. 8.3·10¹⁸ is the *smallest* X it allows, and c_4 ≈ 10^(−3.6·10¹⁸) uses that smallest X.
    → "…the smallest threshold X(C) that (5.6) allows is about 8.3·10¹⁸…". **FACT**

27. **Sources** — "Our sources seat checked every prior result the paper cites against the source itself: …. All match."
    → Seat W says COULD NOT CHECK for the primary PDFs of Ajtai–Komlós–Szemerédi 1980 and Shearer 1983 (ScienceDirect 403). Both were "SECONDARY-VERIFIED only"
    (W §1l). The values.json rewrite appends this but keeps "every … against the source itself", so it still contradicts itself.
    → "Our sources seat checked the paper's citations against the sources themselves: …. All match. Two primary sources, Ajtai–Komlós–Szemerédi 1980 and Shearer 1983, were paywalled and were checked only through secondary sources." **FACT**

28. **Sources** — "We found no other claimed proof of the conjecture and no public objection to this one. The only technical engagement is Ross Kang's Zenodo note…"
    → The next sentences contradict this. Kang's note is itself a claimed proof (its Theorem A: α ≥ 2^−18·n·log d/(rd)), adapted from OpenAI's argument, and the
    companion preprint is a second OpenAI route to the same statement. "The only" is a universal resting on a search.
    → "We found no claimed proof independent of OpenAI's argument, and no public objection to this one. The only technical engagement we found is Ross Kang's Zenodo note…" **OVERCLAIM**

29. **Sources** — "Kaizhe Chen's arXiv:2610.15293 (11 October) already uses Theorem 1.1 to get r(4,t) = t³/(log t)2+o(1)."
    → Chen's Proposition 2.1 combines Theorem 1.1 (for K_5-free graphs) with OpenAI's r(5,t) and r(s,t) lower-bound preprints ("the recent lower bounds … together
    with the recent proof of the AEKS conjecture"). Neither of those was refereed here. Read alone, the sentence suggests Theorem 1.1 alone gives r(4,t).
    → "Kaizhe Chen's arXiv:2610.15293 (11 October) already combines Theorem 1.1 with OpenAI's r(5,t) lower bound, which we have not refereed, to get r(4,t) = t³/(log t)^{2+o(1)}." **FACT**

30. **Sources** — "The community database and erdosproblems.com still say open."
    → The saved copy live/ep802.html carries no status word: the problem box is `id=neutral` and the page shows "Proof claims (0)" and "last edited 26 October
    2025". Seat W's "OPEN" comes from the teorth database. The erdosproblems.com half is not supported by what we saved.
    → "The community database still says open, and erdosproblems.com/802 (last edited 26 October 2025) carries no proof claim." **FACT**

31. **Sources** — "The openai/math repository has issues disabled, so it has no public place for review."
    → Too strong. PR conversations are also locked (W §2a), so the repository is closed to review. But Bloom's 8 October post asks readers to "use the comments to this
    blog post for a general discussion on this release", so a public venue does exist.
    → "The openai/math repository has issues disabled and pull-request conversations locked, so review cannot happen there; the open venue is the comment thread under Bloom's post." **OVERCLAIM**

32. **Sources** — "Thomas Bloom's 8 October post lists #802 among OpenAI's claims and says the list is not an endorsement."
    → True, but this bundle does not record it. Seat W did not fetch the post and relied on search snippets (W §2b.3). The only saved copy is
    verification/1150/openai-referee/seats/world_work/raw/hz_forum_thread_blog_10.html (12 Oct), which lists [802] and says "This post should not be read as any
    kind of endorsement".
    → Keep the sentence, and copy that snapshot (or a fresh one) into verification/802/aeks-refereed/live/. **FACT** (sourcing)

33. **What this entry is** — "…it has no computer-assisted step, and §§1–6 were read line by line by the main seat and again by two separate proof seats."
    → This reads as if each section had two more readers. In fact the two proof seats split the paper (O: §2 and §6; T: §§3–5), so each of §§2–6 had one more
    reader and §1 had none. "The reading" paragraph itself says so ("Seat O took §2 and §6 … Seat T took §§3–5").
    → "…and §§1–6 were read line by line by the main seat; §§2–6 were read again, split between two proof seats (O: §2 and §6; T: §§3–5)." **OVERCLAIM**

34. **What this entry is** — "The Lean is an independent check of the theorem, not of the printed proof."
    → The entry uses "independent" here in a different sense from earlier, where it calls Kang's note and the companion "not an independent check" because they share
    the architecture. The Lean is by the same authors and uses the same architecture (seat L). What makes it strong is the kernel and the matched statement, not
    independence.
    → "The Lean is a machine check of the theorem as stated: OpenAI's own, along the same architecture, and silent on whether the printed text is right." **CONSISTENCY**

35. **What this entry is** — "Ours: the replay and its controls, the bridge to Formal Conjectures' statement and its controls, the readings, the exact-arithmetic checks of §2 and §6, and the remark on global maximality."
    → The list leaves out the constant computation, which is headed "The constant (our arithmetic)" and listed as ours in the README, and seat T's numerical checks of §§3–5.
    → "…the readings, the exact-arithmetic checks of §2 and §6, the numerical checks of §§3–5, the constant arithmetic, and the remark on global maximality." **CONSISTENCY**

36. **Header banner** — "…refereed here 21 Oct, see /day/802-openai-aeks-independence-refereed — … — see our /day entry."
    → On the /day page itself the banner links to itself twice.
    → Suppress the "see /day/…" and "see our /day entry" clauses when the banner renders on this entry. **STYLE**

37. **HEADLINE card (home page, values.json)** — "the Ajtai–Erdős–Komlós–Szemerédi conjecture of 1981 now has a proof — OpenAI's, kernel-checked in Lean on our machine and read line by line"
    → "Now has a proof" reads as settled while erdosproblems.com, Formal Conjectures and the community database all still say open, and the human-language reading is by
    AI seats only. It is defensible because of the Lean, but it should name what carries it.
    → "…the Ajtai–Erdős–Komlós–Szemerédi conjecture of 1981 has a Lean-checked proof — OpenAI's, replayed on our machine and read line by line here". **OVERCLAIM**

38. **Jargon (body)** — "pp.all", "sorryAx", "comparator challenge", "leanchecker --fresh", "seat", "family 184", "cross mass", "FC".
    → None is glossed. "FC" is never expanded: it first appears as "FC's average degree" after the paragraph has said "Formal Conjectures".
    → Add one-line glosses at first use, for example "(pp.all: Lean's fully explicit printing, so two statements compare exactly)", "(sorryAx: the axiom Lean records when a proof is missing)", "(seat: a separately briefed AI reader)", "Formal Conjectures (FC)". **STYLE**

39. **Letters for average degree** — The problem paragraph and the bridge paragraph use t; the claim, argument and constant paragraphs use d. For example, "…with no hypothesis t ≥ 2" contrasts with "Theorem 1.1" stated for d ≥ 2.
    → Use one letter, or say once "average degree t (the paper's d)". **STYLE**

40. **Bundle README** (linked from the entry) — README.md still contains the placeholders "LCLINE" (leanchecker line) and "SEATSLINE" (seats line), and lists "`steps.tsv` = every step's rc and seconds".
    → `steps.tsv` is not in verification/802/aeks-refereed/replay/; it exists only at /tmp/oaimath/184/lean-build/steps.tsv.
    → Fill both placeholders before publishing, and copy steps.tsv (and post.log) into replay/. **CONSISTENCY**

41. **Labels** — "In our labels ((a) proved in the text by elementary means), the whole proof is (a)…"
    → "Elementary" will surprise a reader of an argument built on entropy increments, random walks and rejection-sampling couplings. The label means self-contained and
    not computer-assisted. The sentence is 39 words.
    → "In our labels the whole proof is (a), proved in the text: it is self-contained and has no computer-assisted step." Move the reading-coverage clause to item 33's sentence. **STYLE**

---

Count: FACT 18 (2, 3, 7, 8, 9, 11, 15, 17, 18, 21, 22, 24, 25, 26, 27, 29, 30, 32) · OVERCLAIM 6 (14, 20, 28, 31, 33, 37) ·
CONSISTENCY 6 (4, 6, 19, 34, 35, 40) · STYLE 11 (1, 5, 10, 12, 13, 16, 23, 36, 38, 39, 41). Total 41.

Checked and supported (no item): 3,708 = 860 + 2,848 runs; 540 Lemma 2.3 instances; build of 31/31 modules with 0 errors in 2 min 29 s (03:15:41→03:18:10) at
W = 4 with peak 6.6 GiB (6,969,436 kB, FiniteCoupling); 5,539 lines; Lean v4.34.1 and Mathlib d13f23b7; source-audit zeros (L §3); axioms for all three
declarations; pp.all MATCH (lengths 1285/833); the three matcher mutations; the planted sorry; TypeCtl with 3 ≤ r giving rc 1; the bridge axioms and both bridge
mutations (cast lemma; n → n·n); leanchecker started 03:28:17Z and was still running with an empty log; the K_{m,k} arithmetic (F = 3001 + 6000 − 3000 = 6001;
3000/log 3000 = 374.7); c_4 ≈ 10^(−3.607·10¹⁸) and a_C ≈ 1.65·10⁷ (constant.out); c_r = exp(−Θ(r⁸ log² r)) (X ≈ 16a_C² log² X with a_C = Θ(r⁴)); equation
numbers (2.1), (2.5), (5.6), (6.2) and (6.3) against indep.txt; page counts 21 and 29; the live page's quote and its history; the Kang and Bloom facts; FC PR #7165
of 20 October.
