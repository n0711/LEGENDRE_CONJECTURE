# L001: absolute truncation of the triangular zero sum

## Statement and conventions

**ESTABLISHED.** Let `n >= 1` be an integer, `x=n(n+1)`,
`h=log(1+1/n)`, and `sinc(u)=sin(u)/u`, continuously extended at zero.
Count every nontrivial zeta zero with positive ordinate, with multiplicity.
Define

\[
C_n=2\sum_{\gamma>0}\cos(\gamma\log x)
       \operatorname{sinc}^2(\gamma h/2),\qquad
C_n(T)=2\sum_{0<\gamma\le T}\cos(\gamma\log x)
       \operatorname{sinc}^2(\gamma h/2).
\]

Then the series is absolutely convergent, and, for every real `T >= 1`,

\[
|C_n-C_n(T)|\le B(n,T):=\frac8{h^2}\left[
\frac{\log(T/(2\pi))+1}{2\pi T}
+\frac{0.7\log T+18.175}{T^2}\right].\tag{L001}
\]

**ESTABLISHED.** This is a theorem about ordinates and needs no RH.
**RH-CONDITIONAL.** Identifying this cosine sum with the paired nontrivial-zero
contribution to the prime explicit formula uses `Re(rho)=1/2`.

## Published input and independent specialization

