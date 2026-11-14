import json, itertools, re
full={frozenset(c) for c in itertools.combinations(range(10),5)}
for fn in ['colouring21_sym_7_1_1_1.json','colouring21_sym_5_1_1_1_1_1.json']:
    d=json.load(open('/home/exedev/MathDyad/erdos704/q51/n10/'+fn))
    cl=[frozenset(frozenset(s) for s in c) for c in d['classes']]
    allv=[s for c in cl for s in c]
    g=d.get('g')
    ok = len(cl)==21 and len(allv)==252 and set(allv)==full and all(len(c)==12 for c in cl) and \
        sum(1 for c in cl for a,b in itertools.combinations(c,2) if len(a&b)==3)==0
    inv = set(frozenset(frozenset(g[x] for x in s) for s in c) for c in cl)==set(cl)
    cyc=[];seen=set()
    for x in range(10):
        if x in seen: continue
        l=0;y=x
        while y not in seen: seen.add(y);y=g[y];l+=1
        cyc.append(l)
    print(fn,'proper 21-colouring:',ok,'invariant under g:',inv,'g cycle type',sorted(cyc,reverse=True))
    if '7_1' in fn:
        html=open('/home/exedev/MathDyad/erdos704/q51/page/entry.html').read()
        fams=[frozenset(frozenset(int(ch) for ch in t) for t in re.findall(r'\b\d{5}\b',li)) for li in re.findall(r'<li>([0-9, ;.]+)</li>',html)]
        sh=lambda s: frozenset(((x+1)%7 if x<7 else x) for x in s)
        page=set()
        for f in fams:
            for i in range(7): page.add(f); f=frozenset(sh(s) for s in f)
        print('page colouring == bundle file:', page==set(cl))
