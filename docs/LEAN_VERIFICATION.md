# Lean verification

**LEAN-CERTIFIED — 2026-11-25:** `lean/LegendreAudit.lean` was accepted by
Lean 4.8.0 (compiler commit `df668f00e6c0`) with Mathlib commit
`b5eba595428809e96f3ed113bc7ba776c5f801ac`. Both the toolchain and all Lake
dependency revisions are pinned. The eleven local theorems have individually
checked `#print axioms` reports. Each reports only `propext`, `Classical.choice`,
and `Quot.sound`; there are no custom axioms or incomplete proof terms.

The checked source has SHA-256
`cba1ab83cec6d7c58709ae496dc4a1712f2e32bcf5e88e6745ae53fbd253700c`;
the manifest has SHA-256
`eac4fa421bf1f7afd96f425b65f4ff35edbe1be4aa6265ff186430eae83719ed`.
Source, manifest, Lake configuration and toolchain file hashes matched the
compiled WSL mirror byte for byte. The compiler/audit command exited zero.

**LEAN-CERTIFIED:** The checked statements are:

- `kernel_support_lower`, `kernel_support_upper`: the endpoints are exactly
  `n²` and `(n+1)²` for positive `n`.
- `mem_smallPrimes`: membership is primality together with `p ≤ n`.
- `squareInterval_card`: the open integer interval has `2n` elements.
- `composite_has_small_prime_factor`: a nonprime interval integer has a prime
  divisor at most `n`, for `n ≥ 1`.
- `prime_iff_no_small_divisor`: an interval integer is prime exactly when
  none of those small primes divides it.
- `covered_subset`, `mem_covered`: the actual finite union of small-prime
  divisibility sets is contained in the interval and has the stated membership
  condition.
- `mem_survivors`, `survivors_card`: the complement consists exactly of interval
  primes and has cardinality `2n − |covered|` (natural-number subtraction).
- `union_card_lt_iff_prime_exists`: `|covered| < 2n` is equivalent to the
  Legendre instance for that `n`.
- `mem_smallPhaseCovered`: membership in the threshold state-1 phase is
  exact divisibility by a prime at most the supplied threshold.

**CONJECTURAL:** Positivity of the survivor count for every positive `n` is
still unproved. The file neither assumes RH nor proves Legendre, L001, a
Möbius sum identity, or zero cancellation.

## Reproduce

With the pinned Lean toolchain available, run from `lean/`:

```sh
MATHLIB_NO_CACHE_ON_UPDATE=1 lake update
lake exe cache get Mathlib/Analysis/SpecialFunctions/Log/Basic.lean Mathlib/Data/Nat/Prime.lean Mathlib/Order/Interval/Finset/Nat.lean Mathlib/Tactic/FieldSimp.lean Mathlib/Tactic/Linarith.lean Mathlib/Tactic/Positivity.lean Mathlib/Tactic/Ring.lean
python3 audit.py
python3 -m unittest discover -s . -p test_audit.py
```

`audit.py` fails if compilation fails, any theorem lacks a report, or a report
contains an assumption outside the three declared Lean foundations. It does
not inspect prose claims elsewhere in the repository. The compiler and
Mathlib's imported compiled objects remain part of the verification trust
boundary; no independent checker replay of those dependencies was performed.

**NUMERICAL — software checks:** All five audit-runner regression tests passed:
standard foundations and empty assumption sets are accepted; missing reports,
empty theorem lists, incomplete proof assumptions and custom assumptions are
rejected.

Local verification used Ubuntu under WSL and an exact copy of the tracked
Lean source, configuration and manifest. Reusable tools/cache are outside Git
at `/home/charalampos_nadiotis/.cache/legend-lean-audit/`; the Lean binary is
under `lean-4.8.0-linux/bin/`, and the checked mirror is `project/`. The targeted
cache fetched 1,461 dependency artifacts rather than all of Mathlib. Native
Windows Lean was not installed. IPv4 was selected in this local cache's curl
configuration after IPv6 retrieval stalled.

**ESTABLISHED — complexity scope:** These are universal symbolic proofs;
checking them does not enumerate `n` or the interval integers. The finite-set
definitions are specifications, not proposed efficient algorithms. No runtime
bound in `n` is claimed for evaluating them. The audit-report scan uses time
and space linear in its source/output lengths, separately from Lean's proof
checking and one-time dependency acquisition.
