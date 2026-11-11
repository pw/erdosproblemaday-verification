#!/usr/bin/env python3
import glob,sys
from mpmath import mp,mpf
mp.dps=40
sys.path.insert(0,'.')
from check import parse
def row(path):
    h,bl=parse(path); out=[]
    for b in bl:
        # consistency: tail_lo <= invPi - S_lo  (true tail <= invPi - S_lo), and invPi-S_up <= true tail (hence <= invPi - S_lo)
        ip=mpf(h['invPi']); cons = mpf(b['tail_lo'])<=ip-mpf(b['S_lo']) and ip-mpf(b['S_up'])<=ip-mpf(b['S_lo'])
        out.append((h['y'],b['T'],h['R'],h['E'],b['A_up'],mp.nstr(mpf(b['delta_lo']),12),mp.nstr(mpf(b['ratio_lo']),12),b['certified'],h['total_seconds'] if 'total_seconds' in h else '?',cons))
    return out
for tag in ['R1e6','R1201097']:
    print('param set',tag)
    print('| y | T | R | E | A_up | delta_lo | ratio_lo | certified | selfconsistent |')
    for f in sorted(glob.glob(f'log_target_{tag}_*.txt')):
        for r in row(f): print('| '+' | '.join(str(x) for x in (r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[9]))+' |')
