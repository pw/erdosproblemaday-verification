#!/usr/bin/env python3
"""Assert Bridge687b.lean's erdos_687.variants.quadratic_log is verbatim the statement added by FC draft PR #7442
(head ecd8e11c, diff in fc/FC_PR7442.diff). Exit 0 MATCH / 1 MISMATCH / 2 missing. --mutate must exit 1."""
import re, sys
def norm(s): return re.sub(r'\s+', ' ', s).strip()
diff = open('fc/FC_PR7442.diff').read()
added = '\n'.join(l[1:] for l in diff.splitlines() if l.startswith('+') and not l.startswith('+++'))
ours = open('Bridge687b.lean').read()
if '--mutate' in sys.argv: ours = ours.replace('Real.log (x : ℝ)) ^ 2', 'Real.log (x : ℝ)) ^ 3', 1)
def grab(s):
    s = norm(s); i = s.find('theorem erdos_687.variants.quadratic_log'); j = s.find(':= by', i)
    return None if i < 0 or j < 0 else s[i:j + 5]
a, b = grab(added), grab(ours)
print('PR  :', a); print('ours:', b)
if a is None or b is None: sys.exit(2)
print('MATCH' if a == b else 'MISMATCH'); sys.exit(0 if a == b else 1)
