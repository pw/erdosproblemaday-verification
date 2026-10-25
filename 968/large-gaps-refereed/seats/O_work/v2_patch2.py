s=open('v2_cf.py').read()
old="        K[c0:c0+64]=k*(z-1j*eta*mu - z*z/2 + z**3/3)\n"
new="""        az=np.abs(z); ser=z-z*z/2+z**3/3-z**4/4; ex=np.log(1+z)
        K[c0:c0+64]=k*(np.where(az<1e-3,ser,ex)-1j*eta*mu)   # exact log(1+z); 4-term series only where |z|<1e-3
"""
assert old in s; s=s.replace(old,new); open('v2_cf.py','w').write(s)
