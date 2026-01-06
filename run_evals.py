#!/usr/bin/env python3
"""
Sparkpilot Eval Runner

Runs lint on each scenario branch and compares results against expected findings.
"""

import subprocess
import sys
import os
import re
from dataclasses import dataclass
from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib


@dataclass
class Finding:
    rule_id: str
    file: str
    line: int
    level: str
    description: str = ""

    def __hash__(self):
        return hash((self.rule_id, self.file, self.line))

    def __eq__(self, other):
        if not isinstance(other, Finding):
            return False
        return (
            self.rule_id == other.rule_id
            and self.file == other.file
            and self.line == other.line
        )

    def matches(self, other: "Finding", line_tolerance: int = 3) -> bool:
        """Check if two findings match (with line number tolerance)."""
        return (
            self.rule_id == other.rule_id
            and self.file == other.file
            and abs(self.line - other.line) <= line_tolerance
        )


def get_scenario_branches() -> list[str]:
    """Get all scenario/* branches."""
    result = subprocess.run(
        ["git", "branch", "-r", "--list", "origin/scenario/*"],
        capture_output=True,
        text=True,
        check=True,
    )
    branches = []
    for line in result.stdout.strip().split("\n"):
        line = line.strip()
        if line and "origin/scenario/" in line:
            # Extract branch name without origin/ prefix
            branch = line.replace("origin/", "")
            branches.append(branch)
    return branches


