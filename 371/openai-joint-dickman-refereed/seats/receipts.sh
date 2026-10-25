#!/bin/bash
# Count served-model fields ("model":"…") in each seat's transcript and in the coordinating session's transcript (no other content read).
D=/tmp/claude-1000/-home-exedev/9e99318b-9a72-4d43-954c-4a5087a69f00/tasks   # 06:00Z erdos seat, 2026-10-22
declare -A A=([W]=ab3edab794e70cd2a [A]=a54cc5919c6301096 [R]=aaf230cc09406709c [L]=a68b53e77a1de8452)
for k in W A R L B; do [ -n "${A[$k]:-}" ] && echo "seat $k: $(grep -o '"model":"[^"]*"' $D/${A[$k]}.output 2>/dev/null | sort | uniq -c | tr -s ' ' | tr '\n' ';')"; done
echo "main session: $(grep -o '"model":"[^"]*"' ~/.claude/projects/-home-exedev/9e99318b-9a72-4d43-954c-4a5087a69f00.jsonl 2>/dev/null | sort | uniq -c | tr -s ' ' | tr '\n' ';')"
echo "(<synthetic> = harness-generated messages; \"opus\" in the main session = the requested-model parameter of an Agent call, not a served model)"
