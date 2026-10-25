#!/usr/bin/env python3
"""Anchored in-place edit for the #1083 entry + bundle README once leanchecker --fresh landed.
Each anchor must occur EXACTLY once before the edit and ZERO times after; the new text must occur exactly once after."""
import sys, pathlib
root = pathlib.Path(sys.argv[1])
dry = "--dry-run" in sys.argv
def edit(path, old, new):
    p = root / path; s = p.read_text()
    n = s.count(old)
    assert n == 1, f"{path}: anchor count {n} != 1 for {old[:60]!r}"
    assert s.count(new) == 0, f"{path}: new text already present"
    s2 = s.replace(old, new)
    assert s2.count(new) == 1 and s2.count(old) == 0
    if not dry: p.write_text(s2)
    print(f"{'DRY ' if dry else ''}edited {path}: {old[:50]!r} -> {new[:50]!r}")

# 1. the /day entry's pending sentence
edit("src/index.js",
 "the <code>leanchecker --fresh</code> pass over the whole import closure, Mathlib included, started at 05:43Z on 12 October and was still running when this paragraph was written — it is updated when it lands, and if it rejects anything, that becomes the headline.</p>",
 "the <code>leanchecker --fresh</code> pass over the whole import closure, Mathlib included, started at 05:43Z on 12 October and <strong>exited 0 after 7,919 s (2 h 12 min)</strong> at 07:55Z, printing only Lake's \"has local changes\" warnings and no error line. The two controls for reading that silence as a pass ran on the same build (<code>replay/leanchecker_controls.log</code>): a module that does not exist exits 1 with \"Could not find any oleans\"; a real module exits 0 printing nothing. So Mathlib's cached object files are now kernel-checked too, and nothing in the import closure was rejected.</p>")

# 2. README item 2
edit("verification/1083/openai-referee/README.md",
 "the `leanchecker --fresh\n   DistinctDistances.Main` pass over the whole import closure started 2026-10-12T05:43:04Z and was STILL RUNNING when this README was\n   edited — its log and rc are added here when it lands (sentence in the /day entry anchored \"it is updated when it lands\"), together\n   with the neg/pos controls for reading its silence as a pass (shape: `verification/181/openai-referee/replay/leanchecker_controls.sh`).",
 "the `leanchecker --fresh\n   DistinctDistances.Main` pass over the whole import closure started 2026-10-12T05:43:04Z and EXITED 0 at 07:55:03Z after 7,919 s\n   (`replay/steps.tsv` row `leanchecker_fresh 0 7919`; `replay/leanchecker_fresh.log` = 23 Lake \"has local changes\" warnings, no\n   error line). Controls on the same build (`replay/leanchecker_controls.{sh,log}`): NEG `leanchecker DistinctDistances.DoesNotExist`\n   → \"Could not find any oleans\", rc=1; POS `leanchecker DistinctDistances.Framework` (non-fresh) → silent, rc=0. The Mathlib cache is\n   therefore kernel-checked too; nothing in the import closure was rejected.")

# 3. README Labels line
edit("verification/1083/openai-referee/README.md",
 "OWN FROM-SOURCE REPLAY PRINTED THE SAME THREE STANDARD AXIOMS (verify.sh PASS 2026-10-12 05:42Z; leanchecker --fresh over Mathlib's\ncache still running when this was written).",
 "OWN FROM-SOURCE REPLAY PRINTED THE SAME THREE STANDARD AXIOMS (verify.sh PASS 2026-10-12 05:42Z; leanchecker --fresh over the whole\nimport closure, Mathlib's cache included, exited 0 at 07:55Z).")
edit("verification/1083/openai-referee/README.md",
 "Yao Xu's formal proof, replayed here); the Mathlib cache re-check is the one pending piece.",
 "Yao Xu's formal proof, replayed here); nothing pending.")
print("OK")
