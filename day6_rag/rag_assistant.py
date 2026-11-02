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


def answer_question(question: str) -> None:
    logger.info("Loading embedding model...")

    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    client = chromadb.PersistentClient(path=str(DB_DIR))

    collection = client.get_collection(name="policies_paragraph")

    if collection.count() == 0:
        raise ValueError("The policy collection is empty")

    # Step 1: Convert the question into an embedding
    query_embedding = embedding_model.encode(
        [question],
        normalize_embeddings=True,
    ).tolist()

    # Step 2: Retrieve the top 3 policy chunks
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=min(3, collection.count()),
        include=["documents", "metadatas"],
    )

    # Step 3: Validate retrieved results
    retrieved_documents = results["documents"]
    retrieved_metadatas = results["metadatas"]

    if not retrieved_documents or not retrieved_metadatas:
        raise ValueError("No documents or metadata returned from ChromaDB")

    documents = retrieved_documents[0]
    metadatas = retrieved_metadatas[0]

    if not documents or not metadatas:
        raise ValueError("No matching policy chunks found")

    # Step 4: Build context using retrieved policies
    context_parts = []

    for document, metadata in zip(
        documents,
        metadatas,
        strict=True,
    ):
        source = metadata.get("document")

        if not isinstance(source, str):
            raise ValueError("Invalid policy source metadata")

        context_parts.append(f"Source: {source}\nContent: {document}")

    context = "\n\n".join(context_parts)

    # Step 5: Generate the answer using local Ollama
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

    # Step 6: Display the generated answer and sources
    logger.info("\nANSWER:")
    logger.info("%s", response.message.content)

    logger.info("\nRETRIEVED SOURCES:")

    for metadata in metadatas:
        source = metadata.get("document")

        if isinstance(source, str):
            logger.info("- %s", source)


if __name__ == "__main__":
    question = "What should I do if my parcel arrives damaged?"
    answer_question(question)
