# Second, independent instrument: numpy vectorised brute force over all 4-sets with sum<=N.
import sys, numpy as np
from itertools import combinations
def check(s):
    N = len(s)
    col = np.zeros(N+1, dtype=np.int8); col[0] = -1
    col[1:] = np.frombuffer(s.encode(), dtype=np.uint8) - 48
    tested = 0; mono = 0; first = None
    masks = [m for m in range(1,16)]
    for a in range(1, N+1):
        for b in range(a+1, N+1):
            if a + b + (b+1) + (b+2) > N: break
            R = N - a - b                 # c + d <= R, b < c < d
            cs = np.arange(b+1, R//2 + 1)
            if cs.size == 0: continue
            # d from c+1 .. R-c
            lens = (R - cs) - cs
            keep = lens > 0; cs = cs[keep]; lens = lens[keep]
            C = np.repeat(cs, lens)
            starts = np.repeat(np.cumsum(lens) - lens, lens)
            D = C + 1 + (np.arange(C.size) - starts)
            tested += C.size
            E = [np.full(C.size, a), np.full(C.size, b), C, D]
            ok = np.ones(C.size, dtype=bool); k = col[a]
            for m in masks:
                t = np.zeros(C.size, dtype=np.int64)
                for j in range(4):
                    if m >> j & 1: t = t + E[j]
                ok &= (col[t] == k)
            n = int(ok.sum())
            if n:
                mono += n
                if first is None:
                    i = int(np.argmax(ok)); first = (a, b, int(C[i]), int(D[i]))
    return N, tested, mono, first
if __name__ == '__main__':
    raw = open(sys.argv[1],'rb').read()
    s = bytes(c for c in raw if c in b'01').decode()
    print("N=%d tested=%d mono=%d first=%s" % check(s))
