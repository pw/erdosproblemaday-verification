import re,sys
exec(open('closure.py').read().split('# keyword scan')[0].replace("REPO = sys.argv[1]","REPO=sys.argv[1]").replace("roots = sys.argv[2:]","roots=sys.argv[2:]"))
for m,p in sorted(seen.items()):
    if not m.startswith('Mathlib') and not m.startswith('Aesop') and not m.startswith('Batteries'):
        print(m, p)
