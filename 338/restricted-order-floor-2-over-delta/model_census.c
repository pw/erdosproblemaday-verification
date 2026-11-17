/* Model census for Theorem D (Erdos #338 follow-up a). Periodic-plus-sparse model mod m:
   D = classes where A has every large element (density |D|/m), E = classes holding infinitely many but
   very sparse members (usable any number of times, but a large n needs at least one D summand).
   True restricted order of the model: h(D,E) = min h >= 1 with D + (h-1)(D u E u {0}) = Z/m.
   Report max of h vs. Theorem D's bound ceil(2m/|D|)-1 and vs. the lower-bound shape floor(2m/|D|)-1.
   Controls: (i) bound-1 must be violated (the {0,1} family is tight); (ii) non-generating D u E must be
   detected as unreachable. */
#include <stdio.h>
#include <stdlib.h>
typedef unsigned int u32;
static int m;
static u32 rot(u32 x,int k){ u32 M=(1u<<m)-1; k%=m; if(!k) return x; return ((x<<k)|(x>>(m-k)))&M; }
static u32 sumset(u32 Z,u32 S){ u32 r=0; for(int k=0;k<m;k++) if(S>>k&1) r|=rot(Z,k); return r; }
int main(int argc,char**argv){
  int MMAX=argc>1?atoi(argv[1]):13;
  for(m=2;m<=MMAX;m++){
    u32 full=(1u<<m)-1; long long pairs=0,over_ceil=0,over_floor=0,unreach=0,tight_ceil=0,ctrl_minus1=0;
    int worst_gap=-99; u32 wD=0,wE=0; int wh=0;
    for(u32 D=1;D<=full;D++){
      int d=__builtin_popcount(D); if(2*d>m) continue;            /* density <= 1/2 */
      int ceilb=(2*m+d-1)/d-1, floorb=(2*m)/d-1;
      u32 rest=full&~D;
      for(u32 E=rest;;E=(E-1)&rest){                            /* all subsets E of the complement */
        u32 S=D|E|1u, Z=D; int h=1;
        while(Z!=full && h<=2*m+2){ u32 Z2=sumset(Z,S); if(Z2==Z){h=999;break;} Z=Z2; h++; }
        if(Z!=full) h=999;
        if(h==999){ unreach++; }
        else {
          pairs++;
          if(h>ceilb) over_ceil++;
          if(h==ceilb) tight_ceil++;
          if(h>ceilb-1) ctrl_minus1++;
          if(h>floorb) over_floor++;
          if(h-floorb>worst_gap){worst_gap=h-floorb;wD=D;wE=E;wh=h;}
        }
        if(E==0) break;
      }
    }
    printf("m=%2d sets=%lld  over_ceil_bound=%lld  hits_ceil_bound=%lld  over_floor_shape=%lld  max(h-floor)=%d [D=0x%x E=0x%x h=%d]  | ctrl: over(ceil-1)=%lld unreachable(non-generating)=%lld\n",
      m,pairs,over_ceil,tight_ceil,over_floor,worst_gap,wD,wE,wh,ctrl_minus1,unreach);
    fflush(stdout);
  }
  return 0;
}
