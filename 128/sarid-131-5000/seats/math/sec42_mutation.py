# Mutation control for the end-to-end Section 4.2 test: an instance where the (14) saving is attained with
# EQUALITY for the c*1_Y baseline (G[Y] = K_{4,4} uniform, a = 3/16 <= 1/5), so inflating the saving by 1% must fail.
import numpy as np, sys
from fractions import Fraction as Fr
sys.path.insert(0,'/tmp/erdos1800/seats/math')
src = open('sections234.py').read()
exec(src.split('# ---------- Corollary 4.2')[0])
exec(src[src.index('def L(al):'):src.index('worst = np.inf; nt = 0')])
n = 13; A = np.zeros((n,n)); Y = list(range(5,13))
for i in Y[:4]:
    for j in Y[4:]: A[i,j]=A[j,i]=1
Xmask = np.zeros(n, bool); Xmask[:5] = True
# replicate sec42 but return per-baseline (target, achieved)
X = [i for i in range(n) if Xmask[i]]
nx_, ny = len(X), len(Y); eY = int(A[np.ix_(Y,Y)].sum()//2)
IY = Fr(eY, n*n); s = Fr(ny-nx_, n); a = s/(1+s); c = 1-a; mu = 4*c*c*IY
print("a =", a, " c =", c, " mu =", mu, " L(a) =", L(float(a)))
H = A[np.ix_(Y,Y)]; w = np.full(ny, 1/ny); muH = 0.5*w@H@w; d = H@w; ee = H@(w*d); S = d*(ee-muH*d)
x = 0; dd = d[x]; z = 1-dd; phi = H[x]-dd; al = float(c)
tp = min((1-al)/z, al/dd); tm = min(al/z, (1-al)/dd)
f2 = np.zeros(n); f2[Y] = al
best = min(cost(A, np.where(np.isin(np.arange(n), Y), 0, 0) + 0) for _ in [0])
vals = []
for tt in (tp, -tm):
    g = f2.copy(); g[Y] = al + tt*phi; vals.append(cost(A, g))
achieved = float(mu)/4 - min(vals)
guaranteed = L(float(a))*float(mu)**3/float(c)**2
print(f"B2 baseline: achieved saving = {achieved:.12e}, guaranteed L mu^3/c^2 = {guaranteed:.12e}, ratio = {achieved/guaranteed:.12f}")
print("mutation x1.01 of the guaranteed saving:", "FAILS (test discriminates)" if achieved < 1.01*guaranteed else "still passes")
print("mutation 'forgot 1/(4c^2)' (saving 4 L mu^3):", "FAILS" if achieved < 4*L(float(a))*float(mu)**3 else "passes")
