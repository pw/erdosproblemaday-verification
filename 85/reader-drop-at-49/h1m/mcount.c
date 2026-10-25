/* Independent count of H1 miss matrices (control for menum.py): row-by-row recursion over columns in DESCENDING order,
   no symmetry, Lemma D checked only at complete matrices. Prints the count per case j. */
#include <stdio.h>
static int M[8][8], R[8], rem[8];
static long cnt;
static int ok_D(void){
  for(int X=0;X<8;X++) for(int Y=0;Y<8;Y++){
    if(X==Y || Y==(X^1)) continue;
    if(M[X^1][Y] + M[X][Y^1] > 5) return 0;
  }
  return 1;
}
static void rec(int X, int Y){          /* fill entry (X,Y) for Y from 7 down to X+1 */
  if(X==8){ for(int i=0;i<8;i++) if(rem[i]) return; if(ok_D()) cnt++; return; }
  if(Y<=X){ if(rem[X]) return; rec(X+1, 7); return; }
  if(Y==(X^1)){ rec(X, Y-1); return; }
  int mx = rem[X] < rem[Y] ? rem[X] : rem[Y];
  for(int v=0; v<=mx; v++){
    M[X][Y]=M[Y][X]=v; rem[X]-=v; rem[Y]-=v;
    rec(X, Y-1);
    rem[X]+=v; rem[Y]+=v; M[X][Y]=M[Y][X]=0;
  }
}
int main(void){
  for(int j=0;j<=4;j++){
    for(int p=0;p<4;p++){ R[2*p]=4; R[2*p+1]= p<j ? 4 : 2; }
    for(int i=0;i<8;i++) rem[i]=R[i];
    cnt=0; rec(0,7);
    printf("case j=%d matrices=%ld\n", j, cnt);
  }
  return 0;
}
