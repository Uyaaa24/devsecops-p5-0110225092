import json
import sys

THRESHOLDS = {"HIGH": 0, "MEDIUM": 0, "LOW": 10}

with open("bandit-report.json", encoding="utf-8") as f:
    data = json.load(f)

counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
for issue in data["results"]:
    counts[issue["issue_severity"]] += 1

print("=== Quality Gate: Hasil SAST (Bandit) ===")
failed = False
for level, limit in THRESHOLDS.items():
    status = "OK" if counts[level] <= limit else "GAGAL"
    print(f"{level:7} temuan={counts[level]:3} batas={limit:3} -> {status}")
    if counts[level] > limit:
        failed = True

for issue in data["results"]:
    print(f"- [{issue['issue_severity']}] {issue['test_id']} "
          f"{issue['filename']}:{issue['line_number']} - {issue['issue_text']}")

if failed:
    print("QUALITY GATE: FAILED")
    sys.exit(1)
print("QUALITY GATE: PASSED")