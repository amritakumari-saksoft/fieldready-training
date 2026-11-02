import logging
from pathlib import Path

import chromadb
import ollama
from sentence_transformers import SentenceTransformer

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "vector_db"
MODEL_NAME = "qwen3.5:2b"


def answer_question(question):
    logger.info("Loading embedding model...")

    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    client = chromadb.PersistentClient(path=str(DB_DIR))

    collection = client.get_collection(name="policies_paragraph")

    query_embedding = embedding_model.encode(
        [question],
        normalize_embeddings=True,
    ).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=min(3, collection.count()),
        include=["documents", "metadatas"],
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context_parts = []

    for document, metadata in zip(documents, metadatas, strict=True):
        source = metadata["document"]
        context_parts.append(f"Source: {source}\nContent: {document}")

    context = "\n\n".join(context_parts)

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
    logger.info("%s", response["message"]["content"])

    logger.info("\nRETRIEVED SOURCES:")

    for metadata in metadatas:
        logger.info("- %s", metadata["document"])


if __name__ == "__main__":
    question = "What should I do if my parcel arrives damaged?"
    answer_question(question)
