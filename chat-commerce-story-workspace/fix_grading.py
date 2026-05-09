#!/usr/bin/env python3
import json, os

WORKSPACE = "/Users/ootashougo/Documents/claude-code-test/chat-commerce-story-workspace/iteration-1"

for ev in ["eval-1", "eval-2", "eval-3"]:
    for cfg in ["with_skill", "without_skill"]:
        path = os.path.join(WORKSPACE, ev, cfg, "run-1", "grading.json")
        with open(path) as f:
            g = json.load(f)
        # Add summary field expected by aggregate_benchmark.py
        passed = sum(1 for e in g["expectations"] if e["passed"])
        total = len(g["expectations"])
        g["summary"] = {
            "pass_rate": passed / total,
            "passed": passed,
            "failed": total - passed,
            "total": total
        }
        with open(path, "w") as f:
            json.dump(g, f, ensure_ascii=False, indent=2)
        print(f"{ev}/{cfg}: {passed}/{total}")
