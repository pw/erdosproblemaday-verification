import random, sys
sys.argv=['x']
src=open('localtest.py').read().split("rng = random.Random(1188)")[0]
exec(src)
rng=random.Random(1188); rep=0; tot=0; ks=[]
for L in (72,144,360,720,1080,2520,5040,4200):
    for _ in range(400):
        s=random_minimal(L,rng); tot+=1; mods=[n for _,n in s]; ks.append(len(s))
        if len(set(mods))<len(mods): rep+=1
print(f"{rep}/{tot} tested systems have repeated moduli; classes per system min/median/max = {min(ks)}/{sorted(ks)[len(ks)//2]}/{max(ks)}")
