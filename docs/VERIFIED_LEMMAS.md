# Verified Lemmas

## Established from standard analysis

- For `h=log(1+1/n)`, the kernel support is
  `(n(n+1)e^-h,n(n+1)e^h)=(n^2-1,(n+1)^2)`.
- Integers `n^2-1,n^2,(n+1)^2` lie at or on the support boundary issue.  The
  open support has no integer before `n^2`, and `(n+1)^2` is outside.
- The Mellin integral formula follows by
  `t=x exp u`, `dt=x exp u du`, with the explicit triangular transform.

## Not established

- Any uniform bound `limsup C_n/n<1`.
- Any kernel for which the RH zero sum is proved to remain below principal
  mass by one on every sufficiently large scale.

## Established RH consequence

- Under RH, standard explicit-formula bounds give
  `psi(x)=x+O(sqrt(x)*log^2 x)`, and consequently the classical RH consequence
  `p_{k+1}-p_k=O(sqrt(p_k)*log p_k)` for the prime gap.
- These estimates do not prove Legendre's conjecture; removing the logarithmic
  factor at the square-root scale is the unresolved step.
