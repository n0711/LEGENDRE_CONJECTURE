"""Run Lean and reject missing audits or nonstandard proof assumptions."""

from pathlib import Path
import re
import subprocess


ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def check_audit(source: str, output: str) -> None:
    """Require one clean axiom report for every local theorem."""
    expected = {
        f"LegendreAudit.{name}"
        for name in re.findall(r"^theorem\s+(\w+)", source, re.MULTILINE)
    }
    if not expected:
        raise ValueError("No theorem declarations found")
    reports = {}
    for name, assumptions in re.findall(
        r"'([^']+)' depends on axioms: \[([^\]]*)\]", output
    ):
        reports[name] = {a.strip() for a in assumptions.split(",") if a.strip()}
    for name in re.findall(r"'([^']+)' does not depend on any axioms", output):
        reports[name] = set()
    if expected != set(reports):
        raise ValueError(f"Axiom-report mismatch: {expected ^ set(reports)}")
    for name, assumptions in reports.items():
        unexpected = assumptions - ALLOWED_AXIOMS
        if unexpected:
            raise ValueError(f"Disallowed assumptions in {name}: {unexpected}")


def main() -> None:
    directory = Path(__file__).resolve().parent
    source = (directory / "LegendreAudit.lean").read_text(encoding="utf-8")
    result = subprocess.run(
        ["lake", "env", "lean", "LegendreAudit.lean"],
        cwd=directory,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    print(result.stdout, end="")
    print(result.stderr, end="")
    result.check_returncode()
    check_audit(source, result.stdout)
    print("PASS: every local theorem checked; only the declared Lean foundations occur.")


if __name__ == "__main__":
    main()
