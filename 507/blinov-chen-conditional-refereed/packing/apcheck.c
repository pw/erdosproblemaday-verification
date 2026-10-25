#include <stdio.h>
#include <stdlib.h>
/* independent checker: bitmap membership; for each z in S and each d>0 test z-d,z+d both in S. exit 1 if any AP. */
int main(int c,char**v){FILE*f=fopen(v[1],"r");if(!f){printf("cannot open\n");return 2;}int x,n=0,mx=0;static int a[100000];while(fscanf(f,"%d",&x)==1){a[n++]=x;if(x>mx)mx=x;}
 unsigned char*b=calloc(mx+1,1);for(int i=0;i<n;i++){if(b[a[i]]){printf("dup %d\n",a[i]);return 1;}b[a[i]]=1;}
 long aps=0;for(int i=0;i<n;i++){int z=a[i];for(int d=1;z-d>=0&&z+d<=mx;d++) if(b[z-d]&&b[z+d]) aps++;}
 printf("n=%d max=%d APs=%ld\n",n,mx,aps);return aps?1:0;}
