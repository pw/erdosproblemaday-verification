"""Referee B: brute-force nu_k and every inequality of Lemma 3.1 (printed p.4) on
QR_7 (n=2), QR_19 (n=3), QR_67 (n=4) and the 70-vertex tournament (n=4).
Also: exact pair-count identity, Lemma 2.2/2.3 consequences, Theorem 1.2 case split,
chain-lemma hypothesis (4) and its Phi inequality, and mutation controls."""
import sys, math, time
from itertools import combinations
from math import comb, log
sys.path.insert(0, '/home/exedev/MathDyad/subs-1126/902/refB')
import tb

def F(x):
    return 0.0 if x == 1 else x * log(x) - (x - 1) * log(x - 1)

def Phi(a, b):
    return F(a) - F(a - b)

def run(name, out, n, ident_cap=400000):
    t0 = time.time()
    N = len(out)
    tb.check_tournament(out)
    inm = tb.in_masks(out)
    nu, cnt = tb.nu_all(inm, N, n)
    print(f'== {name}: N={N}, n={n}, nu_0..nu_{n} = {nu}  (sets enumerated per size {cnt})')
    ok = True
    # S_n and Lemma 2.2/2.3 consequences
    print(f'   S_{n}: nu_{n}={nu[n]} >= 1 ? {nu[n] >= 1}')
    print(f'   Lemma 2.2: nu_{n-1}={nu[n-1]} >= n+1={n+1} ? {nu[n-1] >= n+1}')
    for s in range(n):
        c = nu[s] >= 2 * nu[s + 1] + 1
        ok &= c
        print(f'   Lemma 2.3: nu_{s}={nu[s]} >= 2*nu_{s+1}+1={2*nu[s+1]+1} ? {c}')
    # Lemma 3.1, all s-sets
    worst = {}
    tight_first = 0
    n_checks = 0
    n_ident = 0
    mut_fail_h = 0
    mut_fail_nu = 0
    for s in range(n):
        h = nu[s + 1]
        for A in combinations(range(N), s):
            R = tb.D(inm, A, N)
            m = R.bit_count()
            Aset = set(A)
            o = {}
            for y in range(N):
                if y in Aset:
                    assert out[y] & R == 0  # R beats A
                    continue
                oy = (out[y] & R).bit_count()
                o[y] = oy
                bound = m - h - 1 if (R >> y) & 1 else m - h
                if oy > bound:
                    ok = False
                    print('   PER-Y BOUND FAILS', name, A, y, oy, bound)
                # mutation control: h+1 instead of h
                bmut = m - (h + 1) - 1 if (R >> y) & 1 else m - (h + 1)
                if oy > bmut:
                    mut_fail_h += 1
                # identity (2): D(A u {y}) = R & inm[y]
                if (R & inm[y]) != tb.D(inm, A + (y,), N):
                    ok = False
                    print('   IDENTITY (2) FAILS', A, y)
            for k in range(1, n + 1):
                mid = sum(comb(oy, k) for oy in o.values())
                lhs = nu[k] * comb(m, k)
                r1 = (N - s - m) * comb(m - h, k) + m * comb(m - h - 1, k)
                r2 = (N - s) * comb(m - h, k)
                n_checks += 1
                if not (lhs <= mid <= r1 <= r2):
                    ok = False
                    print('   LEMMA 3.1 FAILS', name, s, A, k, lhs, mid, r1, r2)
                if lhs == mid and comb(m, k) > 0:
                    tight_first += 1
                if (nu[k] + 1) * comb(m, k) > mid:
                    mut_fail_nu += 1
                key = (s, k)
                sl = (mid - lhs, r1 - mid, r2 - r1)
                if key not in worst:
                    worst[key] = list(sl)
                else:
                    worst[key] = [min(a, b) for a, b in zip(worst[key], sl)]
                # exact double-count identity: sum over k-subsets U of R of |D(U)|
                if comb(m, k) <= ident_cap and (s <= 1 or comb(m, k) <= 3000):
                    Rl = tb.bits(R)
                    tot = 0
                    for U in combinations(Rl, k):
                        tot += tb.D(inm, U, N).bit_count()
                    n_ident += 1
                    if tot != mid:
                        ok = False
                        print('   COUNT IDENTITY FAILS', A, k, tot, mid)
    print(f'   Lemma 3.1: {n_checks} (A,k) checks, {n_ident} exact count identities, all OK = {ok}')
    print(f'   min slacks (mid-lhs, r1-mid, r2-r1) per (s,k): ' +
          ', '.join(f'{k}:{tuple(v)}' for k, v in sorted(worst.items())))
    print(f'   first inequality attained with equality in {tight_first} (A,k) cases')
    print(f'   CONTROL: per-y bound with h+1 violated {mut_fail_h} times; first ineq with nu_k+1 violated {mut_fail_nu} times (both must be >0 for the check to be able to go red)')
    # Theorem 1.2 case split (n>=3 meaningful)
    if n >= 3:
        Lam = (n + 1) * comb(2 * n + 3, n - 1) / comb(n + 2, 3)
        P = (2 * n + 5) * 2 ** (n - 2)
        if nu[n - 2] == 2 * n + 3:
            print(f'   Thm1.2 Case 1 (nu_(n-2)=2n+3): need N >= Lambda+n-2 = {Lam + n - 2:.3f}; N={N}: {N >= Lam + n - 2}')
        else:
            print(f'   Thm1.2 Case 2 (nu_(n-2)={nu[n-2]} >= 2n+4): need N+1 >= 2^(n-2)(2n+5) = {P}; N+1={N+1}: {N + 1 >= P}')
    # Chain lemma hypothesis (4) with M=N, and its first conclusions
    M = N
    for i in range(2, n + 1):
        m_, h_ = nu[n - i], nu[n - i + 1]
        c4 = comb(m_, n) <= M * comb(m_ - h_, n)
        G = math.log(comb(m_, n) / comb(m_ - h_, n)) if comb(m_ - h_, n) else float('inf')
        ph = n * Phi((m_ + 1) / n, h_ / n)
        print(f'   chain (4) i={i}: C({m_},{n}) <= {M}*C({m_ - h_},{n}) ? {c4};  m-h>=n ? {m_ - h_ >= n};  '
              f'n*Phi((m+1)/n,h/n)={ph:.4f} <= G={G:.4f} <= ln M={log(M):.4f} ? {ph <= G + 1e-12 and G <= log(M) + 1e-12}; '
              f'Phi <= ln2+2ln(n)/n ({log(2) + 2 * log(n) / n:.4f}) ? {ph / n <= log(2) + 2 * log(n) / n} (M<=n^2 2^n: {M <= n*n*2**n})')
    print(f'   time {time.time() - t0:.1f}s')
    return nu, ok

if __name__ == '__main__':
    results = {}
    results['QR7'] = run('QR_7', tb.qr_tournament(7), 2)
    results['QR19'] = run('QR_19', tb.qr_tournament(19), 3)
    results['QR67'] = run('QR_67', tb.qr_tournament(67), 4)
    t70 = tb.load_outlists('/home/exedev/MathDyad/subs-1126/902/repo/proof/thin_S4_N70.txt')
    results['N70'] = run('thin_S4_N70', t70, 4)
    print('ALL OK' if all(r[1] for r in results.values()) else 'SOME FAILURE')
    print('nu vectors:', {k: v[0] for k, v in results.items()})
