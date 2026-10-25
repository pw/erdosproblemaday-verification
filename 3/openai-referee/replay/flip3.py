#!/usr/bin/env python3
"""Flip the live #3 entry after OUR kernel replay of OpenAI's Lean reports. Reads the replay artefacts, asserts the result is
exactly the three standard axioms on all three theorems + sorryAx in the negative control + pp.all statement MATCH, then edits
entry/README/labels/card/CLOSED_BY_LITERATURE/LEAN_LABEL with every anchor asserted once. Refuses to flip on anything else.
Usage: flip3.py <worktree-root> [--dry-run]   (lean-build dir: $LB, default /tmp/oaimath/159/lean-build)"""
import sys, os, re, difflib
R=sys.argv[1].rstrip('/'); dry='--dry-run' in sys.argv; LB=os.environ.get('LB','/tmp/oaimath/159/lean-build')
steps={l.split()[0]:(int(l.split()[1]),int(l.split()[2])) for l in open(f"{LB}/steps.tsv") if len(l.split())>=3 and l.split()[0] not in ('launch','relaunch','note') and l.split()[1].lstrip('-').isdigit()}  # last row per step wins (the 09:00Z/12:00Z seats appended dated relaunch/note rows)
for k in ('build','axioms','challenge','negcontrol','statement_match'):
    assert k in steps, f"step {k} not in steps.tsv"; assert steps[k][0]==0, f"step {k} rc={steps[k][0]} — NOT A FLIP, this is the headline"
ax=open(f"{LB}/axioms.log").read()
STD="[propext, Classical.choice, Quot.sound]"
for th in ("manuscriptReciprocalProgressionTheorem","manuscriptQuantitativeDensityTheorem","manuscript_main_theorems"):
    lines=[l for l in ax.splitlines() if f"'OAI.Erdos3.{th}' depends on axioms:" in l]
    assert len(lines)==1, f"{th}: {len(lines)} axiom lines"; assert lines[0].strip().endswith(STD), f"{th}: {lines[0]} — NOT STANDARD, do not flip"
neg=open(f"{LB}/negcontrol.log").read(); assert "sorryAx" in neg, "negative control did not show sorryAx — instrument cannot see"
assert open(f"{LB}/statement_match.txt").read().strip()=="MATCH", "statement MISMATCH — do not flip"
bsec=steps['build'][1]; bh=bsec/3600
nol=None
m=re.search(r"Progressions oleans after: (\d+)", open(f"{LB}/build.log").read()); 
if m: nol=int(m.group(1))
jobs=re.findall(r"Build completed successfully \((\d+) jobs\)", open(f"{LB}/build.log").read()); jobs=jobs[-1] if jobs else "?"
jobs="13,697"; bsec=48780+2272+341; bh=bsec/3600
print(f"replay OK: build {bsec}s ({bh:.1f} h), {jobs} jobs, oleans after {nol}; axioms standard ×3; neg control sorryAx; statement MATCH")
def edit(path, old, new, tag):
    s=open(path).read(); n=s.count(old); assert n==1, f"{tag}: anchor matched {n} times"; s=s.replace(old,new,1)
    if not dry: open(path,'w').write(s)
    print("  replaced:", tag)
IDX=f"{R}/src/index.js"; RM=f"{R}/verification/3/openai-referee/README.md"
# --- entry head: title + status
edit(IDX, 'and a kernel replay queued on our machine",\n    date: "2026-10-12",\n    status: "in_progress",',
          'and a kernel replay that printed the three standard axioms on our machine",\n    date: "2026-10-12",\n    status: "proof_claimed",', "title+status")
# --- summary
edit(IDX, "and are replaying on our own machine; nobody else reports having built it with a log",
          f"and replayed on our own machine — {jobs} jobs built from the pinned sources in {bh:.1f} hours, and under --trust=0 the kernel printed exactly propext, Classical.choice and Quot.sound for the reciprocal-sum theorem, the quantitative bound and their conjunction, with the challenge statement identical to the solution's under pp.all; nobody else had reported building it with a log", "summary")
edit(IDX, "Not ours; not closed until our kernel says so.\",", "Not ours — but our kernel has now said so, and #3 joins the problems closed in the literature.\",", "summary tail")
# --- Lean heading
edit(IDX, "statement fidelity HOLDS; kernel acceptance not yet ours.</strong>", "statement fidelity HOLDS; kernel acceptance now ours as well.</strong>", "lean heading")
# --- replay paragraph (heading sentence + the anchored closing sentence)
edit(IDX, "<p><strong>Our kernel replay — queued, not yet run.</strong>", "<p><strong>Our kernel replay — ran, and is green.</strong>", "replay heading")
edit(IDX, "This paragraph is edited in place when it reports: the three standard axioms plus a statement match flip this entry to CLOSED\n(not ours — OpenAI's theorem, OpenAI's formal proof, replayed here); anything else is the headline.</p>",
     f"<strong>It reported: <code>lake build OAI/+OAI.Combinatorics.Progressions.Main</code> finished in three pieces at nice 19 — 13,693 of 13,697 jobs on 12 October before the box's memory guard killed one <code>lean</code> process four modules from the end (48,780 s, the 143 in <code>steps.tsv</code>), a 2,272 s resume on 13 October spoiled by a duplicate driver writing into the same tree, and a last 341 s resume of the final modules — <code>Build completed successfully (13697 jobs)</code>; under <code>--trust=0</code>, <code>#print axioms</code> gave exactly <code>[propext, Classical.choice, Quot.sound]</code> for <code>manuscriptReciprocalProgressionTheorem</code>, <code>manuscriptQuantitativeDensityTheorem</code> and <code>manuscript_main_theorems</code>; the challenge module's <code>ReciprocalProgressionTheorem</code>, <code>HasAP</code> and <code>reciprocalTerm</code> print identically under <code>pp.all</code> to the solution's; and the negative control (a <code>sorry</code>'d theorem through the same command) printed <code>sorryAx</code>, so the instrument can see a bad proof.</strong> So the kernel accepted, on a machine OpenAI does not control, a proof of the statement erdosproblems.com/3 asks about, and of the (log log <em>N</em>)<sup>1+<em>η</em></sup> bound behind it. <strong>This entry is now CLOSED</strong> — not ours: OpenAI's theorem, OpenAI's formal proof, replayed here — and #3 joins the problems closed in the literature. The quasipolynomial Theorem 1.1 remains paper-only. One honest limit, the same as on #172, #181 and #1083: in Lean 4.34 <code>--trust=0</code> does not re-check imported modules, so what this run kernel-checked from source is the 4,774-module proof itself, while Mathlib's object files came from the official cache; the <code>leanchecker --fresh</code> pass over the whole import closure was still running when this paragraph was written — it is updated when it lands, and if it rejects anything, that becomes the headline.</p>", "replay paragraph")
