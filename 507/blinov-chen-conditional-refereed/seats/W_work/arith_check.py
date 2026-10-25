from math import comb
from fractions import Fraction as F
import math
k_oai = comb(comb(163,41),3)**2 + 1
eta = F(2, 45435*k_oai+16)
l = math.log10(2) - math.log10(45435*k_oai+16)
print("OpenAI eta = 10^%.6f -> mantissa %.4f e%d" % (l, 10**(l-math.floor(l)), math.floor(l)))
for k,name in ((408781,'Blinov e29a291'),(1166895,'Blinov 840a550')):
    e = F(2, 249*k+5); print(name, 'eta =', e, float(e))
print('Chen eta', F(2,100866719), float(F(2,100866719)), ' > 1/50893237:', F(2,100866719) > F(1,50893237), ' ratio', float(F(2,100866719)/F(1,50893237)))
print('ternary 2921st word:', int(bin(2920)[2:],3), ' k = 2*204391-1 =', 2*204391-1)
# negative controls: wrong k must not reproduce the claimed values
print('NEG k=408780 gives 1/50893237?', F(2,249*408780+5) == F(1,50893237))
print('NEG Chen 2/100866720 > 1/50893237 still?', F(2,100866720) > F(1,50893237), '(control only checks direction is not trivially true for all)')
print('NEG 2/101786476 > 1/50893237?', F(2,101786476) > F(1,50893237))
