# Independent checker for Folkman k=4: bitset intersection, not a 15-sum loop.
# For colour class K (bitmask, bit i <=> colour(i)=K, i in 1..N):
#   valid c for mono pair {a,b}:  K & K>>a & K>>b & K>>(a+b)   (bit c <=> c, c+a, c+b, c+a+b all in K)
#   valid d for mono triple {a,b,c}: AND of K>>s over the 8 subset sums s of {a,b,c} incl. 0
# Bits above N are absent, so the range constraint sum<=N is enforced by the shifts themselves.
import sys
def parse(path, mode):
    raw = open(path,'rb').read()
    if mode == 'strip':      # every 0/1 byte is a colour, whitespace ignored
        bad = set(raw) - set(b'01 \r\n')
        assert not bad, bad
        s = bytes(c for c in raw if c in b'01').decode()
    elif mode == 'firstline':
        s = raw.split(b'\n')[0].decode()
    elif mode == 'literal':  # char i = colour of i, no filtering
        s = raw.decode()
    return s
def count(colstr, want_example=True):
    N = len(colstr)
    assert set(colstr) <= set('01'), "non-0/1 char in colour string: %r" % (set(colstr)-set('01'))
    masks = {}
    for k in '01':
        m = 0
        for i,ch in enumerate(colstr, start=1):
            if ch == k: m |= 1 << i
        masks[k] = m
    total = 0; first = None; per = {}
    for k,K in masks.items():
        cnt = 0
        elems = [i for i in range(1,N+1) if (K>>i)&1]
        for a in elems:
            Ka = K & (K >> a)
            for b in elems:
                if b <= a: continue
                if a + b > N: break
                if not (K >> (a+b)) & 1: continue
                C = Ka & (K >> b) & (K >> (a+b))
                C >>= (b+1)             # c > b
                c = b
                while C:
                    low = (C & -C).bit_length() - 1
                    c += low + 1; C >>= low + 1
                    D = K
                    for s in (a, b, c, a+b, a+c, b+c, a+b+c):
                        D &= K >> s
                    D >>= (c+1)        # d > c
                    n = bin(D).count('1')
                    if n:
                        cnt += n
                        if first is None:
                            d = c + 1 + ((D & -D).bit_length() - 1)
                            first = (a,b,c,d,k)
        per[k] = cnt; total += cnt
    return N, total, per, first
if __name__ == '__main__':
    path, mode = sys.argv[1], sys.argv[2]
    s = parse(path, mode)
    N, total, per, first = count(s)
    print(f"mode={mode} N={N} mono4={total} per_colour={per} first={first}")