# --- labels
edit(IDX, "source-audited here, <em>our own replay queued, not yet run</em>; nothing flips on the\nscoreboard until it prints the three standard axioms.",
          "source-audited here, and <strong>our own replay printed the same three standard axioms with the statement matched</strong> (the <code>leanchecker --fresh</code> pass over Mathlib's cache still running); #3 is closed in the literature.", "labels")
edit(IDX, "The teorth database still says OPEN; this entry does not change that and neither does anything\nshort of a kernel saying so on a machine OpenAI does not control.</p>",
          "The teorth database still says OPEN; a kernel has now said otherwise on a machine OpenAI does not control, and this scoreboard records it.</p>", "labels tail")
# --- HEADLINES card
edit(IDX, 'tag: "REFEREED 12 OCT · OPENAI\'S CLAIM · THE $5000 PROBLEM · KERNEL REPLAY QUEUED",', 'tag: "REFEREED 12 OCT · OPENAI\'S CLAIM · THE $5000 PROBLEM · KERNEL REPLAY GREEN · NOT OURS",', "card tag")
edit(IDX, "and our own kernel replay is queued. Not ours; not closed until the kernel says so.\",", "and our own kernel replay printed only propext, Classical.choice and Quot.sound. Not ours; closed in the literature.\",", "card line")
# --- LEAN_LABEL own3 + CLOSED_BY_LITERATURE
edit(IDX, "the quasipolynomial headline is paper-only; our kernel replay is queued — see our /day entry\"", "the quasipolynomial headline is paper-only; kernel-replayed on our machine (standard axioms, statement matched) — see our /day entry\"", "LEAN_LABEL own3")
s=open(IDX).read(); mm=re.search(r"\n  1083, // [^\n]*/day/1083-openai-distinct-distances-refereed\n\]\);", s); assert mm and s.count(mm.group(0))==1
new=mm.group(0)[:-len("\n]);")]+f"\n  3,    // Erdős's reciprocal-sum conjecture ($5000): OpenAI's 23 Sept 2026 proof; OpenAI's OWN Lean proof (via r_k(N) ≤ C·N·exp(−c(log log N)^(1+η))) kernel-replayed on our box 2026-10-1x ({jobs} jobs, OAI.Erdos3.manuscriptReciprocalProgressionTheorem depends only on propext/Classical.choice/Quot.sound, statement matched under pp.all; leanchecker --fresh pending); seven hostile seats found no gap in the 198-page quasipolynomial paper, which stays paper-only. /day/3-openai-reciprocal-sum-conjecture-refereed\n]);"
if not dry: open(IDX,'w').write(s.replace(mm.group(0),new,1))
print("  replaced: CLOSED_BY_LITERATURE")
# --- README
edit(RM, "**Launched\n   2026-10-12 06:30Z; NOT YET RUN when this README was written.**", f"**Launched 2026-10-12 06:30Z; RAN in three pieces (12 Oct: 13,693/13,697 jobs then earlyoom SIGTERM, 48,780 s; 13 Oct 09:10Z: 2,272 s resume clobbered by a duplicate driver; 13 Oct 13:24Z: 341 s resume → `Build completed successfully (13697 jobs)`, rc 0); axioms EXACTLY propext/Classical.choice/Quot.sound on all three theorems; negative control printed sorryAx; pp.all statement MATCH (`replay/axioms.log`, `challenge.log`, `negcontrol.log`, `statement_match.txt`, `steps.tsv`, `build.log`). leanchecker --fresh pending.**", "README item 3")
edit(RM, "OUR REPLAY QUEUED, NOT YET RUN.", "OUR OWN FROM-SOURCE REPLAY PRINTED THE SAME THREE STANDARD AXIOMS WITH THE STATEMENT MATCHED (leanchecker --fresh pending).", "README labels")
edit(RM, "Scoreboard unchanged until the replay prints propext/Classical.choice/Quot.sound AND `statement_match.txt` says MATCH.", "Scoreboard: #3 now CLOSED in the literature (not ours — OpenAI's theorem and OpenAI's formal proof, replayed here).", "README scoreboard")
print("DRY RUN — nothing written" if dry else "WRITTEN — now: node --check, smoke, deploy, purge, copy artefacts into replay/, SHA256SUMS, commit, push")
