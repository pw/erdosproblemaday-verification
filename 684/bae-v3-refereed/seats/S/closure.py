#!/usr/bin/env python3
"""Compute the Lean import closure of given root modules across the lake packages
and grep every file in it for proof-escape keywords.  Read-only."""
import os, re, sys, json
REPO = sys.argv[1]
roots = sys.argv[2:]
PK = os.path.join(REPO, '.lake', 'packages')
# module prefix -> source root dirs
srcroots = [REPO] + [os.path.join(PK, d) for d in sorted(os.listdir(PK))]
def find(mod):
    rel = mod.replace('.', '/') + '.lean'
    for r in srcroots:
        p = os.path.join(r, rel)
        if os.path.isfile(p):
            return p
    return None
imp_re = re.compile(r'^\s*(?:public\s+)?(?:meta\s+)?import\s+(?:all\s+)?([\w.\'«»]+)', re.M)
seen = {}
missing = set()
stack = list(roots)
while stack:
    m = stack.pop()
    if m in seen or m in missing: continue
    p = find(m)
    if p is None:
        missing.add(m); continue
    src = open(p, encoding='utf-8', errors='replace').read()
    seen[m] = p
    # only consider the header region (imports must precede other commands)
    for im in imp_re.findall(src):
        stack.append(im)
# keyword scan, ignoring comments crudely: strip /- -/ blocks and -- line comments
def strip_comments(s):
    out = []; i = 0; depth = 0; n = len(s)
    while i < n:
        if s.startswith('/-', i):
            depth += 1; i += 2; continue
        if depth and s.startswith('-/', i):
            depth -= 1; i += 2; continue
        if depth: i += 1; continue
        if s.startswith('--', i):
            j = s.find('\n', i); i = n if j < 0 else j; continue
        out.append(s[i]); i += 1
    return ''.join(out)
KW = [r'\bsorry\b', r'\badmit\b', r'^\s*(?:private\s+|protected\s+)?axiom\b', r'\bnative_decide\b',
      r'implemented_by', r'@\[extern', r'\bopaque\b', r'maxHeartbeats\s+0', r'\bdebug\.skipKernelTC\b',
      r'\bunsafe\b', r'Lean\.ofReduceBool', r'\bdecide\s*\+kernel', r'sorryAx']
hits = {}
for m, p in sorted(seen.items()):
    s = strip_comments(open(p, encoding='utf-8', errors='replace').read())
    for kw in KW:
        for mm in re.finditer(kw, s, re.M):
            line = s.count('\n', 0, mm.start()) + 1
            hits.setdefault(m, []).append((kw, line, s.splitlines()[line-1].strip()[:140]))
bypkg = {}
for m, p in seen.items():
    pk = p[len(PK)+1:].split('/')[0] if p.startswith(PK) else 'PROJECT'
    bypkg[pk] = bypkg.get(pk, 0) + 1
print('closure size', len(seen), 'by package', json.dumps(bypkg))
print('missing modules (core Lean/Std/Init etc.):', len(missing), sorted(missing)[:40])
for m in sorted(hits):
    pk = seen[m]
    for kw, line, txt in hits[m]:
        print(f'{m}:{line}: [{kw}] {txt}')
