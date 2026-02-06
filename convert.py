#!/usr/bin/env python3
"""Convert an HLE parquet file to questions.json for the web viewer."""

import json
import sys
import pandas as pd


def convert(parquet_path, output_path="questions.json"):
    df = pd.read_parquet(parquet_path)
    records = []
    for _, row in df.iterrows():
        records.append({
            "id": row["id"],
            "question": row["question"],
            "image": row["image"] if row["image"] else None,
            "answer": row["answer"],
            "answer_type": row["answer_type"],
            "author": row["author_name"] if row["author_name"] else None,
            "rationale": row["rationale"] if row["rationale"] else None,
            "subject": row["raw_subject"] if row["raw_subject"] else None,
            "category": row["category"] if row["category"] else None,
        })
    with open(output_path, "w") as f:
        json.dump(records, f)
    print(f"Converted {len(records)} questions to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert.py <parquet_file> [output.json]")
        sys.exit(1)
    parquet_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "questions.json"
    convert(parquet_path, output_path)
