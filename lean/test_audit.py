"""Regression checks for accepting and rejecting Lean assumption reports."""

import unittest

from audit import check_audit


class AuditTests(unittest.TestCase):
    source = "theorem example : True := by trivial\n"

    def test_standard_foundations(self):
        check_audit(
            self.source,
            "'LegendreAudit.example' depends on axioms: "
            "[propext, Classical.choice, Quot.sound]",
        )

    def test_no_assumptions(self):
        check_audit(
            self.source,
            "'LegendreAudit.example' does not depend on any axioms",
        )

    def test_incomplete_or_custom_assumption_rejected(self):
        for assumption in ("sorryAx", "UnprovedRH"):
            with self.subTest(assumption=assumption), self.assertRaises(ValueError):
                check_audit(
                    self.source,
                    f"'LegendreAudit.example' depends on axioms: [{assumption}]",
                )

    def test_missing_report_rejected(self):
        with self.assertRaises(ValueError):
            check_audit(self.source, "")

    def test_empty_source_rejected(self):
        with self.assertRaises(ValueError):
            check_audit("", "")


if __name__ == "__main__":
    unittest.main()
