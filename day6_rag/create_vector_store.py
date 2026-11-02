import json
import logging
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
CHUNKS_DIR = BASE_DIR / "chunks"
DB_DIR = BASE_DIR / "vector_store"

STRATEGIES = ["fixed", "overlap", "paragraph"]


def main() -> None:
    DB_DIR.mkdir(parents=True, exist_ok=True)

    logger.info("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    for strategy in STRATEGIES:
        chunk_file = CHUNKS_DIR / f"{strategy}.json"

        chunks = json.loads(chunk_file.read_text(encoding="utf-8"))

        if not chunks:
            raise ValueError(f"No chunks found for {strategy}")

        texts = [chunk["text"] for chunk in chunks]

        logger.info(
            "Generating embeddings for %d %s chunks...",
            len(texts),
            strategy,
        )

        embeddings = model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
        )

        embeddings = np.asarray(
            embeddings,
            dtype=np.float32,
        )

        np.save(
            DB_DIR / f"{strategy}_embeddings.npy",
            embeddings,
        )

        metadata = [
            {
                "document": chunk["document"],
                "chunk_id": chunk["chunk_id"],
                "text": chunk["text"],
            }
            for chunk in chunks
        ]

        metadata_file = DB_DIR / f"{strategy}_metadata.json"

        metadata_file.write_text(
            json.dumps(
                metadata,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        logger.info(
            "%s: %d vectors stored",
            strategy,
            len(embeddings),
        )

    logger.info("Vector store created successfully!")


if __name__ == "__main__":
    main()
