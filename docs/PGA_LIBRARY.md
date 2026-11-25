# PGA interval library (experimental v0)

**ESTABLISHED — scope.** This header-only C++20 interface implements the
consecutive-square interval classification. It assumes no RH and does not
establish that every interval has a prime.

Example:

~~~cpp
#include <iostream>
#include "pga/interval.hpp"
int main() {
    const auto r = pga::library::enumerate(100, [](auto p) {
        std::cout << p << '\n';
    });
    std::cout << r.primes << '\n';
}
~~~

Compile with -std=c++20 -O2 -Icpp/include. count(n, block) returns candidates,
rough, edges and primes without storing the output. enumerate(n, callback,
block) streams prime values in increasing order. baseline_count uses a
conventional interval sieve with identical base-prime generation and blocks.
The interface is experimental; it supports positive n with n*n+2*n fitting
uint64_t and a positive block size, subject to available memory.

**ESTABLISHED — stronger degree bound.** Let U=n*n+2*n, z=floor(cuberoot(U)).
After sieving primes <=z, a composite survivor has exactly two prime factors
counted with multiplicity, since three would exceed U. They are distinct
because the open square interval contains no square. Both factors cannot be
<=n, since then their product is <=n*n. Both cannot be >n, since then their
product is >=(n+1)^2. Thus exactly one residual prime <=n divides it.
For n=1 there are no composites. The degree is zero for primes and one
for residual composites, so P=R-E. The implementation checks duplicate
residual edges and the exact identity. This sharpens the older bounded-degree
formulation, but its formal Lean certification remains pending.

**ESTABLISHED — cost.** With block capacity B, base primes are generated
through n using a packed sieve. Word time is
O(n log log(n+2) + ceil(2n/B) pi(n)); every block scans the prime list.
Storage is O(n) bits of base sieve, O(pi(n)) words for base primes, and
O(min(B,2n)) bytes of candidate states, plus any callback-owned storage.
This is not polynomial in log n, and fixed B may introduce substantial
per-block overhead. There is no divide-and-conquer recurrence here.

**NUMERICAL — reproducibility.** Build and run:

~~~sh
g++ -std=c++20 -O2 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -Werror \
  -Icpp/include cpp/tests/pga_library_test.cpp -o pga_library_test
./pga_library_test
./pga_library_test benchmark > pga_benchmark.csv
~~~

Tests compare full prime sequences to independent trial division for n=1..1000
and four block sizes, and check count equality and invalid inputs. Benchmarks
include base generation, allocation, marking and counting, use matched block
sizes, alternate order, and record five repeats. CI uploads raw timing rows.
Do not claim a speedup until the timing artifact is inspected. This is an
internal baseline, not a comparison to optimized primesieve. External
primesieve comparison, distribution, Python bindings, a license decision,
and Lean certification are follow-up milestones. Not intended for production
cryptographic key generation.
