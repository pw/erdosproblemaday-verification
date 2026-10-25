from lemmaA1_cert import cert, u, v, sp
Q0 = [(1, 0), (0, 1), (-1, 0), (0, -1)]
def point(lab):
    s, j = divmod(lab, 4); a, b = Q0[j]
    if s == 2: return (sp.Integer(a), sp.Integer(b))
    return (u*a - v*b, v*a + u*b) if s == 0 else (u*a + v*b, -v*a + u*b)
for S in [(0,1,2,4,5,6,9,11),(0,1,2,4,6,7,8,10),(0,1,4,7,8,9,10,11),(0,1,5,6,8,9,10,11),(0,2,4,6,8,9,10,11),(0,1,2,3,4,5,6,8),(0,1,2,4,5,6,8)]:
    cert([point(i) for i in S], f"{S}")
