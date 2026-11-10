# ruff: noqa: T201
import json
from pathlib import Path

from sentence_transformers import SentenceTransformer

from day9_rag.ask import load_vector_store, retrieve

BASE_DIR = Path(__file__).resolve().parent
GOLDEN_SET = BASE_DIR / "golden_set.json"

MODEL_NAME = "all-MiniLM-L6-v2"


def evaluate():
    golden = json.loads(GOLDEN_SET.read_text(encoding="utf-8"))

    embeddings, metadata = load_vector_store()

    model = SentenceTransformer(MODEL_NAME)

    results = []
    recall_counts = {1: 0, 3: 0, 5: 0}

    for item in golden:
        question = item["question"]
        expected = item["expected_chunk_id"]

        retrieved = retrieve(
            question,
            model,
            embeddings,
            metadata,
            top_k=5,
        )

        retrieved_ids = [chunk["chunk_id"] for chunk in retrieved]

        row = {
            "question": question,
            "expected_chunk_id": expected,
            "retrieved_chunk_ids": retrieved_ids,
        }

        for k in [1, 3, 5]:
            hit = expected in retrieved_ids[:k]

            row[f"recall_at_{k}"] = int(hit)

            recall_counts[k] += int(hit)

        results.append(row)

        print("\nQuestion:", question)
        print("Expected:", expected)
        print("Retrieved:", retrieved_ids)

    total = len(golden)

    print("\n========== RECALL RESULTS ==========")

    for k in [1, 3, 5]:
        score = recall_counts[k] / total

        print(f"Recall@{k}: {recall_counts[k]}/{total} = {score:.2%}")

    output = {
        "total_questions": total,
        "recall": {f"recall_at_{k}": recall_counts[k] / total for k in [1, 3, 5]},
        "results": results,
    }

    output_file = BASE_DIR / "evaluation_results.json"

    output_file.write_text(
        json.dumps(output, indent=2),
        encoding="utf-8",
    )

    print("\nResults saved to:", output_file)


if __name__ == "__main__":
    evaluate()
