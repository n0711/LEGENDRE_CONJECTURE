import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Data.Nat.Prime
import Mathlib.NumberTheory.ArithmeticFunction
import Mathlib.Order.Interval.Finset.Nat
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring

/-!
LEAN-CERTIFIED: Elementary reductions for the Legendre research workspace.
Verifier status and exact dependencies are recorded in docs/LEAN_VERIFICATION.md.
None of these theorems asserts the existence of a prime in every square interval.
-/

namespace LegendreAudit

open scoped BigOperators

/-- LEAN-CERTIFIED: Definition of the triangular kernel's logarithmic half-width. -/
noncomputable def kernelHalfWidth (n : ℕ) : ℝ := Real.log (1 + (1 : ℝ) / n)

/-- LEAN-CERTIFIED: Definition of the geometric midpoint. -/
noncomputable def geometricMidpoint (n : ℕ) : ℝ := (n : ℝ) * (n + 1)

/-- LEAN-CERTIFIED: The lower support endpoint is exactly n². -/
theorem kernel_support_lower (n : ℕ) (hn : 0 < n) :
    geometricMidpoint n * Real.exp (-kernelHalfWidth n) = (n : ℝ) ^ 2 := by
  have hnpos : (0 : ℝ) < n := Nat.cast_pos.mpr hn
  have hn0 : (n : ℝ) ≠ 0 := ne_of_gt hnpos
  unfold geometricMidpoint kernelHalfWidth
  rw [Real.exp_neg, Real.exp_log (by positivity : (0 : ℝ) < 1 + 1 / n)]
  field_simp [hn0]
  ring

/-- LEAN-CERTIFIED: The upper support endpoint is exactly (n+1)². -/
theorem kernel_support_upper (n : ℕ) (hn : 0 < n) :
    geometricMidpoint n * Real.exp (kernelHalfWidth n) = ((n : ℝ) + 1) ^ 2 := by
  have hnpos : (0 : ℝ) < n := Nat.cast_pos.mpr hn
  have hn0 : (n : ℝ) ≠ 0 := ne_of_gt hnpos
  unfold geometricMidpoint kernelHalfWidth
  rw [Real.exp_log (by positivity : (0 : ℝ) < 1 + 1 / n)]
  field_simp [hn0]
  ring

/-- LEAN-CERTIFIED: Definition of the open consecutive-square integer interval. -/
def squareInterval (n : ℕ) : Finset ℕ := Finset.Ioo (n ^ 2) ((n + 1) ^ 2)

/-- LEAN-CERTIFIED: Definition of the finite set of sieving primes. -/
def smallPrimes (n : ℕ) : Finset ℕ := (Finset.range (n + 1)).filter Nat.Prime

/-- LEAN-CERTIFIED: Definition of the union of integers covered by small primes. -/
def covered (n : ℕ) : Finset ℕ :=
  (smallPrimes n).biUnion (fun p => (squareInterval n).filter (fun m => p ∣ m))

/-- LEAN-CERTIFIED: Definition of the uncovered integers. -/
def survivors (n : ℕ) : Finset ℕ := squareInterval n \ covered n

/-- LEAN-CERTIFIED: Membership in the sieving-prime set. -/
theorem mem_smallPrimes {n p : ℕ} : p ∈ smallPrimes n ↔ p.Prime ∧ p ≤ n := by
  simp [smallPrimes, Nat.lt_succ_iff, and_comm]

/-- LEAN-CERTIFIED: The interval contains exactly 2n integers. -/
theorem squareInterval_card (n : ℕ) : (squareInterval n).card = 2 * n := by
  simp only [squareInterval, Nat.card_Ioo]
  have heq : (n + 1) ^ 2 = n ^ 2 + 2 * n + 1 := by ring
  omega

/-- LEAN-CERTIFIED: Every composite inside the interval has a prime divisor at most n. -/
theorem composite_has_small_prime_factor {n m : ℕ} (hn : 1 ≤ n)
    (hlo : n ^ 2 < m) (hhi : m < (n + 1) ^ 2) (hc : ¬m.Prime) :
    ∃ p, p.Prime ∧ p ≤ n ∧ p ∣ m := by
  have hm2 : 2 ≤ m := by nlinarith
  refine ⟨m.minFac, Nat.minFac_prime (by omega), ?_, Nat.minFac_dvd m⟩
  have hs := Nat.minFac_sq_le_self (by omega : 0 < m) hc
  nlinarith

