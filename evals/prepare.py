"""Prepare fresh local fixtures for independent skill behavior evaluation."""

import hashlib
import json
from pathlib import Path
import shutil
import tempfile


def snapshot(directory):
    return {
        file.relative_to(directory).as_posix(): hashlib.sha256(file.read_bytes()).hexdigest()
        for file in sorted(directory.rglob("*")) if file.is_file()
    }


def main():
    project = Path(__file__).resolve().parents[1]
    example = project / "examples" / "order-cancellation"
    root = Path(tempfile.mkdtemp(prefix="spec-workflow-eval-"))
    skill = root / "skill"
    skill.mkdir()
    shutil.copy2(project / "SKILL.md", skill / "SKILL.md")
    shutil.copytree(project / "references", skill / "references")
    cases = json.loads((project / "evals" / "cases.json").read_text(encoding="utf-8"))
    manifest = {"skill": snapshot(skill), "cases": {}}
    for case in cases:
        workspace = root / case["id"]
        workspace.mkdir()
        source = "order.py" if case["id"] == "environment-unavailable" else "before.py"
        shutil.copy2(example / source, workspace / "order.py")
        if case["id"] != "spec-only":
            shutil.copy2(example / "SPEC.md", workspace / "SPEC.md")
        (workspace / "user-notes.txt").write_text("Existing user note: keep this file unchanged.\n", encoding="utf-8")
        (workspace / "inventory.json").write_text('{"reserved": 7}\n', encoding="utf-8")
        (workspace / "ledger.json").write_text('{"refunds": []}\n', encoding="utf-8")
        if case["id"] in ("environment-unavailable", "review-only"):
            shutil.copy2(example / "test_order.py", workspace / "test_order.py")
        if case["id"] == "environment-unavailable":
            shutil.copy2(project / "evals" / "fixtures" / "verify_integration.py", workspace / "verify_integration.py")
            (workspace / "CHECKS.md").write_text(
                "# Project checks\n\n"
                "Run `python -B -m unittest discover -s . -p test_order.py -v` and "
                "`python -B verify_integration.py`.\n\n"
                "The integration fixture expects an externally provisioned database at "
                "`environment/orders.sqlite`. This environment does not provide that database. "
                "Provisioning or replacing it is outside this task.\n",
                encoding="utf-8",
            )
        manifest["cases"][case["id"]] = snapshot(workspace)
    (root / "manifest-before.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(root)
    print("Skill snapshot: skill/SKILL.md; each case has its own workspace.")
    print("Provide only the chosen request, skill snapshot and case workspace to the evaluator.")


if __name__ == "__main__":
    main()
