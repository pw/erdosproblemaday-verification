import sys, json, hashlib, os
root=sys.argv[1]
m=json.load(open(os.path.join(root,'manifest-sha256.json')))
# accept dict or list forms
items = m.get('files', m) if isinstance(m, dict) else m
if isinstance(items, dict): pairs=list(items.items())
else: pairs=[(e.get('path') or e.get('file'), e.get('sha256')) for e in items]
ok=bad=miss=0
listed=set()
for p,h in pairs:
    if not isinstance(h,str): continue
    listed.add(p)
    fp=os.path.join(root,p)
    if not os.path.exists(fp): print("MISSING",p); miss+=1; continue
    d=hashlib.sha256(open(fp,'rb').read()).hexdigest()
    if d==h: ok+=1
    else: print("MISMATCH",p); bad+=1
allf=set(os.path.relpath(os.path.join(d,f),root) for d,_,fs in os.walk(root) for f in fs)
unl=sorted(allf-listed-{'manifest-sha256.json'})
print(f"listed={len(listed)} ok={ok} mismatch={bad} missing={miss} unlisted={len(unl)}")
for u in unl: print("  unlisted:",u)
# negative control: corrupt hash comparison
p,h=pairs[0]; print("negctl:", hashlib.sha256(open(os.path.join(root,p),'rb').read()+b'x').hexdigest()!=h)
