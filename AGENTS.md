# AGENTS.md

## Research status

This repository is a rigorous research workspace for Legendre's conjecture.  It
is not a claim of a solved conjecture.  Numerical observations are never proof.

## Required categories

Every mathematical claim in source or documentation must be tagged as one of:

- **ESTABLISHED**: proved from stated standard definitions or cited literature.
- **LEAN-CERTIFIED**: accepted by Lean/Mathlib and checked for axioms.
- **RH-CONDITIONAL**: follows from RH or GRH.
- **NUMERICAL**: finite computation, not an infinite claim.
- **CONJECTURAL**: plausible but unproved.
- **FAILED**: an attempted approach with a precise obstruction.

## Project rules

- Never use `sorry`, `axiom`, `admit`, or hidden assumptions in completed Lean proofs.
- Record external proof assumptions and verifier status.
- Add tests for every implemented formula or error bound.
- Keep the handoff current after meaningful milestones.
- Preserve unrelated work in an existing workspace.
