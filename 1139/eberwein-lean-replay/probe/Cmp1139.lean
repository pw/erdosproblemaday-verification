import Ref1139
import Erdos1139Official
-- The reference type was fixed when Ref1139 was compiled against Mathlib alone; the kernel must accept the
-- submitted proof at that type.
theorem cmp1139 : type_of% Ref1139.erdos_1139 := Erdos1139.erdos_1139
#print axioms cmp1139
#print axioms Ref1139.erdos_1139
set_option pp.all true in
#check (Ref1139.erdos_1139)
set_option pp.all true in
#check (Erdos1139.erdos_1139)
