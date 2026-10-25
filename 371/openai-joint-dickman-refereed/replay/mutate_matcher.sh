#!/bin/bash
# mutation test of statement_match.py (family 012): each mutant must exit with the wanted code; a mutant whose input is unchanged is REFUSED.
L=/tmp/oaimath/012/lean-build; cd $L
run(){ local name=$1; local want=$2; shift 2; rm -rf mut/$name; mkdir -p mut/$name; cp logs/*.log mut/$name/; "$@";
  if [ "$name" != unmodified ] && diff -rq logs mut/$name --exclude=out.txt --exclude=statement_match.log >/dev/null 2>&1; then echo "$name REFUSED (mutation did not apply)"; return; fi
  python3 statement_match.py mut/$name > mut/$name/out.txt 2>&1; rc=$?; echo "$name rc=$rc want=$want $( [ "$rc" = "$want" ] && echo OK || echo BAD)"; }
run unmodified 0 true
run rho_sign 1 sed -i '/@@@ BEGIN def OAI.Erdos970.NumberTheoryLean.Dickman.rho/,/@@@ BEGIN/ s/@Neg.neg.{0} Real Real.instNeg //' mut/rho_sign/ax_JointDickman.log
run icc_start 1 sed -i '/@@@ BEGIN def OAI.JointDickman.empiricalCount/,/@@@ BEGIN/ s/nat_lit 2/nat_lit 1/g' mut/icc_start/ax_JointDickman.log
run threshold_base 1 sed -i '/@@@ BEGIN thm OAI.JointDickmanPaper.joint_law/,/@@@ BEGIN/ s/LE.le/LT.lt/' mut/threshold_base/ax_JointDickman.log
run extra_axiom 1 sed -i "0,/depends on axioms: \[propext, Classical.choice.{u}, Quot.sound.{u}\]/s//depends on axioms: [propext, sorryAx.{u}, Classical.choice.{u}, Quot.sound.{u}]/" mut/extra_axiom/ax_JointDickman.log
run cmp_no_sorry 1 sed -i "s/sorryAx.{u}, //; s/, sorryAx.{u}//" mut/cmp_no_sorry/cmp_JointDickman.log
run missing_block 2 sed -i '/@@@ BEGIN def OAI.JointDickman.realDensity/d' mut/missing_block/ax_JointDickman.log
run missing_log 2 rm mut/missing_log/cmp_JointDickman.log
