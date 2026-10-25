import sys,json,collections
for f in sys.argv[1:]:
    ev=collections.Counter(); st=collections.Counter(); idx=[]; other=[]
    for line in open(f):
        r=json.loads(line); ev[r.get('event')]+=1
        if r.get('event')=='case': st[r.get('status')]+=1; idx.append(r['index'])
        else: other.append({k:v for k,v in r.items() if k not in('args',)})
    print(f.split('/')[-1], dict(ev), dict(st), 'idx', (min(idx),max(idx),len(idx),len(set(idx))) if idx else None)
    for o in other: print('   ', json.dumps(o)[:400])