**ESTABLISHED (external theorem).** T. S. Trudgian, *An improved upper bound
for the error in the zero-counting formulae for Dirichlet L-functions and
Dedekind zeta-functions*, [arXiv:1206.1844v4, Theorem 2, equation (1.2),
PDF page 1](https://arxiv.org/pdf/1206.1844v4), states, for `T >= 1`,

\[
\left|N_K(T)-\frac T\pi\log\left(d_K
 \left(\frac T{2\pi e}\right)^{n_K}\right)\right|
\le0.317(\log d_K+n_K\log T)+6.333n_K+3.482.
\]

The source counts both signs, `|Im(rho)| <= T`. The exact constants, range,
and normalization were checked in the original paper on 2026-11-25.
The published proof is an external dependency; it has not been re-formalized
or independently replayed in this repository.

**ESTABLISHED (independent deduction).** Take `K=Q`, `n_K=d_K=1`.
There are no real nontrivial zeta zeros: for `0<s<1` the paired alternating
series for `eta(s)` is positive and `1-2^(1-s)<0`, so `zeta(s)<0`.
Conjugation therefore gives `N_Q(T)=2N(T)`, where
`N(T)=#{rho: 0<Im(rho)<=T}`. Consequently, with
`M(t)=t/(2*pi)*log(t/(2*pi*e))`,

\[
|N(t)-M(t)|\le0.1585\log t+4.9075
             \le0.35\log t+9\qquad(t\ge1).\tag{1}
\]

The constants `0.35,9` are a deliberately relaxed corollary, not a quotation
of an original theorem. No attribution to an unverified Backlund or Rosser
constant is needed. A convention excluding zeros exactly at a height is
converted to the stated inclusive convention by taking right limits.

## Proof of L001

**ESTABLISHED (independent proof).** Write `R=N-M` and
`E(t)=a log t+b`, where `(a,b)=(0.35,9)`. Abel summation, first on a finite
interval and then using `N(U)=O(U log U)`, yields

\[
\sum_{\gamma>T}\gamma^{-2}
=-\frac{N(T)}{T^2}+2\int_T^\infty\frac{N(t)}{t^3}\,dt
=\frac{\log(T/(2\pi))+1}{2\pi T}
 -\frac{R(T)}{T^2}+2\int_T^\infty\frac{R(t)}{t^3}\,dt.
\]

The integral converges absolutely. The remainder is bounded above by

\[
\frac{E(T)}{T^2}+2\int_T^\infty\frac{E(t)}{t^3}\,dt
=\frac{2a\log T+2b+a/2}{T^2}
=\frac{0.7\log T+18.175}{T^2}.
\]

Finally, each summand in the absolute cosine tail is at most
`8/(gamma^2 h^2)`. This also proves absolute convergence and L001.
If one instead adds `7/8` to `M`, that constant cancels in Abel summation;
the error envelope must then be adjusted, not silently reused.

**ESTABLISHED (sharper optional bound).** Keeping the first envelope in (1)
replaces `0.7 log T+18.175` by
`0.317 log T+9.89425`. Both versions retain the same leading term.

## Ordinate accuracy and zero-list completeness

**ESTABLISHED (independent proof).** The identity

\[
\operatorname{sinc}^2(\gamma h/2)
=\frac1h\int_{-h}^{h}(1-|u|/h)e^{i\gamma u}\,du
\]

gives a derivative bound `h/3`, by integrating `|u|(1-|u|/h)/h`.
Thus `f(gamma)=2 cos(gamma log x) sinc^2(gamma h/2)` is globally Lipschitz
with constant `L=2(log x+h/3)`. For a fixed complete list with correct
multiplicities, certified errors `|gamma_j-gammahat_j| <= epsilon_j` imply

\[
|\sum_jf(\gamma_j)-\sum_jf(\widehat\gamma_j)|
 \le 2(\log x+h/3)\sum_j\epsilon_j.\tag{2}
\]

**ESTABLISHED.** A numerical upper certificate would need all of:

1. A certified complete list up to `T`, including multiplicities and proof
   of which side of `T` each ordinate lies on.
2. Certified ordinate error bounds as in (2).
3. An outward-rounded enclosure of the finite sum and of `B(n,T)`.

**NUMERICAL.** `python/zero_tail.py` evaluates both tail formulas and (2)
using binary64. These outputs are diagnostic approximations, not interval
certificates. The API restricts `1 <= n <= 2^53` and finite `T >= 1`;
these are implementation limits, not restrictions on the mathematical lemma.
No certified zero data are supplied by this module.

## Cost and obstruction at the required scale

**ESTABLISHED.** Since `h~1/n`, for `n,T -> infinity` the leading tail budget is

\[
\frac{B(n,T)}n\sim\frac4\pi\frac{n\log T}{T}.
\]

For fixed `kappa>0`, `T=kappa*n*log n` gives limit `4/(pi*kappa)`.
For a vanishing tail relative to `n`, the sufficient choice
`T=n*(log n)^(1+delta)` for fixed `delta>0` uses
`N(T)=Theta(n*(log n)^(2+delta))` ordinates. A fixed sufficiently small
relative tail budget instead uses `Theta(n*(log n)^2)` ordinates.
The fixed-budget cutoff scale is also necessary *for this absolute bound*:
if `T=o(n log n)`, its relative tail budget cannot stay bounded.

**ESTABLISHED.** Evaluating `B` has best/average/worst-case `Theta(1)`
binary64 operations and space under the stated bounded-input API; no average
input distribution is assumed. Applying (2) to `M` supplied errors takes
`Theta(M)` input-processing work. Python's compensated `math.fsum` keeps
partial sums; a conservative auxiliary-space bound is `O(M)`. Summing a
supplied zero list similarly requires `Omega(M)` reads, irrespective of how
the data were obtained. Any full pipeline must add zero-generation,
completeness certification, precision, and storage costs; L001 supplies no
efficient certified generator. No divide-and-conquer recurrence occurs, so
the Master Theorem does not apply.

**ESTABLISHED.** With binary input length `ell=Theta(log n)`, even the
fixed-budget `Theta(n log^2 n)` list length is exponential in `ell`.
For a permitted ordinate contribution at most `eta*n`, uniform ordinate
error `epsilon` may be taken at most `eta*n/(2M(log x+h/3))` by (2).
At `T=Theta(n log n)` this sufficient absolute accuracy is
`O(eta/log^3 n)`. Representing ordinates as large as `T` also requires
integer bits: fixed-point width is `O(log T+log(1/epsilon))`.
This statement does not bound evaluation roundoff or certified-generation cost.

**FAILED.** Absolute tail control provides no upper bound below `n` for
the retained signed sum. Neither sharper zero counts nor a faster summation
algorithm establish `limsup C_n/n<1`. That uniform cancellation inequality
remains an independent, unresolved proof obligation.

## Verification

**NUMERICAL.** Tests compare both implementations against independent
80-digit expressions at small and large parameters, integrate the Abel error
term at 60 digits, check a block of four computed zero ordinates, check
ordinate perturbations, and reject inputs outside the diagnostic domain.
They test implemented formulas and regressions, not an infinite assertion.
No Lean certificate for L001 is claimed.

**NUMERICAL.** On 2026-11-25, Python 3.13.16 on Windows 11, the best of five
`timeit.repeat(..., number=20000)` samples at `(n,T)=(1000,10000)` measured
810 ns/call for `truncation_bound` and 565 ns/call for a direct, unvalidated
binary64 transcription of L001. There was no previous tail implementation
in the baseline. The new code pays for validation and avoids forming `T^2`;
no speed improvement is claimed. These local timings exclude import and
zero-data costs and are not machine-independent performance guarantees.
