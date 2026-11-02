import json
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
CHUNKS_DIR = BASE_DIR / "chunks"
DB_DIR = BASE_DIR / "vector_db"

STRATEGIES = ["fixed", "overlap", "paragraph"]


def main():
    logger.info("Loading embedding model...")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    client = chromadb.PersistentClient(path=str(DB_DIR))

    for strategy in STRATEGIES:
        path = CHUNKS_DIR / f"{strategy}.json"

        chunks = json.loads(path.read_text(encoding="utf-8"))

        if not chunks:
            raise ValueError(f"No chunks found for {strategy}")

        collection = client.get_or_create_collection(
            name=f"policies_{strategy}",
            metadata={"hnsw:space": "cosine"},
        )

        ids = [f"{strategy}_{index}" for index in range(len(chunks))]

        texts = [chunk["text"] for chunk in chunks]

        metadatas = [{"document": chunk["document"]} for chunk in chunks]

        logger.info(
            "Embedding %d %s chunks...",
            len(texts),
            strategy,
        )

        embeddings = model.encode(
            texts,
            normalize_embeddings=True,
        ).tolist()

        collection.upsert(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        logger.info(
            "%s: %d vectors stored",
            strategy,
            collection.count(),
        )

    logger.info("Vector store created successfully!")


if __name__ == "__main__":
    main()
