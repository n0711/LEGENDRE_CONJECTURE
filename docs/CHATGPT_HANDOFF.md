# ChatGPT Handoff

## Current status

M0 source verification has begun.  M1 kernel audit has begun.  M2 executable
prime and zero infrastructure has been initialized.  No theorem of Legendre
has been proved.

## Verified derivations

For `x=n(n+1)` and `h=log(1+1/n)`, the support is
`(n^2-1,(n+1)^2)`.  Therefore an integer-weighted sum detects primes only in
that interval; the strict right endpoint must be checked separately.

The Mellin formula stated in the premise is correct:

`F_n(s)=2*x^s*(cosh((s-1/2)h)-1)/(h*(s-1/2)^2)`.

At `s=1`, `F_n(1)=x*h+O(x h^3)=n+O(1)`.

## Verification status

- Alpöge announcement: https://alpo.ge/remark.pdf
- Machine checks: completed builds and replay reports are externally recorded.
- Human refereeing: pending.
- Legendre: unresolved.

## Numerical evidence

A segmented sieve through `(10001)^2=100020001` found no failure for
`1<=n<=10000`.  It found 5,762,536 primes in the scan.  This is finite evidence
only and does not establish an infinite theorem.

The finite run used the positive support interval; it did not numerically
evaluate a complete zero sum.

## Unresolved inequalities

1. Exact normalization of the zero sum and scale of its RH tail.
2. Uniform cancellation or lower bound for `C_n` at the `n` scale.
3. A rigorous positive-weight implication without support ambiguity.
4. A stronger result from the announced Lean proof.

## Failed approaches

The naive direct RH-gap route fails as a proof method because it supplies only
`O(sqrt{x}log x)` or `O(sqrt{x}log^2 x)`, not a uniform \(o(sqrt{x})\) gap.

## Recommended next step

Derive and verify explicit truncation constants for the smooth explicit formula,
then search for a rigorous positive lower bound stronger than crude RH estimates.
