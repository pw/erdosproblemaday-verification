#!/bin/bash
# #778 Didin–Pimenov Lean replay driver. Rows: step rc elapsed -> steps.tsv
export PATH="$HOME/.elan/bin:$PATH"
cd /tmp/erdos778/lean/build/erdos12 || exit 9
T=/tmp/erdos778/lean/build/steps.tsv
row(){ echo -e "$1\t$(date -u +%FT%TZ)\t$2\t$3" >> "$T"; }
run(){ local name=$1; shift; local t0=$(date +%s); echo "[$(date -u +%FT%TZ)] BEGIN $name :: $*" >> ../driver.log; nice -n 19 "$@" > "../$name.log" 2>&1; local rc=$?; row "$name" "$rc" "$(( $(date +%s)-t0 ))s"; echo "[$(date -u +%FT%TZ)] END $name rc=$rc" >> ../driver.log; return $rc; }
row launch 0 "mem_avail=$(free -g | awk '/Mem/{print $7}')G"
run toolchain lean --version || exit 1
run deps lake exe cache get || { row deps_fallback 0 "cache-get-failed-will-build-mathlib?"; exit 2; }
run build lake build || exit 3
run trust0 lake env lean --trust=0 Erdos12.lean || exit 4
cat > ../Axioms.lean <<'L'
import Erdos12
#print axioms Erdos12.erdos_one_two_main
#print axioms Erdos12.greedyStrategy_wins_above_threshold
#check @Erdos12.erdos_one_two_main
#print Erdos12.explicitThreshold
L
run axioms lake env lean ../Axioms.lean || exit 5
# negative control: a sorry'd theorem must show sorryAx
cat > ../NegControl.lean <<'L'
import Erdos12
theorem erdos12_negcontrol : ∃ N : ℕ, ∀ n : ℕ, N ≤ n → ∃ σ : Erdos12.Strategy n, Erdos12.WinningStrategy σ := by sorry
#print axioms erdos12_negcontrol
L
run negcontrol lake env lean ../NegControl.lean
grep -q sorryAx ../negcontrol.log && row negcontrol_sorryAx_seen 0 ok || row negcontrol_sorryAx_seen 1 MISSING
# wrong-shape control: a false statement about the game must NOT elaborate from the library's lemmas
cat > ../WrongShape.lean <<'L'
import Erdos12
example : ∀ n : ℕ, 4 ≤ n → ∃ σ : Erdos12.Strategy n, Erdos12.WinningStrategy σ := Erdos12.erdos_one_two_main
L
run wrongshape lake env lean ../WrongShape.lean
[ -s ../wrongshape.log ] && grep -q error ../wrongshape.log && row wrongshape_rejected 0 ok || row wrongshape_rejected 1 "ACCEPTED-A-WRONG-SHAPE"
row done 0 ok
