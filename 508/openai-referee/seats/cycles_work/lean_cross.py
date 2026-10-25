import itertools
X="X"
def valid(w): return all(w[j]!=w[(j+1)%6] for j in range(6)) and all(not(w[j]!=X and w[(j+3)%6]!=X and w[j]!=w[(j+3)%6]) for j in range(6))
def cross1(w,u):  # Lean FourWordCross w u : forall j, w j != 0 -> u(j+1) != w j and u(j-1) != w j
    return all(w[j]==X or (u[(j+1)%6]!=w[j] and u[(j-1)%6]!=w[j]) for j in range(6))
W=["".join(t) for t in itertools.product("XUV",repeat=6) if valid("".join(t))]
mixed=[w for w in W if {j%2 for j in range(6) if w[j]==X}=={0,1}]
print("one-directional (Lean FourWordCross) isolation:", all([u for u in W if cross1(w,u)]==[w] for w in mixed))
