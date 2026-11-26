"""Referee B: tail of check_bip.py (variable-shadowing bug fixed)."""
import sys, itertools
sys.path.insert(0, '/home/exedev/MathDyad/subs-1126/902/refB')
from check_bip_funcs import has_S, game_value, nus
# enumerator positive control: the same search as in check_bip.py, at total 4 for n=1, must find an example
found = None
for K in range(1, 3):
    for m in range(K, 5 - K):
        for fam in itertools.combinations_with_replacement(range(1 << K), m):
            if has_S(K, m, list(fam), 1):
                found = (K, m, fam); break
        if found: break
    if found: break
print('ENUMERATOR CONTROL: S_{1,1} with |A|+|B|<=4 found:', found)
words = ['111000', '110100', '100011', '010011', '001110', '001101']
ex = [sum(1 << i for i in range(6) if words[i][j] == '1') for j in range(6)]
v = game_value(6, 6, ex); nA, nB = nus(6, 6, ex)
print(f'Remark 5.2 example: v={v:.6f}, nu^A={nA}, nu^B={nB}; Lemma 5.1 A-side ok: '
      f'{all(nA[s+1] <= v*nA[s]+1e-9 for s in range(6))}, B-side ok: {all(nB[s+1] <= (1-v)*nB[s]+1e-9 for s in range(6))}')
print('   Theorem 1.5 chain at n=2: (n+1)^2=9 <= nu^A_1*nu^B_1 =', nA[1] * nB[1], '<= v(1-v)*K*m =', round(v * (1 - v) * 36, 4))
for n in range(2, 6):
    print(f'n={n}: |A|=n,|B|=1 (b->all of A) satisfies the literal S_{{n,n}}: {has_S(n, 1, [(1 << n) - 1], n)} '
          f'(order {n+1} < (n+1)2^n = {(n+1)*2**n});  |A|=|B|=1 satisfies it vacuously: {has_S(1, 1, [1], n)}')
