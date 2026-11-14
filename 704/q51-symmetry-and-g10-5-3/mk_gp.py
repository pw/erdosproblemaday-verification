import numpy as np
M = np.load('copies_rows.npy')[:1600].astype(int)     # rows = copies
R, n = M.shape
with open('lat.gp', 'w') as f:
    f.write('default(parisize, 4000000000);\n')
    f.write('M = Mat([' + ';'.join(','.join(str(int(M[r, c])) for r in range(R)) for c in range(n)) + ']);\n')  # n x R, columns = copies
    f.write('n = %d;\n' % n)
    f.write('e1 = vectorv(n, i, i==1); d12 = vectorv(n, i, (i==1)-(i==2)); ones = vectorv(n, i, 1);\n')
    f.write('t(B,d) = { my(X = matsolvemod(M, d, B)); if(X == 0, 0, 1) };\n')
    for name, B, d in [('3*e_S mod 9', '3*e1', 9), ('e_S mod 9 [control: must be 0]', 'e1', 9), ('e_S - e_S\' mod 9', 'd12', 9),
                       ('11*e_S mod 121', '11*e1', 121), ('e_S mod 121 [control: must be 0]', 'e1', 121), ('e_S - e_S\' mod 121', 'd12', 121),
                       ('all-ones mod 9', 'ones', 9), ('all-ones mod 121', 'ones', 121),
                       ('33*e_S mod 2^4*3^4*5^2*7^2*11^3*13^2', '33*e1', 2**4*3**4*5**2*7**2*11**3*13**2),
                       ('all-ones mod 2^4*3^4*5^2*7^2*11^3*13^2', 'ones', 2**4*3**4*5**2*7**2*11**3*13**2)]:
        f.write('print("%s : ", t(%s, %d));\n' % (name, B, d))
    f.write('quit;\n')
