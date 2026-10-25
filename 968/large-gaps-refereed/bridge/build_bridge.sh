#!/bin/bash
# #968: compile Bridge968 (+ the two mutants, which must FAIL) against the replayed OpenAI closure; write oleans to bridge/out.
L=/tmp/oaimath/026/lean-build; B=/tmp/oaimath/026/bridge; H=/tmp/oaimath/166/lean-build/home
export HOME=$H ELAN_HOME=$H/.elan ELAN_TOOLCHAIN_GC_DISABLE=1 PATH="$H/.elan/toolchains/leanprover--lean4---v4.34.1/bin:/usr/local/bin:/usr/bin:/bin" LEAN_NUM_THREADS=1
export LEAN_PATH=$(cat $L/lean_path.txt)
mkdir -p $B/out; cd $B
cat > /tmp/oaimath/026/bridge/AxBridge.lean <<'AX'
import Bridge968
#print axioms Erdos968.erdos_968
#print axioms Erdos968.mem_iff
#print axioms Erdos968.count_eq
AX
nice -n 19 lean -DautoImplicit=false Bridge968.lean -o out/Bridge968.olean -i out/Bridge968.ilean > Bridge968.log 2>&1; echo "Bridge968 rc=$?" | tee -a Bridge968.log
LEAN_PATH=$B/out:$LEAN_PATH nice -n 19 lean AxBridge.lean > AxBridge.log 2>&1; echo "AxBridge rc=$?" | tee -a AxBridge.log
for m in BridgeMutDef BridgeMutStmt; do nice -n 19 lean -DautoImplicit=false $m.lean > $m.log 2>&1; echo "$m rc=$? (must be nonzero)" | tee -a $m.log; done
