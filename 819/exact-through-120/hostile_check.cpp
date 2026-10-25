#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <tuple>
#include <vector>

struct Result {
    bool exists = false;
    std::uint64_t nodes = 0;
    std::uint64_t leaves = 0;
    std::vector<int> witness;
};

static int collision_excess(const std::vector<int>& a) {
    std::map<int,int> r;
    for (std::size_t i=0;i<a.size();++i)
        for (std::size_t j=i;j<a.size();++j) ++r[a[i]+a[j]];
    int excess=0;
    for (const auto& [sum,count]:r) { (void)sum; excess += count-1; }
    return excess;
}

static int score(int n,const std::vector<int>&a) {
    std::map<int,int> r;
    for(std::size_t i=0;i<a.size();++i)
        for(std::size_t j=i;j<a.size();++j)
            if(a[i]+a[j]<=n)++r[a[i]+a[j]];
    return static_cast<int>(r.size());
}

// Independent implementation: mutable representation counts, rather than
// the producer's immutable integer bit masks.
static Result search_at_most(int k,int length,int budget) {
    Result out;
    std::vector<int> marks{0};
    std::array<unsigned char,256> reps{};
    reps[0]=1;

    auto visit = [&](auto&& self,int start,int defects)->bool {
        ++out.nodes;
        if(static_cast<int>(marks.size())==k){
            ++out.leaves;out.exists=true;out.witness=marks;return true;
        }
        int after=k-static_cast<int>(marks.size())-1;
        for(int x=start;x<=length-after;++x){
            std::array<int,32> sums{};
            int count=0,hits=0;
            for(int old:marks){sums[count++]=x+old;}
            sums[count++]=2*x;
            for(int i=0;i<count;++i){
                for(int j=0;j<i;++j)
                    if(sums[i]==sums[j]) throw std::runtime_error("new sums collided");
                if(reps[sums[i]]!=0)++hits;
            }
            if(defects+hits>budget)continue;
            for(int i=0;i<count;++i)++reps[sums[i]];
            marks.push_back(x);
            if(self(self,x+1,defects+hits))return true;
            marks.pop_back();
            for(int i=0;i<count;++i)--reps[sums[i]];
        }
        return false;
    };
    visit(visit,1,0);
    if(out.exists && collision_excess(out.witness)>budget)
        throw std::runtime_error("bad search witness");
    return out;
}

static Result search_fixed_last(int k,int last,int prefix_bound) {
    Result out;
    std::vector<int> marks{0};
    std::array<unsigned char,256> reps{};
    reps[0]=1;

    auto visit = [&](auto&& self,int start)->bool {
        ++out.nodes;
        if(static_cast<int>(marks.size())==k-1){
            ++out.leaves;
            for(int old:marks)if(reps[last+old])return false;
            if(reps[2*last])return false;
            out.exists=true;out.witness=marks;out.witness.push_back(last);return true;
        }
        int after=(k-1)-static_cast<int>(marks.size())-1;
        for(int x=start;x<=prefix_bound-after;++x){
            std::array<int,32>sums{};int count=0;bool ok=true;
            for(int old:marks)sums[count++]=x+old;
            sums[count++]=2*x;
            for(int i=0;i<count;++i)if(reps[sums[i]]){ok=false;break;}
            if(!ok)continue;
            for(int i=0;i<count;++i)++reps[sums[i]];
            marks.push_back(x);
            if(self(self,x+1))return true;
            marks.pop_back();
            for(int i=0;i<count;++i)--reps[sums[i]];
        }
        return false;
    };
    visit(visit,1);
    if(out.exists && collision_excess(out.witness)!=0)
        throw std::runtime_error("bad fixed-last witness");
    return out;
}

static void expect(bool condition,const std::string&message){
    if(!condition)throw std::runtime_error(message);
}

static void print_result(const std::string&name,const Result&r){
    std::cout<<name<<" exists="<<(r.exists?1:0)<<" nodes="<<r.nodes
             <<" leaves="<<r.leaves;
    if(r.exists){std::cout<<" witness=";for(int x:r.witness)std::cout<<x<<',';}
    std::cout<<'\n';
}

int main(){
    const std::vector<std::tuple<std::string,int,int,int,bool>> cases={
        {"g0_8_lower",8,33,0,false},{"g0_8_upper",8,34,0,true},
        {"g0_9_lower",9,43,0,false},{"g0_9_upper",9,44,0,true},
        {"g1_9_lower",9,39,1,false},{"g1_9_upper",9,40,1,true},
        {"g0_10_lower",10,54,0,false},{"g0_10_upper",10,55,0,true},
        {"g1_10_lower",10,49,1,false},{"g1_10_upper",10,50,1,true},
    };
    for(const auto& [name,k,length,budget,want]:cases){
        Result r=search_at_most(k,length,budget);
        expect(r.exists==want,"existence mismatch: "+name);
        print_result(name,r);
    }
    const std::vector<std::tuple<std::string,int,int,int>> overflow={
        {"n81_L44",9,44,35},{"n81_L45",9,45,34},{"n101_L55",10,55,44},
    };
    for(const auto& [name,k,last,bound]:overflow){
        Result r=search_fixed_last(k,last,bound);
        expect(!r.exists,"overflow survivor: "+name);
        print_result(name,r);
    }

    const std::map<std::string,std::vector<int>> normalized={
        {"k9_defect2",{0,1,4,9,12,13,19,33,35}},
        {"k9_defect1",{0,1,3,10,21,26,34,38,40}},
        {"k9_sidon",{0,1,5,12,25,27,35,41,44}},
        {"k10_defect2",{0,1,7,11,27,29,32,41,44,46}},
        {"k10_defect1",{0,1,4,12,18,28,41,43,48,50}},
        {"k10_sidon",{0,1,6,10,23,26,34,41,53,55}},
    };
    const std::map<std::string,int> defects={
        {"k9_defect2",2},{"k9_defect1",1},{"k9_sidon",0},
        {"k10_defect2",2},{"k10_defect1",1},{"k10_sidon",0},
    };
    for(const auto& [name,a]:normalized)
        expect(collision_excess(a)==defects.at(name),"witness defect mismatch");

    std::vector<int> table;
    for(int n=81;n<=120;++n){
        std::string name;int want;
        if(n==81){name="k9_defect2";want=43;}
        else if(n<=89){name="k9_defect1";want=44;}
        else if(n<=99){name="k9_sidon";want=45;}
        else if(n<=101){name="k10_defect2";want=53;}
        else if(n<=111){name="k10_defect1";want=54;}
        else{name="k10_sidon";want=55;}
        std::vector<int>a=normalized.at(name);
        for(int&x:a)++x;
        expect(static_cast<int>(a.size())==static_cast<int>(std::sqrt(n)),"size failure");
        expect(score(n,a)==want,"score failure at N="+std::to_string(n));
        table.push_back(want);
    }
    std::cout<<"table=";for(int x:table)std::cout<<x<<',';std::cout<<'\n';
    std::cout<<"ALL HOSTILE CHECKS PASSED\n";
}