/-- LEAN-CERTIFIED: No small prime divides an interval integer exactly when it is prime. -/
theorem prime_iff_no_small_divisor {n m : ℕ} (hn : 1 ≤ n)
    (hlo : n ^ 2 < m) (hhi : m < (n + 1) ^ 2) :
    m.Prime ↔ ∀ p, p.Prime → p ≤ n → ¬p ∣ m := by
  constructor
  · intro hm p hp hpn hpm
    have heq : p = m := (Nat.prime_dvd_prime_iff_eq hp hm).mp hpm
    subst p
    nlinarith
  · intro h
    by_contra hc
    obtain ⟨p, hp, hpn, hpm⟩ := composite_has_small_prime_factor hn hlo hhi hc
    exact h p hp hpn hpm

/-- LEAN-CERTIFIED: The covered union is a subset of the interval. -/
theorem covered_subset (n : ℕ) : covered n ⊆ squareInterval n := by
  intro m hm
  obtain ⟨p, _, hp⟩ := Finset.mem_biUnion.mp hm
  exact (Finset.mem_filter.mp hp).1

/-- LEAN-CERTIFIED: Membership in the covered union is an explicit divisibility condition. -/
theorem mem_covered {n m : ℕ} :
    m ∈ covered n ↔ m ∈ squareInterval n ∧ ∃ p, p.Prime ∧ p ≤ n ∧ p ∣ m := by
  simp only [covered, Finset.mem_biUnion, Finset.mem_filter, mem_smallPrimes]
  constructor
  · rintro ⟨p, ⟨hp, hpn⟩, hm, hpm⟩
    exact ⟨hm, p, hp, hpn, hpm⟩
  · rintro ⟨hm, p, hp, hpn, hpm⟩
    exact ⟨p, ⟨hp, hpn⟩, hm, hpm⟩

/-- LEAN-CERTIFIED: Sieve survivors are exactly the primes in the interval. -/
theorem mem_survivors {n m : ℕ} (hn : 1 ≤ n) :
    m ∈ survivors n ↔ n ^ 2 < m ∧ m < (n + 1) ^ 2 ∧ m.Prime := by
  simp only [survivors, Finset.mem_sdiff, mem_covered, squareInterval, Finset.mem_Ioo]
  constructor
  · rintro ⟨⟨hlo, hhi⟩, hnot⟩
    refine ⟨hlo, hhi, (prime_iff_no_small_divisor hn hlo hhi).mpr ?_⟩
    intro p hp hpn hpm
    exact hnot ⟨⟨hlo, hhi⟩, p, hp, hpn, hpm⟩
  · rintro ⟨hlo, hhi, hp⟩
    refine ⟨⟨hlo, hhi⟩, ?_⟩
    rintro ⟨_, p, hpp, hpn, hpm⟩
    exact (prime_iff_no_small_divisor hn hlo hhi).mp hp p hpp hpn hpm

/-- LEAN-CERTIFIED: Exact complement cardinality; no independence assumption occurs. -/
theorem survivors_card (n : ℕ) :
    (survivors n).card = 2 * n - (covered n).card := by
  rw [survivors, Finset.card_sdiff (covered_subset n), squareInterval_card]

/-- LEAN-CERTIFIED: The finite-union inequality is equivalent to the Legendre instance. -/
theorem union_card_lt_iff_prime_exists (n : ℕ) (hn : 1 ≤ n) :
    (covered n).card < 2 * n ↔ ∃ p, p.Prime ∧ n ^ 2 < p ∧ p < (n + 1) ^ 2 := by
  rw [← Nat.sub_pos_iff_lt, ← survivors_card, Finset.card_pos]
  simp only [Finset.Nonempty, mem_survivors hn]
  constructor
  · rintro ⟨p, hlo, hhi, hp⟩
    exact ⟨p, hp, hlo, hhi⟩
  · rintro ⟨p, hp, hlo, hhi⟩
    exact ⟨p, hlo, hhi, hp⟩

/-- ESTABLISHED: The divisor sum of the Möbius function is the unit indicator. -/
theorem moebius_divisor_sum (k : ℕ) :
    (∑ d ∈ k.divisors, ArithmeticFunction.moebius d) = if k = 1 then 1 else 0 := by
  rw [← ArithmeticFunction.coe_mul_zeta_apply,
    ArithmeticFunction.moebius_mul_coe_zeta, ArithmeticFunction.one_apply]

/-- ESTABLISHED: Filtering divisors by divisibility gives the divisors of the gcd. -/
theorem filter_divisors_gcd (m Q : ℕ) (hQ : Q ≠ 0) :
    Q.divisors.filter (fun d => d ∣ m) = (Nat.gcd m Q).divisors := by
  have hg : Nat.gcd m Q ≠ 0 := ne_of_gt (Nat.gcd_pos_of_pos_right m (Nat.pos_of_ne_zero hQ))
  ext d
  simp [Finset.mem_filter, Nat.mem_divisors, hQ, hg, Nat.dvd_gcd_iff]
  exact and_comm

