s=open('v2_cf.py').read()
old="""    for c0 in range(0,M+1,64):
        eta=xi[c0:c0+64]/k; z=1j*eta*mu+rho(eta)
        K[c0:c0+64]=k*(z-1j*eta*mu - z*z/2 + z**3/3)
"""
new="""    K[:]=-np.inf+0j; cut=M+1
    for c0 in range(0,M+1,64):
        eta=xi[c0:c0+64]/k; z=1j*eta*mu+rho(eta)
        K[c0:c0+64]=k*(z-1j*eta*mu - z*z/2 + z**3/3)
        if np.all(K[c0:c0+64].real<-745): cut=c0; break   # |cf| < 1e-323 beyond
"""
assert old in s; s=s.replace(old,new)
s=s.replace("phi=np.exp(K)*np.exp(-1j*xi*(lo-mu))","phi=np.where(np.isfinite(K.real),np.exp(K),0)*np.exp(-1j*xi*(lo-mu))")
s=s.replace("""not claimed)'}] ({time.time()-t0:.0f}s)""","""not claimed)'}] xi_cut={cut}/{M} ({time.time()-t0:.0f}s)""")
open('v2_cf.py','w').write(s)
