"""Referee B: the integer recursion of Section 4.1 (printed p.5-6), written from the
paper's text only.  Exact integer arithmetic (math.comb).

  L_n = 1.  For s = n-1..0: L_s = least integer m >= 2 L_{s+1} + 1, m <= N - s, such that for every
  1 <= k <= min(m, n):  (N-s-m) C(m-L_{s+1}, k) + m C(m-L_{s+1}-1, k) >= lam_k C(m, k),
  lam_k = L_k (k > s),  lam_k = 2^{s+1-k} (L_{s+1}+1) - 1 (k <= s).  L_s = inf if no m qualifies.
  N is "ruled out" iff some L_s = inf (L_0 <= N - 0 automatically otherwise).
"""
import sys
from math import comb as _comb
INF = float('inf')

def comb(x, k):  # paper's convention: C(x,k)=0 when x<k (also for negative x)
    return _comb(x, k) if x >= k else 0

def Ls(n, N, hshift=0):
    """returns list L[0..n] (INF entries if ruled out).  hshift: mutation control (h = L_{s+1}+hshift)."""
    L = [None] * (n + 1)
    L[n] = 1
    for s in range(n - 1, -1, -1):
        b = L[s + 1]
        if b == INF:
            L[s] = INF
            continue
        h = b + hshift
        lam = [None] * (n + 1)
        for k in range(1, n + 1):
            lam[k] = L[k] if k > s else 2 ** (s + 1 - k) * (b + 1) - 1
        found = INF
        for m in range(2 * b + 1, N - s + 1):
            good = True
            for k in range(1, min(m, n) + 1):
                if (N - s - m) * comb(m - h, k) + m * comb(m - h - 1, k) < lam[k] * comb(m, k):
                    good = False
                    break
            if good:
                found = m
                break
        L[s] = found
    return L

def ruled_out(n, N, hshift=0):
    L = Ls(n, N, hshift)
    return any(x == INF for x in L) or L[0] > N

def least_not_ruled_out(n, hshift=0):
    lo = (n + 2) * 2 ** (n - 1) - 1  # classical bound; recursion must not go below it (sanity)
    lo = max(lo - 50, n + 1)
    hi = lo
    while ruled_out(n, hi, hshift):
        hi *= 2
    # binary search on [lo, hi] assuming monotonicity (checked separately on a window)
    assert ruled_out(n, lo, hshift) or n <= 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if ruled_out(n, mid, hshift):
            lo = mid
        else:
            hi = mid
    return hi

if __name__ == '__main__':
    paper = {2: 7, 3: 19, 4: 49, 5: 121, 6: 281, 7: 665, 8: 1485, 9: 3388, 10: 7398, 11: 16569, 12: 35655}
    W = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    allok = True
    for n in range(2, 13):
        V = least_not_ruled_out(n)
        # window check: every N in [V-W, V-1] ruled out, V not ruled out, and a few above V not ruled out
        lo = max(n + 1, V - W)
        win_ok = all(ruled_out(n, N) for N in range(lo, V)) and not any(ruled_out(n, N) for N in range(V, V + 5))
        L = Ls(n, V)
        ok = (V == paper[n]) and win_ok
        allok &= ok
        print(f'n={n:2d}: least N not ruled out = {V:6d}  paper {paper[n]:6d}  match={V == paper[n]}  '
              f'window[{lo},{V + 4}] monotone-consistent={win_ok}  L(V)={L}')
        sys.stdout.flush()
    print('ALL MATCH' if allok else 'MISMATCH')
