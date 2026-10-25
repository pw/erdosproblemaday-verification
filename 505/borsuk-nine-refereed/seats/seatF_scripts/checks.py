import itertools, math, random
import numpy as np
import sympy as sp

# 1. coordinates9 (paper Remark 2.2 / Lean Main.lean) is an isometry on trace-zero symmetric matrices
a = sp.symbols('a0:4_0:4')
A = sp.Matrix(4,4, lambda i,j: sp.Symbol(f'a{min(i,j)}{max(i,j)}'))
A = A.subs(sp.Symbol('a33'), -(sp.Symbol('a00')+sp.Symbol('a11')+sp.Symbol('a22')))
c = [(A[0,0]-A[1,1])/sp.sqrt(2), (A[0,0]+A[1,1]-2*A[2,2])/sp.sqrt(6),
     (A[0,0]+A[1,1]+A[2,2]-3*A[3,3])/sp.sqrt(12)] + [sp.sqrt(2)*A[i,j] for i in range(4) for j in range(i+1,4)]
lhs = sp.expand(sum(x**2 for x in c)); rhs = sp.expand(sum(A[i,j]**2 for i in range(4) for j in range(4)))
print("coordinates9 isometry identity:", sp.simplify(lhs-rhs)==0)

# 2. (2.1): ||uu^T - vv^T||_F^2 = 2 - 2<u,v>^2 for unit u,v
rng = np.random.default_rng(1)
err = 0
for _ in range(1000):
    u = rng.normal(size=4); u/=np.linalg.norm(u); v = rng.normal(size=4); v/=np.linalg.norm(v)
    err = max(err, abs(np.sum((np.outer(u,u)-np.outer(v,v))**2) - (2-2*np.dot(u,v)**2)))
print("(2.1) max err", err)

# 3. Admissible maps exist at the sharp counts k=2 (m=3) and k=3 (m=6): Voronoi covering radius of lines
def cover_radius(lines, dim, n=200000):
    L = np.array([l/np.linalg.norm(l) for l in lines])
    X = rng.normal(size=(n,dim)); X /= np.linalg.norm(X,axis=1)[:,None]
    m = np.abs(X@L.T).max(axis=1)   # cos of angle to nearest line
    return math.degrees(math.acos(m.min()))
lines2 = [np.array([math.cos(t), math.sin(t)]) for t in (0, math.pi/3, 2*math.pi/3)]
print("k=2, 3 lines: covering radius ~", round(cover_radius(lines2,2),3), "deg (need <45)")
phi = (1+5**0.5)/2
ico = [(0,1,phi),(0,1,-phi),(1,phi,0),(1,-phi,0),(phi,0,1),(-phi,0,1)]
print("k=3, 6 icosahedral lines: covering radius ~", round(cover_radius([np.array(p,float) for p in ico],3),3), "deg (need <45)")
# k=4: 12 lines of the 24-cell (D4 roots) alone, and with the dual 24-cell (12 more lines)
d4 = set()
for i,j in itertools.combinations(range(4),2):
    for s in (1,-1):
        v=[0]*4; v[i]=1; v[j]=s; d4.add(tuple(v))
dual = [tuple(1 if k==i else 0 for k in range(4)) for i in range(4)] + \
       [tuple(x) for x in itertools.product((1,-1),repeat=4) if x[0]==1]
print("k=4, 12 lines (24-cell): covering radius ~", round(cover_radius([np.array(p,float) for p in d4],4),3), "deg")
print("k=4, 24 lines (24-cell + dual):", len(d4)+len(dual), "lines, covering radius ~",
      round(cover_radius([np.array(p,float) for p in list(d4)+dual],4),3), "deg (need <45)")
