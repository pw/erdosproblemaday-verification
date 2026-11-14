import json, itertools, math, sys
from fractions import Fraction
# (g) 48-colouring
d=json.load(open('/home/exedev/MathDyad/erdos704/q51/colouring48_n13.json'))
cl=[[frozenset(s) for s in c] for c in d['classes']]
allv=[s for c in cl for s in c]
full={frozenset(c) for c in itertools.combinations(range(13),5)}
print('48-col: classes',len(cl),'sets',len(allv),'distinct',len(set(allv)),'covers',set(allv)==full,
      'all 5-sets', all(len(s)==5 and max(s)<13 and min(s)>=0 for s in allv),
      'bad', sum(1 for c in cl for a,b in itertools.combinations(c,2) if len(a&b)==3),
      'nonempty', all(len(c)>0 for c in cl), 'max class', max(len(c) for c in cl))
# (e)
print('39 mod 5,7,11:', 39%5, 39%7, 39%11)
# (f)
deg=math.comb(5,3)*math.comb(8,2); print('degree',deg)
a=33; V=1287; print('Lovasz (1+ln a)V/a =', (1+math.log(a))*V/a)
print('13!/48/13 =', math.factorial(13)//48//13, ' 13!/48=', math.factorial(13)//48)
print('divisibility table:', [(t,f,t%f) for t,f in [(627,25),(303,17),(147,9),(71,7),(35,3)]])
print('Burnside (13+8)/9 =', Fraction(21,9))
