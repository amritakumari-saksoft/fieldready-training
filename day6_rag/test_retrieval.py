import csv
import logging
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "vector_db"

QUESTIONS = [
    ("How long does standard delivery take?", "01_delivery_times.txt"),
    ("What should I do if my parcel is late?", "02_delayed_parcels.txt"),
    ("How can I track my parcel?", "03_tracking.txt"),
    ("How do I report a damaged parcel?", "04_damaged_parcels.txt"),
    ("When is a parcel considered lost?", "05_lost_parcels.txt"),
    ("How long do refunds take?", "06_refunds.txt"),
    ("How many delivery attempts are made?", "07_delivery_attempts.txt"),
    ("Can I change my delivery address?", "08_address_changes.txt"),
    ("Can I cancel my shipment?", "09_cancellations.txt"),
    ("How do I return a parcel?", "10_returns.txt"),
]

STRATEGIES = ["fixed", "overlap", "paragraph"]


def main() -> None:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path=str(DB_DIR))

    results: list[dict[str, str | int]] = []

    for strategy in STRATEGIES:
        collection = client.get_collection(name=f"policies_{strategy}")

        logger.info("\n--- Testing %s ---", strategy.upper())

        correct_top1 = 0
        correct_top3 = 0

        if collection.count() == 0:
            raise ValueError(f"Collection policies_{strategy} is empty")

        for question, expected_document in QUESTIONS:
            query_embedding = model.encode(
                [question],
                normalize_embeddings=True,
            ).tolist()

            response = collection.query(
                query_embeddings=query_embedding,
                n_results=min(3, collection.count()),
                include=["documents", "metadatas", "distances"],
            )

            # Validate ChromaDB metadata
            retrieved_metadatas = response["metadatas"]

            if not retrieved_metadatas or not retrieved_metadatas[0]:
                raise ValueError("No metadata returned from ChromaDB")

            retrieved_documents: list[str] = []

            for metadata in retrieved_metadatas[0]:
                document_name = metadata.get("document")

                if not isinstance(document_name, str):
                    raise ValueError("Invalid document metadata")

                retrieved_documents.append(document_name)

            # Calculate retrieval accuracy
            top1 = expected_document == retrieved_documents[0]
            top3 = expected_document in retrieved_documents

            correct_top1 += int(top1)
            correct_top3 += int(top3)

            logger.info("\nQuestion: %s", question)
            logger.info("Expected: %s", expected_document)
            logger.info("Retrieved: %s", retrieved_documents)
            logger.info("Top-1 correct: %s", top1)
            logger.info("Top-3 correct: %s", top3)

            results.append(
                {
                    "strategy": strategy,
                    "question": question,
                    "expected_document": expected_document,
                    "retrieved_documents": " | ".join(retrieved_documents),
                    "top1_correct": int(top1),
                    "top3_correct": int(top3),
                }
            )

        logger.info(
            "\nTop-1 accuracy: %d/%d",
            correct_top1,
            len(QUESTIONS),
        )

        logger.info(
            "Top-3 accuracy: %d/%d",
            correct_top3,
            len(QUESTIONS),
        )

    # Save results to CSV
    output_file = BASE_DIR / "retrieval_results.csv"

    fieldnames = [
        "strategy",
        "question",
        "expected_document",
        "retrieved_documents",
        "top1_correct",
        "top3_correct",
    ]

    with output_file.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    logger.info("\nResults saved to %s", output_file)


if __name__ == "__main__":
    main()
