from mpmath import mp, mpf, log
mp.dps = 50
A_h=mpf('1.0001'); z_h=mpf('1.0001'); q_h=mpf('2.48909')
A_t=mpf('1.16312'); z_t=mpf('1.34305'); q_t=mpf('1.34288'); c=mpf('3.3912')
al=1/q_h; be=1/q_t; ga=al*be
M=A_h*log(q_h)+A_t*log(q_t)
E=M+2*ga+al+be-4
H=M+ga+al+be-3
print('alpha',al,'beta',be,'gamma',ga)
print('head tail margin', A_h*log(z_h)-(z_h-1))
print('top tail margin', A_t*log(z_t)-(z_t-1))
print('c log z_t -1', c*log(z_t)-1)
print('1 - c log q_t', 1-c*log(q_t))
print('M',M,'E',E,'H',H,'H+gamma',H+ga,'E+1',E+1)
print('-E-3 (L-exponent first term)', -E-3, ' -H-2', -H-2)
# geometric-series constants
for (A,z,name) in [(A_h,z_h,'head'),(A_t,z_t,'top')]:
    d=(z-1)-A*log(z)
    print(name,'ratio exp(d)=',mp.exp(d),' 1/(1-ratio)=',1/(1-mp.exp(d)))
# Lean point
A_h2=mpf('1.000001'); q_h2=mpf('2.48933')
al2=1/q_h2; ga2=al2*be
E2=A_h2*log(q_h2)+A_t*log(q_t)+2*ga2+al2+be-4
print('Lean point E',E2)
# optimum w/o constraints
