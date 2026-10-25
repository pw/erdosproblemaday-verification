# shared graph generators for seat MATH tests
import numpy as np, networkx as nx, subprocess, itertools

def geng(n, extra=()):
    out = subprocess.run(['nauty-geng', '-t', '-q', *extra, str(n)], capture_output=True, text=True).stdout.split()
    return [nx.to_numpy_array(nx.from_graph6_bytes(s.encode()), dtype=float) for s in out]

def clebsch():
    # folded 5-cube: vertices = even-weight? use complement-free construction: Z2^4, x~y iff x^y has weight 1 or 4
    A = np.zeros((16,16))
    for x in range(16):
        for y in range(16):
            w = bin(x^y).count('1')
            if w in (1,4): A[x,y]=1
    return A

def petersen(): return nx.to_numpy_array(nx.petersen_graph())
def cycle(k): return nx.to_numpy_array(nx.cycle_graph(k))
def andrasfai(k):
    n = 3*k-1; A = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            if ((j-i) % n) % 3 == 1: A[i,j]=A[j,i]=1
    return A
def mobius_kantor(): return nx.to_numpy_array(nx.LCF_graph(16,[5,-5],8))
def higman_sims():
    try:
        return None
    except Exception: return None

def is_tf(A):
    return np.trace(A@A@A) < 0.5

def random_bipartite(rng, n):
    k = rng.integers(1, n)
    A = np.zeros((n,n)); p = rng.uniform(0.1, 1.0)
    for i in range(k):
        for j in range(k, n):
            if rng.random() < p: A[i,j]=A[j,i]=1
    return A

def blowup(A, sizes, rng=None, pdel=0.0):
    idx = np.repeat(np.arange(len(sizes)), sizes)
    B = A[np.ix_(idx, idx)].copy()
    if rng is not None and pdel > 0:
        M = np.triu(rng.random(B.shape) < pdel, 1); M = M | M.T
        B[M] = 0
    return B

def random_tf(rng, n, p):
    # random triangle-free graph by greedy random edge insertion
    A = np.zeros((n,n))
    pairs = list(itertools.combinations(range(n), 2)); rng.shuffle(pairs)
    for (i,j) in pairs:
        if rng.random() < p and not np.any(A[i] * A[j]):
            A[i,j]=A[j,i]=1
    return A
