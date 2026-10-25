#!/bin/bash
# Count served-model fields ("model":"…") in each seat's transcript and in the main session's transcript (no other content read).
D=/tmp/claude-1000/-home-exedev/ab1073f2-ca8c-4a29-a829-af63d4d2962a/tasks
declare -A S=([O]=ad073ed86a3e39050 [T]=a0324d5f04745cd9c [L]=a74d879f2fdae5180 [W]=a1da4e36571d3aa96 [B]=a421182caceea98a5)
for k in O T L W B; do echo "seat $k: $(grep -o '"model":"[^"]*"' $D/${S[$k]}.output 2>/dev/null | sort | uniq -c | tr -s ' ' | tr '\n' ';')"; done
echo "main session: $(grep -o '"model":"[^"]*"' ~/.claude/projects/-home-exedev/ab1073f2-ca8c-4a29-a829-af63d4d2962a.jsonl | sort | uniq -c | tr -s ' ' | tr '\n' ';')"
