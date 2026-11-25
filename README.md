# Legendre Conjecture Research

Research code and documentation for investigating whether RH, or stronger
machinery developed in a formal RH proof, implies Legendre's conjecture.

This repository does not claim that Legendre's conjecture has been solved.

## Layout

- `python/`: prime/zero numerical computations and tests.
- `cpp/`: segmented sieve and integration hooks.
- `lean/`: formalized established and conditional lemmas.
- `docs/`: research log, audit, obligations, and handoff.
- `paper/`: XeLaTeX research paper.
- `scripts/`: reproducible validation entry points.

## Quick start

```powershell
python -m pytest python/tests
python python/legendre_analysis.py --n-max 100000
```