/-- ESTABLISHED: A finite Möbius sum is exactly the coprimality indicator. -/
theorem coprime_moebius_indicator (m Q : ℕ) (hQ : Q ≠ 0) :
    (∑ d ∈ Q.divisors, if d ∣ m then ArithmeticFunction.moebius d else 0) =
      if Nat.Coprime m Q then (1 : ℤ) else 0 := by
  rw [← Finset.sum_filter, filter_divisors_gcd m Q hQ, moebius_divisor_sum]

/-- ESTABLISHED: Exact Möbius inversion for the number of coprime elements of any finite set. -/
theorem coprime_card_moebius (A : Finset ℕ) (Q : ℕ) (hQ : Q ≠ 0) :
    ((A.filter (fun m => Nat.Coprime m Q)).card : ℤ) =
      ∑ d ∈ Q.divisors, ArithmeticFunction.moebius d *
        ((A.filter (fun m => d ∣ m)).card : ℤ) := by
  calc
    _ = ∑ m ∈ A, if Nat.Coprime m Q then (1 : ℤ) else 0 := by simp
    _ = ∑ m ∈ A, ∑ d ∈ Q.divisors,
        if d ∣ m then ArithmeticFunction.moebius d else 0 := by
      apply Finset.sum_congr rfl
      intro m _
      exact (coprime_moebius_indicator m Q hQ).symm
    _ = ∑ d ∈ Q.divisors, ∑ m ∈ A,
        if d ∣ m then ArithmeticFunction.moebius d else 0 := Finset.sum_comm
    _ = _ := by
      apply Finset.sum_congr rfl
      intro d _
      rw [← Finset.sum_filter]
      simp [mul_comm]

/-- ESTABLISHED: Definition of the product of all sieving primes. -/
def smallPrimorial (n : ℕ) : ℕ := ∏ p ∈ smallPrimes n, p

/-- ESTABLISHED: The empty-product convention also makes this positive at n=1. -/
theorem smallPrimorial_pos (n : ℕ) : 0 < smallPrimorial n := by
  apply Finset.prod_pos
  intro p hp
  exact (mem_smallPrimes.mp hp).1.pos

/-- ESTABLISHED: Coprimality to the primorial is exactly avoidance of every sieving prime. -/
theorem coprime_smallPrimorial (n m : ℕ) :
    Nat.Coprime m (smallPrimorial n) ↔ ∀ p, p.Prime → p ≤ n → ¬p ∣ m := by
  rw [smallPrimorial, Nat.coprime_prod_right_iff]
  constructor
  · intro h p hp hpn
    exact hp.coprime_iff_not_dvd.mp (h p (mem_smallPrimes.mpr ⟨hp, hpn⟩)).symm
  · intro h p hp
    obtain ⟨hpp, hpn⟩ := mem_smallPrimes.mp hp
    exact (hpp.coprime_iff_not_dvd.mpr (h p hpp hpn)).symm

/-- ESTABLISHED: The certified sieve complement agrees with the coprimality filter. -/
theorem survivors_eq_coprime_filter (n : ℕ) (hn : 1 ≤ n) :
    survivors n = (squareInterval n).filter (fun m => Nat.Coprime m (smallPrimorial n)) := by
  ext m
  rw [mem_survivors hn, Finset.mem_filter]
  simp only [squareInterval, Finset.mem_Ioo]
  constructor
  · rintro ⟨hlo, hhi, hp⟩
    exact ⟨⟨hlo, hhi⟩, (coprime_smallPrimorial n m).mpr
      ((prime_iff_no_small_divisor hn hlo hhi).mp hp)⟩
  · rintro ⟨⟨hlo, hhi⟩, hc⟩
    exact ⟨hlo, hhi, (prime_iff_no_small_divisor hn hlo hhi).mpr
      ((coprime_smallPrimorial n m).mp hc)⟩

/-- ESTABLISHED: The Legendre survivor count is an exact Möbius-weighted multiple count. -/
theorem survivors_moebius_counts (n : ℕ) (hn : 1 ≤ n) :
    ((survivors n).card : ℤ) =
      ∑ d ∈ (smallPrimorial n).divisors, ArithmeticFunction.moebius d *
        (((squareInterval n).filter (fun m => d ∣ m)).card : ℤ) := by
  rw [survivors_eq_coprime_filter n hn]
  exact coprime_card_moebius _ _ (ne_of_gt (smallPrimorial_pos n))

