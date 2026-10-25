import OAI.NumberTheory.Jacobsthal.Main
import DepProbe
theorem unusedProbeConstant970 : True := trivial
#eval report "970 iterated_log -> dirichlet_real_zero_bound" `OAI.Erdos970.Erdos970Final.erdos_970_iterated_log `OAI.Erdos970.WeightedTorusJets.dirichlet_real_zero_bound
#eval report "970 quadratic -> dirichlet_real_zero_bound" `OAI.Erdos970.Erdos970Final.erdos_970_quadratic `OAI.Erdos970.WeightedTorusJets.dirichlet_real_zero_bound
#eval report "970 iterated_log -> large_modulus_siegel_walfisz" `OAI.Erdos970.Erdos970Final.erdos_970_iterated_log `OAI.Erdos970.Erdos970Dependency.SiegelWalfisz.large_modulus_siegel_walfisz
#eval report "NEGATIVE CONTROL 970 -> unusedProbeConstant970" `OAI.Erdos970.Erdos970Final.erdos_970_iterated_log `unusedProbeConstant970
#eval report "970 POSITIVE CONTROL iterated_log -> IteratedLogBudget.separation" `OAI.Erdos970.Erdos970Final.erdos_970_iterated_log `OAI.Erdos970.NumberTheoryLean.IteratedLogBudget.separation
#eval report "970 quadratic -> dirichletRealZeroBound_proof (wrapper)" `OAI.Erdos970.Erdos970Final.erdos_970_quadratic `OAI.Erdos970.WeightedTorusJets.dirichletRealZeroBound_proof
