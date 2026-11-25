import Mathlib

/-- The exact real logarithmic support parameter used by the triangular kernel. -/
def kernelHalfWidth (n : ℕ) : ℝ :=
  Real.log (1 + (1 : ℝ) / n)

/-- The geometric midpoint of the consecutive-square interval. -/
def geometricMidpoint (n : ℕ) : ℝ :=
  (n : ℝ) * (n + 1)

theorem kernel_support_lower (n : ℕ) (hn : 0 < n) :
    geometricMidpoint n * Real.exp (-kernelHalfWidth n) = (n : ℝ) ^ 2 := by
  have hn0 : (n : ℝ) ≠ 0 := by
    exact_mod_cast (Nat.ne_of_gt hn)
  simp [geometricMidpoint, kernelHalfWidth]
  field_simp [hn0]
  rw [Real.exp_log]
  · ring
  · positivity
