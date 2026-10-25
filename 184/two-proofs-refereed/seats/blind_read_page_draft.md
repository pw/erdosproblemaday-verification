# Blind hostile read — #184 draft (draft_for_blind_read.txt + insert184.py title/summary/card), 2026-10-20

Draft lines are cited as `draft:N` (line numbers of draft_for_blind_read.txt) and `ins:N` (insert184.py, as re-read at 09:24Z, after
the Kim summary was filled in). Bundle = `/home/exedev/ErdosProblemADay-1020-0900/verification/184/two-proofs-refereed/`.
Everything not listed here was checked and holds (all UTC times and differences, 601/93,195, 34/21,451, 493 s, 9,574 jobs/1,755 s,
3,680 s, 3,673 s, 100 s, 64/0, 16,000/200,092, 36 deviations, 31 errata, sha 9f36e4e0…, page counts 152/32/32/22, PR #6898 quote,
FC docstring quote, page quote, Kim's v2 notes, the v6.1 "must not be recorded" quote, "follows this paper section by section",
FC main = capture and still on 4.33.1/0df444a3, teorth still "open", Palomar 404s).

## WRONG

1. **WRONG** — draft:13: "the repository has one squashed commit, so nothing outside backs that date".
   Evidence: `gh api repos/openai/math/commits` lists 5 commits (adc7f12 "Initial commit" 10-06 21:58:50Z, 3014888 10-08, fd4aeeb,
   2710f99, 1581d4c 10-12). The world seat's own wording is "one squashed 'Initial commit'" (seats/referee_world.md:24).
   Replace: "…and the repository's history begins with one squashed 'Initial commit' (6 October; later commits do not touch this
   paper), so nothing outside backs that date".

2. **WRONG** — ins:63 (card line): "the two-line transport between them was in neither repository".
   Evidence: bridge/Bridge.lean is 211 lines (helper lemmas, `exists_sub`, `per_graph_aux`, `per_graph`, `bridge`); the formal seat
   called it "≈190 lines" (seats/referee_formal.md:294). Nothing about it is two lines.
   Replace: "the transport between them (routine on paper, about 200 lines of Lean) was in neither repository, so we wrote it and the
   kernel accepted it".

## OVERSTATED