/-- ESTABLISHED: Counting interval multiples gives a difference of integer quotients. -/
theorem squareInterval_multiples_card (n d : ℕ) :
    ((squareInterval n).filter (fun m => d ∣ m)).card =
      (n ^ 2 + 2 * n) / d - n ^ 2 / d := by
  have hs : (squareInterval n).filter (fun m => d ∣ m) =
      ((Finset.Ioc 0 (n ^ 2 + 2 * n)).filter (fun m => d ∣ m)) \
      ((Finset.Ioc 0 (n ^ 2)).filter (fun m => d ∣ m)) := by
    ext m
    simp only [squareInterval, Finset.mem_filter, Finset.mem_Ioo,
      Finset.mem_sdiff, Finset.mem_Ioc]
    constructor
    · rintro ⟨⟨hlo, hhi⟩, hd⟩
      refine ⟨⟨⟨by omega, by nlinarith⟩, hd⟩, ?_⟩
      rintro ⟨⟨_, hle⟩, _⟩
      omega
    · rintro ⟨⟨⟨hmpos, hmub⟩, hd⟩, hnot⟩
      refine ⟨⟨?_, by nlinarith⟩, hd⟩
      by_contra h
      exact hnot ⟨⟨hmpos, by omega⟩, hd⟩
  have hsub : ((Finset.Ioc 0 (n ^ 2)).filter (fun m => d ∣ m)) ⊆
      ((Finset.Ioc 0 (n ^ 2 + 2 * n)).filter (fun m => d ∣ m)) := by
    intro m hm
    simp only [Finset.mem_filter, Finset.mem_Ioc] at *
    exact ⟨⟨hm.1.1, by omega⟩, hm.2⟩
  rw [hs, Finset.card_sdiff hsub, Nat.Ioc_filter_dvd_card_eq_div,
    Nat.Ioc_filter_dvd_card_eq_div]

/-- ESTABLISHED: Exact floor-quotient Möbius formula for the Legendre survivor count. -/
theorem survivors_moebius_floor (n : ℕ) (hn : 1 ≤ n) :
    ((survivors n).card : ℤ) =
      ∑ d ∈ (smallPrimorial n).divisors, ArithmeticFunction.moebius d *
        (((n ^ 2 + 2 * n) / d - n ^ 2 / d : ℕ) : ℤ) := by
  simpa only [squareInterval_multiples_card] using survivors_moebius_counts n hn

/-- ESTABLISHED: Loop threshold used to split the small-prime and large-prime phases.
    This is an abstract threshold; cube-root reduction supplies y = floor(cuberoot(U)). -/
def thresholdPrimes (n y : ℕ) : Finset ℕ :=
  (smallPrimes n).filter (fun p => p ≤ y)

/-- ESTABLISHED: Large-prime phase covers precisely the complement of the threshold set. -/
def largePrimes (n y : ℕ) : Finset ℕ :=
  (smallPrimes n).filter (fun p => y < p)

/-- ESTABLISHED: Union of interval multiples removed in the cube-root phase. -/
def smallPhaseCovered (n y : ℕ) : Finset ℕ :=
  (thresholdPrimes n y).biUnion
    (fun p => (squareInterval n).filter (fun m => p ∣ m))

/-- ESTABLISHED: Union of interval multiples first removed in the large-prime phase. -/
def largePhaseCovered (n y : ℕ) : Finset ℕ :=
  (largePrimes n y).biUnion
    (fun p => (squareInterval n).filter (fun m => p ∣ m))

/-- ESTABLISHED: At each small-prime phase step, a candidate enters state 1 exactly
    when the selected prime divides it. -/
theorem mem_smallPhaseCovered {n y m : ℕ} :
    m ∈ smallPhaseCovered n y ↔
      m ∈ squareInterval n ∧ ∃ p, p.Prime ∧ p ≤ y ∧ p ≤ n ∧ p ∣ m := by
  simp only [smallPhaseCovered, thresholdPrimes, Finset.mem_biUnion, Finset.mem_filter,
    Finset.mem_filter, mem_smallPrimes]
  constructor
  · rintro ⟨p, ⟨⟨hp, hpn⟩, hpy⟩, hm, hpm⟩
    exact ⟨hm, p, hp, hpy, hpn, hpm⟩
  · rintro ⟨hm, p, hp, hpy, hpn, hpm⟩
    exact ⟨p, ⟨⟨hp, hpn⟩, hpy⟩, hm, hpm⟩

#print axioms moebius_divisor_sum
#print axioms filter_divisors_gcd
#print axioms coprime_moebius_indicator
#print axioms coprime_card_moebius
#print axioms smallPrimorial_pos
#print axioms coprime_smallPrimorial
#print axioms survivors_eq_coprime_filter
#print axioms survivors_moebius_counts
#print axioms squareInterval_multiples_card
#print axioms survivors_moebius_floor
#print axioms kernel_support_lower
#print axioms kernel_support_upper
#print axioms mem_smallPrimes
#print axioms squareInterval_card
#print axioms composite_has_small_prime_factor
#print axioms prime_iff_no_small_divisor
#print axioms covered_subset
#print axioms mem_covered
#print axioms mem_survivors
#print axioms survivors_card
#print axioms union_card_lt_iff_prime_exists
#print axioms mem_smallPhaseCovered

end LegendreAudit
