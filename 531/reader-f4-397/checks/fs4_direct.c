/* fs4_direct.c -- our own checker (Erdos #531, k=4), written 2026-10-22 without reading the submitter's code.
   Reads a 0/1 string (colour of 1..N, other chars ignored).  Enumerates every a<b<c<d with a+b+c+d<=N,
   forms all 15 nonempty subset sums, and counts the sets whose sums are all one colour.
   Usage: fs4_direct FILE [N]   (N defaults to string length; N<len truncates)
   Output: N=<N> eligible=<count> mono=<count> mono0=<..> mono1=<..> ; exit 1 if mono>0, 2 on bad input. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(int argc,char**argv){
  if(argc<2){fprintf(stderr,"usage\n");return 2;}
  FILE*f=fopen(argv[1],"r"); if(!f){perror("open");return 2;}
  static unsigned char col[100000]; long n=0; int ch;
  col[0]=255;
  while((ch=fgetc(f))!=EOF){ if(ch=='0'||ch=='1'){ if(n+1>=100000){fprintf(stderr,"too long\n");return 2;} col[++n]=(unsigned char)(ch-'0'); } else if(ch!='\n'&&ch!='\r'){fprintf(stderr,"bad char %d\n",ch);return 2;} }
  fclose(f);
  long N=n; if(argc>2){ N=atol(argv[2]); if(N>n||N<1){fprintf(stderr,"bad N\n");return 2;} }
  long long elig=0,mono[2]={0,0}; int printed=0;
  for(long a=1;a<=N;a++) for(long b=a+1;a+b<=N;b++) for(long c=b+1;a+b+c<=N;c++) for(long d=c+1;a+b+c+d<=N;d++){
    long g[4]={a,b,c,d}; elig++;
    int seen0=0,seen1=0;
    for(int m=1;m<16;m++){ long s=0; for(int i=0;i<4;i++) if(m>>i&1) s+=g[i];
      if(s<1||s>N){fprintf(stderr,"internal: sum out of range\n");return 2;}
      if(col[s]) seen1=1; else seen0=1; if(seen0&&seen1) break; }
    if(!(seen0&&seen1)){ int cc=seen1?1:0; mono[cc]++; if(printed<3){printf("MONO colour=%d A={%ld,%ld,%ld,%ld}\n",cc,a,b,c,d);printed++;} }
  }
  printf("N=%ld eligible=%lld mono=%lld mono0=%lld mono1=%lld\n",N,elig,mono[0]+mono[1],mono[0],mono[1]);
  return (mono[0]+mono[1])?1:0;
}
