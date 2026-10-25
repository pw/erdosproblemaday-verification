// Does the periodic split-prime sieve A(P) = {z in Z[i] : z != 0 mod pi_p, z != 0 mod conj(pi_p), p in P}
// contain an infinite self-avoiding walk with steps |v|^2 <= R2 ?  (Erdős #952 / OpenAI family 28, Theorem 1.2 in miniature)
// Method: union-find with lift offsets on the torus (Z/Q)^2, Q = prod P. A cycle on the torus whose lift displacement is a
// nonzero vector of (QZ)^2 exists iff the periodic graph has an infinite component (then it contains an infinite simple path).
// Output: INFINITE (with the first nonzero cycle displacement) or FINITE (+ the largest component size on the torus = the
// largest component of the lift, since a component with no nonzero cycle injects into the torus).
// usage: sieve_perc R2 p1 p2 ...
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static int32_t *par; static int64_t *ox, *oy; static int32_t *sz;
static int32_t find(int32_t u, int64_t *dx, int64_t *dy){ // returns root, and lift(u) = lift(root) + (dx,dy)
  int64_t ax=0, ay=0; int32_t r=u;
  while(par[r]!=r){ ax+=ox[r]; ay+=oy[r]; r=par[r]; }
  // path compression
  int64_t cx=ax, cy=ay; int32_t v=u;
  while(par[v]!=v){ int32_t nx=par[v]; int64_t tx=ox[v], ty=oy[v]; par[v]=r; ox[v]=cx; oy[v]=cy; cx-=tx; cy-=ty; v=nx; }
  *dx=ax; *dy=ay; return r;
}
int main(int argc,char**argv){
  if(argc<3){fprintf(stderr,"usage\n");return 2;}
  int R2=atoi(argv[1]); int np=argc-2; int64_t Q=1; int64_t P[16], rt[16];
  for(int k=0;k<np;k++){ P[k]=atoll(argv[k+2]); if(P[k]%4!=1){fprintf(stderr,"p must be 1 mod 4\n");return 2;} Q*=P[k];
    int64_t r=-1; for(int64_t x=1;x<P[k];x++) if((x*x+1)%P[k]==0){r=x;break;} rt[k]=r; }
  if(Q*Q>400000000LL){fprintf(stderr,"too big\n");return 2;}
  int64_t N=Q*Q;
  uint8_t *in=malloc(N); par=malloc(N*4); ox=malloc(N*8); oy=malloc(N*8); sz=malloc(N*4);
  if(!in||!par||!ox||!oy||!sz){fprintf(stderr,"oom\n");return 2;}
  int64_t cnt=0;
  for(int64_t x=0;x<Q;x++) for(int64_t y=0;y<Q;y++){ int ok=1;
    for(int k=0;k<np&&ok;k++){ int64_t p=P[k]; int64_t a=(x+y*rt[k])%p, b=((x-y*rt[k])%p+p)%p; if(a==0||b==0) ok=0; }
    int64_t id=x*Q+y; in[id]=ok; par[id]=(int32_t)id; ox[id]=oy[id]=0; sz[id]=1; cnt+=ok; }
  // steps: half of the nonzero vectors with |v|^2<=R2 (lexicographically positive), edges are undirected
  int st[1000][2], ns=0; int Rm=1; while(Rm*Rm<=R2) Rm++;
  for(int dx=-Rm;dx<=Rm;dx++) for(int dy=-Rm;dy<=Rm;dy++){ if(dx*dx+dy*dy==0||dx*dx+dy*dy>R2) continue; if(dx>0||(dx==0&&dy>0)){st[ns][0]=dx;st[ns][1]=dy;ns++;} }
  int infinite=0; int64_t cyx=0,cyy=0;
  for(int64_t x=0;x<Q&&!infinite;x++) for(int64_t y=0;y<Q&&!infinite;y++){ int64_t u=x*Q+y; if(!in[u]) continue;
    for(int s=0;s<ns;s++){ int64_t X=x+st[s][0], Y=y+st[s][1]; int64_t wx=((X%Q)+Q)%Q, wy=((Y%Q)+Q)%Q; int64_t v=wx*Q+wy; if(!in[v]) continue;
      // lift: lift(v_neighbor) = lift(u) + step ; v sits at torus cell (wx,wy) whose canonical lift is (wx,wy); the neighbour's actual lift is (X,Y)
      // We track lift positions relative to canonical cell coordinates: define L(node) = canonical coords. Edge says (X,Y) - (x,y) = step,
      // i.e. canonical(v) + (X-wx, Y-wy) - canonical(u) = step. Offset relation between roots via canonical coordinates:
      int64_t du,dvv, eu,ev; int32_t ru=find((int32_t)u,&du,&eu), rv=find((int32_t)v,&dvv,&ev);
      // position(u) = position(ru) + (du,eu); position(v-copy) = position(rv) + (dvv,ev) + (X-wx, Y-wy)... treat copy shift k = (X-wx,Y-wy)
      // relation: pos(v) = pos(u) + step - k  (with pos = canonical lift chosen per component)
      // we store offsets as differences of "pos"; for the same root a contradiction = nonzero multiple of Q
      int64_t kx=X-wx, ky=Y-wy; // multiples of Q (0 or ±Q)
      // want pos(v) - pos(u) = (wx - x, wy - y) + ... ; in lift coords: lift(v) = lift(u) + step means v's lift sits k off its canonical cell
      // define pos(node) = lift of node in the component's lifted copy; then pos(v) = pos(u) + step. canonical difference = step - k.
      int64_t gx=kx, gy=ky; // copy shift along this edge: K(v) = K(u) + (kx,ky)
      // gx,gy are multiples of Q: the copy index shift between u's canonical cell and v's canonical cell along this edge
      if(ru==rv){ int64_t cx=du+gx-dvv, cy=eu+gy-ev; if(cx||cy){ infinite=1; cyx=cx; cyy=cy; break; } }
      else { if(sz[ru]<sz[rv]){ par[ru]=rv; ox[ru]=dvv-gx-du; oy[ru]=ev-gy-eu; sz[rv]+=sz[ru]; }
             else { par[rv]=ru; ox[rv]=du+gx-dvv; oy[rv]=eu+gy-ev; sz[ru]+=sz[rv]; } }
    }
  }
  int64_t big=0; if(!infinite) for(int64_t u=0;u<N;u++) if(in[u]&&par[u]==u&&sz[u]>big) big=sz[u];
  printf("R2=%d P=",R2); for(int k=0;k<np;k++) printf("%s%lld",k?",":"",(long long)P[k]);
  printf(" Q=%lld density=%.4f steps=%d ", (long long)Q, (double)cnt/N, 2*ns);
  if(infinite) printf("INFINITE cycle_shift=(%lld,%lld)\n",(long long)cyx,(long long)cyy); else printf("FINITE max_component=%lld\n",(long long)big);
  return 0;
}
