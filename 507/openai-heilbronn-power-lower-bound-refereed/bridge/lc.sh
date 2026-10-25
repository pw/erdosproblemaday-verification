#!/bin/bash
# leanchecker --fresh over Extra507 (Mathlib + OpenAI 195-module closure + EveryN507 + Bridge507 + Extra507), then a missing-module control.
B=/tmp/oaimath/191/bridge; source $B/lean_env.sh
step(){ local name="$1"; shift; local t0=$SECONDS; "$@"; local rc=$?; echo "$name $rc $((SECONDS-t0))" >> "$L/steps.tsv"; return 0; }
cd $B
step leanchecker_fresh bash -c "nice -n 19 /usr/bin/time -f 'maxrss_kb=%M wall_s=%e' leanchecker --fresh Extra507 > $L/logs/leanchecker_fresh.log 2>&1"
step leanchecker_missing_control bash -c "nice -n 19 leanchecker --fresh OAI.Geometry.HeilbronnTriangle.DoesNotExist > $L/logs/leanchecker_missing.log 2>&1"
touch $L/LC_DONE
