#!/bin/bash
# Count served-model fields ("model":"…") in each seat's transcript and in the coordinating session's transcript (no other content read).
D=/tmp/claude-1000/-home-exedev/0e962950-1430-455c-94bc-e87501ae3f0f/tasks   # 15:00Z erdos seat 2026-10-22
declare -A A=([R1]=a0ad13494dfccc925 [R2]=ad0fcbb8765d457b3 [C]=a5a6ca6d41b07b9ae [W]=a3a19c380e6bbfac1 [B]=aafa1b60414c4a27d)
for k in R1 R2 C W B; do echo "seat $k: $(grep -o '"model":"[^"]*"' $D/${A[$k]}.output 2>/dev/null | sort | uniq -c | tr -s ' ' | tr '\n' ';')"; done
echo "main session: $(grep -o '"model":"[^"]*"' ~/.claude/projects/-home-exedev/0e962950-1430-455c-94bc-e87501ae3f0f.jsonl 2>/dev/null | sort | uniq -c | tr -s ' ' | tr '\n' ';')"
echo "(\"opus\" in a main session = the requested-model parameter of an Agent tool call, not a served model)"
