#include <array>
#include <cstdint>
#include <iostream>
#include <vector>
using namespace std;

int main() {
  constexpr int n = 7, U = 1 << n;
  array<bool,U> red{};
  for (int a=0;a<U;++a) {
    int r=__builtin_popcount((unsigned)a);
    red[a]=(r==0||r==2||r==3||r==5);
  }
  uint64_t totals[2]={}, surviving[2]={};
  for (int want=0;want<2;++want) {
    vector<int> v;
    for(int a=0;a<U;++a) if(red[a]==bool(want)) v.push_back(a);
    for(int i=0;i<(int)v.size();++i)
    for(int j=i+1;j<(int)v.size();++j)
    for(int k=j+1;k<(int)v.size();++k)
    for(int l=k+1;l<(int)v.size();++l)
    for(int m=l+1;m<(int)v.size();++m) {
      ++totals[want]; vector<int> a={v[i],v[j],v[k],v[l],v[m]}; bool ok=true;
      array<bool,U> in{}; for(int q:a) in[q]=true;
      for(size_t x=0;x<a.size()&&ok;++x) for(size_t y=0;y<a.size()&&ok;++y) {
        for(int q:{a[x]|a[y],a[x]&a[y]}) {
          if(red[q]!=bool(want)){ok=false;break;}
          if(!in[q]){in[q]=true;a.push_back(q);}
        }
      }
      surviving[want]+=ok;
    }
  }
  cout << "blue five-seeds " << totals[0] << " monochromatic closures " << surviving[0] << "\n";
  cout << "red five-seeds " << totals[1] << " monochromatic closures " << surviving[1] << "\n";
  if(surviving[0]||surviving[1]) return 1;
  cout << "DIRECT FIVE-SEED CLOSURE AUDIT PASS\n";
}
