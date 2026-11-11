"""RAG answering service with graceful missing-store handling."""

import json
import logging
from pathlib import Path
from typing import Any

import httpx
import numpy as np

from app.config import Settings
from app.services.llm_client import LLMClient

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
STORE_DIR = PROJECT_ROOT / "day6_rag" / "vector_store"

SIMILARITY_THRESHOLD = 0.30
MAX_CONTEXT_TOKENS = 3000
MAX_RESULTS = 5

UNKNOWN_ANSWER = "I don't know based on the available sources."


def load_vector_store() -> tuple[
    np.ndarray | None,
    list[dict[str, Any]],
]:
    """Load embeddings and metadata safely."""

    embeddings_path = STORE_DIR / "paragraph_embeddings.npy"
    metadata_path = STORE_DIR / "paragraph_metadata.json"

    try:
        if not embeddings_path.is_file():
            logger.warning("RAG embeddings file is missing")
            return None, []

        if not metadata_path.is_file():
            logger.warning("RAG metadata file is missing")
            return None, []

        embeddings = np.load(
            embeddings_path,
            allow_pickle=False,
        )

        with metadata_path.open(encoding="utf-8") as file:
            metadata = json.load(file)

        if not isinstance(metadata, list):
            return None, []

        if not all(isinstance(item, dict) for item in metadata):
            return None, []

        if embeddings.ndim != 2:
            return None, []

        if len(embeddings) != len(metadata):
            return None, []

        return embeddings, metadata

    except OSError, ValueError, json.JSONDecodeError:
        logger.exception("Unable to load RAG vector store")
        return None, []


def retrieve(question: str) -> list[dict[str, Any]]:
    """Retrieve relevant passages using cosine similarity."""

    embeddings, metadata = load_vector_store()

    if embeddings is None or not metadata:
        logger.warning("Vector store unavailable")
        return []

    try:
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("all-MiniLM-L6-v2")

        question_embedding = model.encode(
            [question],
            normalize_embeddings=True,
        )

        vectors = embeddings.astype(
            np.float32,
            copy=False,
        )

        norms = np.linalg.norm(
            vectors,
            axis=1,
            keepdims=True,
        )

        normalized = np.divide(
            vectors,
            norms,
            out=np.zeros_like(vectors),
            where=norms != 0,
        )

        scores = normalized @ question_embedding[0]

        results: list[dict[str, Any]] = []

        for index in np.argsort(scores)[::-1][:MAX_RESULTS]:
            score = float(scores[index])

            if score < SIMILARITY_THRESHOLD:
                continue

            results.append(
                {
                    **metadata[index],
                    "similarity": score,
                }
            )

        return results

    except Exception:
        logger.exception("RAG retrieval failed")
        return []


def build_context(
    retrieved: list[dict[str, Any]],
) -> str:
    """Build context while respecting the token budget."""

    context_parts: list[str] = []
    token_count = 0

    for item in retrieved:
        passage = str(item.get("text", "")).strip()

        if not passage:
            continue

        estimated_tokens = len(passage.split())

        if token_count + estimated_tokens > MAX_CONTEXT_TOKENS:
            continue

        context_parts.append(passage)
        token_count += estimated_tokens

    return "\n\n".join(context_parts)


def build_citations(
    retrieved: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Build unique citations."""

    citations: list[dict[str, Any]] = []
    seen: set[tuple[Any, Any]] = set()

    for item in retrieved:
        source = item.get("source")
        chunk_id = item.get("chunk_id")

        key = (source, chunk_id)

        if key in seen:
            continue

        seen.add(key)

        citations.append(
            {
                "source": source,
                "chunk_id": chunk_id,
            }
        )

    return citations


def answer_question(question: str) -> dict[str, Any]:
    """Generate a grounded answer using retrieved passages."""

    retrieved = retrieve(question)

    if not retrieved:
        return {
            "answer": UNKNOWN_ANSWER,
            "citations": [],
        }

    context = build_context(retrieved)

    if not context:
        return {
            "answer": UNKNOWN_ANSWER,
            "citations": [],
        }

    prompt = f"""
Answer the question using only the provided context.

If the answer is not present in the context,
say that you don't know.

Context:
{context}

Question:
{question}
"""

    try:
        settings = Settings()

        with httpx.Client() as client:
            llm = LLMClient(
                settings=settings,
                http_client=client,
            )

            result = llm.complete(
                system_prompt=(
                    "You are a helpful assistant. Answer using only the provided context."
                ),
                user_prompt=prompt,
                temperature=0.0,
            )

        answer = result.content.strip() or UNKNOWN_ANSWER

        return {
            "answer": answer,
            "citations": build_citations(retrieved),
        }

    except Exception:
        logger.exception("Failed to generate answer")

        return {
            "answer": UNKNOWN_ANSWER,
            "citations": [],
        }
