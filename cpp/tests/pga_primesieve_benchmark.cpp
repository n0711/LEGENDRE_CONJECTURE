#include "pga/interval.hpp"
#include <primesieve.hpp>
#include <chrono>
#include <iostream>
using namespace pga::library;

int main() {
    primesieve::set_num_threads(1);
    std::cout<<"n,repeat,algorithm,count,microseconds\n";
    for (u64 n:{1ULL,10ULL,1000ULL,10000ULL,100000ULL,1000000ULL}) {
        const auto expected=primesieve::count_primes(n*n+1,n*n+2*n);
        for (int rep=0;rep<5;++rep) {
            for (int j=0;j<3;++j) {
                const int mode=(j+rep)%3;
                const auto start=std::chrono::steady_clock::now();
                const auto observed=mode==0?count(n).primes:mode==1?baseline_count(n):
                    primesieve::count_primes(n*n+1,n*n+2*n);
                const auto end=std::chrono::steady_clock::now();
                if (observed!=expected) throw std::runtime_error("prime-count mismatch");
                std::cout<<n<<','<<rep<<','<<(mode==0?"pga":mode==1?"baseline":"primesieve")
                    <<','<<observed<<','<<std::chrono::duration_cast<std::chrono::microseconds>(end-start).count()<<'\n';
            }
        }
    }
}
