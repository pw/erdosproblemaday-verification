import pathlib
p=pathlib.Path('/tmp/erdos160/entry/apply160.py'); s=p.read_text()
n=0
def rep(old,new):
    global s,n
    c=s.count(old); assert c==1,(c,old[:90])
    s=s.replace(old,new); n+=1
rep("each build Shi–Dong's colouring of ℤ/<em>p</em>⁴ℤ and test every pair (<em>a</em>, <em>d</em>), <em>d</em> ≠ 0: for <em>p</em> = 5, 7, 11, 13 (up to 28,561 × 28,560 ≈ 8.2·10⁸\nprogressions) <strong>zero symmetrically coloured 4-APs</strong>, the palette exactly 27<em>p</em> for <em>p</em> ≥ 7 (123–125 of 135 at <em>p</em> = 5), and three controls each find violations: drop\nthe norm coordinate; replace the norm by the isotropic cubic <em>x</em>₁³; drop τ on one digit.",
    "each build Shi–Dong's colouring of ℤ/<em>p</em>⁴ℤ and test every pair (<em>a</em>, <em>d</em>), <em>d</em> ≠ 0 — the Python checker for <em>p</em> = 5, 7, 11, the C checker for <em>p</em> = 5, 7, 11, 13 (up to\n28,561 × 28,560 ≈ 8.2·10⁸ progressions), and seat B's own third implementation for <em>p</em> = 5, 7, 11, so every <em>p</em> ≤ 11 has at least two independent implementations and <em>p</em> = 13\nthe C checker alone: <strong>zero symmetrically coloured 4-APs</strong>; the palette within 27<em>p</em> throughout, attained in full at <em>p</em> = 11 and 13 (297, 351) and by the C checker's cubic at\n<em>p</em> = 7 (189), while the Python checker's cubics leave 10 of 135 and 2 of 189 colours unused at <em>p</em> = 5, 7 (which colours are attained depends on the cubic); and three controls each find violations: drop\nthe <em>Q</em> coordinate; replace the norm by the isotropic cubic <em>x</em>₁³; drop τ on one digit.")
rep("the two independent exhaustive verifications of the 27<em>p</em>-colouring for\n<em>p</em> ≤ 13 and the <em>k</em> = 6 sample",
    "the exhaustive verifications of the 27<em>p</em>-colouring (two independent implementations through <em>p</em> = 11, one at <em>p</em> = 13) and the <em>k</em> = 6 sample")
rep("and enumerated every \" +\n      \"4-AP in ℤ/p⁴ℤ for p = 5, 7, 11, 13 — none symmetrically coloured, palette exactly 27p, three controls fire — sampled",
    "and enumerated every \" +\n      \"4-AP in ℤ/p⁴ℤ for p = 5, 7, 11 (and in C for p = 13) — none symmetrically coloured, palette within 27p, three controls fire — sampled")
rep("enumerated Shi–Dong's 27p-colouring of ℤ/p⁴ℤ for p ≤ 13 in two implementations (none symmetric, palette exactly 27p, controls fire)",
    "enumerated Shi–Dong's 27p-colouring of ℤ/p⁴ℤ for p ≤ 13 (two implementations through p = 11; none symmetric, palette within 27p, controls fire)")
rep("(LeechLattice on MathOverflow, December 2021: partition\nF<sub><em>p</em></sub>³ into the 8<em>p</em>² translates of a twisted cubic)",
    "(LeechLattice on MathOverflow, December 2021: partition\nF<sub><em>p</em></sub>³ into the <em>p</em>² translates of a twisted cubic, project to ℤ and shift, which covers [0, 8<em>p</em>³) with 8<em>p</em>² classes)")
rep("its abstract states the slightly weaker /log log <em>N</em> form, which is what the forum comment quotes)",
    "its abstract states the slightly weaker /log log <em>N</em> form; the forum comment quotes the (log <em>N</em>)<sup>1/6−o(1)</sup> form)")
rep("brute-forced Lemma 4.1 for every <em>P</em> ≤ 121, Lemma 5.1",
    "brute-forced Lemma 4.1 for <em>P</em> = 25, 49, 73, 97, 121 (every <em>P</em> = 24<em>B</em> + 1 up to 121) and for its modulus-4, -6 and -3 variants, Lemma 5.1")
rep("their Remark 4.2 notes that Chevalley–Warning caps what any\nconstant-degree polynomial can add to <em>k</em>²/4 at O<sub><em>k</em></sub>(1).",
    "their Remark 4.2 suggests, by Chevalley–Warning, that a constant-degree polynomial in this framework should not gain more than\nO<sub><em>k</em></sub>(1) dimensions over <em>k</em>²/4 — a heuristic, in their own words \"one should not expect\".")
