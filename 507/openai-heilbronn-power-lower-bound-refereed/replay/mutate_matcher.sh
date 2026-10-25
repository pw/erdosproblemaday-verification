#!/bin/bash
# mutation test of statement_match_v2.py (family 191): each mutant must exit with the wanted code; a mutant whose input is unchanged is REFUSED.
L=/tmp/oaimath/191/lean-build; cd $L
run(){ local name=$1; local want=$2; shift 2; rm -rf mut/$name; mkdir -p mut/$name; cp logs/*.log mut/$name/; "$@";
  if [ "$name" != unmodified ] && diff -q <(cat logs/ax_HeilbronnTriangle.log logs/cmp_HeilbronnTriangle.log logs/kid_Ax.log logs/kid_Cmp.log 2>/dev/null) <(cat mut/$name/ax_HeilbronnTriangle.log mut/$name/cmp_HeilbronnTriangle.log mut/$name/kid_Ax.log mut/$name/kid_Cmp.log 2>/dev/null) >/dev/null 2>&1; then echo "$name REFUSED (mutation did not apply)"; return; fi
  python3 statement_match_v2.py mut/$name > mut/$name/out.txt 2>&1; rc=$?; echo "$name rc=$rc want=$want $( [ "$rc" = "$want" ] && echo OK || echo BAD)"; }
run unmodified 0 true
run K_body_plus2 1 sed -i '/@@@ BEGIN def OAI.Problem355.heilbronnK/,/@@@ BEGIN/ s/(nat_lit 1) (instOfNatNat (nat_lit 1))/(nat_lit 2) (instOfNatNat (nat_lit 2))/' mut/K_body_plus2/ax_HeilbronnTriangle.log
run K_kernel_hash 1 sed -i 's/OAI.Problem355.heilbronnK kernel_hints=regular 7 value_hash=3603132665/OAI.Problem355.heilbronnK kernel_hints=regular 7 value_hash=1111111111/' mut/K_kernel_hash/kid_Ax.log
run K_hints_opaque 1 sed -i 's/OAI.Problem355.heilbronnK kernel_hints=regular 7/OAI.Problem355.heilbronnK kernel_hints=opaque/' mut/K_hints_opaque/kid_Cmp.log
run D_is_43 1 sed -i '/@@@ BEGIN def OAI.Problem355.heilbronnD/,/@@@ BEGIN/ s/nat_lit 41/nat_lit 43/g' mut/D_is_43/ax_HeilbronnTriangle.log
run area_no_abs 1 sed -i '/@@@ BEGIN def OAI.Problem355.triangleArea/,/@@@ BEGIN/ s/abs\.{0}/neg.{0}/' mut/area_no_abs/ax_HeilbronnTriangle.log
run extra_axiom 1 sed -i "s/depends on axioms: \[propext, Classical.choice.{u}, Quot.sound.{u}\]/depends on axioms: [propext, sorryAx.{u}, Classical.choice.{u}, Quot.sound.{u}]/" mut/extra_axiom/ax_HeilbronnTriangle.log
run missing_kid 2 rm mut/missing_kid/kid_Cmp.log
run missing_block 2 sed -i '/@@@ BEGIN def OAI.Problem355.heilbronnT/d' mut/missing_block/ax_HeilbronnTriangle.log
run refusal_guard_control 1 true
