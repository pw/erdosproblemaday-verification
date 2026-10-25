#!/bin/bash
# mutation test of statement_match.py (family 28): each mutant must exit with the wanted code; a mutant whose input is unchanged is REFUSED.
L=/tmp/oaimath/028/lean-build; cd $L
run(){ local name=$1; local want=$2; shift 2; rm -rf mut/$name; mkdir -p mut/$name; cp logs/*.log mut/$name/; "$@";
  if [ "$name" != unmodified ] && diff -rq logs mut/$name --exclude=out.txt --exclude=statement_match.log >/dev/null 2>&1; then echo "$name REFUSED (mutation did not apply)"; return; fi
  python3 statement_match.py mut/$name > mut/$name/out.txt 2>&1; rc=$?; echo "$name rc=$rc want=$want $( [ "$rc" = "$want" ] && echo OK || echo BAD)"; }
run unmodified 0 true
run def_irreducible 1 sed -i '/@@@ BEGIN def OAI.GaussianMoat.PrimeVertex/,/@@@ BEGIN/ s/Irreducible/Prime/' mut/def_irreducible/ax_GaussianMoat.log
run dist_token 1 sed -i '/@@@ BEGIN def OAI.GaussianMoat.primeGraph/,/@@@ BEGIN/ s/LE.le/LT.lt/' mut/dist_token/ax_GaussianMoat.log
run uniform_token 1 sed -i '/@@@ BEGIN def OAI.GaussianMoat.UniformEndpoint/,/@@@ BEGIN/ s/Set.ncard/Set.encard/' mut/uniform_token/ax_GaussianMoat.log
run extra_axiom 1 sed -i "s/depends on axioms: \[propext, Classical.choice.{u}, Quot.sound.{u}\]/depends on axioms: [propext, sorryAx, Classical.choice.{u}, Quot.sound.{u}]/" mut/extra_axiom/ax_GaussianMoat.log
run cmp_no_sorry 1 sed -i "s/sorryAx.{u}, //; s/, sorryAx.{u}//" mut/cmp_no_sorry/cmp_GaussianMoat.log
run missing_block 2 sed -i '/@@@ BEGIN def OAI.GaussianMoat.component/d' mut/missing_block/ax_GaussianMoat.log
run missing_log 2 rm mut/missing_log/cmp_GaussianMoat.log
