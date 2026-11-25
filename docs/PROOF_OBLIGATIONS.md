# Proof obligations

## Completed written proofs — ESTABLISHED

- K001: correct square endpoints, Mellin transform, `0<=f<=1`.
- K002/K004: explicit higher-prime-power and trivial-zero bounds.
- L001: requested truncation constants for `T>=1`, original-source audit,
  sharper optional bound, and ordinate perturbation budget.
- Exact Möbius floor identity, square-endpoint congruences, disjoint
  semiprime correction, and eventual failure of every fixed odd Bonferroni depth.

These are written proofs. Lean certification has a separate record in
`LEAN_VERIFICATION.md`; numerical tests do not certify infinite claims.

## Exact discrete target — CONJECTURAL

For `L=n²`, `U=n²+2n`, `Q=product_{p<=n}p`, prove, for every `n>=1`,

`sum_{d|Q} mu(d)({L/d}-{U/d}) > -2n product_{p<=n}(1-1/p)`.

Equivalently, with `z=floor(U^(1/3))`, prove

`S_z(n) > sum_{z<p<=n}[pi(floor(U/p))-pi(floor(n²/p))]`.

No positive uniform lower bound for either expression is established.

## Analytic target — CONJECTURAL

With RH assumed, a sufficient finite inequality is

`C_n(T)+B(n,T) < [F(1)-D_n-E_n]/[h sqrt(x)]`.

K005 proves this implication **RH-CONDITIONALLY**. The strict infinite
target `limsup C_n/n<1` is sufficient for eventual positivity, but also
requires an effective cutoff and finite verification below it. The bound
`limsup C_n/n<=1` already follows **RH-CONDITIONALLY** from nonnegativity;
it does not supply the missing margin. Certified computations additionally
need complete zero lists, ordinate enclosures, and outward rounding.

## Next research objective

Establish a rigorous uniform bound
\[
C_{n,k(n)}(4k(n)(n+1))\le(1-\epsilon)n
\]
for fixed \(\epsilon>0\) and all sufficiently large n.

PGA-L029 provides an audited fixed-k truncation form.  PGA-L030 remains
constant-dependent until the Stieltjes/N(T) tails are written with explicit
admissible constants.  PGA-L028 remains incomplete until the generalized
kernel principal term and remainder are fixed.

Find a bound exploiting the phases `-n² mod d` across the full signed
Möbius sum, or an upper bound for the *aggregate* disjoint semiprime
correction smaller than the rough-survivor count. Fixed-degree
inclusion–exclusion is excluded by the proved obstruction. RH may be
used, but independence, pair correlation, or GRH must not be added silently.

## External machinery

Alpöge's inspected terminal dependency yields right-half-plane Dirichlet
L-function nonvanishing. No stronger short-interval estimate was found in
the inspected statements. Finding such a quantitative intermediate lemma
remains open; reproducing an RH proof is outside this task.

**FAILED:** the former goal `gap=o(sqrt(x)log x)` was insufficient by
itself: this scale can still be much larger than the square interval.
