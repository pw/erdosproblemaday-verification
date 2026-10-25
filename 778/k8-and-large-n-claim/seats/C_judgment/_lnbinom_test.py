from scipy.special import betaln, gammaln
from mpmath import mp, binomial, log, mpf
import math
mp.dps = 50
for n, k in [(10**17, 10**5), (10**12, 3*10**4), (10**8, 10**6), (1000, 7), (10**20, 40)]:
    exact = float(log(binomial(mpf(n), mpf(k))))
    b = -math.log(n+1) - betaln(n-k+1, k+1)
    g = gammaln(n+1) - gammaln(k+1) - gammaln(n-k+1)
    print(n, k, exact, b - exact, g - exact)
