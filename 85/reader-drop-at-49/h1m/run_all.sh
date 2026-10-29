#!/bin/bash
# 2026-10-25 09Z erdos seat (Patrick answered ask 61eb8959: "Run it on our box").
# Kissat pass over all 13,351 cells (retried once for any non-UNSAT row), then the CaDiCaL+DRAT+drat-trim pass.
# Stops before DRAT if runs/ALARM_SAT exists. Stop everything: kill the PID in runs/run_all.pid, then the xargs PID in
# runs/campaign_<mode>.pid (NOT pkill -f). Tally: python3 tally.py kissat|drat (exit 0 only if all keys done).
cd ~/MathDyad/erdos85/h1m
echo $$ > runs/run_all.pid
P=${P:-10}
bash campaign.sh kissat $P 3600
bash campaign.sh kissat $P 3600      # resumable: only re-runs cells without an UNSAT row
[ -e runs/ALARM_SAT ] && { echo "$(date -u +%FT%TZ) ALARM_SAT — stopped before DRAT" >> runs/run_all.log; exit 3; }
echo "$(date -u +%FT%TZ) kissat passes finished; tally: $(~/.venv/bin/python tally.py kissat 2>&1 | tail -1)" >> runs/run_all.log
bash campaign.sh drat $P 3600
bash campaign.sh drat $P 3600
echo "$(date -u +%FT%TZ) drat passes finished; tally: $(~/.venv/bin/python tally.py drat 2>&1 | tail -1)" >> runs/run_all.log
