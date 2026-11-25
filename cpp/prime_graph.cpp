#include <algorithm>
#include <cmath>
#include <cstddef>
#include <cstdint>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <vector>
#include <numbers>

namespace pga {

using u64 = std::uint64_t;
using usize = std::size_t;

inline u64 cube_root_floor(u64 value) {
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
        u64 start = p * p;
        for (u64 m = start; m <= limit; m += p) block[m - 2] = false;
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
    while ((cutoff + 1) <= upper / (cutoff + 1) &&
           (cutoff + 1) * (cutoff + 1) * (cutoff + 1) <= upper) ++cutoff;
    while (cutoff > upper / cutoff / cutoff) --cutoff;

    const auto primes = sieve(upper);
    Stats s{n, 2 * n, cutoff, 0, 0, 0, 0, 0, 0};
    for (u64 m = lower + 1; m <= upper; ++m) {
        u64 degree = 0;
        for (u64 p : primes) {
            if (p > cutoff && p < m && m % p == 0) ++degree;
        }
        if (degree == 0) {
            bool small_factor = false;
            for (u64 p : primes) {
                if (p > cutoff) break;
                if (m % p == 0) { small_factor = true; break; }
            }
            if (!small_factor) {
                ++s.rough;
                bool composite = false;
                for (u64 p : primes) {
                    if (p < m && m % p == 0) { composite = true; break; }
                }
                if (!composite) ++s.primes;
            }
        } else {
            if (degree == 1) ++s.degree_one;
            else if (degree == 2) ++s.degree_two;
            else ++s.degree_three_or_more;
            ++s.rough;
        }
        u64 residual_degree = 0;
        for (u64 p : primes) {
            if (p > cutoff && p < m && m % p == 0) ++residual_degree;
        }
        s.edge_incidence += residual_degree;
    }
    return s;
}

bool valid_identity(const Stats &s) {
    u64 h = s.degree_three_or_more;
    u64 lower = s.rough - s.edge_incidence + s.degree_two - h;
    return lower == s.primes;
}

bool sufficient(const Stats &s) {
    return 3 * s.rough + 2 * s.degree_two > 3 * s.edge_incidence;
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
