#!/bin/bash
# re-run of the four control compiles with a CORRECT exit code (controls.sh logged rc after a $(date) substitution, so always 0)
cd /tmp/e488/lean; export PATH="$HOME/.elan/bin:$PATH"
until ! kill -0 $(cat controls.pid 2>/dev/null || echo 999999) 2>/dev/null; do sleep 5; done
for f in Bridge NegConst NegSorry NegBridge; do
  lake env lean $f.lean > ctl2_$f.log 2>&1; rc=$?
  printf '%s\t%s\trc=%s\terrors=%s\tsorryAx=%s\n' "$(date -u +%FT%TZ)" "ctl2_$f" "$rc" "$(grep -c 'error' ctl2_$f.log)" "$(grep -c sorryAx ctl2_$f.log)" >> steps.tsv
done