3. **OVERSTATED** — draft:27 "So Formal Conjectures' statement now has two kernel-checked routes on our machine: … and OpenAI's proof
   through this bridge"; same claim in ins:16 (title "bridged to Formal Conjectures' own"), ins:22–23 (summary "Formal Conjectures'
   statement now has two machine-checked routes"), ins:61 (card tag "OUR KERNEL-CHECKED BRIDGE CLOSES IT"), ins:56 and ins:76
   ("FC's statement also derived from OpenAI's"; "which we derived from it").
   Evidence: the bridge proves `Bridge184.erdos_184`, a namespaced COPY elaborated under Mathlib d13f23b7; FC's constant cannot be
   imported there (bridge/Bridge.lean:11–17; README "Residual: textual + definitional identity across two toolchains, not one
   Expr.equal"). The body's own "What remains" sentence (draft:27) says exactly this; the summary sentences drop it.
   Replace (body): "So FC's statement has one kernel-checked proof on our machine (Coffey's, against FC's own constant) and a second
   route through OpenAI's proof that is kernel-checked against a verbatim copy of it, the copy matched to the original as above."
   Card tag: "OUR BRIDGE PROVES A VERBATIM COPY OF IT FROM OPENAI'S THEOREM".

4. **OVERSTATED** — draft:27: "copy and original are matched by text and by definitional equality across two toolchains".
   Evidence: no definitional-equality check crosses toolchains. InstDefeq.lean proves the two instance paths defeq *inside* each
   environment (bridge/logs/instdefeq_{oai,coffey}.log). The pp.all match shows the same constant NAMES; whether those names unfold
   to the same definitions in the two Mathlibs rests on the formal seat's textual diff of a list of files, and "Asymptotics.IsBigO,
   Finset/Fintype core, Sym2 quotient core" were NOT diffed (seats/referee_formal.md:149–150, 355–356).
   Replace: "What remains: copy and original are matched by their elaborated text (names identical), by an in-environment defeq
   check of the one differing instance path (run in both environments), and by a read-through diff of the Mathlib definitions those
   names unfold to (IsBigO and the Finset/Fintype/Sym2 core not diffed) — not by one Expr.equal in a single environment, which
   these pins do not allow."

5. **OVERSTATED** — draft:18: "OpenAI's are explicit and astronomical".
   Evidence: the paper chooses D_* "large enough for" four lemmas plus eventual inequalities (induction.tex:442–458); only a LOWER
   bound is explicit. The world seat: "Not computed numerically" (seats/referee_world.md:110).
   Replace: "OpenAI's are not computed either, but its explicit parameters force log₂ D_* ≥ 7.64·10¹², so C ≥ 4T(D_*) > 2^(7.6·10¹²),
   which the paper does not say".

6. **OVERSTATED** — ins:18: "Three full proofs then appeared".
   Evidence: body says "claims the full conjecture" (draft:5); title/card say "claimed".
   Replace: "Three claimed proofs of the full conjecture then appeared".

7. **OVERSTATED** — ins:23 (summary, now filled): "Hostile referee seats found no gap in any of the three papers".
   Evidence: Coffey seat: HOLDS AS READ on the load-bearing chain only; "COULD NOT CHECK line by line: the device lemmas of s3–s5 …
   The Lean is the evidence for their truth" and "The weight now rests on the device lemmas" (seats/referee_coffey.md:25–40, 105).
   OpenAI seat: GGKO sketch behind Cor 1.2(ii) "COULD NOT CHECK" (referee_openai.md:17–18). Kim seat did not re-prove BM Lemma 14 /
   Thm 24 (referee_kim.md:3). The body (draft:30) scopes this correctly; the summary does not.
   Replace: "Hostile AI referee seats found no gap in the parts they checked: OpenAI's paper (expository fixes), Coffey's
   load-bearing chain (his §3–§5 device lemmas checked only at statement level; the Lean carries them) and Kim's v2, read line by
   line (nothing above exposition; the cited BM results not re-proved)."

8. **OVERSTATED** — ins:61 card tag: "HOSTILE SEATS: NO GAP FOUND IN THE LOAD-BEARING CHAINS".
   Evidence: as item 7 — for Coffey the seat itself says the chain's decaying per-round bounds rest on device lemmas it took from the
   Lean (referee_coffey.md:105). Replace: "AI REFEREE SEATS: NO GAP FOUND IN WHAT THEY CHECKED".

9. **OVERSTATED** — draft:24 "Both formalizations were rebuilt from source on our machine"; ins:20 "We rebuilt both Lean proofs from
   source".
   Evidence: Mathlib came from the Mathlib build cache — Coffey: "Decompressed 8690 file(s)" (replay/coffey/logs/cache_get.log);
   OpenAI: "mathlib oleans present: 8529" before any build (replay/openai/driver.log). Only the project modules and FC's modules were
   compiled. leanchecker --fresh then re-checked every declaration, Mathlib included — which is the real guarantee.
   Replace: "Both formalizations were compiled from source on our machine against Mathlib's published build cache, and
   leanchecker --fresh then re-checked every declaration in each import closure, Mathlib included."

10. **OVERSTATED** — draft:30: "the lifting argument was simulated end to end (16,000 random instances …)".
    Evidence: "Route *existence* is lem:routing's job and is not simulated; this checks that the routing lemma's guaranteed
    properties suffice for the lifting and the ledger" (seats/referee_openai.md:275–276); instances are small random ones.
    Replace: "the lifting step was simulated on 16,000 small random instances, routes drawn to satisfy exactly the routing lemma's
    three guarantees (200,092 lifted quotient cycles, all simple, …)".

## UNCLEAR / misreadable

11. **UNCLEAR** — draft:18: "Lengths: 152, 32 and 22 pages."
    The paragraph's order is OpenAI, Coffey, Kim, so a reader maps 152 → OpenAI. Truth: Coffey 152, OpenAI 32, Kim 22 (v2; v1 32).
    Replace: "Lengths: OpenAI 32 pages, Coffey 152, Kim 22 (v2; v1 was 32)."

12. **UNCLEAR** — draft:30: "In two places the Lean does not follow the paper: … The repository's DEVIATIONS.md records 36 route
    differences".
    Two vs 36 in consecutive sentences reads as a contradiction. Seat: "for two of them [the device lemmas] the Lean does not
    follow the paper's proof" (referee_coffey.md:40); D1–D36 overall (:138).
    Replace: "In two load-bearing places the Lean does not follow the paper's proof: …".

13. **UNCLEAR** — draft:30: "Corollary 1.2(ii) rests on Proposition 6.3 of Girão–Granet–Kühn–Osthus (2021), whose converse direction
    is only sketched".
    "Converse" of what? The sketched direction is (⇐), Erdős–Gallai ⇒ Conjecture 1.14 — exactly the direction the corollary uses
    (refs/ggko/ggko_v2.txt:2949–2971; referee_openai.md:113–121).
    Replace: "…Proposition 6.3 of GGKO, whose relevant direction (Erdős–Gallai ⇒ their Conjecture 1.14, the one the corollary uses)
    is only sketched there".

14. **UNCLEAR** — draft:30: "The fixes: say how big C is; the routing lemma's proof uses the Aharoni–Haxell matching theorem, while the
    Lean proves the same statement by an elementary greedy argument …".
    The middle item is a fact, not a fix; the seat's fix A.4 is "note the greedy routing proof / that AH is avoidable"
    (referee_openai.md:7).
    Replace: "…; note that Aharoni–Haxell is avoidable — the Lean proves the routing lemma's exact statement by an elementary greedy
    argument and proves Lovász 1968 from scratch, so the formal proof has no outside input beyond Mathlib; …".

15. **UNCLEAR** — draft:33: "We found no independent human verification of any of the three proofs on record, Kim's statement about his
    own aside, and no public response from Bucić or Montgomery".
    Garbled: "his own aside" parses as a noun phrase.
    Replace: "Apart from Kim's statement about his own paper, we found no human verification of any of the three proofs on record,
    and no public response from Bucić or Montgomery (a statement about what our searches covered)."

16. **UNCLEAR (independence)** — draft:30: "Five tool-equipped referee seats, each briefed to refute …".
    Nothing in the seats paragraph says the seats are AI models, or which family; the only disclosure is the last sentence of the page
    ("Nothing here is a human referee's verdict", draft:39). The 03:00Z driver seat that briefed them was Opus 5.5
    (replay/openai/ESTIMATE.md:1); Coffey's proof was written "using Claude Opus 5.5" and Kim used Claude. If the seats ran Claude,
    the reviewer shares a model family with two of the three authors' tools. The bundle does not record the seats' model.
    Replace: "Five tool-equipped AI referee seats (Claude models — the family Coffey's proof was written with and one of Kim's
    tools, so not independent of them), each briefed to refute …". Record the seat model in the bundle README.

