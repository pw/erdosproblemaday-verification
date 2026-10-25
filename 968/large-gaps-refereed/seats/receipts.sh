#!/bin/bash
# Model receipts for #968 seats: count served-model fields in each agent/session transcript.
T06=/tmp/claude-1000/-home-exedev/d7d10d2c-6fd8-410b-996a-c84a0f6e80b6/tasks
T09=/tmp/claude-1000/-home-exedev/80cf1b4e-f619-4b45-b10a-6f3d89b30269/tasks
row(){ local seat="$1" f=$(readlink -f "$2"); local o=$(grep -o '"model":"claude-opus-5-5"' "$f" | wc -l); local other=$(grep -o '"model":"[^"]*"' "$f" | grep -v -e claude-opus-5-5 -e '<synthetic>' -e '"model":"opus"' | wc -l); local syn=$(grep -o '"model":"<synthetic>"' "$f" | wc -l); printf "%s\t%s\t%s\t%s\t%s\n" "$seat" "$(basename $2 .output | cut -c1-8)" "$o" "$other" "$syn"; }
printf "seat\tagent\tclaude-opus-5-5 msgs\tother model strings\tsynthetic (harness) msgs\n"
row L_lean_06Z $T06/abc22b768a74a48be.output
row O_06Z_died $T06/a09b7d71da2caafc3.output
row T_06Z_died $T06/a817404ffbd9a39f4.output
row W_06Z_died $T06/aabd68f2e2cb79ff7.output
row W_06Z_agentA $T06/a3f6f56cd9a9b27c7.output
row W_06Z_agentB_died $T06/a8ae30999a3554ab9.output
row O_09Z $T09/ac837b7aceac466b1.output
row T_09Z $T09/abf5790cd29f1e370.output
row W_09Z $T09/a00c9cf9fc2afdc8e.output
[ -n "$BLIND" ] && row blind_09Z $T09/$BLIND.output
f=~/.claude/projects/-home-exedev/80cf1b4e-f619-4b45-b10a-6f3d89b30269.jsonl; printf "main_09Z\t80cf1b4e\t%s\t%s\t-\n" "$(grep -o '"model":"claude-opus-5-5"' $f | wc -l)" "$(grep -o '"model":"[^"]*"' $f | grep -v -e claude-opus-5-5 -e '"model":"opus"' -e synthetic | wc -l)"
f=$(ls ~/.claude/projects/-home-exedev/d7d10d2c-6fd8-410b-996a-c84a0f6e80b6.jsonl 2>/dev/null); [ -n "$f" ] && printf "main_06Z\td7d10d2c\t%s\t%s\t-\n" "$(grep -o '"model":"claude-opus-5-5"' $f | wc -l)" "$(grep -o '"model":"[^"]*"' $f | grep -v -e claude-opus-5-5 -e '"model":"opus"' -e synthetic | wc -l)"
echo '# "<synthetic>" = harness-inserted message (the 06Z seats died on "You have hit your session limit"); "model":"opus" strings are Agent-tool parameters, not served-model fields.'
