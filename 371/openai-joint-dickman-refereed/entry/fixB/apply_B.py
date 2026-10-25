#!/usr/bin/env python3
"""Apply blind-read B's MUST/SHOULD/NIT fixes to the #371 entry (entry371.js + the spliced copy in src/index.js),
plus banner/headline/closed_by/OAI_CLAIMS/README/FC-issue counts. Every anchor asserted exactly once per file."""
import sys
WT = sys.argv[1]; dry = '--dry-run' in sys.argv
E = '/tmp/oaimath/012/entry/'
body = [
 # M1
 ("<li>§4 supposes the decorrelation fails along some sequence of scales and passes to a limit profile on (0,∞) × Ẑ. It then amplifies with a divisor weight that counts factorisations n = am, n+1 = c·l.</li>",
  "<li>§2.6 supposes the decorrelation fails along some sequence of scales and passes to a limit profile on (0,∞) × Ẑ. §4 then amplifies that profile with a divisor weight that counts factorisations n = am, n+1 = c·l; Lemma 4.4 shows the profile survives the weight.</li>"),
 ("Then read §4's profile extraction, §5's coupling",
  "Then read §2.6's profile extraction and its preservation under the divisor weight (Lemma 4.4), §5's coupling"),
 # M2 + N1
 ("\"0 &lt; |j| ≤ T\" should be strict. Prop. 7.1 states c₇ = 1/200 where its proof gives 1/80. ",
  "§5.1 writes \"0 &lt; |j| ≤ T\" where §1.2 has the strict 0 &lt; |j| &lt; T (harmless: the non-strict bound is also true). "),
 # M3
 ("the Lean statement and proof of #928 as posed;",
  "an unconditional Lean proof of #928 as posed, stated in Formal Conjectures' density language (jbaelaw/Erdos928 stated #928 in Lean, and proved it from a hypothesised joint law, first);"),
 ("<strong>Formal Conjectures and #928 in Lean (ours).</strong>",
  "<strong>Formal Conjectures' erdos_371 and an unconditional #928 in Lean (ours; #928's Lean statement and the implication were jbaelaw's first).</strong>"),
 # M4
 ("A scan of all 1,837 source files for forbidden constructs found nothing in the proof:",
  "A scan of every Lean file in the closure for forbidden constructs (seat L's, plus the three modules its file list missed, which seat B scanned) found nothing in the proof:"),
 # M5
 ("Its import closure is 1,837 modules and 221,524 lines:</p>",
  "Its import closure is 1,836 modules and 221,509 lines (we built 1,837: that closure plus the one-line umbrella module <code>OAI.NumberTheory.JointDickman</code>, which imports it):</p>"),
 ("1,793 of OpenAI's own (1,457 under <code>JointDickman</code>",
  "1,792 of OpenAI's own (1,456 under <code>JointDickman</code>"),
 ("in 1,626 of the 1,837 modules", "in 1,626 of the 1,836 modules"),
 ("Its Lean proof — 1,837 modules here,", "Its Lean proof — a 1,836-module closure,"),
 # M6
 ("The joint law approaches its limit slowly and from below.",
  "At every tested (a, b) the joint share at 10<sup>10</sup> is below its limit, and at small exponents it is not yet moving toward it: at (0.3, 0.7) it reads 0.0134, 0.0121, 0.0121 at 10<sup>6</sup>, 10<sup>8</sup>, 10<sup>10</sup> against a limit of 0.0152, close to what the second-order term below predicts (0.0118)."),
 # S2
 ("<code>decreasing_order</code> with no hypotheses, over",
  "<code>decreasing_order</code> with no hypotheses beyond 0 &lt; a, b &lt; 1 (no analytic input is assumed), over"),
 # S3
 ("<p>An independent re-check by <code>leanchecker --fresh</code> over the whole closure and our bridge (which replays every declaration through the kernel from the stored terms) exited 0",
  "<p>A second replay by <code>leanchecker --fresh</code> over the whole closure and our bridge (it re-checks every declaration from the stored terms through the same kernel, independently of the build's elaboration) exited 0"),
 # S4
 ("<p>For thresholds n<sup>a</sup> that move with n, the classical second-order term predicts that the marginal density near n is about ρ(1/a) − γρ(1/a − 1)/log n, which is below the limit. At X = 10<sup>10</sup> that predicts 0.2806 for a = ½ and 0.6171 for a = 0.7; we count 0.2811 and 0.6172.</p>",
  "<p>A heuristic check (label (c)). For thresholds n<sup>a</sup> that move with n, de Bruijn's two-term formula for Ψ(x, y) suggests that the marginal density near n is about ρ(1/a) − γρ(1/a − 1)/log n, below the limit. Averaged over n ≤ 10<sup>10</sup> (1/log n averages to about li(X)/X) that gives 0.2806 for a = ½ and 0.6171 for a = 0.7; we count 0.2811 and 0.6172. The pointwise values at n = 10<sup>10</sup> would be 0.2818 and 0.6183.</p>"),
 ("The α-question is (b), modulo Theorem 1.1.",
  "The α-question is (b), modulo Theorem 1.1. The second-order comparison is (c), a heuristic."),
 # S5
 ("McDiarmid's inequality, a Chebyshev bound, the finite-bin distribution) are each supplied by a proof.",
  "McDiarmid's inequality, a Chebyshev bound, a prime-reciprocal sum, the finite-bin distribution) are each supplied by a proof."),
 ("Each of the eight inputs the unconditional proof uses is proved with a non-vacuous statement.",
  "Each of the eight inputs L traced into the unconditional proof is proved with a non-vacuous statement; the two the dependency walk adds (the Chebyshev bound and the prime-reciprocal sum) are proved too (checked by seat B)."),
 # S6
 ("is o(log t), a Littlewood-strength bound the library proves from Weyl differencing.",
  "is o(log t), a bound weaker than Littlewood's O(log t/log log t) that the library proves from Weyl differencing."),
 # S7
 ("141 of them OpenAI's Matomäki–Radziwiłł and Halász files",
  "141 of them OpenAI's Matomäki–Radziwiłł and Halász files (140 of those from <code>TwoPointCorrelations</code>, the Lean of OpenAI's sibling family 007, \"Ordinary two-point correlations of multiplicative functions\", which the paper does not cite)"),
 # S8
 ("Epoch's four Lean runs on <code>Erdos371</code> (September, $300–$1,000 budgets) were all scored incomplete.",
  "Epoch's four LeanOpenProblems runs on <code>Erdos371</code> ($300–$1,000 budgets) are all scored \"I\" in its results."),
 # S9
 ("and Erdős–Pomerance p. 311 against their sources; every arXiv version cited is current.",
  "and Erdős–Pomerance p. 311 against their sources; every arXiv version cited is current. W could not open de la Bretèche–Pomerance–Tenenbaum, Lü–Wang or Wang 2021 in full; those three are checked only secondhand."),
 # S10
 ("It says Erdős and Pomerance proved that each ordering has positive upper density; their paper says \"the lower density of integers n for which P(n) &gt; P(n+1) is positive\", which is stronger.",
  "It says Erdős and Pomerance proved that this set and its complement both have positive upper density. Their paper proves positive lower density, which is stronger: \"the lower density of integers n for which P(n) &gt; P(n+1) is positive\" (p. 312), and §6 (p. 319) gives at least 0.0099 and adds \"the same is true for integers n for which P(n) &lt; P(n+1)\"."),
 ("They proved that each ordering occurs for a positive proportion of n.",
  "They proved that each ordering has positive lower density (at least 0.0099)."),
 # S11
 ("Erdős and Pomerance posed it in 1978, together with",
  "Erdős and Pomerance stated it in 1978 (the paper and Teräväinen trace the ordering question to Erdős and Turán), together with"),
 ("Erdős and Pomerance conjectured in 1978 that P(n) < P(n+1)",
  "Erdős and Pomerance stated in 1978 (the question goes back to Erdős and Turán) that P(n) < P(n+1) should hold"),
 # S13
 ("Tao and Teräväinen proved it in natural density at almost all scales.",
  "Tao and Teräväinen sketched it at almost all scales in 2019 (their Remark 3.3) and proved a quantitative form, still outside an exceptional set of scales, in 2025–26."),
 # N2
 ("All coupling failures together cost O(B<sup>50</sup>/P₀).",
  "All coupling failures together cost O(B<sup>50</sup>/P₀) + O(B<sup>50</sup>e<sup>−B</sup>)."),
 # N3
 ("decided with a margin of 10<sup>−9</sup> in log(P(n+1)/P(n)) − α·log n.",
  "decided with a margin of 10<sup>−9</sup> in 20·(log(P(n+1)/P(n)) − α·log n), that is 5·10<sup>−11</sup> in the quantity itself."),
 # N5
 ("match the comparator's character for character: 10 of 10.",
  "match the comparator's character for character (after collapsing whitespace and dropping <code>noncomputable</code> and <code>@[reducible]</code> markers): 10 of 10."),
 # N6
 ("Their 2026 paper (arXiv 2512.01739v2, Theorem 1.8)",
  "Their later paper (arXiv 2512.01739; v1 1 December 2025, v2 2026; Theorem 1.8)"),
 # N7
 ("for all n beyond an explicit n₀, because", "for all n ≥ n₀ = ⌈2<sup>β/δ</sup>⌉, because"),
 # N8
 ("Two of the library's docstrings, though, still describe discharged inputs as",
  "One of the library's docstrings (in <code>PublishedInputs.lean</code>), though, still describes discharged inputs as"),
 # N9
 ("An older conditional route through", "A conditional route through"),
 # N11
 ("Seat R found the same consequence unprompted.", "Seats R and W found the same consequence unprompted."),
 # N12
 ("Each entry is #{n ≤ X : P(n) ≤ n<sup>a</sup>, P(n+1) ≤ n<sup>b</sup>} divided by the product of #{n ≤ X : P(n) ≤ n<sup>a</sup>}/X and #{n ≤ X : P(n+1) ≤ n<sup>b</sup>}",
  "Each entry is (1/X)·#{n ≤ X : P(n) ≤ n<sup>a</sup>, P(n+1) ≤ n<sup>b</sup>} divided by the product of (1/X)·#{n ≤ X : P(n) ≤ n<sup>a</sup>} and (1/X)·#{n ≤ X : P(n+1) ≤ n<sup>b</sup>}"),
 # N13
 ("[ErPo78, p. 320; Er79e; ErGr80, p. 70; Er85c, p. 82]", "[ErPo78, p. 320; Er79e; ErGr80, p. 70; Er85c, p. 82; Va99, 1.10]"),
]
index_only = [
 ("via the joint Dickman law in natural density — refereed here 22 Oct, see /day/371-openai-joint-dickman-law-refereed",
  "via the joint Dickman law in natural density — read by four AI seats here 22 Oct, see /day/371-openai-joint-dickman-law-refereed"),
]
label = [("1,837 modules (1,793 OpenAI + patched PrimeNumberTheoremAnd/StrongPNT + LeanArchitect), 0 errors",
          "PaperMain's 1,836-module closure (1,792 OpenAI + patched PrimeNumberTheoremAnd/StrongPNT + LeanArchitect) plus the umbrella module, 0 errors")]
head = [("LEAN KERNEL-REPLAYED HERE (1,837 MODULES", "LEAN KERNEL-REPLAYED HERE (1,836-MODULE CLOSURE")]
closed = [("Its Lean (1,837 modules incl.", "Its Lean (1,836-module closure incl.")]
def apply(path, pairs, jsonish=False):
    s = open(path).read()
    for o, n in pairs:
        oo, nn = (o, n)
        if jsonish:  # LEAN_LABEL is json.dumps'd into index.js; quotes inside our pairs are plain text
            oo, nn = o.replace('"', '\\"'), n.replace('"', '\\"')
        c = s.count(oo); assert c == 1, (path, o[:70], c); s = s.replace(oo, nn)
    if not dry: open(path, 'w').write(s)
    print(('checked ' if dry else 'applied ') + path, len(pairs))
apply(E + 'entry371.js', body)
apply(WT + '/src/index.js', body + index_only + head + closed)
apply(WT + '/src/index.js', label, jsonish=True)
apply(E + 'lean_label.txt', label); apply(E + 'headline.js', head); apply(E + 'closed_by.txt', closed)
