-- Independent axiom check of OpenAI's Lean proof of Erdős #3 (family 159), run with `lake env lean --trust=0`.
import OAI.Combinatorics.Progressions.Main
#print axioms OAI.Erdos3.manuscriptReciprocalProgressionTheorem
#print axioms OAI.Erdos3.manuscriptQuantitativeDensityTheorem
#print axioms OAI.Erdos3.manuscript_main_theorems
set_option pp.all true in
#print OAI.Erdos3.ReciprocalProgressionTheorem
set_option pp.all true in
#print OAI.Erdos3.HasAP
set_option pp.all true in
#print OAI.Erdos3.reciprocalTerm
set_option pp.all true in
#print OAI.Erdos3.QuantitativeDensityBound
#check @OAI.Erdos3.manuscriptReciprocalProgressionTheorem
