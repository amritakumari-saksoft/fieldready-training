"""Production RAG answering service.

Retrieves policy chunks, builds grounded context, calls the configured
OpenAI-compatible LLM, and returns source citations.
"""

import json
import logging
from functools import lru_cache
from pathlib import Path

import httpx
import numpy as np
from sentence_transformers import SentenceTransformer

from app.config import get_settings
from app.models.schemas import AskResponse, Citation
from app.services.llm_client import LLMClient
from day9_rag.context import assemble_context

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parents[2]
STORE_DIR = BASE_DIR / "day6_rag" / "vector_store"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
DEFAULT_TOP_K = 3
DEFAULT_TOKEN_BUDGET = 2000
MIN_SIMILARITY = 0.30


@lru_cache(maxsize=1)
def load_vector_store():
    """Load and validate the local vector store."""

    embeddings = np.load(
        STORE_DIR / "paragraph_embeddings.npy",
        allow_pickle=False,
    )

    metadata = json.loads((STORE_DIR / "paragraph_metadata.json").read_text(encoding="utf-8"))

    if embeddings.ndim != 2 or len(embeddings) == 0:
        raise ValueError("Invalid or empty vector store")

    if len(embeddings) != len(metadata):
        raise ValueError("Embedding and metadata counts do not match")

    if not np.isfinite(embeddings).all():
        raise ValueError("Vector store contains invalid embeddings")

    if any(not all(key in item for key in ("document", "chunk_id", "text")) for item in metadata):
        raise ValueError("Vector store metadata is incomplete")

    return embeddings, metadata


@lru_cache(maxsize=1)
def load_embedding_model():
    """Load the embedding model once."""

    return SentenceTransformer(EMBEDDING_MODEL)


@lru_cache(maxsize=1)
def get_llm_client():
    """Create a reusable provider-agnostic LLM client."""

    settings = get_settings()
    http_client = httpx.Client()

    return LLMClient(settings, http_client)


def retrieve(question: str, top_k: int = DEFAULT_TOP_K) -> list[dict]:
    """Retrieve the most relevant policy chunks."""

    embeddings, metadata = load_vector_store()
    model = load_embedding_model()

    query_embedding = model.encode(
        question,
        normalize_embeddings=True,
        convert_to_numpy=True,
    )

    query_embedding = np.asarray(query_embedding, dtype=np.float32)

    if query_embedding.shape != (embeddings.shape[1],):
        raise ValueError("Query and document embedding dimensions differ")

    # The current vector store is a single-accessible policy corpus.
    # Add authorization filtering here BEFORE similarity ranking when
    # document/user permission metadata is introduced.

    scores = embeddings @ query_embedding

    indices = np.argsort(-scores)[:top_k]

    results = []

    for index in indices:
        item = dict(metadata[int(index)])
        item["score"] = float(scores[int(index)])
        results.append(item)

    return results


def answer_question(question: str) -> AskResponse:
    """Generate an answer grounded only in retrieved policy passages."""

    if not question or not question.strip():
        raise ValueError("Question cannot be empty")

    retrieved = retrieve(question)

    # Reject weak retrieval results.
    relevant = [chunk for chunk in retrieved if chunk["score"] >= MIN_SIMILARITY]

    if not relevant:
        return AskResponse(
            answer="I don't know. The available sources do not sufficiently support an answer.",
            citations=[],
        )

    context, selected_chunks = assemble_context(
        relevant,
        token_budget=DEFAULT_TOKEN_BUDGET,
    )

    if not selected_chunks:
        return AskResponse(
            answer="I don't know. No supporting passage fits the context budget.",
            citations=[],
        )

    system_prompt = (
        "You are a parcel logistics support assistant. "
        "Answer customer questions using only the supplied policy passages. "
        "Never invent delivery times, policies, or other details. "
        "If the passages do not support an answer, say exactly "
        "'I don't know.' Keep answers concise."
    )

    user_prompt = f"""
Policy passages:

{context}

Customer question:

{question}

Answer using only the policy passages above.
"""

    llm = get_llm_client()

    result = llm.complete(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        temperature=0.0,
    )

    answer = result.content.strip()

    if not answer:
        answer = "I don't know. No supported answer was generated."

    citations = [
        Citation(
            source=f"{chunk['document']} ({chunk['chunk_id']})",
            passage=chunk["text"],
        )
        for chunk in selected_chunks
    ]

    logger.info(
        "RAG answer generated: retrieved=%d selected=%d model=%s",
        len(retrieved),
        len(selected_chunks),
        result.model,
    )

    return AskResponse(
        answer=answer,
        citations=citations,
    )
