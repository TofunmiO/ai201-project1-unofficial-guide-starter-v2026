#!/usr/bin/env python3
"""
Added this after feedback on my graded unit 1. Milestone 4: measure retrieval distances for the relevance cutoff.

Runs every question in `questions.QUESTIONS` (in-corpus) and
`questions.OUT_OF_SCOPE` (out-of-corpus) through `store.search`, records the
best distance for each, and writes the result to results/ as a JSON file whose
name encodes the settings it was measured with — so the numbers in the
README's "My relevance cutoff" table can be regenerated instead of taken on
faith.

    python measure_cutoff.py
    python measure_cutoff.py --top-k 4
"""

import argparse
import json

import config
import questions as qs
from store import search


def main():
    parser = argparse.ArgumentParser(description="Measure best retrieval distance per question.")
    parser.add_argument("--corpus", default=None)
    parser.add_argument("--variant", default="default")
    parser.add_argument("--top-k", type=int, default=None)
    args = parser.parse_args()

    corpus = args.corpus or config.CORPUS
    top_k = args.top_k or config.TOP_K

    rows = []
    for item in qs.answered():
        results = search(item["question"], top_k=top_k, corpus=corpus, variant=args.variant)
        best = min(results, key=lambda r: r.distance)
        rows.append({
            "question": item["question"],
            "in_corpus": True,
            "best_distance": best.distance,
            "best_source": best.source,
        })

    for question in qs.OUT_OF_SCOPE:
        results = search(question, top_k=top_k, corpus=corpus, variant=args.variant)
        best = min(results, key=lambda r: r.distance)
        rows.append({
            "question": question,
            "in_corpus": False,
            "best_distance": best.distance,
            "best_source": best.source,
        })

    out = {
        "produced_by": "measure_cutoff.py::main",
        "retrieval": "store.py::search",
        "corpus": corpus,
        "variant": args.variant,
        "top_k": top_k,
        "rows": rows,
    }

    config.RESULTS_DIR.mkdir(exist_ok=True)
    path = config.RESULTS_DIR / f"cutoff_{corpus}_topk{top_k}.json"
    path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    for row in rows:
        tag = "in " if row["in_corpus"] else "out"
        print(f"  [{tag}] {row['best_distance']:.4f}  {row['question']}")
    print(f"\nWrote {path.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
