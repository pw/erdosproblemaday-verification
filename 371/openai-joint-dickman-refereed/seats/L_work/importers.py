import os,re,sys
root='/tmp/oaimath/012/src/oai'
imp={}
for dp,dn,fn in os.walk(root+'/OAI'):
    for f in fn:
        if f.endswith('.lean'):
            p=os.path.join(dp,f); m=p[len(root)+1:-5].replace('/','.')
            imp[m]=[l.split()[1] for l in open(p) if l.startswith('import ')]
rev={}
for m,ims in imp.items():
    for i in ims: rev.setdefault(i,[]).append(m)
def path_to(target, goalprefix='OAI.NumberTheory.JointDickman'):
    # BFS up importers until reaching a JointDickman module
    from collections import deque
    q=deque([[target]]); seen={target}
    while q:
        pth=q.popleft()
        for r in rev.get(pth[-1],[]):
            if r in seen: continue
            seen.add(r)
            if r.startswith(goalprefix): return pth+[r]
            q.append(pth+[r])
for t in sys.argv[1:]:
    print(t,'->',path_to(t))
