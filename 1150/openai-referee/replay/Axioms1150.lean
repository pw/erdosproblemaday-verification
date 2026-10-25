-- Independent axiom check of OpenAI's Lean proof behind Erdős #1150 (family 076), run with `lake env lean --trust=0`.
import OAI.Analysis.Littlewood.Main
import OAI.Analysis.Littlewood.FiniteFlatness
#print axioms OAI.AsymptoticallyMinimalLittlewood.main
#print axioms OAI.AsymptoticallyMinimalLittlewoodFiniteFlatness.main
set_option pp.all true in
#print OAI.AsymptoticallyMinimalLittlewood.MainStatement
set_option pp.all true in
#print OAI.AsymptoticallyMinimalLittlewood.littlewoodValue
set_option pp.all true in
#print OAI.AsymptoticallyMinimalLittlewood.IsRealSigning
#check @OAI.AsymptoticallyMinimalLittlewood.main
#check @OAI.AsymptoticallyMinimalLittlewoodFiniteFlatness.main
