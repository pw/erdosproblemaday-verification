default(parisize, 200000000);
t=getabstime(); c=0; for(n=10^6-2000,10^6, if(issquarefree(n^4+2), c++)); print(c, " ", getabstime()-t, " ms");
t=getabstime(); c=0; for(n=10^6-2000,10^6, f=factor(n^4+2); for(j=1,#f~, if(f[j,2]>=2 && f[j,1]>n, c++))); print(c, " ", getabstime()-t, " ms");
