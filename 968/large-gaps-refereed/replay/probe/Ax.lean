import OAI.NumberTheory.PrimeGaps.RatioCorollary
set_option pp.all true
#eval IO.println "@@@ BEGIN thm OAI.Problem344.large_gaps_and_ratio_density"
#check @OAI.Problem344.large_gaps_and_ratio_density
#print axioms OAI.Problem344.large_gaps_and_ratio_density
#eval IO.println "@@@ BEGIN def OAI.LargePrimeGaps.prime"
#print OAI.LargePrimeGaps.prime
#eval IO.println "@@@ BEGIN def OAI.LargePrimeGaps.largeGapIndices"
#print OAI.LargePrimeGaps.largeGapIndices
#eval IO.println "@@@ BEGIN def OAI.Problem344.primeAt"
#print OAI.Problem344.primeAt
#eval IO.println "@@@ BEGIN def OAI.Problem344.initialCount"
#print OAI.Problem344.initialCount
#eval IO.println "@@@ BEGIN def OAI.Problem344.lowerAsymptoticDensity"
#print OAI.Problem344.lowerAsymptoticDensity
#eval IO.println "@@@ BEGIN def OAI.Problem344.ratioIncreaseIndices"
#print OAI.Problem344.ratioIncreaseIndices
#eval IO.println "@@@ END"
#eval IO.println "@@@ EXTRA axioms"
#print axioms OAI.LargePrimeGaps.main
#print axioms OAI.LargePrimeGaps.bombieriVinogradov
#print axioms OAI.LargePrimeGaps.siegelWalfisz
#print axioms OAI.Problem344.positive_lower_density_prime_ratio_increases
#eval IO.println "@@@ EXTRA bv-sw statements"
#print OAI.LargePrimeGaps.BombieriVinogradov
#print OAI.LargePrimeGaps.SiegelWalfisz
#print OAI.LargePrimeGaps.endpointError
