#!/bin/bash
# Source scan of OpenAI's OAI/Analysis/Littlewood tree (the import cone of the Erdős #1150 Lean proof, besides Mathlib).
# Usage: scan.sh <path-to-openai-math/lean>. Positive control: scan_control.log (a planted `sorry` must count 1).
L="$1"; T="$L/OAI/Analysis/Littlewood"
echo "files: $(find $T -name '*.lean' | wc -l)   lines: $(find $T -name '*.lean' | xargs cat | wc -l)"
echo "imports outside Mathlib/own tree: $(grep -rh '^import ' $T | sed 's/import //' | grep -v '^Mathlib' | grep -v '^OAI\.Analysis\.Littlewood' | sort -u)"
for pat in '\bsorry\b' '\badmit\b' '^\s*axiom\b' 'native_decide' 'implemented_by' '@\[extern' '\bunsafe\b' '^\s*opaque\b' 'partial def' 'maxHeartbeats' 'maxRecDepth' 'set_option debug'; do
  n=$(grep -rnE -- "$pat" $T 2>/dev/null | grep -vE '^[^:]+:[0-9]+:\s*--' | wc -l); printf "%-20s %s\n" "$pat" "$n"; done
