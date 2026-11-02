"""Seat C: empirical test of 'minimal (no proper subfamily covers) <=> every class has a private point'
on random covering systems (moduli not necessarily distinct, so the test is wider than needed)."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import checker
random.seed(1188)
tested = covering = agree = minimal = 0
while covering < 3000:
    k = random.randint(2, 7)
    S = []
    for _ in range(k):
        n = random.choice([2, 3, 4, 5, 6, 8, 9, 10, 12])
        S.append((random.randrange(n), n))
    S = list(dict.fromkeys(S))
    tested += 1
    if not checker.covers(S):
        continue
    covering += 1
    a = checker.minimal_private(S); b = checker.minimal_subfamily(S)
    agree += (a == b); minimal += a
print('random systems tested', tested, 'coverings', covering, 'agreement private<->subfamily', agree, 'of', covering, '; minimal among them', minimal)
