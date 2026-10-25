# Seat P, task 3: the reserved-tag packing, exhaustively.
import sys
words = []
for m in range(1 << 12):
    c = sum(((m >> j) & 1) * 3**j for j in range(12))
    words.append(c)
W = sorted(words)
Wset = set(W)
assert len(W) == 4096 and len(Wset) == 4096
below10 = [c for c in W if c < 10]
below = [c for c in W if c < 204391]
print('words below 10:', below10, 'count', len(below10))
print('words below 204391:', len(below), ' max:', max(below), ' next word:', min(c for c in W if c >= 204391))
print('binary of 2920 =', bin(2920)[2:], '; its ternary reading =', int(bin(2920)[2:], 3))
norm = [c for c in below if c >= 10]
T = len(norm)
k = 2*204391 - 1
print('T (norm words) =', T, ' k =', k, ' 2*max(norm) =', 2*max(norm), ' k-1 =', k-1)
# positions
i_pos = norm; j_pos = norm; l_pos = [k-1-2*c for c in norm]
assert all(0 <= x < k for x in i_pos + l_pos)
assert len(set(l_pos)) == T and len(set(i_pos)) == T
print('min l position =', min(l_pos), ' max l =', max(l_pos))
# Midpoint freeness on the FULL cube: x+y=2z with x,y,z in cube => x=y=z  (exhaustive over all pairs x<=y)
viol = 0; pairs = 0
for a in range(4096):
    x = W[a]
    for b in range(a, 4096):
        y = W[b]; pairs += 1
        s = x + y
        if s % 2 == 0 and (s // 2) in Wset and a != b: viol += 1
print(f'full cube: {pairs} unordered pairs (incl. equal), midpoint violations: {viol}')
# restricted 2921-set
S = below; Sset = set(S); viol2 = 0; pairs2 = 0
for a in range(len(S)):
    for b in range(a, len(S)):
        pairs2 += 1
        s = S[a] + S[b]
        if s % 2 == 0 and (s // 2) in Sset and a != b: viol2 += 1
print(f'2921-set: {pairs2} unordered pairs, violations: {viol2}')
# Full support matching with tags: row1 support {0} U norm, row2 {0,1,3,4,9} U norm, row3 l-positions
tags = [0, 1, 3, 4, 9]
def matching_triples(row1, row2, row3set):
    out = []
    r3 = set(row3set)
    for p1 in row1:
        for p2 in row2:
            p3 = k - 1 - p1 - p2
            if p3 in r3: out.append((p1, p2, p3))
    return out
row1 = [0] + norm; row2 = tags + norm
assert not (set([0]) & set(norm)) and not (set(tags) & set(norm))
trip = matching_triples(row1, row2, l_pos)
good = all(p1 == p2 and p1 in set(norm) and p3 == k-1-2*p1 for (p1, p2, p3) in trip)
print(f'with tags: {len(trip)} position triples summing to k-1; all matched (a=a\'=a\'\') & tag-free: {good}')
# the tag-row-2-alone and two-tag cases are included above (row1 tag 0 x row2 tags)
# CONTROL 1: a tag at 8 (not a cube word) must create a spurious triple: 8 + 12 + l(10) = k-1
tagsbad = [0, 1, 3, 4, 8]
tripb = matching_triples([0] + norm, tagsbad + norm, l_pos)
spur = [t for t in tripb if not (t[0] == t[1] and t[0] in set(norm))]
print(f'CONTROL tag set {tagsbad}: spurious triples {len(spur)} (must be >0), e.g. {spur[:3]}')
# CONTROL 2: positions l_a = k - 2c (off by one) must lose the matching
tripc = matching_triples(row1, row2, [k - 2*c for c in norm if k-2*c < k])
print(f'CONTROL l=k-2c: matched triples {sum(1 for t in tripc if t[0]==t[1])} (must be 0 or broken), total {len(tripc)}')
# CONTROL 3: a non-midpoint-free set (all integers 10..2925) must violate
S3 = list(range(10, 10+T)); S3set = set(S3)
v3 = sum(1 for a in range(0, len(S3), 7) for b in range(a+1, len(S3), 7) if (S3[a]+S3[b]) % 2 == 0 and (S3[a]+S3[b])//2 in S3set)
print(f'CONTROL consecutive-integer positions: midpoint violations (sampled) {v3} (must be >0)')
# eta
eta_den = 249*k + 5
print('k =', k, ' 249k+5 =', eta_den, ' 2/(249k+5) = 1/', eta_den/2)
