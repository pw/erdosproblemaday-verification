#!/bin/bash
# Count served-model fields ("model":"…") in each seat's transcript and in the coordinating session's transcript (no other content read).
D=/tmp/claude-1000/-home-exedev/a899cde7-080d-473c-8a33-c1e932670abe/tasks   # 12:00Z erdos seat 2026-10-22
declare -A A=([M1]=a713669878e40daf6 [M2]=a285f3851b39e1f61 [L]=a883ed6c902ef0dc3 [W]=ade1c13e4bb59376a)
for k in "${!A[@]}"; do echo "seat $k: $(grep -o '"model":"[^"]*"' $D/${A[$k]}.output 2>/dev/null | sort | uniq -c | tr -s ' ' | tr '\n' ';')"; done
B=${B:-a164307e1de7258b1}; [ -n "$B" ] && echo "seat B: $(grep -o '"model":"[^"]*"' $D/$B.output 2>/dev/null | sort | uniq -c | tr -s ' ' | tr '\n' ';')"
echo "main session: $(grep -o '"model":"[^"]*"' ~/.claude/projects/-home-exedev/a899cde7-080d-473c-8a33-c1e932670abe.jsonl | sort | uniq -c | tr -s ' ' | tr '\n' ';')"
echo "(\"opus\" in a main session = the requested-model parameter of an Agent tool call, not a served model)"
