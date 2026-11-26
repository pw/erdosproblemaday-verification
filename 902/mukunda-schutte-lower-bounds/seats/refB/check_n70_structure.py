"""Referee B: Section 10 claim - the 70-vertex S_4 tournament is QR_67 plus three vertices and has
a triple with exactly 5 dominators; also report which triples attain 5 and in-degrees of added vertices."""
import sys
from itertools import combinations
sys.path.insert(0, '/home/exedev/MathDyad/subs-1126/902/refB')
import tb
t = tb.load_outlists('/home/exedev/MathDyad/subs-1126/902/repo/proof/thin_S4_N70.txt')
tb.check_tournament(t)
q = tb.qr_tournament(67)
mask67 = (1 << 67) - 1
same = all((t[v] & mask67) == q[v] for v in range(67))
rev = all((t[v] & mask67) == (mask67 & ~q[v] & ~(1 << v)) for v in range(67))
print('vertices 0..66 induce QR_67 (j-i square):', same, ' or its reverse:', rev)
inm = tb.in_masks(t)
B = (67, 68, 69)
print('D(B) =', tb.bits(tb.D(inm, B, 70)), ' in-degrees of 67,68,69:', [inm[v].bit_count() for v in B])
five = [X for X in combinations(range(70), 3) if tb.D(inm, X, 70).bit_count() == 5]
print('triples with exactly 5 dominators:', len(five), five[:10])
print('min in-degree', min(x.bit_count() for x in inm), 'max', max(x.bit_count() for x in inm))