def checkout_branch(branch: str) -> bool:
    """Checkout a branch."""
    result = subprocess.run(
        ["git", "checkout", branch],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def load_expected_findings(repo_path: Path) -> list[Finding]:
    """Load expected findings from .spark/expected.toml."""
    expected_path = repo_path / ".spark" / "expected.toml"
    if not expected_path.exists():
        return []

    with open(expected_path, "rb") as f:
        data = tomllib.load(f)

    findings = []
    for item in data.get("findings", []):
        findings.append(
            Finding(
                rule_id=item["rule_id"],
                file=item["file"],
                line=item["line"],
                level=item["level"],
                description=item.get("description", ""),
            )
        )
    return findings


def parse_lint_output(output: str) -> list[Finding]:
    """Parse spark lint output to extract findings."""
    findings = []
    current_file = None

    for line in output.split("\n"):
        # Match file header: "  📄  src/config/database.ts"
        file_match = re.match(r"^\s+📄\s+(.+)$", line)
        if file_match:
            current_file = file_match.group(1).strip()
            continue

        # Match finding: "    [E] L3:21 │ Message..."
        # or "    [W] L5:3 │ Message..."
        finding_match = re.match(
            r"^\s+\[([EW])\]\s+L(\d+):\d+\s+│\s+(.+)$", line
        )
        if finding_match and current_file:
            level_char = finding_match.group(1)
            line_num = int(finding_match.group(2))
            message = finding_match.group(3).strip()

            level = "error" if level_char == "E" else "warning"

            # Extract rule_id from the context (we need to track which policy section we're in)
            # For now, we'll need to get it from the summary section
            findings.append(
                Finding(
                    rule_id="",  # Will be filled in later
                    file=current_file,
                    line=line_num,
                    level=level,
                    description=message,
                )
            )

    return findings


def run_lint(repo_path: Path, spark_binary: str, convex_url: str, debug: bool = False) -> tuple[str, list[Finding]]:
    """Run spark lint and return output and parsed findings."""
    env = os.environ.copy()
    env["CONVEX_URL"] = convex_url

    result = subprocess.run(
        [spark_binary, "lint", "--all"],
        capture_output=True,
        text=True,
        cwd=repo_path,
        env=env,
        timeout=300,  # 5 minute timeout
    )

    output = result.stdout + result.stderr

    if debug:
        print(f"DEBUG: Output length: {len(output)}")
        print(f"DEBUG: First 500 chars: {repr(output[:500])}")

    # Parse findings with rule_id from the grouped output
    findings = []
    current_file = None

    lines = output.split("\n")
    for i, line in enumerate(lines):
        # Track current file - match emoji or text pattern
        # Pattern: "  📄  src/config/database.ts" or similar with whitespace
        if "📄" in line or (line.strip().startswith("src/") and not "[" in line):
            # Extract file path after emoji or at start
            if "📄" in line:
                parts = line.split("📄")
                if len(parts) > 1:
                    current_file = parts[1].strip()
            else:
                current_file = line.strip()
            if debug:
                print(f"DEBUG: Found file: {current_file}")
            continue

        # Match finding line: "    [E] L3:21 │ Message..." or "    [W] L5:3 │ Message..."
        # Use a more flexible pattern that handles various Unicode box-drawing chars
        finding_match = re.match(
            r"^\s+\[([EW])\]\s+L(\d+):\d+\s+[│|]\s+(.+)$", line
        )
        if finding_match and current_file:
            level_char = finding_match.group(1)
            line_num = int(finding_match.group(2))
            message = finding_match.group(3).strip()

            level = "error" if level_char == "E" else "warning"

            # Try to infer rule_id from message patterns
            rule_id = infer_rule_id(message)

            findings.append(
                Finding(
                    rule_id=rule_id,
                    file=current_file,
                    line=line_num,
                    level=level,
                    description=message,
                )
            )
            if debug:
                print(f"DEBUG: Found finding: {rule_id} @ {current_file}:{line_num}")

    return output, findings


def infer_rule_id(message: str) -> str:
    """Infer rule_id from finding message content."""
    message_lower = message.lower()

    # SQL injection patterns
    if "sql injection" in message_lower or "parameterized quer" in message_lower or "interpolat" in message_lower and "query" in message_lower:
        return "SQL_INJECTION"

    # Hardcoded secrets patterns
    if "hardcoded" in message_lower or "hard-coded" in message_lower or "hard coded" in message_lower:
        if any(x in message_lower for x in ["secret", "password", "key", "credential", "jwt", "api key", "connection string", "stripe"]):
            return "NO_HARDCODED_SECRETS"

    # Sensitive logging patterns
    if any(x in message_lower for x in ["logging", "log ", "logs "]):
        if any(x in message_lower for x in ["password", "token", "credential", "sensitive", "secret"]):
            return "NO_SENSITIVE_LOGGING"

    # Async error handling patterns
    if any(x in message_lower for x in ["try/catch", "try-catch", "error handling", "missing error", "unhandled promise rejection"]):
        return "ASYNC_ERROR_HANDLING"

    # Floating promises patterns
    if any(x in message_lower for x in ["floating promise", "not awaited", "is not awaited", "unawaited", "without await"]):
        return "FLOATING_PROMISES"

    # Rust unwrap patterns
    if any(x in message_lower for x in [".unwrap()", ".expect(", "can panic", "will panic"]):
        return "NO_UNWRAP"

    # Path handling patterns
    if "path" in message_lower and any(x in message_lower for x in ["utf-8", "utf8", "non-utf", "invalid"]):
        return "PATH_HANDLING"

    # Error context patterns
    if "error context" in message_lower or "anyhow" in message_lower:
        return "ERROR_CONTEXT"

    # Result ignored patterns
    if "result" in message_lower and "ignored" in message_lower:
        return "RESULT_IGNORED"

    return "UNKNOWN"


def compare_findings(
    expected: list[Finding], actual: list[Finding], line_tolerance: int = 3
) -> tuple[list[Finding], list[Finding], list[Finding]]:
    """
    Compare expected vs actual findings.

    Returns: (matched, missed, unexpected)
    """
    matched = []
    missed = []
    unexpected = list(actual)  # Start with all actual as potentially unexpected

    for exp in expected:
        found = False
        for i, act in enumerate(unexpected):
            if exp.matches(act, line_tolerance):
                matched.append(exp)
                unexpected.pop(i)
                found = True
                break
        if not found:
            missed.append(exp)

    return matched, missed, unexpected


def print_results(
    branch: str,
    expected: list[Finding],
    matched: list[Finding],
    missed: list[Finding],
    unexpected: list[Finding],
) -> bool:
    """Print eval results for a branch. Returns True if passed."""
    total_expected = len(expected)
    total_matched = len(matched)
    total_missed = len(missed)
    total_unexpected = len(unexpected)

    # Calculate pass rate
    if total_expected > 0:
        pass_rate = (total_matched / total_expected) * 100
    else:
        pass_rate = 100.0

    passed = total_missed == 0

    print(f"\n{'=' * 60}")
    print(f"Eval: {branch}")
    print(f"{'=' * 60}")
    print(f"Expected: {total_expected}  Matched: {total_matched}  Missed: {total_missed}  Unexpected: {total_unexpected}")
    print(f"Pass rate: {pass_rate:.1f}%")
    print()

    if matched:
        print("MATCHED:")
        for f in matched[:10]:  # Show first 10
            print(f"  ✓ {f.rule_id} @ {f.file}:{f.line}")
        if len(matched) > 10:
            print(f"  ... and {len(matched) - 10} more")
        print()

    if missed:
        print("MISSED (expected but not found):")
        for f in missed:
            print(f"  ✗ {f.rule_id} @ {f.file}:{f.line} - {f.description}")
        print()

    if unexpected:
        print("UNEXPECTED (found but not expected):")
        for f in unexpected[:10]:  # Show first 10
            print(f"  ? {f.rule_id} @ {f.file}:{f.line}")
        if len(unexpected) > 10:
            print(f"  ... and {len(unexpected) - 10} more")
        print()

    status = "PASSED" if passed else "FAILED"
    print(f"Result: {status}")

    return passed


def main():
    # Configuration
    repo_path = Path(__file__).parent.resolve()
    spark_binary = os.environ.get(
        "SPARK_BINARY",
        str(Path.home() / "sparkpilot-1" / "rust" / "target" / "release" / "spark"),
    )
    convex_url = os.environ.get(
        "CONVEX_URL", "https://adorable-wren-14.convex.cloud"
    )
    debug = "--debug" in sys.argv

    # Get scenario branches
    os.chdir(repo_path)
    branches = get_scenario_branches()

    if not branches:
        print("No scenario branches found!")
        sys.exit(1)

    print(f"Found {len(branches)} scenario branches: {', '.join(branches)}")
    print(f"Using spark binary: {spark_binary}")
    print(f"Using Convex URL: {convex_url}")

    all_passed = True
    results = []

    for branch in branches:
        print(f"\n{'─' * 60}")
        print(f"Running eval: {branch}")
        print(f"{'─' * 60}")

        # Checkout branch
        if not checkout_branch(branch):
            print(f"Failed to checkout {branch}")
            all_passed = False
            continue

        # Load expected findings
        expected = load_expected_findings(repo_path)
        if not expected:
            print(f"No expected.toml found for {branch}, skipping...")
            continue

        print(f"Loaded {len(expected)} expected findings")

        # Run lint
        print("Running spark lint --all...")
        output, actual = run_lint(repo_path, spark_binary, convex_url, debug=debug)

        print(f"Found {len(actual)} actual findings")

        # Compare
        matched, missed, unexpected = compare_findings(expected, actual)

        # Print results
        passed = print_results(branch, expected, matched, missed, unexpected)
        results.append((branch, passed, len(expected), len(matched), len(missed)))

        if not passed:
            all_passed = False

    # Summary
    print(f"\n{'=' * 60}")
    print("EVAL SUMMARY")
    print(f"{'=' * 60}")
    for branch, passed, expected, matched, missed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}  {branch}: {matched}/{expected} matched, {missed} missed")

    print()
    if all_passed:
        print("All evals passed!")
        sys.exit(0)
    else:
        print("Some evals failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
