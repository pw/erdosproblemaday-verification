#!/usr/bin/env python3
"""In-place edit of the live #1083 entry after our kernel replay landed (build + verify.sh + three audits green, standard axioms;
leanchecker --fresh over the import closure still running). Every replacement anchored on exact live text, asserted once.
Usage: flip1083.py <index.js> [--dry-run]"""
import sys, re, difflib
P = sys.argv[1]; dry = '--dry-run' in sys.argv
s = open(P).read(); orig = s
def rep(old, new, tag):
    global s
    n = s.count(old); assert n == 1, f"{tag}: anchor matched {n} times (expected 1)"
    s = s.replace(old, new, 1); print(f"  replaced: {tag}")

# 1. head: title + status
rep('    slug: "1083-openai-distinct-distances-refereed",\n    problemNum: 1083,\n'
    '    title: "#1083: OpenAI\'s proof of the higher-dimensional distinct-distances conjecture, constant factor included — 103 pages read by twelve hostile seats, sources checked, and a third-party Lean 4 kernel check we are replaying",\n'
    '    date: "2026-10-11",\n    status: "in_progress",',
    '    slug: "1083-openai-distinct-distances-refereed",\n    problemNum: 1083,\n'
    '    title: "#1083: OpenAI\'s proof of the higher-dimensional distinct-distances conjecture, constant factor included — 103 pages read by twelve hostile seats, sources checked, and a third-party Lean 4 kernel check replayed on our own machine",\n'
    '    date: "2026-10-11",\n    status: "proof_claimed",', "status+title")

# 2. summary
rep("— taking a weaker planar route that, it turns out, the paper never needed — with our own kernel replay queued behind #181's. Verdict on the paper as written:",
    "— taking a weaker planar route that, it turns out, the paper never needed — and our own from-source kernel replay of it printed exactly the three standard axioms (the fresh re-check of Mathlib's cached object files is still running); #1083 is closed in the literature. Verdict on the paper as written:",
    "summary")

# 3. Lean paragraph heading
rep("<p><strong>The Lean 4 formalization, at source (seat: lean) — statement fidelity HOLDS; kernel acceptance not yet ours.</strong>",
    "<p><strong>The Lean 4 formalization, at source (seat: lean) — statement fidelity HOLDS; kernel acceptance now ours as well.</strong>",
    "lean heading")

# 4. conditional → fact
rep("If our replay is green, that is a fact about the <em>theorem</em>:",
    "Our replay is green (below), so that is a fact about the <em>theorem</em>:",
    "lean conditional")

# 5. replay paragraph tail
old_tail = ("trust in the formal object therefore rests on an independent kernel run. Ours is queued on this machine behind the #181\n"
 "replay whose 22 GB of built packages it reuses (the manifests pin the same OpenAI and Mathlib revisions), gated on memory\n"
 "headroom; it builds from the pinned sources, runs the repository's verify.sh, compiles its three audit files under\n"
 "<code>--trust=0</code>, and then runs <code>leanchecker --fresh</code> over the whole import closure. This paragraph is edited in\n"
 "place when it finishes; three standard axioms flip this entry to CLOSED, anything else is the headline.</p>")
new_tail = ("trust in the formal object therefore rests on an independent kernel run. <strong>Ours ran on this machine on 12 October and is green.</strong> "
 "It waited behind the #181 replay, whose 22 GB of built packages it reuses (the two lake manifests pin the same OpenAI revision "
 "<code>adc7f124</code> and the same Mathlib <code>d13f23b7</code>; the driver asserts this), opened its gates at 01:37Z with 39 GB free, "
 "checked out the pinned commit <code>88919b8</code>, applied the repository's own OpenAI patches, fetched Mathlib's object files from the "
 "official cache, and built: <code>lake build DistinctDistances.Main</code> — <strong>10,172 jobs in 13,960 s (3 h 53 min) at nice 19 on four threads, "
 "<code>Build completed successfully</code>, zero <code>error</code> lines</strong>. The repository's <code>scripts/verify.sh</code> then "
 "exited 0 in 153 s: <code>Challenge.lean</code> matches its frozen blob; the copied Formal Conjectures definitions are identical in "
 "statement and proof; <code>challenge exit 0, main exit 0, pp.all outputs identical: True</code>; and under <code>--trust=0</code> "
 "<code>'DistinctDistances.jsp_000900' depends on axioms: [propext, Classical.choice, Quot.sound]</code> — <code>PASS: all axioms are in "
 "the permitted set</code>, <code>scanned 756 files: PASS: no forbidden constructs</code>. The three audit files "
 "(<code>Audit/TargetProbes.lean</code>, <code>Audit/IndependentRestatement.lean</code>, <code>Audit/NonVacuity.lean</code>) compiled under "
 "<code>--trust=0</code> on the same build (14 s, 14 s, 30 s), their probes carrying the same three axioms. So the kernel accepted, on our "
 "machine, a proof of Theorem 1.1 with its constant factor, which implies the statement erdosproblems.com/1083 asks about. "
 "<strong>This entry is now CLOSED</strong> — not ours: the theorem is OpenAI's, the formal proof Yao Xu's — and #1083 joins the "
 "problems closed in the literature. The driver, <code>steps.tsv</code>, the axiom output, the verify and audit excerpts and the build "
 "log are in the bundle. One honest limit, the same one as on #172 and #181: in Lean 4.34 <code>--trust=0</code> no longer re-checks "
 "imported modules, so what this run kernel-checked from source is the proof itself and OpenAI's 503-module library, while Mathlib's "
 "object files came from the cache; the <code>leanchecker --fresh</code> pass over the whole import closure, Mathlib included, started "
 "at 05:43Z on 12 October and was still running when this paragraph was written — it is updated when it lands, and if it rejects "
 "anything, that becomes the headline.</p>")
