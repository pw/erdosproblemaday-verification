#!/usr/bin/env bash
set -u

cubes=(00 010 011 100 101 110 111)
pids=()
for cube in "${cubes[@]}"; do
  (
    set +e
    ERDOS773_CUBE="$cube" ERDOS773_COLOR_SLACK=33 \
      /usr/bin/time -v ./dfs_n71 \
      > "cube_${cube}.log" 2> "cube_${cube}.time"
    status=$?
    printf '%s\n' "$status" > "cube_${cube}.status"
    [[ "$status" -eq 20 ]]
  ) &
  pids+=("$!")
done

overall=0
for pid in "${pids[@]}"; do
  wait "$pid" || overall=1
done

for cube in "${cubes[@]}"; do
  printf '%s ' "$cube"
  tr -d '\n' < "cube_${cube}.status"
  printf ' '
  cat "cube_${cube}.log"
done
exit "$overall"
