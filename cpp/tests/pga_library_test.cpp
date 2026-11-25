#include "pga/interval.hpp"
#include <chrono>
#include <iostream>
#include <string>
#include <vector>

using pga::library::u64;
using namespace pga::library;
bool prime(u64 x) {
    if(x<2) return false;
    for(u64 p=2;p<=x/p;++p) if(x%p==0) return false;
    return true;
}
void require(bool ok) { if(!ok) throw std::runtime_error("test failed"); }
int main(int argc,char**) {
    if(argc==1) {
        for(u64 n=1;n<=1000;++n) {
            std::vector<u64> expected;
            for(u64 r=1;r<=2*n;++r) if(prime(n*n+r)) expected.push_back(n*n+r);
            for(std::size_t b:{1U,17U,1024U,65536U}) {
                std::vector<u64> actual;
                const auto a=enumerate(n,[&](u64 p){actual.push_back(p);},b);
                require(actual==expected && a.primes==expected.size());
                require(a.rough==a.edges+a.primes && a.candidates==2*n);
                require(baseline_count(n,b)==a.primes);
            }
        }
        bool bad=false;
        try { count(0); } catch(const std::invalid_argument&) { bad=true; }
        require(bad);
        bad=false;
        try { count(1,0); } catch(const std::invalid_argument&) { bad=true; }
        require(bad);
        bad=false;
        try { count(4294967296ULL); } catch(const std::overflow_error&) { bad=true; }
        require(bad);
        std::cout<<"4000 interval/block cases and 3 invalid-input cases passed\n";
        return 0;
    }
    std::cout<<"n,block,repeat,algorithm,count,microseconds\n";
    for(u64 n:{1000ULL,10000ULL,100000ULL,1000000ULL})
        for(std::size_t b:{4096U,65536U})
            for(int rep=0;rep<5;++rep) {
                const auto expected=baseline_count(n,b);
                for(int j=0;j<2;++j) {
                    const bool graph=(j+rep)%2==0;
                    const auto start=std::chrono::steady_clock::now();
                    const auto observed=graph?count(n,b).primes:baseline_count(n,b);
                    const auto end=std::chrono::steady_clock::now();
                    require(observed==expected);
                    std::cout<<n<<','<<b<<','<<rep<<','<<(graph?"pga":"baseline")
                        <<','<<observed<<','<<std::chrono::duration_cast<std::chrono::microseconds>(end-start).count()<<'\n';
                }
            }
}
