"""Save the golden-set result of the prompt on main as the baseline."""
import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "supportdesk"))
import stand_in
from prompts import SYSTEM
from suite import run_suite

result = run_suite(stand_in.asker(stand_in.make_client(), SYSTEM))
(ROOT / "evals" / "baseline.json").write_text(json.dumps(result, indent=1) + "\n")
print("baseline saved:", sum(r["pass"] for r in result.values()), "of", len(result), "pass")
