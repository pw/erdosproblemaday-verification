#!/bin/bash
# Family 25: compile Bridge304 + Bridge148_293 (+ four mutants, which must FAIL) against the replayed OpenAI closure; oleans to bridge/out.
B=/tmp/oaimath/025/bridge; source $B/lean_env.sh
mkdir -p $B/out; cd $B
cat > AxBridge.lean <<'AX'
import Bridge304
import Bridge148_293
#print axioms Erdos304.upper_bound
#print axioms Erdos304.erdos_304.variants.lower_1950
#print axioms Erdos304.smallestCollectionTo_eq_maxMinLength
#print axioms Erdos148.F_eq_oai
#print axioms Erdos148.erdos_148.variants.double_log_order
#print axioms Erdos293.v_eq_oai
#print axioms Erdos293.erdos_293.variants.explicit_bounds
#print axioms Erdos293.erdos_293.variants.double_log_order
AX
for m in Bridge304 Bridge148_293; do
  nice -n 19 lean -DautoImplicit=false $m.lean -o out/$m.olean -i out/$m.ilean > $m.log 2>&1; echo "$m rc=$?" | tee -a $m.log
done
LEAN_PATH=$B/out:$LEAN_PATH nice -n 19 lean AxBridge.lean > AxBridge.log 2>&1; echo "AxBridge rc=$?" | tee -a AxBridge.log
for m in Bridge304MutDef Bridge304MutStmt Bridge148MutDef Bridge293MutStmt; do nice -n 19 lean -DautoImplicit=false $m.lean > $m.log 2>&1; echo "$m rc=$? (must be nonzero)" | tee -a $m.log; done
python3 verbatim_check.py > verbatim.log 2>&1; echo "verbatim rc=$?" | tee -a verbatim.log
python3 verbatim_check.py --mutate > verbatim_mut.log 2>&1; echo "verbatim --mutate rc=$? (must be 1)" | tee -a verbatim_mut.log
python3 verbatim_check.py --mutate148 > verbatim_mut148.log 2>&1; echo "verbatim --mutate148 rc=$? (must be 1)" | tee -a verbatim_mut148.log