17. **UNCLEAR (attribution)** — draft:27: "The bridge's instance-generic helper lemmas follow the approach of Coffey's own
    EGCheck/BridgeLemmas.lean." (and "The bridge (ours)", "Whose … the bridge", draft:39).
    Evidence: `degree_eq_ncard` and `card_edgeFinset_eq_ncard` are copied with identical statements and identical proofs
    (bridge/Bridge.lean:59–67 vs coffey repo formal/EGCheck/BridgeLemmas.lean:196–205); `mem_edgeSet_comap` (:333) and the
    `isBigO_refl … const_mul_left` term (BridgeCore.lean:51) are also his; the formal seat says "ported from Coffey"
    (referee_formal.md:298, 332–334). Coffey's repo is Apache-2.0.
    Replace: "Three helper lemmas and the instance-generic strategy are taken from Coffey's EGCheck/BridgeLemmas.lean (Apache-2.0);
    the transport from OpenAI's statement is ours."

18. **UNCLEAR** — draft:15: "Coffey's was public first: by five days and twenty-one and a half hours over OpenAI's".
    The 5 d 21 h 34 m is to OpenAI's repository CREATION, which is a lower bound on when it became public (public by 23:15:35Z, first
    HN post; referee_world.md:43, 59); both repos were empty at creation (Coffey's first commit was pushed 00:18:44Z).
    Replace: "by at least five days and twenty-one and a half hours over OpenAI's (repository creation to repository creation)".

19. **UNCLEAR** — draft:18: Kim's argument is described from v2 (heavy cycles "by degree"), but nothing says so; v1 defined heaviness
    by vertex weights and used random colouring (kim_src/erdos_gallai_v2.tex:893).
    Replace: "Kim (as simplified in v2): no rounds and no quotients…".

20. **UNCLEAR** — draft:18: "decompose G[S], delete those vertices with their at most two remaining edges".
    "those vertices" can be read as all of S. Kim: "at least |H|/12 vertices of H have at most two remaining edges. We remove these
    vertices" (erdos_gallai_v2.tex:78).
    Replace: "decompose G[S], then delete the ≥ |S|/12 vertices of S that now have at most two edges left, with those edges".

21. **UNCLEAR** — draft:18 (whole paragraph) presents three arguments without saying that two of them share a skeleton. The world seat:
    OpenAI and Coffey "share the quotient-induction-and-lift skeleton on top of Bucić–Montgomery expanders … differ in essentially
    every implementation choice"; Kim "shares neither" (referee_world.md:9, 96–99, 124). Given Bloom's public "accusations of
    plagiarism" remark, a reader will compare the paragraphs and wonder whether we noticed.
    Add: "OpenAI's and Coffey's share a skeleton — strictly smaller simple quotients, decomposed by induction and lifted back through
    edges reserved in expanders — and differ in every implementation choice; Kim's shares neither. We draw no inference from this."

22. **UNCLEAR** — draft:15: "We say nothing about how any author arrived at an argument" — the page then reports each author's AI use
    (draft:9, 11, 39). Replace: "We make no inference about priority of ideas or copying; we report what each document argues and
    what a machine has checked."

## UNSUPPORTED

23. **UNSUPPORTED** — draft:9: "("using Claude Opus 5.5", per his proof claim)".
    The claim was "posted by user American-Pharaoh" (referee_world.md:35; world/claims184.txt); nothing ties that account to Coffey.
    Replace: "per the proof claim posted for him on erdosproblems.com".

## MINOR

24. **MINOR** — draft:24: "with the estimate written before any CPU was spent". ESTIMATE.md was written ~03:15Z while the Mathlib
    cache download was "running now" (replay/openai/ESTIMATE.md:8), and a 10-15 seat had already run one. Replace: "with the
    estimate written before any build or check ran".

25. **MINOR** — draft:24: "Our first constant-bound control, written at 03:00Z". File mtime 03:13:39Z; it was written by the 03:00Z
    seat. Replace: "written by the 03:00Z seat".

26. **MINOR** — draft:24: the OpenAI constant-bound control has no positive twin (replay/openai/probe/WrongShape.lean), so its type
    mismatch shows only that the type differs — the very weakness the page fixes on Coffey's side. Either add "(on OpenAI's side the
    pp.all statement match is the positive control)" or run a twin.

