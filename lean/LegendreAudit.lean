import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Data.Nat.Prime
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

end LegendreAudit
