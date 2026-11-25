# Research Context

## Objective

**CONJECTURAL:** for every positive integer `n`, prove that a prime lies strictly between
`n^2` and `(n+1)^2`.

## External assumption

**RH-CONDITIONAL:** the Riemann Hypothesis is an explicit assumption for conditional derivations only.
As of 2026-11-25, independent machine verification reports for Levent Alpöge's
announcement agree that the formal target depends only on Lean's standard
axioms and has been replayed by independent kernels.  The human-readable proof
has not yet undergone ordinary mathematical refereeing.

## Existing kernel

**ESTABLISHED:** `x=n(n+1)`, `h=log(1+1/n)`, and

`f_n(t)=sqrt(x/t)*max(0,1-|log(t/x)|/h)`.

Its Mellin transform is

`F_n(s)=2*x^s*(cosh((s-1/2)*h)-1)/(h*(s-1/2)^2)`.

**ESTABLISHED:** the positive set is `{t>0 : |log(t/x)|<h}`, namely
`(n(n+1)/(1+1/n), n(n+1)*(1+1/n)) = (n^2,(n+1)^2)`.
This corrects the baseline's `n^2-1` algebraic error. The closed support
also contains the zero-valued endpoints. Full proofs and updated obligations
are in `VERIFIED_LEMMAS.md`, `DISCRETE_SIEVE.md`, and `L001_TRUNCATION.md`.
