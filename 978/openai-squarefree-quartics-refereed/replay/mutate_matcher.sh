#!/bin/bash
# mutation test of statement_match.py (family 20): each mutant must exit with the wanted code; a mutant whose input is unchanged is REFUSED.
L=/tmp/oaimath/020/lean-build; cd $L
run(){ local name=$1; local want=$2; shift 2; rm -rf mut/$name; mkdir -p mut/$name; cp logs/*.log mut/$name/; "$@";
  if [ "$name" != unmodified ] && diff -q <(cat logs/ax_PowerFreeValues.log logs/cmp_PowerFreeValues.log 2>/dev/null) <(cat mut/$name/ax_PowerFreeValues.log mut/$name/cmp_PowerFreeValues.log 2>/dev/null) >/dev/null 2>&1; then echo "$name REFUSED (mutation did not apply)"; return; fi
  python3 statement_match.py mut/$name > mut/$name/out.txt 2>&1; rc=$?; echo "$name rc=$rc want=$want $( [ "$rc" = "$want" ] && echo OK || echo BAD)"; }
run unmodified 0 true
run def_powerfree_dvd 1 sed -i '/@@@ BEGIN def OAI.QuarticPowerFree.PowerFree/,/@@@ BEGIN/ s/@HPow.hPow.{0, 0, 0} Int Nat Int/@HMul.hMul.{0, 0, 0} Int Nat Int/' mut/def_powerfree_dvd/ax_PowerFreeValues.log
run count_Icc 1 sed -i '/@@@ BEGIN def OAI.QuarticPowerFree.count/,/@@@ BEGIN/ s/Finset.Icc/Finset.Ico/' mut/count_Icc/ax_PowerFreeValues.log
run density_littleO 1 sed -i '/@@@ BEGIN def OAI.QuarticPowerFree.DensityStatement/,/@@@ BEGIN/ s/Asymptotics.IsLittleO/Asymptotics.IsBigO/' mut/density_littleO/ax_PowerFreeValues.log
run thm_degree 1 sed -i '/@@@ BEGIN thm OAI.QuarticPowerFree.allDegrees/,/@@@ BEGIN/ s/(nat_lit 4) (instOfNatNat (nat_lit 4))/(nat_lit 5) (instOfNatNat (nat_lit 5))/' mut/thm_degree/ax_PowerFreeValues.log
run extra_axiom 1 sed -i "s/depends on axioms: \[propext, Classical.choice.{u}, Quot.sound.{u}\]/depends on axioms: [propext, sorryAx.{u}, Classical.choice.{u}, Quot.sound.{u}]/" mut/extra_axiom/ax_PowerFreeValues.log
run cmp_no_sorry 1 sed -i "s/sorryAx.{u}, //; s/, sorryAx.{u}//" mut/cmp_no_sorry/cmp_PowerFreeValues.log
run missing_block 2 sed -i '/@@@ BEGIN def OAI.QuarticPowerFree.rho/d' mut/missing_block/ax_PowerFreeValues.log
run missing_log 2 rm mut/missing_log/cmp_PowerFreeValues.log
run refusal_guard_control 1 true
