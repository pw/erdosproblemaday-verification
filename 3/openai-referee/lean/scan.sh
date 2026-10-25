#!/bin/bash
# Source scan of OpenAI's OAI/Combinatorics/Progressions tree (the import cone of the Erdős #3 Lean proof, besides Mathlib).
# Usage: scan.sh <path-to-openai-math/lean>  — prints counts; a nonzero count on a forbidden construct is a finding.
# Positive control: run it on a directory containing a file with `sorry` and the sorry count must be nonzero (see scan_control.log).
L="$1"; T="$L/OAI/Combinatorics/Progressions"
echo "files: $(find $T $L/OAI/Combinatorics/Progressions.lean -name '*.lean' 2>/dev/null | wc -l)   lines: $(find $T $L/OAI/Combinatorics/Progressions.lean -name '*.lean' 2>/dev/null | xargs cat | wc -l)"
echo "imports outside Mathlib/own tree: $(grep -rh '^import ' $T $L/OAI/Combinatorics/Progressions.lean 2>/dev/null | sed 's/import //' | grep -v '^Mathlib' | grep -v '^OAI\.Combinatorics\.Progressions' | sort -u | wc -l)"
for pat in '\bsorry\b' '\badmit\b' '^\s*axiom\b' 'native_decide' 'implemented_by' '@\[extern' '\bunsafe\b' '^\s*opaque\b' 'partial def' 'maxHeartbeats' 'maxRecDepth' 'set_option debug'; do
  n=$(grep -rnE -- "$pat" $T $L/OAI/Combinatorics/Progressions.lean 2>/dev/null | grep -vE '^[^:]+:[0-9]+:\s*--' | wc -l); printf "%-20s %s\n" "$pat" "$n"; done
