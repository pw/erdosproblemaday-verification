\\ Independent factorisation-based regeneration of all 111 obstruction rows.
left=133858454292;
right=133858454404;
for(n=left+1,right-1,f=factor(n);found=0;for(i=1,matsize(f)[1],p=f[i,1];e=f[i,2];if(!found&&p%4==3&&e%2==1,print("[",n,",",p,",",e,"]");found=1));if(!found,error("missing obstruction at ",n)));