rep("and Shi–Dong's Remark 4.2 says the polynomial method as used here cannot get there.",
    "and Shi–Dong's Remark 4.2 suggests the polynomial method as used here will not get there.")
rep("(Math. Proc. Cambridge Philos. Soc. 179 (2025) 79–103, peer-reviewed; both are standard Behrend-type colourings and we re-read them)",
    "(Math. Proc. Cambridge Philos. Soc. 179 (2025) 79–103, peer-reviewed; Lemma 7.11 is proved there and seat A re-checked it for <em>a</em> = (1, 2, 3, 4); Lemma 3.2 is a sketch there — a\nBehrend-type pattern-free set after Ruzsa plus random translates, classical — which we did not re-prove)")
rep("(both refereed; seat B matched the two displayed inputs to them word for word, re-derived the exponent arithmetic, and checked that \"exponent above <em>k</em>\" refutes\nConjecture 1.10 with the quantifiers in DTZ's order).",
    "(both refereed; seat B matched the two displayed inputs to them exactly — exponent, range of α, constant dependence; the notation differs — re-derived the exponent arithmetic, and checked that\n\"exponent above <em>k</em>\" refutes Conjecture 1.10 with the quantifiers in DTZ's order; two caveats it names: Gowers's Conjecture 4.2 was read through DTZ's refereed restatement, the GAFA original being\npaywalled and the 2000 preprint on his site carrying no numbered conjectures, and DTZ's own proof of Theorem 2.8 has β<sub><em>k</em></sub> inverted in its final display while the statement Shi–Dong quote is correct).")
rep("and with the digit labels removed ABAB appears on every horizon;",
    "and with the digit labels removed ABAB appears on every horizon, but the three-equal control fires only at <em>L</em> = 2 — at <em>L</em> = 1 the square norm alone admits no three-equal pattern — so our\nchecker reports \"cannot see\" on that row, and seat D's modulus-4 rerun below is the evidence that counts;")
rep("solved by CaDiCaL, each satisfying assignment re-verified by an independent checker and each\nthreshold UNSAT re-proved on a second solver (Glucose 4) under a second encoding (six equality indicators per progression and the seven forbidden two-colour patterns), gives",
    "solved by CaDiCaL, each satisfying assignment re-verified by an independent checker, and the thresholds (13, 3) and (23, 4) re-proved UNSAT on a second solver (Glucose 4)\nunder a second encoding (six equality indicators per progression and the seven forbidden two-colour patterns), gives")
rep("(the solver is still running past 51; the UNSAT at (36, 5) took CaDiCaL 764 s, and Glucose's second-encoding run at (36, 5) had not finished when this went live — the two lower thresholds it has re-proved)",
    "(the search stopped at (52, 6) on its 900-second cap, so <em>h</em>(52) ∈ {6, 7} is undecided; the UNSAT at (36, 5) took CaDiCaL 764 s and rests on CaDiCaL alone until Glucose's second-encoding run at (36, 5), still going when this went live, lands)")
rep("and ruizshi's own comment under Itabe's claim (24 July) says their 1/4 construction was inspired by \"a 1/3 bound suggested by GPT-5.6 Sol\" and that he is \"not entirely\nsure whether our result may have been indirectly influenced by this comment\".",
    "and ruizshi's own comment under Itabe's claim (24 July, 01:38) says: \"it was not until I posted our latest 1/4 result … that I realized there was already a 1/3 argument in this comment.\nTo be honest, while developing our result, we were inspired by a 1/3 bound suggested by GPT-5.6 Sol. Therefore, I am not entirely sure whether our result may have been indirectly influenced by this\ncomment\", adds that an idea suggested by an LLM is hard to attribute precisely, and promises to cite the comment in a future version — which v2 did, four days later.")
rep("and a priority story their 'concurrent' understates — Itabe was public eight days before their v1, and his colouring is exactly their k = 4 colouring restricted to the subgroup pℤ/p⁴ℤ.",
    "and, on priority, that Itabe's manuscript was public eight days before Shi–Dong's v1, which did not cite it; v2 cites it as 'a concurrent result'. Itabe's cubic factor is, up to the choice of basis, their k = 4 colouring restricted to pℤ/p⁴ℤ.")
rep("and a priority story the paper calls 'concurrent' that the dates do not support — Itabe's colouring is their k = 4 colouring restricted to pℤ/p⁴ℤ.",
    "and, on priority, that Itabe was public eight days before Shi–Dong's v1, which did not cite him; v2 calls it 'a concurrent result'. His cubic factor is, up to basis, their k = 4 colouring restricted to pℤ/p⁴ℤ.")
