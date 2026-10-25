# Seat S: negative controls for S_params.run (each perturbation must trip the named check), fast settings.
import sys; sys.path.insert(0, '/tmp/oaimath/028/seats/S_work')
from S_params import run, mpf
fr = ('1', '1.05')
print("baseline M=90:", run(90, fracs=fr)[0])
print("NC1 n_i=T^{beta_i} (drop the 6/5)  ->", run(90, n_exp=mpf(1), fracs=fr)[0])
print("NC2 r_i-r_{i+1}=beta_i (gap halved) ->", run(90, gap=1, fracs=fr)[0])
print("NC3 g1=e^{-M} instead of e^{-M^3}  ->", run(90, g1log=lambda M: M, fracs=fr)[0])
print("NC4 g2=e^{-M^3} instead of e^{-100M^20} ->", run(90, g2log=lambda M: M**3, fracs=fr)[0])
print("NC5 heavy hidden constants C43=1e6, CD=1e9, g0=1e-6 at M=90 ->", run(90, C43=mpf('1e6'), CD=mpf('1e9'), g0=mpf('1e-6'), fracs=fr)[0])
print("NC5 same at M=120 ->", run(120, C43=mpf('1e6'), CD=mpf('1e9'), g0=mpf('1e-6'), fracs=fr)[0])
