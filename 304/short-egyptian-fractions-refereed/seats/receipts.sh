#!/bin/bash
# Count served-model fields ("model":"…") in each seat's transcript and in the main session's transcript (no other content read).
D=/tmp/claude-1000/-home-exedev/28e9bf3d-653f-43c9-96b1-abd05bdc587c/tasks
declare -A S=([U]=af47439f3a4065aaa [P]=aeaa6bf0b83b79c61 [L]=a328adea920f1039d [W]=a77e354bbc983dee2 [B]=aa08cd4fe46e4dd3c)
for k in U P L W B; do echo "seat $k: $(grep -o '"model":"[^"]*"' $D/${S[$k]}.output 2>/dev/null | sort | uniq -c | tr -s ' ' | tr '\n' ';')"; done
echo "main session: $(grep -o '"model":"[^"]*"' ~/.claude/projects/-home-exedev/28e9bf3d-653f-43c9-96b1-abd05bdc587c.jsonl | sort | uniq -c | tr -s ' ' | tr '\n' ';')"
echo "(\"model\":\"opus\" in the main session = the Agent tool's requested-model argument, not a served model)"
