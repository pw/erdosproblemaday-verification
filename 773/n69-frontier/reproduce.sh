#!/usr/bin/env bash
set -euo pipefail

HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd "$HERE"

sha256sum --check SHA256SUMS
python3 check_witness.py
python3 audit_pair_bound.py
python3 audit_dfs_certificate.py

if [[ ${FULL:-0} != 1 ]]; then
    printf '%s\n' 'PASS frozen certificate audit (set FULL=1 to rerun all cubes)'
    exit 0
fi

work=$(mktemp -d "${TMPDIR:-/tmp}/erdos773-full-XXXXXXXX")
trap 'rm -rf "$work"' EXIT

g++ -O3 -DNDEBUG -std=c++20 -Wall -Wextra -pedantic \
    dfs_hypergraph_coloring.cpp -o "$work/dfs_hypergraph_coloring"
test "$(sha256sum "$work/dfs_hypergraph_coloring" | cut -d' ' -f1)" = \
    e9d471fb6df395f0807c21efc2fffbda64403511cd92b8098bb9100eaaa5655a

cubes=(00 010 011 100 101 110 111)
pids=()
for cube in "${cubes[@]}"; do
    (
        set +e
        env ERDOS773_CUBE="$cube" ERDOS773_COLOR_SLACK=32 \
            /usr/bin/time -v "$work/dfs_hypergraph_coloring" \
            > "$work/cube_${cube}.log" 2> "$work/cube_${cube}.time"
        status=$?
        printf '%s\n' "$status" > "$work/cube_${cube}.exit"
        exit 0
    ) &
    pids+=("$!")
done
for pid in "${pids[@]}"; do
    wait "$pid"
done

python3 - "$work" <<'PY'
import itertools
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])
cubes = ("00", "010", "011", "100", "101", "110", "111")
total = 0
for cube in cubes:
    assert (root / f"cube_{cube}.exit").read_text().strip() == "20"
    output = (root / f"cube_{cube}.log").read_text()
    match = re.fullmatch(
        r"status=UNSATISFIABLE nodes=(\d+) seconds=([0-9.e+-]+) "
        r"prefix_prunes=(\d+) blocked_prunes=(\d+) color_calls=(\d+) "
        rf"color_prunes=(\d+) color_slack=32 cube={cube}\n",
        output,
    )
    assert match, (cube, output)
    total += int(match.group(1))
for assignment in map("".join, itertools.product("01", repeat=3)):
    assert sum(assignment.startswith(cube) for cube in cubes) == 1
print(f"PASS fresh exhaustive cube cover total_nodes={total}")
PY

printf '%s\n' 'PASS full recomputation'
