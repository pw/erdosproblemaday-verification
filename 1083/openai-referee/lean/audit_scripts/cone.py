import re,os,sys,json,collections
root=sys.argv[1]
def path(m): return os.path.join(root,m.replace('.','/')+'.lean')
start=sys.argv[2]
seen=set();q=[start];ext=collections.Counter();oai=set()
while q:
    m=q.pop()
    if m in seen: continue
    seen.add(m)
    p=path(m)
    if not os.path.exists(p): print("MISSING",m); continue
    for imp in re.findall(r'^\s*import\s+(\S+)',open(p,encoding='utf-8').read(),re.M):
        if imp.startswith('DistinctDistances'): q.append(imp)
        elif imp.startswith('OAI'): oai.add(imp)
        else: ext[imp.split('.')[0]]+=1
allmods=set()
for dp,dn,fn in os.walk(os.path.join(root,'DistinctDistances')):
    for f in fn:
        if f.endswith('.lean'):
            allmods.add(os.path.relpath(os.path.join(dp,f),root)[:-5].replace('/','.'))
allmods.add('DistinctDistances')
dead=sorted(allmods-seen)
print("cone",len(seen),"all",len(allmods),"outside cone",len(dead))
lines=sum(len(open(path(m),encoding='utf-8').read().splitlines()) for m in seen)
print("cone lines",lines)
print("OAI direct from cone",len(oai))
json.dump({'cone':sorted(seen),'dead':dead,'oai':sorted(oai)},open(sys.argv[3],'w'),indent=0)
for d in dead: print("DEAD",d)
