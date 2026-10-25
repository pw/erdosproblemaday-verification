#!/usr/bin/env bash
set -euo pipefail

cxx=${CXX:-g++}
"$cxx" -O3 -DNDEBUG -std=c++17 search20_direct.cpp -o search20_direct

# The four larger-core rows are kept as single ranges.
for spec in "20 100" "19 90" "18 81" "17 72"; do
  read -r core lo <<< "$spec"
  /usr/bin/time -f "TIME rc=%x elapsed=%e user=%U rss_kb=%M" \
    ./search20_direct 151 "$core" "$lo" 151 \
    > "direct_core${core}.log" 2> "direct_core${core}_time.txt" &
done
wait

: > direct_whole_results.txt
for core in 20 19 18 17; do
  cat "direct_core${core}.log" >> direct_whole_results.txt
  cat "direct_core${core}_time.txt" >> direct_whole_results.txt
done

# Smaller cores are exact-center slices.  Parallelism changes only scheduling.
max_jobs=${MAX_JOBS:-14}
run_center() {
  local core=$1 center=$2
  ./search20_direct 151 "$core" "$center" "$center" \
    > "direct_core${core}_t${center}.log"
}

for core in 16 15 14; do
  case "$core" in
    16) lo=64 ;;
    15) lo=56 ;;
    14) lo=49 ;;
  esac
  for center in $(seq "$lo" 151); do
    if (( core == 15 && center % 2 == 1 )); then
      continue
    fi
    while (( $(jobs -rp | wc -l) >= max_jobs )); do
      wait -n
    done
    run_center "$core" "$center" &
  done
done
wait

python3 freeze_direct_results.py > direct_sliced_results.txt
python3 verify_direct_logs.py > direct_log_verification.txt
