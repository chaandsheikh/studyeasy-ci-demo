"""Read the JSON from claude -p and post each finding as an inline PR comment.
REVIEW_MODE=shadow: post, never fail.  REVIEW_MODE=gate: fail on any high finding."""
import json, os, subprocess, sys

out = json.load(open(sys.argv[1], encoding="utf-8"))
review = out.get("structured_output") or json.loads(out["result"])
findings = review["findings"]
mode = os.getenv("REVIEW_MODE") or "shadow"
repo, pr = os.environ["GITHUB_REPOSITORY"], os.environ["PR_NUMBER"]
api = f"repos/{repo}/pulls/{pr}/comments"

posted = json.loads(subprocess.run(["gh", "api", api, "--paginate"],
                                   capture_output=True, text=True, check=True).stdout)
seen = {(c["path"], c.get("line"), c["body"]) for c in posted}

for f in findings:
    body = f"**{f['severity']}** {f['message']}"
    if mode == "shadow":
        body += "\n\n_AI review in shadow mode: this does not block the merge._"
    print(f"{f['file']}:{f['line']} [{f['severity']}] {f['message']}")
    if (f["file"], f["line"], body) in seen:
        print("  already posted, skipped")
        continue
    subprocess.run(["gh", "api", api, "-f", f"body={body}", "-f", f"path={f['file']}",
                    "-F", f"line={f['line']}", "-f", "side=RIGHT",
                    "-f", f"commit_id={os.environ['HEAD_SHA']}"],
                   check=True, capture_output=True)
    print("  posted as an inline comment")

high = [f for f in findings if f["severity"] == "high"]
print(f"{len(findings)} findings, {len(high)} high, mode {mode}")
if mode == "gate" and high:
    print("gate: a high finding blocks the merge")
    sys.exit(1)
