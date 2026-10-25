import os, re, sys
root = sys.argv[1]
hits = []
for dp, dn, fn in os.walk(root):
    for f in fn:
        if not f.endswith('.lean'): continue
        p = os.path.join(dp, f)
        s = open(p, encoding='utf-8').read()
        # strip nested block comments
        out = []; i = 0; depth = 0
        while i < len(s):
            if s.startswith('/-', i): depth += 1; i += 2; continue
            if depth and s.startswith('-/', i): depth -= 1; i += 2; continue
            if depth: i += 1; continue
            if s.startswith('--', i):
                j = s.find('\n', i); i = len(s) if j < 0 else j; continue
            if s[i] == '"':
                j = i+1
                while j < len(s) and s[j] != '"':
                    if s[j] == '\\': j += 1
                    j += 1
                i = j+1; continue
            out.append(s[i]); i += 1
        code = ''.join(out)
        for m in re.finditer(r'\b(sorry|admit|axiom|implemented_by|extern|unsafe|opaque)\b', code):
            ln = code.count('\n', 0, m.start()) + 1
            hits.append((p, m.group(1)))
for h in hits: print(h)
print('total', len(hits))
