"""The CI eval gate. Runs the golden set on the prompt in this commit,
compares with the baseline from main, and checks the release criteria.
Exit code 1 fails the check, and the pull request cannot merge."""
import json, os, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "supportdesk"))
import stand_in
from prompts import SYSTEM
from suite import run_suite

MIN_PASS_RATE = 1.0          # release criterion: every golden case passes

baseline = json.loads((ROOT / "evals" / "baseline.json").read_text())
current = run_suite(stand_in.asker(stand_in.make_client(), SYSTEM))

rows = []
for cid, r in current.items():
    was = "pass" if baseline[cid]["pass"] else "FAIL"
    now = "pass" if r["pass"] else "FAIL"
    tag = " critical" if r["critical"] else ""
    why = "; ".join(r["failed"])
    rows.append(f"{cid}{tag}: baseline {was} -> now {now} {why}".rstrip())
    print(rows[-1])

regressions = [c for c in current if baseline[c]["pass"] and not current[c]["pass"]]
critical = [c for c in current if current[c]["critical"] and not current[c]["pass"]]
rate = sum(r["pass"] for r in current.values()) / len(current)

criteria = [("no regressions against main", not regressions),
            ("every critical case passes", not critical),
            (f"pass rate {rate:.0%} (needs {MIN_PASS_RATE:.0%})", rate >= MIN_PASS_RATE)]
for name, ok in criteria:
    print(("PASS " if ok else "FAIL ") + name)
release = all(ok for _, ok in criteria)
print("decision:", "release" if release else "block the merge")

summary = os.getenv("GITHUB_STEP_SUMMARY")
if summary:
    with open(summary, "a", encoding="utf-8") as f:
        f.write("## Eval gate\n\n" + "\n".join(f"- {r}" for r in rows) + "\n\n")
        f.write("\n".join(f"- {'✅' if ok else '❌'} {n}" for n, ok in criteria))
        f.write(f"\n\n**{'release' if release else 'block the merge'}**\n")
sys.exit(0 if release else 1)
