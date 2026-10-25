import numpy as np, math
from lem24 import ball, counts
for shape in [[(10,3,1),(20,3,1),(40,3,1)],[(6,6,1),(10,10,1),(14,14,1)],[(3,3,3),(4,4,4),(5,5,5),(6,6,6)],[(12,6,2),(24,6,2)],[(20,8,2)]]:
    for (R1,R2,R3) in shape:
        tmax=40
        h=counts(R1,R2,R3,tmax)
        base=(R1*R2*R3)**2
        mx=max(range(1,tmax+1),key=lambda t:h[t+tmax])
        print(f"R=({R1},{R2},{R3}) count(t=1)/(R1R2R3)^2={h[1+tmax]/base:.2f}  max_t count/(R1R2R3)^2={h[mx+tmax]/base:.2f} at t={mx}  /log^2(2R1)={h[mx+tmax]/base/math.log(2*R1)**2:.2f}",flush=True)
