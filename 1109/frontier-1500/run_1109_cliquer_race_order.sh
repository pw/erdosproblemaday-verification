#!/usr/bin/env bash
set -euo pipefail

graph=${1:?usage: run_1109_cliquer_race_order.sh GRAPH ORDERING LOG RESULT_FILE}
ordering=${2:?usage: run_1109_cliquer_race_order.sh GRAPH ORDERING LOG RESULT_FILE}
log=${3:?usage: run_1109_cliquer_race_order.sh GRAPH ORDERING LOG RESULT_FILE}
result_file=${4:?usage: run_1109_cliquer_race_order.sh GRAPH ORDERING LOG RESULT_FILE}
n=${graph##*_}
n=${n%.dimacs}

case "$ordering" in
  degree|default|none) ;;
  *) printf 'unsupported ordering: %s\n' "$ordering" >&2; exit 2 ;;
esac

{
  printf 'started_utc=%s\n' "$(date -u +%FT%TZ)"
  printf 'n=%s target=44 ordering=%s cap_seconds=1800\n' "$n" "$ordering"
  sha256sum /usr/bin/cliquer "$graph"
  printf 'COMMAND: timeout 1800 /usr/bin/cliquer -u -m 44 -M 44 -r %s -q %s\n' \
    "$ordering" "$graph"
  /usr/bin/time -v timeout 1800 /usr/bin/cliquer -u -m 44 -M 44 \
    -r "$ordering" -q "$graph"
  printf 'finished_utc=%s\n' "$(date -u +%FT%TZ)"
} >"$log" 2>&1

if grep -Fqx 'No such clique found.' "$log"; then
  status='exists=False'
elif grep -q '^size=44, weight=44:' "$log"; then
  status='exists=True'
elif grep -q 'Command exited with non-zero status 124' "$log"; then
  status='result=TIMEOUT'
else
  status='result=ABORTED_OR_PARSE_ERROR'
fi
printf 'n=%s ordering=%s %s log_sha256=%s\n' \
  "$n" "$ordering" "$status" "$(sha256sum "$log" | cut -d' ' -f1)" \
  | tee -a "$result_file"
test "$status" = 'exists=False' -o "$status" = 'exists=True'
