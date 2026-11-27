import json, re, sys
from fractions import Fraction as F
from decimal import Decimal
sys.path.insert(0, '/home/exedev/MathDyad/subs-1127/36/mine')
from overlap_eval import *

def from_decimals(strs):
    vals = [F(Decimal(x)) for x in strs]
    D = 1
    for v in vals:
        D = D * v.denominator // __import__('math').gcd(D, v.denominator)
    return [int(v * D) for v in vals], D

def score_of(strs, label, published=None):
    a, D = from_decimals(strs)
    N = len(a)
    T, mx, am, scale = scores(a, D)
    val = mx * scale
    integ = F(2 * sum(a), N * D)
    print(f"[{label}] N={N} integral={float(integ):.17f} (exact==1: {integ == 1}) max H={float(val):.16f} argmax k={am}")
    if published is not None:
        print(f"     published {published}; |diff| = {abs(float(val) - float(published.split()[0])):.3e}")
    return a, D, val

def mirror(first_half_with_middle, odd):
    # cells listed from x=0 up to the middle cell; mirror f(x)=f(2-x)
    h = list(first_half_with_middle)
    return h + h[:-1][::-1] if odd else h + h[::-1]

# Haugland 2016, 15 steps (n=15: 7 cells + middle cell)
h15 = ['0','0.09938602','0.64299877','0.36104582','0.69536426','0.59241335','0.89573331','0.92611694']
score_of(mirror(h15, True), 'Haugland15', '0.38153155 (rounded up)')
# 19 steps
h19 = ['0','0','0.348795091509472207','0.742684181900847446','0.207655267155520404','0.780222086674911898',
       '0.568104573396874436','0.689049157609512654','0.967251286500411737','0.892476710504898436']
score_of(mirror(h19, True), 'Haugland19', '0.381112263316104816')
# 51 steps
h51 = ['0']*5 + ['0.0002938681556273','0.5952882223921177','0.7844530825484313','0.8950034338013842','0.0597964076006748',
       '0.0189602838469592','0.7420501628172980','0.6444559588500921','0.3549040817844764','0.8762442385073478',
       '0.5437907313675501','0.2679640048997296','0.8518954615823791','0.5211171156914872','1',
       '0.5506146790047043','0.9007715390796991','0.8229000691941086','0.8879541710440111','0.9315424878319221','1']
assert len(h51) == 26
a51, D51, v51 = score_of(mirror(h51, True), 'Haugland51', '0.3809268534330870')

# Wrong-convention control: g = 1 - f NOT truncated to [0,2) (i.e. g = 1 outside) -> should differ
def wrong_convention(strs):
    vals = [F(Decimal(x)) for x in strs]; N = len(vals); w = F(2, N)
    # H(kw) = w * sum_i f_i * (1 - f_{i-k} if in range else 1)
    best = None
    for k in range(-N, N + 1):
        t = sum(vals[i] * ((1 - vals[i - k]) if 0 <= i - k < N else 1) for i in range(N))
        best = t if best is None or t > best else best
    return best * w
print("[Haugland51, WRONG convention g=1 outside [0,2)] max =", float(wrong_convention(mirror(h51, True))), "(expected: 1 = trivially bad)")

# AlphaEvolve published step function
nb = json.load(open('/home/exedev/MathDyad/subs-1127/36/ext/ae/mathematical_results.ipynb'))
src = ''.join(nb['cells'][78]['source'])
body = src[src.index('np.array([') + len('np.array(['): src.index('])')]
nums = re.findall(r'[-+]?\d+\.?\d*(?:e[-+]?\d+)?', body)
seq = nums[:-1] + nums[::-1]   # best_sequence[:-1] ++ reversed(best_sequence)
print("AlphaEvolve raw entries:", len(nums), "full length:", len(seq))
score_of(seq, 'AlphaEvolve', '0.380924 (paper, rounded)')
import numpy as np
fs = np.array([float(x) for x in seq])
print("     AlphaEvolve's own float formula:", np.max(np.correlate(fs, 1 - fs, mode='full')) / len(fs) * 2)

# Negative controls on the submission
obj = json.load(open('/home/exedev/MathDyad/subs-1127/36/repo/construction.json'))
a, D = list(obj['numerators']), obj['denominator']
N = len(a)
T0, mx0, am0, sc = scores(a, D)
U0 = mx0 * sc
# (i) mass-preserving perturbation: move eps between two interior cells, keep 0<=a<=D and sum
i1 = next(i for i in range(N) if 0 < a[i] < D)
i2 = next(i for i in range(N - 1, -1, -1) if 0 < a[i] < D)
eps = 1000
b = list(a); b[i1] += eps; b[i2] -= eps
print("neg control 1 (mass-preserving +/-%d at cells %d,%d): side conditions" % (eps, i1, i2), side_conditions(b, D) or "pass",
      "; U changed:", scores(b, D)[1] * sc != U0, "; new - old = %.3e" % float(scores(b, D)[1] * sc - U0))
# single-cell perturbation of the peak-relevant structure by one unit
b = list(a); j = 5000 if 0 < a[5000] < D else i1; b[j] += 1
print("neg control 2 (+1 at cell %d, mass broken):" % j, side_conditions(b, D))
b = list(a); b[i1] = D + 1
print("neg control 3 (cell above 1):", side_conditions(b, D))
b = list(a); b[i1] = -1
print("neg control 4 (negative cell):", side_conditions(b, D))
# (ii) an engineered profile whose max is known in closed form: f = 1 on [1/2, 3/2) -> overlap max = 1/2 (Erdos 1955 upper bound)
N4 = 4; a4 = [0, 1, 1, 0]
T4, m4, k4, s4 = scores(a4, 1)
print("closed-form control f=1_[1/2,3/2): max H =", m4 * s4, "(expected 1/2) argmax", k4)
