#include <algorithm>
#include <cmath>
#include <cstddef>
#include <iostream>
#include <vector>

std::vector<unsigned long long> segmented_sieve(unsigned long long limit,
                                                unsigned long long block_size = 1 << 16) {
    if (limit < 2) return {};
    const auto small_limit = static_cast<unsigned long long>(std::sqrt(static_cast<long double>(limit)));
    std::vector<bool> small(small_limit + 1, true);
    small[0] = small[1] = false;
    for (unsigned long long p = 2; p * p <= small_limit; ++p) {
        if (small[p]) {
            for (unsigned long long m = p * p; m <= small_limit; m += p) small[m] = false;
        }
    }
    std::vector<unsigned long long> base;
    for (unsigned long long i = 2; i <= small_limit; ++i) if (small[i]) base.push_back(i);

    std::vector<unsigned long long> primes;
    for (unsigned long long lo = 2; lo <= limit; lo += block_size) {
        const unsigned long long hi = std::min(limit, lo + block_size - 1);
        std::vector<bool> block(hi - lo + 1, true);
        for (unsigned long long p : base) {
            unsigned long long first = std::max(p * p, ((lo + p - 1) / p) * p);
            if (first > hi) continue;
            for (unsigned long long m = first; m <= hi; m += p) block[m - lo] = false;
        }
        for (unsigned long long i = 0; i < block.size(); ++i) {
            if (block[i]) primes.push_back(lo + i);
        }
    }
    return primes;
}

int main(int argc, char** argv) {
    unsigned long long limit = argc > 1 ? std::stoull(argv[1]) : 1000000;
    auto primes = segmented_sieve(limit);
    std::cout << primes.size() << '\n';
}