rep("Three colours on every four-term progression: the exponent falls from 0.355 to 1/4 — a cubic field norm kills the one pattern Behrend sets never could",
    "Three colours on every four-term progression: the claimed exponent falls from 0.355 to 1/4 — two preprints, refereed here — and a cubic field norm handles the one pattern Behrend-type colourings had not")
rep("which \" +\n      \"kills the one two-colour pattern (ABBA) that Behrend-style colourings cannot.",
    "which \" +\n      \"handles the one two-colour pattern (ABBA) that Behrend-style colourings are not known to.")
rep("Ours: the referee report, the checks, and the first exact values — h(N) = 3 for 4 ≤ N ≤ 12, 4 for 13 ≤ N ≤ 22, 5 for 23 ≤ N ≤ 35, 6 for 36 ≤ N ≤ 51.",
    "Ours: the referee report, the checks, and exact values we could not find written down anywhere — h(N) = 3, 4, 5, 6 on 4–12, 13–22, 23–35, 36–51.")
rep("Also the first exact values: h(N) = 3, 4, 5 on 4–12, 13–22, 23–35.",
    "Also exact values we could not find written down anywhere: h(N) = 3, 4, 5, 6 on 4–12, 13–22, 23–35, 36–51.")
rep("Shi–Dong's parity step — symmetry forces an even polynomial, so only\nodd layers are needed — is the new algebraic idea, and it is what gets <em>k</em>²/4 dimensions instead of <em>k</em>(<em>k</em>−1)/2.",
    "Shi–Dong's parity step run across every odd layer — symmetry forces an even polynomial, so only\nodd layers are needed — is what is new relative to Führer, and it is what gets <em>k</em>²/4 dimensions instead of <em>k</em>(<em>k</em>−1)/2; Itabe's §7.2 uses the same symmetry for the single cubic layer.")
rep("from the Bloom–Sisask 3-AP bound — because a colour class restricted to [<em>N</em>/4, 3<em>N</em>/4] must be 3-AP-free",
    "from the Bloom–Sisask 3-AP bound via Hunter's observation (MO 410808, 2021): a colour class restricted to [<em>N</em>/4, 3<em>N</em>/4] must be 3-AP-free")
rep("all nine audited endpoints depend on exactly\n<code>[propext, Classical.choice, Quot.sound]</code> (the displayed-threshold identity needs only <code>propext, Quot.sound</code>)",
    "eight of the nine audited endpoints depend on exactly\n<code>[propext, Classical.choice, Quot.sound]</code>, and the ninth, the displayed-threshold identity, on <code>propext</code> and <code>Quot.sound</code> alone")
rep("Clone at the tag, Lean v4.30.0 and Mathlib v4.30.0 — his own pins; because the pin is a tagged release the Mathlib cache downloads in three minutes —\nthen <code>lake build</code> of all 21 first-party modules (174 s), his <code>AxiomAudit.lean</code> under <code>--trust=0</code>:",
    "Clone at the tag, Lean v4.30.0 and Mathlib v4.30.0 — his own pins; the Mathlib cache step took three minutes (a tagged release, and the oleans were already on this box) —\nthen his own <code>check_release.sh</code> built all 21 first-party modules from source and ran his <code>AxiomAudit.lean</code> (174 s for build, audit and scans together; the from-source build is the kernel\ncheck of his modules — Mathlib's own oleans stay trusted until the <code>leanchecker</code> pass below), and our re-run of that audit:")
rep("and the eight-pattern case analysis in the proof of Corollary 1.3 is complete.",
    "and the eight-pattern case analysis that the proof of Corollary 1.3 leaves implicit goes through.")
rep("so that the <em>k</em> symmetry conditions give a degree-(<em>k</em>−1) polynomial <em>k</em> distinct roots",
    "so that the <em>k</em>/2 symmetry conditions give a degree-(<em>k</em>−1) polynomial <em>k</em> distinct roots")
rep("in Shi–Dong's Lemma 2.1 the\n\"interval <em>i</em> − 1 or <em>i</em> + 1\" step needs", "in Shi–Dong's Lemma 2.1 the\nstep to interval <em>i</em> − 1 or <em>i</em> + 1 needs")
rep("Gap 2: Lemma 5.3's \"a carry … would place the\npair on opposite sides of <em>M</em>/2, so τ differs\" is false in general",
    "Gap 2: Lemma 5.3's reason that a carry \"would place the corresponding pair on opposite sides of <em>M</em>/2\" and so change τ is false in general")
