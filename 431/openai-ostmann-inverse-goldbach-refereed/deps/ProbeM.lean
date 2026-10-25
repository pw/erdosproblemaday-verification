import OAI.NumberTheory.Ostmann.Main
import DepProbe
theorem unusedProbeConstant : True := trivial
#eval report "M main -> dirichlet_real_zero_bound" `OAI.Ostmann.main `OAI.Erdos970.WeightedTorusJets.dirichlet_real_zero_bound
#eval report "M main -> dirichletRealZeroBound_proof (wrapper)" `OAI.Ostmann.main `OAI.Erdos970.WeightedTorusJets.dirichletRealZeroBound_proof
#eval report "M main -> large_modulus_siegel_walfisz" `OAI.Ostmann.main `OAI.Erdos970.Erdos970Dependency.SiegelWalfisz.large_modulus_siegel_walfisz
#eval report "POSITIVE CONTROL main -> actual_no_decomposition" `OAI.Ostmann.main `OAI.Ostmann.Conclusion.actual_no_decomposition
#eval report "NEGATIVE CONTROL main -> unusedProbeConstant" `OAI.Ostmann.main `unusedProbeConstant
