# PGA kernel audit

## Definitions

Let \(x=n(n+1)\), \(h=\log(1+1/n)\), and let
\[
w_k(\gamma)=\operatorname{sinc}^{k}(\gamma h/k),
\qquad
C_{n,k}(T)=2\sum_{0<\gamma\le T}\cos(\gamma\log x)w_k(\gamma),
\]
with even \(k\).  The adaptive values are
\[
k(n)=2\max(2,\lceil\log\log(n+1)\rceil),
\qquad T(n)=4k(n)(n+1).
\]

## Independent formula audit

**ESTABLISHED — truncation method.**  The standard zero-count bound
\(N(T)=O(T\log T)\) gives, for fixed even \(k\),
\[
\sum_{\gamma>T}w_k(\gamma)
=O_k(n^k\log T/T^{k-1}),
\]
because \(|\operatorname{sinc}(u)|\le\min(1,1/|u|)\), \(|h|\asymp1/n\),
and \(k\) is fixed.  This proves the form of PGA-L029 but not every
unpublished numerical constant.  It is not an RH-dependent localization
statement.

**DERIVED, CONSTANTS PENDING — adaptive form.**  Substitution of
\(T=4kn\) in the fixed-\(k\) bound gives
\[
O_k\left(k n\log T\,4^{-k}\right),
\]
up to \(k\)-dependent constants.  Since \(k(n)\asymp\log\log n\),
this is \(o(n)\) if the constants depend only on the fixed zero-count
method and no normalized lower bound is silently used.  It is not yet
a completed PGA-L030 certificate.

**ESTABLISHED — prime powers.**  The bound
\(\log U\sum_{j=2}^{\log_2 U}1/j=O(\log n\log\log n)\) remains valid
for every fixed smooth kernel.  The looser claim
\(O(\log n(\log\log n)^2)=o(n)\) follows, but it is not stronger than
the existing \(O(\log n\log\log n)\) estimate.

**ESTABLISHED — zero evaluation count.**  With \(T=4k(n)(n+1)\),
\[
N(T)=\Theta(T\log T)
=\Theta(n\log n\log\log n),
\]
excluding zero generation and precision certification.  The explicit
\(\Theta\) uses the standard complete zero-count asymptotic, not the RH
zero-free or square-interval location problem.

**ESTABLISHED — square center.**  For \(n\ge2\),
\(\Lambda(n(n+1))=0\), because \(n(n+1)\) is composite and is not a
prime power: the two coprime factors \(n,n+1\) cannot both be powers of
the same prime.  This identity does not by itself localize cancellation.

## Labeled lemmas

- **PGA-L028 — CONJECTURAL/INCOMPLETE:** a generalized smooth-kernel criterion
  converting a uniform normalized \(C_{n,k(n)}(T)\) bound into a positive
  prime lower bound.  A kernel-specific principal term, tail constant and
  prime-power/trivial-zero remainder must be supplied.
- **PGA-L029 — ESTABLISHED in form, CONSTANTS PENDING:** fixed even \(k\)
  truncation is \(O_k(n^k\log T/T^{k-1})\).
- **PGA-L030 — DERIVED, NOT CERTIFIED:** adaptive \(T\) gives
  \(O(kn\log T\,4^{-k})=o(n)\) with explicit admissible constants.
- **PGA-L031 — ESTABLISHED:** normalized prime-power remainder is
  \(O(\log n\log\log n)=o(n)\).

## Counterexamples and limitations

- \(\operatorname{sinc}^{k}(\gamma h/k)\) is not a certified interval
  enclosure by itself; C++/Python values are diagnostics.
- Positive and signed pair correlation estimates do not imply the required
  one-sided bound \((1-\epsilon)n\).
- The center identity \(\Lambda(n(n+1))=0\) does not imply a short-interval
  Dirichlet-convolution estimate.
- No pair-correlation conjecture or Montgomery conjecture is assumed.
