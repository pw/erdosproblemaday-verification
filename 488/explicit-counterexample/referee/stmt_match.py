import re, difflib, sys
fc = open('/tmp/e488/lean/fc_488_main.lean').read()
ad = open('/home/exedev/MathDyad/erdos488/src/gessel/Erdos488.lean').read()
fc_body = fc[fc.index('theorem erdos_488 :') + len('theorem erdos_488 :'): fc.index(':= by\n  sorry')]
ad_body = ad[ad.index('abbrev proposition : Prop :=') + len('abbrev proposition : Prop :='): ad.index('theorem refutation')]
strip_comments = lambda s: re.sub(r'--[^\n]*', '', s)
norm = lambda s: re.sub(r'\s+', ' ', strip_comments(s)).strip()
a, b = norm(fc_body), norm(ad_body)
print("FC body  :", a); print("Adapter  :", b)
print("identical after removing the one `--` comment and collapsing whitespace:", a == b)
print("char-level opcodes:", [op for op in difflib.SequenceMatcher(None, a, b).get_opcodes() if op[0] != 'equal'])
print("raw (with comment) line diff:")
for l in difflib.unified_diff(fc_body.strip().splitlines(), ad_body.strip().splitlines(), 'fc', 'adapter', lineterm='', n=0): print('  ', l)
