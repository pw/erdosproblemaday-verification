#!/bin/bash
# usage: build_bridge.sh core|final   — compiles the bridge files against the replay's oleans.
set -u
L=/tmp/oaimath/012/lean-build; B=/tmp/oaimath/012/bridge
H=/tmp/oaimath/166/lean-build/home; export HOME=$H ELAN_HOME=$H/.elan ELAN_TOOLCHAIN_GC_DISABLE=1
export PATH="$H/.elan/toolchains/leanprover--lean4---v4.34.1/bin:/usr/local/bin:/usr/bin:/bin" LEAN_NUM_THREADS=1
mkdir -p $B/out
export LEAN_PATH=$B/out:$(cat $L/lean_path.txt)
cd $B
step(){ local name="$1"; shift; local t0=$SECONDS; "$@"; local rc=$?; echo "$name $rc $((SECONDS-t0))" | tee -a $B/steps.tsv; }
if [ "$1" = core ]; then
  step core_compile bash -c "nice -n 19 lean -DautoImplicit=false BridgeCore.lean > BridgeCore.log 2>&1"
else
  step bridge_compile bash -c "nice -n 19 lean -DautoImplicit=false Bridge371.lean -o out/Bridge371.olean -i out/Bridge371.ilean > Bridge371.log 2>&1"
  step bridge_axioms bash -c "nice -n 19 lean --trust=0 -DautoImplicit=false AxBridge.lean > AxBridge.log 2>&1"
  for m in MutValue MutStrict928 MutDensityDef; do
    step mut_$m bash -c "nice -n 19 lean -DautoImplicit=false Bridge$m.lean > Bridge$m.log 2>&1"
  done
fi
