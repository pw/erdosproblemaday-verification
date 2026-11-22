#include <bits/stdc++.h>
using namespace std;
static bool squarefree(long long n){ if(n<=0) return false; for(long long p=2;p*p<=n;++p) if(n%(p*p)==0) return false; return true; }
int main(int argc,char**argv){
 if(argc!=2){cerr<<"usage: verify_erdos1109_67 witness.txt\n";return 2;}
 ifstream in(argv[1]); int k,N; if(!(in>>k>>N)){cerr<<"bad header\n";return 2;}
 vector<long long>A; long long x; while(in>>x) A.push_back(x);
 if(k!=67||A.size()!=67||A.back()!=N){cerr<<"bad size/max\n";return 1;}
 if(!is_sorted(A.begin(),A.end())||adjacent_find(A.begin(),A.end())!=A.end()){cerr<<"not strictly sorted\n";return 1;}
 for(long long a:A) if(a<1||a>N||(a%2)==0||!squarefree(a)||!squarefree(2*a)){cerr<<"bad vertex "<<a<<"\n";return 1;}
 long long c=0;
 for(int i=0;i<67;i++) for(int j=i;j<67;j++){++c; long long s=A[i]+A[j]; if(!squarefree(s)){cerr<<"bad sum "<<A[i]<<"+"<<A[j]<<"="<<s<<"\n";return 1;}}
 cout<<"PASS N="<<N<<" |A|="<<A.size()<<" checked_sums="<<c<<"\n";
 cout<<"A=";for(auto a:A)cout<<a<<' ';cout<<'\n';
}
