c=0; for(n=1,100000, if(issquarefree(n^4+1), c++)); print("x^4+1 n<=1e5 sqfree: ", c);
c=0; for(n=1,100000, if(issquarefree(n^4+2), c++)); print("x^4+2 n<=1e5 sqfree: ", c);
quit;
