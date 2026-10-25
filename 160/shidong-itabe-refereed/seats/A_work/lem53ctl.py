import math, importlib.util, sys
# negative control for the carry test: tau = floor(2x/M) (two halves) admits the middle-only carry
for j in (3,4,5):
    M = 2**j; tau = [(2*x)//M for x in range(M)]; bad = 0
    for s in range(M):
        for y0 in range(M):
            y = [(y0+i*s) % M for i in range(4)]
            if tau[y[0]]==tau[y[1]] and tau[y[2]]==tau[y[3]] and len({int(y[i+1]<y[i]) for i in range(3)})!=1: bad += 1
    print(f"control tau=floor(2x/M), M={M}: carry-consistency violations = {bad} (expect >0)")
