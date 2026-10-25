import re
exec(open('holes.py').read().split("pats={")[0])
files=open('files.txt').read().split()
for f in files:
    s=strip(open(f,encoding='utf8').read())
    for i,l in enumerate(s.splitlines(),1):
        if re.search(r'Classical\.choice|^\s*open\s+(scoped\s+)?Classical|^\s*attribute\s*\[(?!local|scoped)',l):
            print(f.replace('/tmp/oaimath/021/',''),i,l.strip()[:130])