rep(old_tail, new_tail, "replay paragraph")

# 6. closing paragraph
rep("Our own replay of it is queued on this machine behind the #181 replay and starts when memory allows; the Lean paragraph above is\n"
    "edited in place when it reports.</p>",
    "Our own replay of it ran on this machine on 12 October and printed the same three standard axioms; the Lean paragraph above has\n"
    "the numbers, and the Mathlib cache re-check is the one piece still running.</p>", "closing paragraph")

# 7. labels
rep("author-reported replays, <em>our own\nreplay queued, not yet run</em>. The paper as written:",
    "author-reported replays, and <strong>our own\nfrom-source replay printed the same three standard axioms</strong> (the <code>leanchecker --fresh</code> pass over Mathlib's cached object files still running). The paper as written:",
    "labels")
rep("This entry does not change the scoreboard: #1083 is not closed by our standard until our own replay prints\n"
    "the three standard axioms. The teorth database still says OPEN",
    "This entry now moves the scoreboard: #1083 joins the problems closed in the literature — closed by OpenAI's theorem and\n"
    "Yao Xu's kernel proof, replayed here, none of it ours. The teorth database still says OPEN", "scoreboard sentence")

# 8. HEADLINES card (reason: its tag and line said the replay was QUEUED; it has run)
rep('tag: "REFEREED 11–12 OCT · OPENAI\'S CLAIM · TWELVE SEATS, NO GAP FOUND · KERNEL REPLAY QUEUED",',
    'tag: "REFEREED 11–12 OCT · OPENAI\'S CLAIM · TWELVE SEATS, NO GAP FOUND · KERNEL REPLAY GREEN · NOT OURS",', "headline tag")
rep("a third-party Lean 4 proof exists and our own kernel replay is queued. Not ours; not closed until the kernel says so.",
    "a third-party Lean 4 proof exists and our own kernel replay of it printed only propext, Classical.choice and Quot.sound (the fresh re-check of Mathlib's cache still running). Not ours; closed in the literature.",
    "headline line")

# 9. LEAN_LABEL
rep('third1083: "no Lean in the release — but a third-party Lean 4 proof following the paper (Yao Xu, cadamcat/distinct-distances-lean4) exists; twelve hostile seats read the paper and our kernel replay is queued — see our /day entry"',
    'third1083: "no Lean in the release — but a third-party Lean 4 proof following the paper (Yao Xu, cadamcat/distinct-distances-lean4) exists and was kernel-replayed on our machine on 12 Oct 2026 (standard axioms; the leanchecker --fresh pass over Mathlib\'s cache still running); twelve hostile seats read the paper — see our /day entry"',
    "LEAN_LABEL third1083")

# 10. CLOSED_BY_LITERATURE += 1083 (after the 181 line)
m = re.search(r"\n  181,  // [^\n]*/day/181-openai-hypercube-ramsey-refereed\n\]\);", s)
assert m and s.count(m.group(0)) == 1, "CLOSED_BY_LITERATURE 181 line not found once"
line1083 = ("\n  1083, // Erdős distinct distances in ℝ^d, d ≥ 3, with the constant factor: OpenAI's 23 Sept 2026 proof; third-party Lean 4 proof (Yao Xu, cadamcat/distinct-distances-lean4) kernel-replayed on our box 2026-10-12 (10,172 jobs, verify.sh PASS, DistinctDistances.jsp_000900 depends only on propext/Classical.choice/Quot.sound; leanchecker --fresh pending); twelve hostile seats found no mathematical gap in the paper. /day/1083-openai-distinct-distances-refereed")
s = s.replace(m.group(0), m.group(0)[:-len("\n]);")] + line1083 + "\n]);", 1); print("  replaced: CLOSED_BY_LITERATURE")

assert s.count("1083-openai-distinct-distances-refereed") == orig.count("1083-openai-distinct-distances-refereed") + 1
if dry:
    for l in difflib.unified_diff(orig.splitlines(), s.splitlines(), lineterm="", n=0):
        if l.startswith(("+","-")) and not l.startswith(("+++","---")): print(l[:160])
    print("DRY RUN — nothing written")
else:
    open(P,"w").write(s); print("WRITTEN")
