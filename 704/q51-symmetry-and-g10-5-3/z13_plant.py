"""Planted-solution control for the exact-3-cover step of z13.c: feed the search a record list in which a synthetic third mask
(the complement of a real disjoint pair) has been appended; the C search must print exactly the planted solution(s)."""
import struct, subprocess, sys
REC = 32   # u128 mask (16) + 13 roles + 3 pad  -> matches kept_t in z13.c (sizeof = 32)
data = open('z13_kept.bin', 'rb').read(); n = len(data) // REC
recs = [(int.from_bytes(data[i*REC:i*REC+16], 'little'), data[i*REC+16:i*REC+29]) for i in range(n)]
full = (1 << 99) - 1
pair = None
for i in range(n):
    if not recs[i][0] & 1: continue
    for j in range(n):
        if recs[i][0] & recs[j][0] == 0: pair = (i, j); break
    if pair: break
i, j = pair; rest = full ^ recs[i][0] ^ recs[j][0]
assert bin(rest).count('1') == 33
out = bytearray(data) + rest.to_bytes(16, 'little') + bytes([99] * 13) + bytes(3)
open('z13_kept_planted.bin', 'wb').write(out)
print('planted complement of real disjoint pair', i, j, 'as a fake record with roles 99..99; records', n + 1)
