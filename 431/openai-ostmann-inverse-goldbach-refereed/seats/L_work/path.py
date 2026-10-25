import re, os, sys, collections
# Textual over-approximation of the declaration-reference graph inside one import closure.
# Edge X -> Y if the body text of a declaration with short name X mentions an identifier whose last component is Y.
# Prints a shortest chain src -> dst (to be verified by hand: short-name matching can create spurious edges).
base = '/tmp/oaimath/013'
closure, src, dst = sys.argv[1], sys.argv[2], sys.argv[3]

def path(mod):
    parts = mod.split('.')
    roots = {'OAI': f'{base}/repo/lean/',
             'PrimeNumberTheoremAnd': f'{base}/ext/PrimeNumberTheoremAnd/',
             'StrongPNT': f'{base}/ext/StrongPNT/',
             'BernoulliRegular': f'{base}/ext/AINTLIB/projects/FltRegularBernoulli/',
             'Common': f'{base}/ext/AINTLIB/Common/'}
    if parts[0] not in roots:
        return None
    p = roots[parts[0]] + '/'.join(parts) + '.lean'
    return p if os.path.exists(p) else None

declre = re.compile(r'^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*'
                    r'(theorem|lemma|def|abbrev|instance|structure|inductive|class)\s+([^\s:(\[{]+)')
tok = re.compile(r"[A-Za-z_][A-Za-z0-9_'.]*")
bodies = collections.defaultdict(list)   # short name -> list of (file, token set)
for m in open(closure):
    p = path(m.strip())
    if not p:
        continue
    cur, toks = None, set()
    for line in open(p, errors='replace'):
        mm = declre.match(line)
        if mm:
            if cur:
                bodies[cur.split('.')[-1]].append((p, toks))
            cur, toks = mm.group(2), set()
        if cur:
            for t in tok.findall(line):
                toks.add(t.split('.')[-1])
    if cur:
        bodies[cur.split('.')[-1]].append((p, toks))
names = set(bodies)
edges = {s: set().union(*[t for _, t in lst]) & names - {s} for s, lst in bodies.items()}
prev = {src: None}
dq = collections.deque([src])
while dq:
    x = dq.popleft()
    if x == dst:
        break
    for y in edges.get(x, ()):
        if y not in prev:
            prev[y] = x
            dq.append(y)
print('decls indexed:', len(names), ' reachable from src:', len(prev))
if dst in prev:
    chain, x = [], dst
    while x:
        chain.append(x)
        x = prev[x]
    for c in reversed(chain):
        print(c, '  @', bodies[c][0][0].replace(base + '/repo/lean/', ''))
else:
    print('NO PATH')
