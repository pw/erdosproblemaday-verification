#!/usr/bin/env python3
"""Insert the #341 referee entry at the top of entries[], a HEADLINES card at the top of HEADLINES, and 341 into
CLOSED_BY_LITERATURE in src/index.js. Usage: apply341.py <worktree> [--dry-run]. Each anchor asserted exactly once."""
import sys, pathlib
wt = pathlib.Path(sys.argv[1]); dry = "--dry-run" in sys.argv
p = wt / "src" / "index.js"; s = p.read_text()
body = pathlib.Path("/tmp/erdos2100/entry341_body.html").read_text()
assert "`" not in body and "${" not in body
ENTRY = '''  {
    slug: "341-li-disproof-refereed",
    problemNum: 341,
    title: "#341: Dickson's greedy problem is answered NO — Zhiheng Li's 21-element seed (with GPT-5.6 Sol), refereed: his closed-form set reproduced term for term to 10⁷ by our own greedy, the mod-49 shield and the scale-eight controller recomputed, the Lean kernel-replayed on our machine on the three standard axioms, the statement matched to Erdős–Graham's 1980 wording — and the same seed is periodic under the other summand convention",
    date: "2026-10-13",
    status: "proof_claimed",
    originatedByUs: false,
    summary:
      "Erdős–Graham's version of Dickson's 1934 question: extend a finite set greedily by the least integer that is not a sum of two earlier terms (equal terms allowed) — are the gaps " +
      "always eventually periodic? The proof-claims tab has carried a disproof since 9 August 2026: Zhiheng Li, using GPT-5.6 Sol, writes down the greedy extension of " +
      "A = {1, 2, 3, 5, 7, 13, 22, 27, 28, 32, 36, 40, 47, 48, 52, 63, 71, 77, 81, 89, 97} in closed form — five full residue classes mod 49, three 'rail' classes 7/14/28 switched on and off " +
      "at quotients taken from blocks [4·8^k, 8·8^k) and their two sumset-complements — proves it obeys the rule by a finite residue check, and reads aperiodicity off the geometric blocks. " +
      "Formal Conjectures marks the problem solved; the page and the teorth database still say open. We refereed it: our own greedy from the seed agrees with his set at every integer up to 10⁷ " +
      "(1,224,508 terms, 0 mismatches, mutation controls fail), the residue shield and the three controller identities recompute, the Lean (v4.33.0-rc1, tagged Mathlib) builds in 8,663 jobs " +
      "with the final theorem and the p ≥ 18 family theorem on exactly propext/Classical.choice/Quot.sound, the statement is the problem's negation definition by definition and bridges to the Formal Conjectures statement by a kernel check, and a hostile seat found " +
      "no gap. Also ours: under Queneau's distinct-index variant — the other convention Green lists — the same seed is eventually periodic (gap period 693, certified), so that variant stays open; " +
      "and {1, 4, 9, 16, 25} is periodic within 87 terms under either rule, not 'thousands'. The counterexample is Li's; the board now says NO.",
    body: `
''' + body + '''
`,
    links: [
      { label: "Zhiheng Li, \\"Counterexamples to Erdős Problem 341\\" (paper PDF, repository LiAlreadyExists/Erdos-341)", url: "https://github.com/LiAlreadyExists/Erdos-341/blob/main/paper/Erdos341.pdf" },
      { label: "The Lean formalization — LeanProject/Erdos341.lean (final theorem erdos_341_negative), Erdos341Shield.lean, Erdos341g.lean (the p ≥ 18 family)", url: "https://github.com/LiAlreadyExists/Erdos-341/tree/main/LeanProject" },
      { label: "Zenodo record of the formalization — v2.1.0 (20 Aug 2026, = commit c1d9121), DOI 10.5281/zenodo.22030579", url: "https://doi.org/10.5281/zenodo.22030579" },
      { label: "Zenodo v2.0.1 (20 Aug 2026), the deposit the paper cites, DOI 10.5281/zenodo.22030511 (Lean files identical)", url: "https://doi.org/10.5281/zenodo.22030511" },
      { label: "The proof claim on erdosproblems.com/341 (submitted 9 Aug 2026)", url: "https://www.erdosproblems.com/forum/thread/341/proof-claims" },
      { label: "Formal Conjectures, Erdős 341 — research solved, answer(False), citing Li (PR #6070, 18 Sep 2026)", url: "https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/341.lean" },
      { label: "plby/lean-proofs — Li's development re-hosted on Lean v4.33.0 / Mathlib v4.33.0 with the wrapper theorem not_erdos_341", url: "https://github.com/plby/lean-proofs/blob/8822f7ddef30fadbd92e1c6ab4ed897af356af5e/src/latest/ErdosProblems/Erdos341.lean" },
      { label: "Erdős and Graham, Old and New Problems and Results in Combinatorial Number Theory (1980), p. 53 — the original wording", url: "https://www.math.ucsd.edu/~ronspubs/80_11_number_theory.pdf" },
      { label: "Ben Green, 100 Open Problems — comments to Problem 7 (Dickson's rule vs Queneau's variant)", url: "https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf" },
      { label: "Calkin–Finch, Conditions on periodicity for sum-free sets (Experiment. Math. 1996)", url: "https://doi.org/10.1080/10586458.1996.10504584" },
      { label: "Our July 2026 working report — the finite all-future certificate, 4,094 of 4,095 seeds in [12], the one undecided seed", url: "/report/341" },
      { label: "Our referee bundle — greedy341.c, check_li.py (+ mutations), certify.py, the Lean replay (driver, build log, pp.all audit, controls, leanchecker), referee reports, the live captures, the Erdős–Graham OCR", url: "https://github.com/pw/ErdosProblemADay.com/tree/main/verification/341/li-disproof-refereed" },
      { label: "erdosproblems.com/341", url: "https://www.erdosproblems.com/341" },
    ],
  },
'''
CARD = '''  {
    n: 341, kind: "solved", tag: "REFEREED 13 OCT · READER'S DISPROOF ON THE TAB SINCE 9 AUG · OUR GREEDY REPRODUCES HIS SET TO 10⁷ · KERNEL REPLAY GREEN · BRIDGED TO THE FORMAL CONJECTURES STATEMENT · PREPRINT, NOT PEER-REVIEWED · NOT OURS · UNREVIEWED BY HUMANS",
    title: "Dickson's greedy gaps need not be periodic: a 21-element seed whose greedy extension has no eventual period — Zhiheng Li's August disproof of #341, refereed here",
    line: "Extend a finite set by the least integer that is not a sum of two earlier terms; Erdős–Graham asked whether the gaps are always eventually periodic. " +
      "Li (with GPT-5.6 Sol) writes the greedy extension of {1, 2, 3, 5, 7, 13, 22, 27, 28, 32, 36, 40, 47, 48, 52, 63, 71, 77, 81, 89, 97} in closed form — five full residue classes mod 49 and three rails " +
      "switched by blocks of quotients that grow like powers of eight — and proves it obeys the rule by a finite check mod 49. Our own greedy from the seed matches his set at every integer to 10⁷, " +
      "the Lean builds on the three standard axioms on our machine, and the statement is the problem's negation. Under the other convention (distinct summands, Queneau) the same seed is periodic, " +
      "certified — that variant stays open. The answer to #341 is no; nothing in it is ours.",
    href: "/day/341-li-disproof-refereed",
  },
'''
CBL = "  341,  // Dickson's greedy-gap periodicity question (Erdős–Graham 1980 p.53): answer NO — Zhiheng Li (with GPT-5.6 Sol), Aug 2026, explicit 21-element seed; Lean 4 kernel-replayed on our box 2026-10-13 (8,663 jobs, erdos_341_negative on propext/Classical.choice/Quot.sound, statement matched), own greedy reproduces the set to 10^7, hostile seat no gap, FC statement bridged (Bridge.lean, standard axioms). Preprint (GitHub + Zenodo), not peer-reviewed; Formal Conjectures research-solved 2026-09-18. /day/341-li-disproof-refereed\n"
a1 = "const entries = [\n"; assert s.count(a1) == 1
s = s.replace(a1, a1 + ENTRY, 1)
a2 = "const HEADLINES = [\n"; assert s.count(a2) == 1
s = s.replace(a2, a2 + CARD, 1)
a3 = "const CLOSED_BY_LITERATURE = new Set([\n"; assert s.count(a3) == 1
s = s.replace(a3, a3 + CBL, 1)
assert s.count('slug: "341-li-disproof-refereed"') == 1 and s.count("n: 341, kind:") == 1
if dry: print("dry-run ok; entry chars", len(ENTRY)); sys.exit(0)
p.write_text(s); print("applied")
