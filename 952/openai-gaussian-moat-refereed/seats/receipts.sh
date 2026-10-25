#!/bin/bash
# Count served-model fields ("model":"…") in each seat's transcript and in both coordinating sessions' transcripts (no other content read).
D0=/tmp/claude-1000/-home-exedev/90c3e813-c9c4-44a2-8942-f5c2251760da/tasks   # 00:00Z seat (died ~00:24Z on the session limit)
D1=/tmp/claude-1000/-home-exedev/13ac841a-08e7-4612-b7a4-f28b5cd05a38/tasks   # 03:00Z seat
declare -A A0=([G]=afe75d6957a030b5d [I]=a6ee39511fa994696 [L]=a4b4e56271c7cd674 [S_died]=a182b1f6fd03d5542 [W_died]=a721aa54582d09366)
declare -A A1=([S]=a0272203d78f2d49c [W]=a19da8902f85c14c0 [B]=a06de35505aeeb15b)
for k in G I L S_died W_died; do echo "00Z seat $k: $(grep -o '"model":"[^"]*"' $D0/${A0[$k]}.output 2>/dev/null | sort | uniq -c | tr -s ' ' | tr '\n' ';')"; done
for k in S W B; do echo "03Z seat $k: $(grep -o '"model":"[^"]*"' $D1/${A1[$k]}.output 2>/dev/null | sort | uniq -c | tr -s ' ' | tr '\n' ';')"; done
echo "00Z main session: $(grep -o '"model":"[^"]*"' ~/.claude/projects/-home-exedev/90c3e813-c9c4-44a2-8942-f5c2251760da.jsonl | sort | uniq -c | tr -s ' ' | tr '\n' ';')"
echo "03Z main session: $(grep -o '"model":"[^"]*"' ~/.claude/projects/-home-exedev/13ac841a-08e7-4612-b7a4-f28b5cd05a38.jsonl | sort | uniq -c | tr -s ' ' | tr '\n' ';')"
echo "(<synthetic> = harness-generated messages, e.g. the session-limit notice; not a model)"
echo "(\"opus\" in a main session = the requested-model parameter of an Agent tool call, not a served model)"
