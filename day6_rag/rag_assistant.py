import json
import logging
from pathlib import Path

import numpy as np
import ollama
from sentence_transformers import SentenceTransformer

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
STORE_DIR = BASE_DIR / "vector_store"
MODEL_NAME = "qwen3.5:2b"


def answer_question(question: str) -> None:
    logger.info("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    embeddings_path = STORE_DIR / "paragraph_embeddings.npy"
    metadata_path = STORE_DIR / "paragraph_metadata.json"

    embeddings = np.load(embeddings_path, allow_pickle=False)
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

    if len(embeddings) == 0 or len(embeddings) != len(metadata):
        raise ValueError("Invalid or empty vector store")

    # Convert the customer question into an embedding.
    query_embedding = model.encode(
        question,
        normalize_embeddings=True,
        convert_to_numpy=True,
    )

    # Calculate cosine similarity using normalized embeddings.
    scores = embeddings @ np.asarray(
        query_embedding,
        dtype=np.float32,
    )

    top_indices = np.argsort(-scores)[:3]

    # Build context from the top 3 retrieved policy chunks.
    context_parts: list[str] = []
    sources: list[str] = []

    for index in top_indices:
        item = metadata[int(index)]

        source = item["document"]
        document = item["text"]

        if not isinstance(source, str) or not isinstance(document, str):
            raise ValueError("Invalid policy metadata")

        context_parts.append(f"Source: {source}\nContent: {document}")
        sources.append(source)

    context = "\n\n".join(context_parts)

    # Generate a grounded answer using local Ollama.
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a parcel logistics support assistant. "
                    "Answer using only the provided policy context. "
                    "If the context does not contain the answer, "
                    "say you do not have enough information. "
                    "Do not invent policies or delivery details. "
                    "Keep answers short and clear."
                ),
            },
            {
                "role": "user",
                "content": (f"Policy context:\n{context}\n\nCustomer question: {question}"),
            },
        ],
        options={"temperature": 0},
    )

    logger.info("\nANSWER:")
    logger.info("%s", response.message.content)

    logger.info("\nRETRIEVED SOURCES:")
    for source in sources:
        logger.info("- %s", source)


if __name__ == "__main__":
    answer_question("What should I do if my parcel arrives damaged?")
