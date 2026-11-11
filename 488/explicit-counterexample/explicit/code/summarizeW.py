import re,sys
first={}; seen=set()
for l in open(sys.argv[1]):
    m=re.match(r"y=(\d+) T=(\d+) n=(\d+) .*bestW=(\d+) .*ratio_lo=([\d.]+) certified=(\d)",l)
    if m:
        y=int(m.group(1)); seen.add(y)
        if m.group(6)=='1' and y not in first: first[y]=(int(m.group(3)),int(m.group(2)),int(m.group(4)),float(m.group(5)))
for y in sorted(seen):
    if y in first: n,T,W,r=first[y]; print(f"y={y} first certified T={T:.3e} n={n:.4e} W={W} ratio_lo={r:.5f}")
    else: print(f"y={y} none certified")
