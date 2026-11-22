"""Run the golden set: one result per case, did every behavioral check hold?"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "supportdesk"))
from checks import CHECKS

HERE = pathlib.Path(__file__).parent
GOLDEN = json.loads((HERE / "golden_set.json").read_text(encoding="utf-8"))


def run_suite(ask):
    results = {}
    for case in GOLDEN:
        response = ask(case["text"])
        outcomes = [CHECKS[name](response, arg) for name, arg in case["checks"]]
        failed = [why for ok, why in outcomes if not ok]
        results[case["id"]] = {"pass": not failed, "critical": case["critical"],
                               "failed": failed}
    return results
