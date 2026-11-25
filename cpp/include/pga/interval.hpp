#pragma once
#include <algorithm>
#include <cstddef>
#include <cstdint>
#include <limits>
#include <stdexcept>
#include <vector>

namespace pga::library {
using u64 = std::uint64_t;
struct Result {
    u64 candidates{}, rough{}, edges{}, primes{};
};

inline u64 cube_root(u64 x) {
    u64 lo=0, hi=u64{1}<<22;
    while (hi-lo>1) {
        const u64 m=lo+(hi-lo)/2;
        if (m<=x/m/m) lo=m; else hi=m;
    }
    return lo;
}
inline std::vector<u64> base_primes(u64 n) {
    std::vector<bool> flags(static_cast<std::size_t>(n+1),true);
    flags[0]=false; flags[1]=false;
    for (u64 p=2;p<=n/p;++p)
        if (flags[static_cast<std::size_t>(p)])
            for (u64 j=p*p;j<=n;j+=p) flags[static_cast<std::size_t>(j)]=false;
    std::vector<u64> out;
    for (u64 p=2;p<=n;++p)
        if (flags[static_cast<std::size_t>(p)]) out.push_back(p);
    return out;
}
inline void validate(u64 n, std::size_t block) {
    if (!n || !block) throw std::invalid_argument("positive n and block required");
    if (n>4294967295ULL || n>=std::numeric_limits<std::size_t>::max())
        throw std::overflow_error("interval or base sieve exceeds integer range");
}

// ESTABLISHED: after the cube-root cutoff every surviving composite is pq
// with p<q, p<=n<q. Consequently each residual candidate has one edge.
template<bool Graph, class Emit>
Result scan(u64 n, std::size_t block, Emit emit) {
    validate(n,block);
    const u64 lower=n*n, width=2*n;
    const u64 cutoff=cube_root(lower+width);
    const auto primes=base_primes(n);
    Result result{width,0,0,0};
    std::vector<std::uint8_t> state;
    for (u64 done=0;done<width;) {
        const u64 len=std::min(width-done,static_cast<u64>(block));
        state.assign(static_cast<std::size_t>(len),1);
        const u64 before=lower+done;
        for (u64 p:primes) {
            for (u64 r=p-before%p;r<=len;r+=p) {
                auto& s=state[static_cast<std::size_t>(r-1)];
                if constexpr (Graph) {
                    if (p<=cutoff) s=0;
                    else if (s==1) s=2;
                    else if (s==2) throw std::logic_error("duplicate residual edge");
                } else s=0;
            }
        }
        for (u64 i=0;i<len;++i) {
            const auto s=state[static_cast<std::size_t>(i)];
            if (s==1) { ++result.primes; emit(before+i+1); }
            if constexpr (Graph) {
                if (s!=0) ++result.rough;
                if (s==2) ++result.edges;
            }
        }
        done+=len;
    }
    if constexpr (Graph) {
        if (result.rough-result.edges!=result.primes)
            throw std::logic_error("graph identity failed");
    }
    return result;
}
inline Result count(u64 n,std::size_t block=65536) {
    return scan<true>(n,block,[](u64){});
}
inline u64 baseline_count(u64 n,std::size_t block=65536) {
    return scan<false>(n,block,[](u64){}).primes;
}
template<class Emit>
Result enumerate(u64 n,Emit emit,std::size_t block=65536) {
    return scan<true>(n,block,emit);
}
} // namespace pga::library