27. **MINOR** — draft:24: "(it back-ports a soundness fix to Lean 4.33.1)". The patch is to comparator: it "backports a Lean v4.34
    soundness fix that comparator relies on" (`Expr.proj` in `getUsedConstants`, comparator issue 68) for a v4.33.1 build (Coffey
    README:209–211). Replace: "(a comparator patch that back-ports a Lean 4.34 soundness fix for use on 4.33.1)".

28. **MINOR** — draft:27: "identical character for character". pp_compare.py normalises whitespace (bridge/pp_compare.py:16–20).
    Replace: "identical token for token (whitespace normalised)".

29. **MINOR** — draft:27: "proves the two PairwiseDisjoint propositions equal by Iff.rfl". Iff.rfl proves ↔; that it type-checks
    shows they are definitionally equal. Replace: "shows the two PairwiseDisjoint propositions definitionally equal (Iff.rfl
    type-checks)".

30. **MINOR** — draft:30: "Every inequality the induction uses was recomputed (64 checks, 0 fail)". The 64 checks span the whole paper
    (routing, Chernoff constants, folding), and the asymptotic ones are grid checks (referee_openai.md:258–268). Replace: "The
    induction's inequalities were recomputed, the asymptotic ones on grids (64 numeric checks across the paper, 0 failures)".

