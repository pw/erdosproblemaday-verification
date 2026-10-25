# Count tau-symmetric APs (Lemma 2.2 setting) in which some non-top digit has effective step
# delta_j + carry_in == p (step 0 mod p but TRUE carry 1) -- the case where Lemma 2.1's e_i (=0)
# differs from the true carry (=1). Verify the true carries are still constant there.
import sys
k, p, L = 4, 13, 3
P = p**L
tau = [((k-1)*x)//p for x in range(p)]
dig = lambda n: [(n // p**j) % p for j in range(L)]
edge = bad = 0
for d in range(1, P):
    dd = dig(d)
    for a in range(P):
        ns = [(a + i*d) % P for i in range(k)]
        xs = [dig(n) for n in ns]
        if not all(tau[xs[i-1][j]] == tau[xs[k-i][j]] for j in range(L-1) for i in range(1, k//2+1)):
            continue
        # true carries per transition per digit
        hit = False
        carries = []
        for i in range(k-1):
            c = 0; row = []
            for j in range(L):
                tot = xs[i][j] + dd[j] + c
                if j < L-1 and dd[j] + c == p: hit = True
                c = tot // p; row.append(c)
            carries.append(row)
        if hit:
            edge += 1
            if any(len({carries[i][j] for i in range(k-1)}) != 1 for j in range(L-1)): bad += 1
print(f"k={k} p={p} L={L}: tau-symmetric APs hitting the delta_j+carry=p edge case: {edge}; with non-constant true carries out of digits 0..L-2: {bad}")
sys.exit(1 if bad else 0)
