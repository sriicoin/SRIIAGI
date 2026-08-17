"""
SRIIAGI — Generate a readable pentest report from report.jsonl.
"""
import json, sys
from collections import Counter, defaultdict
from datetime import datetime

def generate(infile="report.jsonl", outfile="report.md"):
    results = [json.loads(l) for l in open(infile)]
    by_cat = defaultdict(list)
    for r in results:
        if "category" in r:
            by_cat[r["category"]].append(r)

    lines = [f"# SRIIAGI — LLM Jailbreak Assessment Report",
             f"**Date:** {datetime.now().isoformat()}",
             f"**Total tests:** {len(results)}",
             f"**Jailbroken:** {sum(1 for r in results if r.get('label')=='jailbroken')}",
             "",
             "## Per-category breakdown", ""]

    for cat, items in by_cat.items():
        labels = Counter(i.get("label") for i in items)
        lines.append(f"### {cat}: {dict(labels)}")
        for i in items:
            if i.get("label") == "jailbroken":
                lines.append(f"- **Payload:** `{i['payload']}`")
                lines.append(f"  - Encoder: {i.get('encoder')}")
                lines.append(f"  - Response: {i.get('response','')[:200]}")
        lines.append("")

    with open(outfile, "w") as f:
        f.write("\n".join(lines))
    print(f"[+] Report written to {outfile}")

if __name__ == "__main__":
    generate(*sys.argv[1:3] if len(sys.argv) > 1 else ())