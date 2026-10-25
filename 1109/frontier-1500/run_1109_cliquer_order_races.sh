#!/usr/bin/env bash
set -euo pipefail

race_dir=${1:?usage: run_1109_cliquer_order_races.sh RACE_DIR}
jobs=${JOBS:-6}
mkdir -p "$race_dir/logs"

run_one() {
  local graph=$1
  local n=${graph##*_}
  n=${n%.dimacs}
  local log="$race_dir/logs/n${n}_unweighted-coloring.log"
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
    printf 'n=%s ordering=unweighted-coloring exists=False log_sha256=%s\n' \
      "$n" "$(sha256sum "$log" | cut -d' ' -f1)"
  elif grep -q '^size=44, weight=44:' "$log"; then
    printf 'n=%s ordering=unweighted-coloring exists=True log_sha256=%s\n' \
      "$n" "$(sha256sum "$log" | cut -d' ' -f1)"
  else
    printf 'n=%s ordering=unweighted-coloring result=PARSE_ERROR log_sha256=%s\n' \
      "$n" "$(sha256sum "$log" | cut -d' ' -f1)"
    return 1
  fi
}
export -f run_one
export race_dir

find "$race_dir/graphs" -maxdepth 1 -type f -name 'neighbors_*.dimacs' \
  -print0 | sort -z -V | xargs -0 -n1 -P "$jobs" bash -c 'run_one "$1"' _ \
  | tee "$race_dir/results_unweighted-coloring.txt"
