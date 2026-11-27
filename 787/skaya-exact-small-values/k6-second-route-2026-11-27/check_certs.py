"""OUR exact checker for skaya's k=6 Farkas archive (v1.1.1, data/k6_farkas_certs.jsonl.gz).
Written from the definitions, not from their code.

Claim certified by a record (T, y): there are no reals 0 < x_0 < x_1 < ... < x_{m-1}
with x_i + x_j = x_l for every (i,j,l) in T.
Proof: for any solution, sum_q y_q (x_i + x_j - x_l) = 0.  Write the left side as sum_s c_s x_s
(c = A^T y, A row = e_i + e_j - e_l) and substitute x_s = d_0 + ... + d_s with every d_t > 0:
it equals sum_t d_t C_t, C_t = c_t + c_{t+1} + ... + c_{m-1} (suffix sums).  If all C_t >= 0 and
some C_t > 0 (or all <= 0 and some < 0) the sum is nonzero: contradiction.  Integers only.

Usage: check_certs.py FILE.jsonl.gz [--dump-clauses OUT]   (OUT: one line per cert, our triple ids)
Exit 0 = every record certified; 1 = some record failed; 2 = cannot read / empty."""
import sys, gzip, json, time

M = 22

def certify(m, T, y):
    """Return +1 / -1 (sign convention used) if (T, y) is a valid certificate, else 0."""
    if len(T) == 0 or len(T) != len(y):
        return 0
    c = [0] * m
    for (i, j, l), w in zip(T, y):
        if type(i) is not int or type(j) is not int or type(l) is not int or type(w) is not int:
            return 0
        if not (0 <= i < j < l < m):
            return 0
        c[i] += w; c[j] += w; c[l] -= w
    pos = neg = False
    C = 0
    for t in range(m - 1, -1, -1):
        C += c[t]
        if C > 0: pos = True
        elif C < 0: neg = True
    if pos and not neg: return 1
    if neg and not pos: return -1
    return 0

def tid(i, j, l, m=M):
    # our numbering of triples, lexicographic in (i, j, l): same as triple_index() in sat_close.py
    return TID[(i, j, l)]

TID = {}
for _i in range(M):
    for _j in range(_i + 1, M):
        for _l in range(_j + 1, M):
            TID[(_i, _j, _l)] = len(TID)

def main():
    path = sys.argv[1]
    dump = sys.argv[sys.argv.index('--dump-clauses') + 1] if '--dump-clauses' in sys.argv else None
    out = open(dump, 'w') if dump else None
    t0 = time.time()
    n = bad = 0; hist = {}; conv = {1: 0, -1: 0}; zero_w = 0; dup_triple_in_rec = 0
    seen = set(); dups = 0; maxabs = 0; other_mk = 0
    try:
        f = gzip.open(path, 'rt', encoding='utf-8')
        for ln, line in enumerate(f, 1):
            line = line.strip()
            if not line: continue
            rec = json.loads(line)
            n += 1
            if rec.get('m') != M or rec.get('k') != 6: other_mk += 1
            T = [tuple(t) for t in rec['triples']]
            y = rec['weights']
            if any(len(t) != 3 for t in T): bad += 1; print('BAD shape line', ln); continue
            if len(set(T)) != len(T): dup_triple_in_rec += 1
            s = certify(rec.get('m'), T, y) if rec.get('m') == M else 0
            if s == 0:
                bad += 1
                if bad <= 20: print('NOT CERTIFIED line', ln, line[:200], flush=True)
                continue
            conv[s] += 1
            zero_w += sum(1 for w in y if w == 0)
            maxabs = max(maxabs, max(abs(w) for w in y))
            key = tuple(sorted(T))
            if key in seen: dups += 1
            else: seen.add(key)
            hist[len(T)] = hist.get(len(T), 0) + 1
            if out:
                # clause = OR of NOT s(t) over triples with nonzero weight (a zero-weight triple is not needed)
                out.write(' '.join(str(TID[t]) for t, w in zip(T, y) if w != 0) + '\n')
    except (OSError, EOFError, ValueError) as e:
        print('CANNOT READ:', repr(e)); sys.exit(2)
    if out: out.close()
    gt8 = sum(v for k, v in hist.items() if k > 8)
    print(f"records={n} certified={n-bad} NOT_certified={bad} distinct_triple_sets={len(seen)} duplicate_sets={dups}")
    print(f"sign convention: C>=0 (theirs) {conv[1]}, C<=0 {conv[-1]}; zero weights={zero_w}; repeated triple inside a record={dup_triple_in_rec}; records with m!=22 or k!=6: {other_mk}")
    print(f"terms: max={max(hist)} >8 terms={gt8}; max |weight|={maxabs}; size histogram={sorted(hist.items())}")
    print(f"time {time.time()-t0:.1f}s")
    if n == 0: sys.exit(2)
    sys.exit(0 if bad == 0 else 1)

if __name__ == '__main__':
    main()
