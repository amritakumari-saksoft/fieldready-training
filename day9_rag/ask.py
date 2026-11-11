# ruff: noqa: T201
import json
from pathlib import Path

import numpy as np
import ollama
from sentence_transformers import SentenceTransformer

from day9_rag.citations import build_citations
from day9_rag.context import assemble_context

BASE_DIR = Path(__file__).resolve().parent.parent
STORE_DIR = BASE_DIR / "day6_rag" / "vector_store"

MODEL_NAME = "qwen3.5:2b"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

DEFAULT_TOKEN_BUDGET = 2000
DEFAULT_TOP_K = 3
MIN_SIMILARITY = 0.30


def load_vector_store():
    embeddings = np.load(
        STORE_DIR / "paragraph_embeddings.npy",
        allow_pickle=False,
    )

    metadata = json.loads((STORE_DIR / "paragraph_metadata.json").read_text(encoding="utf-8"))

    if len(embeddings) == 0 or len(embeddings) != len(metadata):
        raise ValueError("Invalid or empty vector store")

    return embeddings, metadata


def retrieve(
    question,
    model,
    embeddings,
    metadata,
    top_k=DEFAULT_TOP_K,
):
    query_embedding = model.encode(
        question,
        normalize_embeddings=True,
        convert_to_numpy=True,
    )

    scores = embeddings @ np.asarray(
        query_embedding,
        dtype=np.float32,
    )

    indices = np.argsort(-scores)[:top_k]

    results = []

    for index in indices:
        item = dict(metadata[int(index)])
        item["score"] = float(scores[int(index)])
        results.append(item)

    return results


def ask(
    question,
    retriever=None,
    generator=None,
    token_budget=DEFAULT_TOKEN_BUDGET,
    top_k=DEFAULT_TOP_K,
    min_similarity=MIN_SIMILARITY,
):
    """Retrieve evidence and generate a cited answer."""

    if not question or not question.strip():
        raise ValueError("Question cannot be empty")

    if token_budget <= 0:
        raise ValueError("Token budget must be positive")

    if top_k < 1:
        raise ValueError("top_k must be positive")

    # Dependency injection allows tests without loading AI models.
    if retriever is None:
        embeddings, metadata = load_vector_store()
        model = SentenceTransformer(EMBEDDING_MODEL)

        retrieved = retrieve(
            question,
            model,
            embeddings,
            metadata,
            top_k,
        )
    else:
        retrieved = retriever(question, top_k)

    if not retrieved:
        return {
            "answer": "I don't know. I could not find supporting policy information.",
            "citations": [],
        }

    relevant = [chunk for chunk in retrieved if chunk.get("score", 1.0) >= min_similarity]

    if not relevant:
        return {
            "answer": "I don't know. The available sources do not sufficiently support an answer.",
            "citations": [],
        }

    context, selected_chunks = assemble_context(
        relevant,
        token_budget,
    )

    if not selected_chunks:
        return {
            "answer": "I don't know. No supporting passage fits the context budget.",
            "citations": [],
        }

    prompt = f"""
Use only the policy passages below to answer the customer.

Rules:
- Do not invent policy details.
- If the answer is not supported, say "I don't know."
- Refer only to facts supported by the passages.
- Keep the answer clear and concise.

Policy passages:
{context}

Customer question:
{question}
"""

    if generator is None:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a parcel logistics support assistant. "
                        "Answer only using the provided policy passages. "
                        "Never invent policy information."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            options={"temperature": 0},
        )

        answer = response.message.content
    else:
        answer = generator(prompt)

    if not answer or not answer.strip():
        answer = "I don't know. No supported answer was generated."

    citations = build_citations(selected_chunks)

    return {
        "answer": answer,
        "citations": citations,
    }


if __name__ == "__main__":
    question = input("Ask a logistics policy question: ")

    result = ask(question)

    print("\nANSWER:")
    print(result["answer"])

    print("\nCITATIONS:")

    for citation in result["citations"]:
        print(f"- {citation['document']} ({citation['chunk_id']})")