rep("and the sentence \"choosing ε &lt; (<em>k</em>−2)²/(4(<em>k</em>−1))\nmakes the exponent larger than <em>k</em>\" is true only once",
    "and the sentence \"choosing ε &lt; (<em>k</em>−2)²/(4(<em>k</em>−1))\nmakes the exponent larger than the random exponent <em>k</em>\" is true only once")
rep("which is exactly\nDeng–Tidor–Zhao's Conjecture 1.6 (\"<em>N</em><sup>o(1)</sup> colours suffice?\"), and which they could only attack with the ℤ/22ℤ tensor construction.",
    "which is exactly\nDeng–Tidor–Zhao's Conjecture 1.6 (an <em>N</em><sup>o(1)</sup>-colouring of [<em>N</em>] without symmetrically coloured 4-APs exists for every <em>N</em>), for which their best construction was the\nℤ/22ℤ tensor power.")
rep("a wrap would move a digit from the top third to the bottom third and so always changes τ", "a wrap would move a digit from the top interval to the bottom one and so always changes τ")
rep("This exercises the layered\npolynomial, which <em>k</em> = 4 does not;", "This exercises a third layer (a degree-5 norm), which <em>k</em> = 4 does not;")
rep("with a randomly chosen irreducible cubic each time (the result is basis-independent, and this tests that):", "with a randomly chosen irreducible cubic each time:")
rep("record, for each digit, which third of [0, <em>p</em>) it lies in", "record, for each digit but the top one, which third of [0, <em>p</em>) it lies in")
rep("the +1 bridge against brute force for <em>N</em> ≤ 7", "the +1 bridge against brute force for 4 ≤ <em>N</em> ≤ 7")
rep("(it holds for every <em>m</em> ≤ 3000, tight at <em>m</em> = 1–3)", "(it holds for every <em>m</em> ≤ 3000; the Lean's floor-square-root version is tight at <em>m</em> = 1–3)")
rep("the modulus 24 is never motivated (any even modulus ≥ 3 works)", "the modulus 24 (DTZ Lemma 7.11's 4!) is not explained in the text; any even modulus ≥ 4 works")
rep("that is <em>h</em>(<em>N</em>) − 1 — Itabe proves the shift in Lean, §9 of his manuscript.", "that is <em>h</em>(<em>N</em>) − 1 for <em>N</em> ≥ 4 — Itabe proves the shift in Lean, §9 of his manuscript.")
rep("for every ε &gt; 0 and all large <em>N</em>, explicitly <em>h</em>(<em>N</em>)<sup>3<em>k</em></sup>", "for every ε &gt; 0 and all large <em>N</em>, explicitly, for every integer <em>k</em> ≥ 1, <em>h</em>(<em>N</em>)<sup>3<em>k</em></sup>")
rep("What no instrument here reaches: Shi–Dong's general-<em>k</em> theorem at <em>k</em> ≥ 8, and", "What no instrument here reaches: the <em>k</em> = 4 colouring itself beyond <em>p</em> = 13 — the primes the <em>N</em><sup>1/4+o(1)</sup> corollary actually uses — Shi–Dong's general-<em>k</em> theorem at <em>k</em> ≥ 8, and")
rep("(DTZ Lemma 7.11 for ABAB; Shi–Dong's Lemma 5.3 and Itabe's §5 for AABB, both with a dyadic bucket label to keep the base-<em>M</em> digits from wrapping).",
    "(DTZ Lemma 7.11 for ABAB; Shi–Dong's Lemma 5.3 and Itabe's §5 for AABB, both with a dyadic bucket label to keep the base-<em>M</em> digits from wrapping; Itabe's §4 handles the three-equal patterns and ABAB together with one mod-24 label).")
rep("records N^{log 3/log 22} ≈ N^{0.355} above", "records N^{log 3/log 22+o(1)} ≈ N^{0.355} above")
rep("last updated 31 August 2025. Nothing in 2026 is refereed.", "last updated 31 August 2025. None of the 2026 claims has been through a journal.")
rep("and unfolds <code>siteH</code> to the infimum over\n<em>k</em> of colourings Icc 1 <em>n</em> → Fin <em>k</em> under which", "and unfolds <code>siteH</code> to the least <em>k</em> for which\nthere is a colouring Icc 1 <em>n</em> → Fin <em>k</em> under which")
rep("Raghavan — 3-AP-free sets of size ≤ exp(−c(log N)^(1/6)/log log N)·N (arXiv:2603.27045, March 2026)", "Raghavan — Improved bounds for 3-progressions: 3-AP-free sets have size ≤ exp(−c(log N)^(1/6)/log log N)·N (arXiv:2603.27045, March–May 2026)")
p.write_text(s); print("applied",n,"fixes; remaining 'exactly 27':", s.count("exactly 27"))
