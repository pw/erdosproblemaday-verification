import re, json, sys
src = open('/home/exedev/MathDyad/subs-1127/36/repo/Overlap/Data.lean').read()
defs = {}
for m in re.finditer(r'^def (\w+) : Tree := (.*)$', src, re.M):
    defs[m.group(1)] = m.group(2)
tok = re.compile(r'Tree\.leaf (\d+)|\b((?:heights|events)_\d+)\b')
memo = {}
def expand(name):
    if name in memo: return memo[name]
    out = []
    for m in tok.finditer(defs[name]):
        if m.group(1) is not None: out.append(int(m.group(1)))
        else: out.extend(expand(m.group(2)))
    memo[name] = out
    return out
# sanity: each def body only contains Tree.node, Tree.leaf, parens, names
for k, v in defs.items():
    rest = re.sub(r'Tree\.node|Tree\.leaf \d+|(?:heights|events)_\d+|[() ]', '', v)
    assert rest == '', (k, rest[:50])
H = expand('heights'); E = expand('events')
obj = json.load(open('/home/exedev/MathDyad/subs-1127/36/repo/construction.json'))
print("Data.lean heights:", len(H), " == construction.json numerators:", H == obj['numerators'])
T = json.load(open('/home/exedev/MathDyad/subs-1127/36/mine/T_child.json'))
N = len(H)
mine = [int(T[str(k)]) for k in range(-(N - 1), N)]
print("Data.lean events:", len(E), " == my T_k for k=-(N-1)..N-1:", E == mine)
print("events[7123] =", E[7123], " max(events) =", max(E), " index of max:", [i for i, x in enumerate(E) if x == max(E)])
# count leaf-tree structure: does every heights_i / events_i get used exactly once?
used = re.findall(r'\b((?:heights|events)_\d+)\b', defs['heights'] + defs['events'])
print("sub-defs referenced:", len(used), "distinct:", len(set(used)), "defined:", len([k for k in defs if '_' in k]))
