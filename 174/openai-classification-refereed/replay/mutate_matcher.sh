#!/bin/bash
# mutation test of statement_match.py (family 172): each mutant must exit with the wanted code; a mutant whose input is unchanged is REFUSED (exit 3).
L=/tmp/oaimath/172/lean-build; cd $L
run(){ local name=$1; local want=$2; shift 2; rm -rf mut/$name; mkdir -p mut/$name; cp logs/*.log mut/$name/; "$@";
  if [ "$name" != unmodified ] && diff -rq logs mut/$name --exclude=out.txt --exclude=statement_match.log >/dev/null 2>&1; then echo "$name REFUSED (mutation did not apply)"; return; fi
  python3 statement_match.py mut/$name > mut/$name/out.txt 2>&1; rc=$?; echo "$name rc=$rc want=$want $( [ "$rc" = "$want" ] && echo OK || echo BAD)"; }
run unmodified 0 true
run def_token 1 sed -i '/@@@ BEGIN def OAI.EuclideanRamsey.Congruent/,/@@@ BEGIN/ s/Dist.dist/Inner.inner/' mut/def_token/ax_EuclideanRamseyCircle.log
run thm_numeral 1 sed -i '0,/nat_lit 5/ s/nat_lit 5/nat_lit 6/' mut/thm_numeral/ax_EuclideanRamseyCircle.log
run nine_count 1 sed -i '0,/nat_lit 9/ s/nat_lit 9/nat_lit 8/' mut/nine_count/ax_EuclideanRamseyNine.log
run extra_axiom 1 sed -i "s/depends on axioms: \[propext, Classical.choice.{u}, Quot.sound.{u}\]/depends on axioms: [propext, sorryAx, Classical.choice.{u}, Quot.sound.{u}]/" mut/extra_axiom/ax_GrahamSpherical.log
run cmp_no_sorry 1 sed -i "s/sorryAx, //; s/, sorryAx//" mut/cmp_no_sorry/cmp_EuclideanRamsey.log
run missing_block 2 sed -i '/@@@ BEGIN def OAI.GrahamSpherical.parameter/d' mut/missing_block/ax_GrahamSpherical.log
run missing_log 2 rm mut/missing_log/cmp_EuclideanRamseyTransitive.log
