# Proof Obligations

## P0: Source verification

- [ ] Read a human-readable proof of the RH proof.
- [ ] Identify stronger intermediate results than terminal RH/GRH.

## P1: Kernel audit

- [ ] Formalize Mellin normalization.
- [ ] Bound endpoint and truncation errors.
- [ ] Justify that prime powers and smooth Fourier tails are negligible.

## P2: Central inequality

- **CONJECTURAL**: for the selected kernel,
  `limsup C_n/n < 1`, or a sufficiently stronger equivalent strict inequality.
- No proof of this condition is known in this workspace.

## P3: Legendre implication

- Prove existence of a prime in `(n^2,(n+1)^2)` from a positive weighted sum
  with no parity or endpoint ambiguity.

## P4: Eliminate logarithmic factors

- [ ] Establish `p_{k+1}-p_k=o(sqrt(p_k) log p_k)` in the needed range, or
      derive an alternative square-root bound.
- [ ] Identify any stronger uniform bound proved by the announced Lean proof.
