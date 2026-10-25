#!/usr/bin/env bash
set -euo pipefail

graph=${1:?usage: run_1109_cliquer_race_one.sh GRAPH LOG RESULT_FILE}
log=${2:?usage: run_1109_cliquer_race_one.sh GRAPH LOG RESULT_FILE}
result_file=${3:?usage: run_1109_cliquer_race_one.sh GRAPH LOG RESULT_FILE}
n=${graph##*_}
n=${n%.dimacs}

{
  printf 'started_utc=%s\n' "$(date -u +%FT%TZ)"
  printf 'n=%s target=44 ordering=unweighted-coloring\n' "$n"
  sha256sum /usr/bin/cliquer "$graph"
  printf 'COMMAND: /usr/bin/cliquer -u -m 44 -M 44 -r unweighted-coloring -q %s\n' "$graph"
  /usr/bin/time -v /usr/bin/cliquer -u -m 44 -M 44 \
    -r unweighted-coloring -q "$graph"
  printf 'finished_utc=%s\n' "$(date -u +%FT%TZ)"
} >"$log" 2>&1

if grep -Fqx 'No such clique found.' "$log"; then
  status='exists=False'
elif grep -q '^size=44, weight=44:' "$log"; then
  status='exists=True'
else
  status='result=PARSE_ERROR'
fi
printf 'n=%s ordering=unweighted-coloring %s log_sha256=%s\n' \
  "$n" "$status" "$(sha256sum "$log" | cut -d' ' -f1)" | tee -a "$result_file"
test "$status" != 'result=PARSE_ERROR'

