#!/usr/bin/env bash
set -euo pipefail

bundle_dir="$(cd -- "$(dirname -- "$0")" && pwd)"
cd "$bundle_dir"

g++ -O3 -DNDEBUG -std=c++17 search_direct.cpp -o search_direct

for specification in "19 90" "18 81" "17 72" "16 64" "15 56"; do
    read -r core lower <<<"$specification"
    /usr/bin/time -f 'TIME rc=%x elapsed=%e user=%U rss=%M' \
        ./search_direct 133 "$core" "$lower" 133 \
        > "direct_core${core}.log" 2>&1
done

seq 49 133 | xargs -P 8 -I{} \
    ./search_direct 133 14 {} {} > direct_core14_slices.log

python3 summarize_slices.py
