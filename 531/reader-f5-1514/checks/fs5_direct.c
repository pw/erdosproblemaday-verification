/* fs5_direct.c -- second Erdos #531 checker (ours, 2026-10-29), structurally different from fs_grow.c:
   plain nested loops a<b<c<d<e over a byte array col[], no bitsets.  At each depth the NEW subset sums (those
   containing the newest element) are listed explicitly and tested against the colour of a; a set is counted
   iff all 2^5-1 nonempty subset sums have a's colour.  Sum bound: e runs only while a+b+c+d+e <= N.
   Also counts ELIGIBLE 5-sets (sum <= N) when invoked with "count" (no colour test), for the DP cross-check.
   Usage: fs5_direct FILE [N] [count]   Exit 0 iff no monochromatic 5-set. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXN 8192
static unsigned char col[MAXN+2];
int main(int argc,char**argv){
  if(argc<2) return 2;
  FILE*f=fopen(argv[1],"rb"); if(!f) return 2;
  int n=0,ch; while((ch=fgetc(f))!=EOF){ if(ch=='0'||ch=='1') col[++n]=ch-'0'; else if(ch!='\n'&&ch!='\r'){fprintf(stderr,"bad char\n");return 2;} }
  int N = argc>2? atoi(argv[2]) : n; if(N<1||N>n) return 2;
  int countonly = argc>3 && !strcmp(argv[3],"count");
  long long mono[2]={0,0}, elig=0; int exA[5]={0};
  for(int a=1;a<=N;a++){ int k=col[a];
   for(int b=a+1;a+b<=N;b++){
    if(!countonly && (col[b]!=k || col[a+b]!=k)) continue;
    for(int c=b+1;a+b+c<=N;c++){
     if(!countonly){ int s3[4]={c,a+c,b+c,a+b+c}; int ok=1; for(int t=0;t<4;t++) if(col[s3[t]]!=k){ok=0;break;} if(!ok) continue; }
     for(int d=c+1;a+b+c+d<=N;d++){
      if(!countonly){ int p[3]={a,b,c}; int ok=1;
        for(int m=0;m<8&&ok;m++){ int s=d; for(int t=0;t<3;t++) if(m>>t&1) s+=p[t]; if(col[s]!=k) ok=0; }
        if(!ok) continue; }
      for(int e=d+1;a+b+c+d+e<=N;e++){
       if(countonly){ elig++; continue; }
       int p[4]={a,b,c,d}; int ok=1;
       for(int m=0;m<16&&ok;m++){ int s=e; for(int t=0;t<4;t++) if(m>>t&1) s+=p[t]; if(col[s]!=k) ok=0; }
       if(ok){ if(!mono[0]&&!mono[1]){exA[0]=a;exA[1]=b;exA[2]=c;exA[3]=d;exA[4]=e;} mono[k]++; }
      }}}}}
  if(countonly){ printf("N=%d eligible5=%lld\n",N,elig); return 0; }
  printf("N=%d mono5 colour0=%lld colour1=%lld",N,mono[0],mono[1]);
  if(mono[0]+mono[1]) printf("  e.g. {%d,%d,%d,%d,%d}",exA[0],exA[1],exA[2],exA[3],exA[4]);
  printf("\n%s\n", mono[0]+mono[1]? "RESULT NOT PROPER":"RESULT PROPER (no monochromatic 5-set)");
  return (mono[0]+mono[1])?1:0;
}
