from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def read_jsonl(path: Path):
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                yield json.loads(line)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--output", default="quarry/normalized/alpacka-ai-category-prefixes.json")
    args = parser.parse_args()

    one = Counter()
    two = Counter()
    three = Counter()
    examples: dict[str, list[str]] = {}

    for row in read_jsonl(Path(args.input)):
        if row.get("category_observed"):
            continue
        label = (row.get("raw_label_observed") or "").strip()
        tokens = label.split()
        if not tokens:
            continue
        p1 = " ".join(tokens[:1])
        p2 = " ".join(tokens[:2]) if len(tokens) >= 2 else p1
        p3 = " ".join(tokens[:3]) if len(tokens) >= 3 else p2
        one[p1] += 1
        two[p2] += 1
        three[p3] += 1
        examples.setdefault(p1, [])
        if len(examples[p1]) < 3:
            examples[p1].append(label[:240])

    result = {
        "unclassified_records": sum(one.values()),
        "first_token_counts": dict(one.most_common(80)),
        "first_two_token_counts": dict(two.most_common(100)),
        "first_three_token_counts": dict(three.most_common(100)),
        "examples_by_first_token": {k: examples[k] for k, _ in one.most_common(80)},
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status":"ok","unclassified_records":result["unclassified_records"],"output":str(output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
