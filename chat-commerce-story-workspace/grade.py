#!/usr/bin/env python3
import json
import os

WORKSPACE = "/Users/ootashougo/Documents/claude-code-test/chat-commerce-story-workspace/iteration-1"

ASSERTIONS = [
    {
        "id": "has-service-overview",
        "description": "サービスのジャンルと概要セクションが含まれているか",
        "keywords": ["ジャンル", "サービス概要", "ブランド概要", "サービス・ブランドの特徴"]
    },
    {
        "id": "has-product-ranking",
        "description": "人気商品が3件以上リストされているか",
        "keywords": ["コンパクトホットプレート", "カタログギフト", "エアフライヤー", "ブレンダー", "ガラスエアフライヤー"],
        "min_count": 3
    },
    {
        "id": "has-first-visitor-pattern",
        "description": "初回訪問者向けストーリーパターンが含まれているか",
        "keywords": ["初回"]
    },
    {
        "id": "has-repeat-customer-pattern",
        "description": "リピーター向けストーリーパターンが含まれているか",
        "keywords": ["リピーター"]
    },
    {
        "id": "has-vip-pattern",
        "description": "VIP向けストーリーパターンが含まれているか",
        "keywords": ["VIP"]
    },
    {
        "id": "has-conversation-format",
        "description": "ボットの発言と選択肢形式の会話フローが含まれているか",
        "keywords": ["ボット", "BOT", "[選択肢]", "🤖"]
    },
    {
        "id": "has-purchase-cta",
        "description": "購入誘導（商品ページ/カート）への誘導が含まれているか",
        "keywords": ["カート", "商品を見る", "購入"]
    },
]

def grade_file(filepath):
    try:
        with open(filepath, "r") as f:
            content = f.read()
    except FileNotFoundError:
        return None

    results = []
    for a in ASSERTIONS:
        if "min_count" in a:
            count = sum(1 for kw in a["keywords"] if kw in content)
            passed = count >= a["min_count"]
            evidence = f"{count}/{a['min_count']} 件の商品キーワードを検出"
        else:
            found = [kw for kw in a["keywords"] if kw in content]
            passed = len(found) > 0
            evidence = f"検出キーワード: {found}" if found else f"キーワード未検出: {a['keywords']}"
        results.append({
            "text": a["description"],
            "passed": passed,
            "evidence": evidence
        })
    return results

evals = ["eval-1", "eval-2", "eval-3"]
configs = ["with_skill", "without_skill"]

for ev in evals:
    for cfg in configs:
        path = os.path.join(WORKSPACE, ev, cfg, "outputs", "result.md")
        grading_path = os.path.join(WORKSPACE, ev, cfg, "grading.json")
        grades = grade_file(path)
        if grades:
            passed = sum(1 for g in grades if g["passed"])
            total = len(grades)
            grading = {
                "eval_id": ev,
                "config": cfg,
                "pass_rate": passed / total,
                "passed": passed,
                "total": total,
                "expectations": grades
            }
            with open(grading_path, "w") as f:
                json.dump(grading, f, ensure_ascii=False, indent=2)
            print(f"{ev}/{cfg}: {passed}/{total} ({passed/total*100:.0f}%)")
        else:
            print(f"{ev}/{cfg}: FILE NOT FOUND")
