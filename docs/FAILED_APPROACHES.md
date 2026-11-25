# Failed approaches

- **FAILED — ordinary RH interval estimates:** a radius of order
  `sqrt(x)log x` eventually exceeds a square interval's radius. Merely
  improving this to `o(sqrt(x)log x)` need not suffice. Even an
  `O(sqrt(x))` estimate requires a suitable constant and placement.
  See [Dudek–Grenié–Molteni, Theorem 1.1](https://arxiv.org/html/1503.05403v2#S1.Thmtheorem1).
- **FAILED — absolute zero sums:** the triangle's nonnegative envelope is
  `Theta(n log n)`, whereas its principal mass is `Theta(n)`; see K006.
  Improving L001's constants controls the tail without proving cancellation.
- **FAILED — termwise Möbius errors:** the elementary lower bound
  `2n product(1-1/p)-(2^pi(n)-1)` is negative already at `n=3`.
- **FAILED — any fixed odd Bonferroni depth:** its lower bound becomes
  negative for all sufficiently large `n`, proved in `DISCRETE_SIEVE.md`.
  This does not exclude increasing depth or specially optimized weights.
- **FAILED — independent CRT phases:** the offsets are `-n² mod d`,
  determined by one integer. Full-period CRT counts do not eliminate the
  remainder in an interval of length `2n`.
- **FAILED — monotone survivor induction:** `S(4)=3>S(5)=2` is an exact
  finite counterexample to monotonicity, not to Legendre.
- **FAILED — semiprime density substitution:** after the cube-root sieve,
  cofactor intervals near `p=n` have bounded length. Replacing their prime
  counts by expected densities supplies no proved upper bound on their sum.
- **FAILED — inherited endpoint analysis:** the baseline's lower endpoint
  `n²-1` was an algebraic error; the correct positive set is `(n²,(n+1)²)`.
