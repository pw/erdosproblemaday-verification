/* Referee checker D: ONE-DEFECT census, ascending order a1<...<ak.
   For each k-set A of distinct positive integers with all subset sums <= N, and colour c,
   if every subset sum except those equal to one value p has colour c (and p has colour 1-c),
   then flipping p would make A monochromatic. Tallies defect[p]. Also tallies true mono sets (no defect).
   usage: chkD FILE K OUTFILE [example_pos]   -> OUTFILE lines "p count" for p with count>0 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int N,K,expos; static unsigned char col[1<<16]; static long long defect[1<<16], mono;
static int sums[16][1<<12]; static int setv[16]; static int printed;
static void rec(int j,int last,int c,int p){
  int ns=1<<j, total=sums[j][ns-1];
  if(j==K){ if(p==0) mono++; else { defect[p]++; if(p==expos && printed<3){ printed++; printf("EXAMPLE defect p=%d colour-after-flip %d:",p,c); for(int t=0;t<K;t++) printf(" %d",setv[t]); printf("\n"); } } return; }
  for(int x=last+1; x+total<=N; x++){
    int q=p, ok=1;
    for(int t=0;t<ns;t++){ int v=sums[j][t]+x; if(col[v]!=c){ if(q==0) q=v; else if(v!=q){ok=0;break;} } }
    if(!ok) continue;
    for(int t=0;t<ns;t++){ sums[j+1][t]=sums[j][t]; sums[j+1][t+ns]=sums[j][t]+x; }
    setv[j]=x; rec(j+1,x,c,q);
  }
}
int main(int argc,char**argv){
  FILE*f=fopen(argv[1],"rb"); static char buf[1<<17]; size_t n=fread(buf,1,sizeof buf,f); fclose(f);
  size_t L=0; while(L<n&&buf[L]!='\n'&&buf[L]!='\r') L++;
  for(size_t i=0;i<L;i++){ if(buf[i]!='0'&&buf[i]!='1') return 2; col[i+1]=buf[i]-'0'; }
  N=(int)L; K=atoi(argv[2]); expos = argc>4?atoi(argv[4]):-1;
  sums[0][0]=0;
  for(int c=0;c<2;c++) rec(0,0,c,0);
  FILE*o=fopen(argv[3],"w"); long long tot=0; int np=0;
  for(int p=1;p<=N;p++) if(defect[p]){ fprintf(o,"%d %lld\n",p,defect[p]); tot+=defect[p]; np++; }
  fclose(o);
  printf("N=%d K=%d mono=%lld one_defect_sets=%lld positions_with_defect=%d (of %d)\n",N,K,mono,tot,np,N);
  return 0;
}
