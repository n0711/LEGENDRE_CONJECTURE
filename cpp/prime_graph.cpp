#include <algorithm>
#include <cmath>
#include <cstddef>
#include <cstdint>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <vector>

namespace pga {

using u64 = std::uint64_t;
using usize = std::size_t;

inline u64 cube_root_floor(u64 value) {
    if (value <= 1) return value;
    u64 low = 0;
    u64 high = value < 4 ? value + 1 : 1ULL << 22;
    while (low + 1 < high) {
        u64 middle = low + (high - low) / 2;
        if (middle <= value / middle / middle) low = middle;
        else high = middle;
    }
    return low;
}

double sinc(double value) {
    if (value == 0.0) return 1.0;
    return std::sin(value) / value;
}

double fixed_kernel_weight(double gamma, double h, u64 k) {
    if (k == 0) throw std::invalid_argument("k must be positive");
    if (k > static_cast<u64>(std::numeric_limits<int>::max()))
        throw std::invalid_argument("k exceeds integer exponent range");
    return std::pow(sinc(gamma * h / static_cast<double>(k)), static_cast<int>(k));
}

u64 adaptive_k(u64 n) {
    if (n < 1) throw std::invalid_argument("n must be positive");
    const double log_log = std::log(std::log(static_cast<double>(n + 1)));
    u64 rounded = 1;
    if (std::isfinite(log_log)) {
        rounded = static_cast<u64>(std::ceil(log_log));
    }
    if (rounded < 2) rounded = 2;
    return 2 * rounded;
}

u64 adaptive_cutoff(u64 n) {
    const u64 k = adaptive_k(n);
    if (n > (~u64{0}) / 4 / k) throw std::overflow_error("adaptive cutoff overflow");
    return 4 * k * (n + 1);
}

double fixed_zero_sum(u64 n, const std::vector<double> &ordinates,
                      u64 k, double cutoff) {
    if (n == 0) throw std::invalid_argument("n must be positive");
    const double h = std::log1p(1.0 / static_cast<double>(n));
    const double x = static_cast<double>(n) * static_cast<double>(n + 1);
    double total = 0.0;
    for (double gamma : ordinates) {
        if (!std::isfinite(gamma) || gamma <= 0.0)
            throw std::invalid_argument("ordinates must be positive and finite");
        if (gamma <= cutoff)
            total += 2.0 * std::cos(gamma * std::log(x)) *
                     fixed_kernel_weight(gamma, h, k);
    }
    return total;
}

double adaptive_zero_sum(u64 n, const std::vector<double> &ordinates) {
    const u64 k = adaptive_k(n);
    return fixed_zero_sum(n, ordinates, k,
                          static_cast<double>(adaptive_cutoff(n)));
}

std::vector<u64> sieve(u64 limit) {
    if (limit < 2) return {};
    u64 root = static_cast<u64>(std::sqrt(static_cast<long double>(limit)));
    while (root + 1 <= limit / (root + 1)) ++root;
    while (root > limit / root) --root;
    std::vector<bool> small(root + 1, true);
    small[0] = small[1] = false;
    for (u64 p = 2; p <= root / p; ++p) {
        if (small[p]) {
            for (u64 m = p * p; m <= root; m += p) small[m] = false;
        }
    }
    std::vector<u64> primes;
    for (u64 p = 2; p <= root; ++p) if (small[p]) primes.push_back(p);

    std::vector<bool> block(limit - 1, true);
    for (u64 p : primes) {
        if (p > limit / p) continue;
        u64 start = p * p;
        for (u64 m = start;; m += p) {
            block[m - 2] = false;
            if (m > limit - p) break;
        }
    }
    primes.clear();
    for (u64 m = 2; m <= limit; ++m) if (block[m - 2]) primes.push_back(m);
    return primes;
}

struct Stats {
    u64 n = 0;
    u64 candidates = 0;
    u64 cutoff = 0;
    u64 rough = 0;
    u64 edge_incidence = 0;
    u64 degree_one = 0;
    u64 degree_two = 0;
    u64 degree_three_or_more = 0;
    u64 primes = 0;
};

Stats analyze(u64 n) {
    if (n == 0) throw std::invalid_argument("n must be positive");
    if (n > (~u64{0}) / n) throw std::overflow_error("n*n overflow");
    u64 lower = n * n;
    if (lower > (~u64{0}) - 2 * n) throw std::overflow_error("interval overflow");
    u64 upper = lower + 2 * n;
    u64 cutoff = cube_root_floor(upper);
    while (cutoff > upper / cutoff / cutoff) --cutoff;

    if (2 * n > static_cast<u64>(std::numeric_limits<usize>::max()))
        throw std::overflow_error("candidate interval does not fit address space");
    const auto primes = sieve(n);
    Stats s{n, 2 * n, cutoff, 0, 0, 0, 0, 0, 0};
    std::vector<std::uint8_t> live(static_cast<usize>(2 * n), 1);
    std::vector<std::uint8_t> degree(static_cast<usize>(2 * n), 0);

    for (u64 p : primes) {
        if (p > cutoff) break;
        u64 offset = p - lower % p;
        for (u64 r = offset; r <= 2 * n;) {
            live[static_cast<usize>(r - 1)] = 0;
            if (2 * n - r < p) break;
            r += p;
        }
    }

    for (u64 p : primes) {
        if (p <= cutoff) continue;
        u64 offset = p - lower % p;
        for (u64 r = offset; r <= 2 * n;) {
            const auto index = static_cast<usize>(r - 1);
            if (live[index])
                degree[index] = static_cast<std::uint8_t>(degree[index] + 1U);
            if (2 * n - r < p) break;
            r += p;
        }
    }

    for (usize i = 0; i < live.size(); ++i) {
        if (!live[i]) continue;
        ++s.rough;
        const auto d = degree[i];
        s.edge_incidence += d;
        if (d == 0) ++s.primes;
        else if (d == 1) ++s.degree_one;
        else if (d == 2) ++s.degree_two;
        else ++s.degree_three_or_more;
    }
    return s;
}

bool valid_identity(const Stats &s) {
    const auto lhs = static_cast<std::int64_t>(s.primes);
    const auto rhs = static_cast<std::int64_t>(s.rough) -
                     static_cast<std::int64_t>(s.edge_incidence) +
                     static_cast<std::int64_t>(s.degree_two) -
                     static_cast<std::int64_t>(s.degree_three_or_more);
    return lhs == rhs;
}

bool sufficient(const Stats &s) {
    const auto lhs = 3 * static_cast<std::int64_t>(s.rough) +
                     2 * static_cast<std::int64_t>(s.degree_two);
    const auto rhs = 3 * static_cast<std::int64_t>(s.edge_incidence);
    return lhs > rhs;
}

} // namespace pga

#ifndef PGA_MAIN_ONLY
int main(int argc, char **argv) {
    try {
        pga::u64 n = argc > 1 ? std::stoull(argv[1]) : 1000;
        auto s = pga::analyze(n);
        std::cout << s.n << ' ' << s.rough << ' ' << s.edge_incidence << ' '
                  << s.degree_one << ' ' << s.degree_two << ' '
                  << s.degree_three_or_more << ' ' << s.primes << ' '
                  << pga::valid_identity(s) << ' ' << pga::sufficient(s) << '\n';
    } catch (const std::exception &e) {
        std::cerr << e.what() << '\n';
        return 1;
    }
}
#endif
