import sys,json
d=json.load(open(sys.argv[1]))
for r in d['records']:
    print("N",r['minimum'],"terms",r['terms'],"len",len(r['denominators']),"cmp",r.get('comparison_upper'),"cmplen",len(r.get('comparison_denominators',[])))
    print(" den",",".join(r['denominators']))
    print(" cmp",",".join(r.get('comparison_denominators',[])))
    print(" keys",[k for k in r if k not in('denominators','comparison_denominators')])
