# Verified lemmas

## K001: support and normalization — ESTABLISHED

Let `n>=1`, `x=n(n+1)`, `h=log(1+1/n)` and
`f(t)=sqrt(x/t) max(0,1-|log(t/x)|/h)` for `t>0`.
Then `x exp(-h)=n²` and `x exp(h)=(n+1)²` exactly. The **positive set** is
`(n²,(n+1)²)`; the closed support includes its zero-valued endpoints.
The baseline assertion `n²-1` was an algebraic error.

Substitute `t=x exp(u)` and integrate the triangle to obtain

`F(s)=integral f(t)t^(s-1)dt = x^s h [sinh((s-1/2)h/2)/((s-1/2)h/2)]²`.

The removable value at `s=1/2` is `sqrt(x)h`. In particular,
`F(1)=x h [sinh(h/4)/(h/4)]² = n+1/2+O(1/n)` and `h sqrt(x)->1`.
This stable expression avoids subtraction of nearly equal cosh values.
For `u>=0`, `f<=1` directly. For `u=-v<=0`, use
`exp(v/2)(1-v/h)<=exp(v/2-v/h)<=1`, since `h<=log 2<2`.
Equality holds at `t=x`; `f` is strictly positive throughout the open interval.

## K002: higher prime powers — ESTABLISHED

Put `U=n²+2n`, `K=floor(log₂ U)`, and
`Q_n=sum_{p prime,k>=2,n²<p^k<=U} log(p) f(p^k)`.
There are no squares in the interval. For each `k>=3`, the base interval
`(n^(2/k),(n+1)^(2/k))` has length less than one: the derivative of
`t^(2/k)` on `[1,infinity)` is at most `2/k<1`. It contains at most one
integer base. Since `p>=2` implies `k<=K`, and `log p<=log U/k`,

`0<=Q_n<=D_n := log(U) sum_{k=3}^K 1/k = O(log n log log n)=o(n)`.

An empty sum is zero. This uses neither primality distribution nor RH.
The bound may overcount composite bases, whereas `Q_n` uses prime bases only.

## K003: explicit formula — RH-CONDITIONAL

For `n>=2`, the zeta explicit formula applied to K001 is

`W_n := sum_m Lambda(m)f(m) = F(1)-h sqrt(x) C_n-R_n`,

where `C_n=2 sum_{gamma>0} cos(gamma log x)sinc²(gamma h/2)` counts zero
multiplicities, and `R_n=sum_{j>=1}F(-2j)`.
Here `sinc(v)=sin(v)/v`, with value one at zero. Indeed
`F(1/2+i gamma)=h sqrt(x) exp(i gamma log x)sinc²(gamma h/2)`;
pair conjugate zeros. RH enters at this substitution.

Justification: Mellin inversion on `Re s>1` and the absolutely convergent
Dirichlet series for `-zeta'/zeta` give the integral of `-zeta'/zeta * F`.
Shift the contour past the pole at 1 and all zeta zeros. The continuous,
piecewise differentiable triangle has `F(s)=O_n((1+|Im s|)^-2)` on bounded
vertical strips. Standard zero-avoiding heights make horizontal integrals
vanish. Negative vertical integrals vanish as the line moves left because
the support is bounded below by `n²>1`. There is no pole at zero.
The zero series converges absolutely by `N(T)=O(T log T)`; the trivial-zero
series converges geometrically. For the classical contour method see
[Dudek–Grenié–Molteni, section 1](https://arxiv.org/html/1503.05403v2#S1).
The particular Mellin kernel and its normalization are derived here.

## K004: trivial zeros — ESTABLISHED

For `n>=2`, nonnegative termwise integration gives

`R_n=integral_{n²}^{(n+1)²} f(t)/(t(t²-1)) dt`,
`0<R_n<=E_n := (2n+1)/(n²(n⁴-1))=O(n^-5)`.

Use `f<=1` and the decreasing positive reciprocal denominator. This does
not require RH. For `n=1`, the prime 2 directly supplies the desired witness.

## K005: finite sufficient inequality — RH-CONDITIONAL

Writing `P_n=sum_{p prime}log(p)f(p)`, L001 and K002–K004 imply

`P_n >= F(1)-h sqrt(x)[C_n(T)+B(n,T)]-D_n-E_n`.

Strict positivity on the right proves a prime in the required interval.
A numerical application needs every zero up to the cutoff with multiplicity
and an upper enclosure of the finite sum including zero-location and
arithmetic errors. Ordinary floating-point evaluation is not a certificate.

## K006: the missing margin

**RH-CONDITIONAL:** `W_n>=0` already gives `C_n<=F(1)/(h sqrt(x))`,
hence `limsup C_n/n<=1`. This non-strict bound does not prove Legendre.

**RH-CONDITIONAL implication:** `limsup C_n/n<1` would imply `P_n>=c n`
eventually for some `c>0`, hence at least `c n/log U` primes in each such
interval, since `f<=1`. This asks for more than the single prime required
by Legendre. A limiting argument also needs an effective cutoff to reduce
the remaining work to an explicit finite check.

**CONJECTURAL:** the strict limsup inequality is unproved here.

**RH-CONDITIONAL:** the exact prime-existence criterion is
`C_n < [F(1)-R_n-Q_n]/[h sqrt(x)]`.

**FAILED:** replacing cosines by absolute values gives the envelope
`2 sum sinc²(gamma h/2)=Theta(n log n)`. For the lower bound, restrict to
`gamma<=1/h`; sinc² is bounded below there and
`N(1/h)=Theta(h^-1 log(1/h))`. For the upper bound, split there and use
L001's reciprocal-square estimate for the tail. Since `h~1/n`, the envelope
exceeds the principal mass by a logarithmic factor. This envelope estimate
itself is unconditional. Smaller tail constants do not fix signed cancellation.

## Verification scope

**ESTABLISHED:** discrete proofs are in [DISCRETE_SIEVE.md](DISCRETE_SIEVE.md),
and L001's constants and proof in [L001_TRUNCATION.md](L001_TRUNCATION.md).
The analytic lemmas above have written proofs and numerical regression
tests, but no Lean certification. See [LEAN_VERIFICATION.md](LEAN_VERIFICATION.md)
for the actual compiler and axiom-audit status of the elementary lemmas.
