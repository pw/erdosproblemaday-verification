import re,sys,os
src_dir='/tmp/e1125/dl787/repo/proofs'; out='/tmp/e1125/787work/lean'
for f in sorted(os.listdir(src_dir)):
    s=open(os.path.join(src_dir,f)).read()
    ns=re.search(r'^namespace (\S+)',s,re.M).group(1)
    names=re.findall(r'^(?:theorem|lemma) (\S+)',s,re.M)
    body=s.rstrip()
    probe='\n'+'\n'.join(f'#print axioms {ns}.{n}' for n in names)+'\n'
    open(os.path.join(out,f),'w').write(body+'\n'+probe)
    print(f,len(names))
