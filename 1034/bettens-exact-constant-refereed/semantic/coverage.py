import json, itertools, re, ast
import numpy as np
model = json.load(open('../deposit/verification_model.json'))
P7 = list(itertools.combinations(range(7), 2)); pidx = {p: i for i, p in enumerate(P7)}
reps = np.array(model["graph_slack_flags"], dtype=np.int64)
table = np.full(1 << 21, -1, dtype=np.int32)
for perm in itertools.permutations(range(7)):
    out = np.zeros_like(reps)
    for b, (i, j) in enumerate(P7):
        out |= ((reps >> b) & 1) << pidx[(min(perm[i], perm[j]), max(perm[i], perm[j]))]
    table[out] = np.arange(1044)
hit = set(); per = []
for line in open('run_main.log'):
    m = re.match(r'trial \d+: K=(\d+) m=(\[.*?\]) A=(\[\[.*?\]\]) classes_hit=(\d+)', line)
    if not m: continue
    K = int(m.group(1)); A = np.array(ast.literal_eval(m.group(3)))
    tup = np.array(list(itertools.product(range(K), repeat=7)))
    mask = np.zeros(len(tup), dtype=np.int64)
    for b, (i, j) in enumerate(P7): mask |= A[tup[:, i], tup[:, j]].astype(np.int64) << b
    s = set(table[mask].tolist()); per.append((len(s), int(m.group(4)))); hit |= s
print("union classes hit:", len(hit), "per-trial (ours, logged) agree:", all(a == b for a, b in per))
# twin-free count
def has_twin(mask):
    adj = [[(mask >> pidx[(min(i,j),max(i,j))]) & 1 if i != j else 0 for j in range(7)] for i in range(7)]
    for u in range(7):
        for v in range(u+1, 7):
            if all(adj[u][w] == adj[v][w] for w in range(7) if w not in (u, v)): return True
    return False
print("graphs with a twin pair:", sum(has_twin(int(x)) for x in reps))
