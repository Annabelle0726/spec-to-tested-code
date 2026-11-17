"""Replay one test suite against the before and after implementations."""

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


RUNNER = """
import json
import unittest
suite = unittest.defaultTestLoader.discover('.', pattern='test_order.py')
result = unittest.TextTestRunner(verbosity=2).run(suite)
print(json.dumps({
    'tests': result.testsRun,
    'failures': len(result.failures),
    'errors': len(result.errors),
    'skipped': len(result.skipped),
}))
raise SystemExit(0 if result.wasSuccessful() else 1)
"""


def run_phase(phase):
    root = Path(__file__).resolve().parent
    source = root / ("before.py" if phase == "red" else "order.py")
    with tempfile.TemporaryDirectory(prefix="order-example-") as directory:
        work = Path(directory)
        shutil.copyfile(source, work / "order.py")
        shutil.copyfile(root / "test_order.py", work / "test_order.py")
        result = subprocess.run(
            [sys.executable, "-B", "-c", RUNNER], cwd=work,
            capture_output=True, text=True, timeout=30,
        )
    print(f"[{phase}]", file=sys.stderr)
    print(result.stderr, file=sys.stderr, end="")
    summary = json.loads(result.stdout)
    summary.update(phase=phase, exit_code=result.returncode)
    print(json.dumps(summary))
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=("red", "green", "all"), default="all")
    phase = parser.parse_args().phase
    if phase != "all":
        return run_phase(phase)["exit_code"]
    red, green = run_phase("red"), run_phase("green")
    valid = (
        red["exit_code"] == 1 and red["failures"] > 0
        and red["errors"] == 0 and red["skipped"] == 0
        and green["exit_code"] == 0 and green["failures"] == 0
        and green["errors"] == 0 and green["skipped"] == 0
        and red["tests"] == green["tests"] and green["tests"] > 0
    )
    print("RED -> GREEN verified" if valid else "Unexpected test outcome")
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
