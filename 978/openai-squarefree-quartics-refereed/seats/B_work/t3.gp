rho2(f,p)={my(q=p^2,c=0);for(a=0,q-1,if(subst(f,x,a)%q==0,c++));c};
eu(f,P)={my(s=0.,d=poldisc(f));forprime(p=2,P,my(r);if(p<500||d%p==0,r=rho2(f,p),r=#polrootsmod(f,p));s+=log(1-r/p^2));exp(s)};
f=x^4-2*x^2+2; print("disc ",factor(poldisc(f))); print("T^4-2T^2+2: ",eu(f,10^6));
g=x^4-x^2+2; print("n^4-n^2+2: ",eu(g,10^6));
quit;
