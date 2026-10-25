import re, sys, os, urllib.request, collections, json
REV="adc7f1241b42e322a6451854ab7e4b4c146bf78a"
BASE=f"https://raw.githubusercontent.com/openai/math/{REV}/lean/"
OUT="/tmp/oaimath/166/oai_lean"
roots=[l.strip() for l in open(sys.argv[1]) if l.strip()]
maxdepth=int(sys.argv[2]) if len(sys.argv)>2 else 99
depth={r:1 for r in roots}
q=collections.deque(roots); seen=set(roots); edges={}
fails=[]
while q:
    m=q.popleft()
    path=m.replace('.','/')+'.lean'
    dest=os.path.join(OUT,path)
    if not os.path.exists(dest):
        try:
            req=urllib.request.Request(BASE+path,headers={'User-Agent':'curl/8.5.0'})
            data=urllib.request.urlopen(req,timeout=60).read()
        except Exception as e:
            fails.append((m,str(e))); continue
        os.makedirs(os.path.dirname(dest),exist_ok=True)
        open(dest,'wb').write(data)
    txt=open(dest,encoding='utf-8',errors='replace').read()
    imps=re.findall(r'^\s*(?:public\s+)?(?:meta\s+)?import\s+(?:all\s+)?(OAI\.[\w.]+)',txt,re.M)
    edges[m]=imps
    for i in imps:
        if i not in seen and depth[m]<maxdepth:
            seen.add(i); depth[i]=depth[m]+1; q.append(i)
json.dump({'depth':depth,'edges':edges,'fails':fails},open(os.path.join(OUT,'_closure.json'),'w'),indent=1)
print(len(seen),"modules; fails",len(fails)); 
c=collections.Counter(depth.values()); print(sorted(c.items()))
for f in fails[:20]: print("FAIL",f)
