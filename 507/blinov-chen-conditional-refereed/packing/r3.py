# exact r_3(n): largest 3-AP-free subset of {0..n-1}; DFS with simple bound. Returns (size, lexicographically-first optimal set)
import sys
from functools import lru_cache
def r3_table(nmax):
    best = [0]*(nmax+1); sets=[None]*(nmax+1)
    for n in range(1, nmax+1):
        # set must include 0 wlog? (translate) -- yes, optimal set can be translated to contain 0 if min>0 (stays in range)
        target = best[n-1]+1   # r3(n) <= r3(n-1)+1
        found = None
        def dfs(cur, forb, nxt, need):
            nonlocal found
            if found: return
            if len(cur) == target:
                found = list(cur); return
            # bound: remaining positions
            rem = need - len(cur)
            if n - nxt < rem: return
            # bound via best table: elements in [nxt, n) at most best[n-nxt]
            if best[n-nxt] < rem: return
            for x in range(nxt, n):
                if (forb >> x) & 1: continue
                if best[n-x] < rem: return
                # add x: forbid 2x - y for y in cur (x is largest so 2x-y > x) and (x+y)/2 not needed (y<x, midpoint < x already checked? midpoint m of y,x: need m not in set -> check)
                ok = True
                for y in cur:
                    if (x + y) % 2 == 0 and ((x+y)//2) in curset: ok=False; break
                if not ok: continue
                newf = forb
                for y in cur:
                    z = 2*x - y
                    if z < n: newf |= (1 << z)
                cur.append(x); curset.add(x)
                dfs(cur, newf, x+1, need)
                cur.pop(); curset.discard(x)
                if found: return
        curset = {0}
        dfs([0], 0, 1, target)
        if found:
            best[n] = target; sets[n] = found
        else:
            best[n] = best[n-1]; sets[n] = sets[n-1]
    return best, sets
if __name__ == "__main__":
    nmax = int(sys.argv[1])
    b, s = r3_table(nmax)
    for n in range(1, nmax+1):
        print(n, b[n], s[n])
