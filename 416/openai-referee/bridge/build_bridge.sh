#!/bin/bash
# #416: compile Bridge416 (+ the two mutants, which must FAIL) against the replayed OpenAI closure; oleans to bridge/out.
L=/tmp/oaimath/024/lean-build; B=/tmp/oaimath/024/bridge; H=/tmp/oaimath/166/lean-build/home
export HOME=$H ELAN_HOME=$H/.elan ELAN_TOOLCHAIN_GC_DISABLE=1 PATH="$H/.elan/toolchains/leanprover--lean4---v4.34.1/bin:/usr/local/bin:/usr/bin:/bin" LEAN_NUM_THREADS=1
export LEAN_PATH=$(cat $L/lean_path.txt)
mkdir -p $B/out; cd $B
cat > AxBridge.lean <<'AX'
import Bridge416
#print axioms Erdos416.erdos_416.parts.i
#print axioms Erdos416.erdos_416.variants.regularly_varying
#print axioms Erdos416.V_eq
AX
nice -n 19 lean -DautoImplicit=false Bridge416.lean -o out/Bridge416.olean -i out/Bridge416.ilean > Bridge416.log 2>&1; echo "Bridge416 rc=$?" | tee -a Bridge416.log
LEAN_PATH=$B/out:$LEAN_PATH nice -n 19 lean AxBridge.lean > AxBridge.log 2>&1; echo "AxBridge rc=$?" | tee -a AxBridge.log
for m in BridgeMutDef BridgeMutStmt; do nice -n 19 lean -DautoImplicit=false $m.lean > $m.log 2>&1; echo "$m rc=$? (must be nonzero)" | tee -a $m.log; done
