import re,sys
s=open(sys.argv[1]).read()
for e in re.findall(r'<entry>(.*?)</entry>',s,re.S):
    t=' '.join(re.search(r'<title>(.*?)</title>',e,re.S).group(1).split())
    d=re.search(r'<published>(.*?)</published>',e).group(1)[:10]
    u=re.search(r'<updated>(.*?)</updated>',e).group(1)[:10]
    i=re.search(r'<id>(.*?)</id>',e).group(1)
    a=', '.join(re.findall(r'<name>(.*?)</name>',e))[:70]
    print(d,u,i.split('/abs/')[-1],'|',t[:115],'|',a)