31. **MINOR** — draft:30: "Of 31 errata found against v6.1 … two (ROUND-RULES, M-INTEGER) we would grade as gaps in v6". Both were
    already fixed in v6.1 (ERRATA_v6.1.md:89, 93), and the earlier "major gap" PV-ARC-END found by AI review and repaired as CR1-PV
    (referee_coffey.md:205) is omitted. Replace: "…two of them, already fixed in v6.1 by formalization triage (ROUND-RULES,
    M-INTEGER), we would grade as gaps in v6; earlier, AI review had found one major gap (PV-ARC-END), repaired before the Lean".

32. **MINOR** — draft:11: quote ends "…takes full responsibility." Source continues "for the content of the paper"
    (erdos_gallai_v2.tex:897). Add "…" or the full clause.

33. **MINOR** — draft:18 (Kim): "Theorem 1.4, Conlon–Fox–Sudakov's linear-minimum-degree theorem pushed down with Bucić–Montgomery's
    expanders". Kim proves it from BM's expanders and cycle-decomposition result plus CFS's sparse-graph decomposition result
    (erdos_gallai_v2.tex:92), not by applying CFS's linear-degree theorem. Replace: "Theorem 1.4, which extends Conlon–Fox–Sudakov
    from linear to polynomial minimum degree, using Bucić–Montgomery's expanders and CFS's sparse-graph decomposition".

34. **MINOR** — draft:18 (OpenAI): "identify each pair, which gives smaller simple quotient graphs". Simple only after setting aside
    E_err (loops and all but one edge per parallel class) as single edges (folding.tex:34). Add "(after setting aside the few edges
    that would become loops or parallel)".

35. **MINOR** — draft:18 (Coffey): "modify their Lemma 14 (τ-rules and a cap on guest degrees)". The τ-rules modify Lemma 14; the
    guest-degree cap (rule GC) is a separate rule of the hierarchy (referee_world.md:106). Replace: "modify their Lemma 14 with
    τ-rules and add a cap on guest degrees".

36. **MINOR** — draft:2: "complete bipartite graphs need (3/2 − o(1))n". Only the unbalanced K_{2k+1, n−2k−1} family does. Replace:
    "some complete bipartite graphs need …".

37. **MINOR** — draft:13: "family 181 of the openai/math release". On this site /day/181 is Erdős #181 (hypercube Ramsey), which is
    OpenAI family 171 (referee_world.md:146). Add "(OpenAI's numbering, not Erdős #181)".

38. **MINOR** — draft:21: "The two statements are equivalent (our formal seat wrote out both directions)". On paper; only
    MainStatement ⇒ erdos_184 is kernel-checked. Replace: "(our formal seat proved both directions on paper; the bridge below
    kernel-checks the one needed)".

39. **MINOR** — draft:33: "Bloom's 8 October post … says he has not checked the proofs". His words: "I have not yet looked at in any
    serious way any of the proofs in this release" (release-wide disclaimer; Wayback 20261019093239 of /forum/thread/blog:10).
    Replace: "says he has not yet looked seriously at any of the release's proofs, nor checked the formalizations or statements".

40. **MINOR** — draft:33: "so does our own board, which reads it". The deploy recipe re-runs gen_tracker, which also pulls FC main
    (now `research solved`), so after this ships the board may show FC's "solved" beside the database's "open". Check the rendered
    /problem/184 before publishing that sentence.

41. **MINOR** — draft:36 (Labels): the papers get no letter. If they are (c), say so: "OpenAI's paper and Coffey's load-bearing chain:
    (c) — no gap found by our AI seats, no human check; the formalizations, not the papers, carry the theorem."

42. **MINOR** — ins:21 (summary): "wrong-shape and planted-sorry controls fail as they should". Planted-sorry controls elaborate and
    show sorryAx; they do not "fail". Replace: "wrong-shape controls are rejected and planted-sorry controls show sorryAx".

43. **MINOR (bundle the page links)** — README.md:85 promises `SHA256SUMS` "covers every file"; no such file exists. README.md:23
    lists `kim_checks/` but the Kim results cite `seats/referee_kim_checks/`; both directories exist. bridge/Bridge.lean:6 (and the
    byte-identical draft) still says "DRAFT … NOT YET COMPILED" though it is the compiled file. Fix before the link goes live.
