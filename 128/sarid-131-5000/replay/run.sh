#!/bin/bash
# Kernel replay of Sarid's Erdos128 Lean package (claim repo ba85f319, Mathlib v4.30.0 @ c5ea0035 hard-linked
# from ~/MathDyad/lean/boxcover). Written BEFORE any CPU was spent: estimate ~680 project modules, 1-3 h at nice 19
# on 8 pinned cores; RAM a few GB; disk < 3 GB. Watchdog kills ONLY this build's process group.
W=/tmp/erdos1800/lean-build; P=$W/erdos128; T=$HOME/.elan/toolchains/leanprover--lean4---v4.30.0/bin
export PATH=$T:$PATH; S=$W/steps.tsv
step(){ printf '%s\t%s\t%s\t%s\n' "$1" "$(date -u +%FT%TZ)" "$2" "$3" >> "$S"; }
guard(){ a=$(awk '/MemAvailable/{print int($2/1048576)}' /proc/meminfo); d=$(df -BG --output=avail /tmp | tail -1 | tr -dc 0-9); echo "$a $d"; }
cd "$P" || { step cd 10 -; exit 10; }
step launch 0 "mem_disk=$(guard)"
run_step(){ # name, logfile, cmd...
  local name=$1 log=$2; shift 2; local t0=$(date +%s)
  setsid nice -n 19 taskset -c 8-15 "$@" > "$log" 2>&1 &
  local pid=$!; local pgid=$(ps -o pgid= "$pid" | tr -d ' ')
  while kill -0 "$pid" 2>/dev/null; do
    read a d < <(guard)
    if [ "$a" -lt 6 ] || [ "$d" -lt 2 ]; then echo "WATCHDOG $name mem=${a}G disk=${d}G $(date -u +%FT%TZ)" >> "$W/watchdog.log"; kill -- -"$pgid" 2>/dev/null; sleep 2; step "$name" 137 "watchdog mem=${a}G disk=${d}G"; return 137; fi
    sleep 20
  done
  wait "$pid"; local rc=$?; step "$name" "$rc" "$(( $(date +%s) - t0 ))s"; return $rc
}
run_step build "$W/build.log" lake build || exit 1
run_step axioms "$W/axioms.log" lake env lean AxiomAudit.lean
run_step probe "$W/probe.log" lake env lean "$W/Probe.lean"
run_step negcontrol "$W/negcontrol.log" lake env lean "$W/NegControl.lean"
run_step wrongshape "$W/wrongshape.log" lake env lean "$W/WrongShape.lean"   # EXPECT rc != 0
# statement-match verdict (sorryAx must appear in negcontrol and nowhere in axioms/probe; wrongshape must fail)
python3 - "$W" <<'PY'
import sys,re,io
W=sys.argv[1]
ax=open(f"{W}/axioms.log").read(); pr=open(f"{W}/probe.log").read(); ng=open(f"{W}/negcontrol.log").read()
std="[propext, Classical.choice, Quot.sound]"
lines=[l for l in ax.splitlines() if "depends on axioms" in l]
ok_ax = len(lines)==5 and all(l.strip().endswith(std) for l in lines)
plines=[l for l in pr.splitlines() if "depends on axioms" in l]
ok_pr = len(plines)>=7 and all(l.strip().endswith(std) for l in plines)
ok_ng = "sorryAx" in ng
steps=open(f"{W}/steps.tsv").read()
ws=[l.split('\t') for l in steps.splitlines() if l.startswith('wrongshape')]
ok_ws = bool(ws) and ws[-1][2] not in ('0',)
verdict = "MATCH" if (ok_ax and ok_pr and ok_ng and ok_ws) else "MISMATCH"
open(f"{W}/statement_match.txt","w").write(f"{verdict}\naudit_lines={len(lines)} all_std={ok_ax}\nprobe_axiom_lines={len(plines)} all_std={ok_pr}\nnegcontrol_sorryAx={ok_ng}\nwrongshape_failed={ok_ws}\n")
print(verdict)
PY
step statement_match $? "$(head -1 $W/statement_match.txt)"
# optional, hours: leanchecker --fresh over the whole cone (Mathlib cache re-check)
run_step leanchecker_fresh "$W/leanchecker_fresh.log" lake env leanchecker --fresh Erdos128
