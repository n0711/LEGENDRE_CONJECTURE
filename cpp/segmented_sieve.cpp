#include <algorithm>
#include <cmath>
#include <cstddef>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

// ESTABLISHED: Eratosthenes marking; finite outputs are NUMERICAL evidence.
std::vector<unsigned long long> segmented_sieve(unsigned long long limit,
                                                unsigned long long block_size = 1 << 16) {
    if (block_size == 0) throw std::invalid_argument("block_size must be positive");
    if (limit < 2) return {};
    auto small_limit = static_cast<unsigned long long>(std::sqrt(static_cast<long double>(limit)));
    while (small_limit > limit / small_limit) --small_limit;
    while (small_limit + 1 <= limit / (small_limit + 1)) ++small_limit;
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
    for (unsigned long long lo = 2; lo <= limit;) {
        const unsigned long long hi = lo + std::min(block_size - 1, limit - lo);
        std::vector<bool> block(hi - lo + 1, true);
        for (unsigned long long p : base) {
            const auto delta = (p - lo % p) % p;
            if (delta > hi - lo) continue;
            const auto first = std::max(p * p, lo + delta);
            if (first > hi) continue;
            for (unsigned long long m = first;;) {
                block[m - lo] = false;
                if (hi - m < p) break;
                m += p;
            }
        }
        for (unsigned long long i = 0; i < block.size(); ++i) {
            if (block[i]) primes.push_back(lo + i);
        }
        if (hi == limit) break;
        lo = hi + 1;
    }
    return primes;
}

int main(int argc, char** argv) {
    try {
        auto parse = [](const std::string& s) {
            if (s.empty() || s.find_first_not_of("0123456789") != std::string::npos)
                throw std::invalid_argument("arguments must be nonnegative integers");
            return std::stoull(s);
        };
        const auto limit = argc > 1 ? parse(argv[1]) : 1000000ULL;
        const auto block_size = argc > 2 ? parse(argv[2]) : (1ULL << 16);
        auto primes = segmented_sieve(limit, block_size);
        std::cout << primes.size() << '\n';
    } catch (const std::exception& e) {
        std::cerr << e.what() << '\n';
        return 1;
    }
}
