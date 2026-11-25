#include "pga/batch.hpp"
#include <chrono>
#include <iostream>
using namespace pga::library;
void require(bool ok) { if (!ok) throw std::runtime_error("batch test failed"); }
bool equal(const Result& a,const Result& b) {
    return a.candidates==b.candidates && a.rough==b.rough && a.edges==b.edges && a.primes==b.primes;
}
int main(int argc,char**) {
    if (argc==1) {
        std::vector<u64> inputs{1000,1,10,1000,3};
        for (u64 n=2;n<=256;++n) inputs.push_back(n);
        for (std::size_t w:{1U,2U,4U,8U}) {
            const auto results=count_batch(inputs,w,127);
            require(results.size()==inputs.size());
            for (std::size_t i=0;i<inputs.size();++i) require(equal(results[i],count(inputs[i],127)));
        }
        require(count_batch({},4).empty());
        for (int i=0;i<3;++i) {
            bool rejected=false;
            try { (void)count_batch(i==0?std::vector<u64>{0}:std::vector<u64>{1},i==1?0:2,i==2?0:127); }
            catch (const std::invalid_argument&) { rejected=true; }
            require(rejected);
        }
        std::cout<<"1040 ordered result comparisons, empty input and 3 invalid cases passed\n";
        return 0;
    }
    std::vector<u64> inputs;
    for (u64 n=200000;n<216000;n+=1000) inputs.push_back(n);
    const auto expected=count_batch(inputs,1);
    std::cout<<"workers,repeat,intervals,microseconds\n";
    for (int rep=0;rep<5;++rep) {
        for (int j=0;j<3;++j) {
            const std::size_t w=std::size_t{1}<<((j+rep)%3);
            const auto start=std::chrono::steady_clock::now();
            const auto results=count_batch(inputs,w);
            const auto end=std::chrono::steady_clock::now();
            require(results.size()==expected.size());
            for (std::size_t i=0;i<results.size();++i) require(equal(results[i],expected[i]));
            std::cout<<w<<','<<rep<<','<<inputs.size()<<','<<std::chrono::duration_cast<std::chrono::microseconds>(end-start).count()<<'\n';
        }
    }
}
