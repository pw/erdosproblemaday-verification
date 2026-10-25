#!/usr/bin/env python3
"""Spot-check of PROOF.md's sentence 'Li's seed under rule Q is eventually periodic (membership period
5,733 = 49*117 ...)' on the referee's own greedy output (to 1e6). Not a proof; a consistency check.
Also: find the smallest membership period p <= 20000 that holds on [3364, 1e6-p] and the onset."""
import sys
L = 10**6
S = set(int(x) for x in open('greedy_Li_ruleQ_1e6.txt'))
ind = bytearray(L + 1)
for x in S: ind[x] = 1
def holds(p, start):
    return all(ind[t] == ind[t + p] for t in range(start, L - p + 1))
print("5733 == 49*117:", 5733 == 49 * 117)
print("membership period 5733 holds on [3364, 1e6]:", holds(5733, 3364))
print("... and fails from 3363?", not holds(5733, 3363))
cnt = sum(ind[t] for t in range(3364, 3364 + 5733))
print("elements per period window:", cnt)
best = None
for p in range(1, 20001):
    if all(ind[t] == ind[t + p] for t in range(500000, 520000)):
        if holds(p, 3364):
            best = p; break
print("smallest p<=20000 with ind(t)=ind(t+p) on [3364,1e6]:", best)
