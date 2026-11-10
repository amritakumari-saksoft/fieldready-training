def build_citations(chunks: list[dict]) -> list[dict]:
    """Create citations from retrieved source chunks."""
    citations = []
    seen = set()

    for chunk in chunks:
        chunk_id = chunk["chunk_id"]

        if chunk_id in seen:
            continue

        seen.add(chunk_id)

        citations.append(
            {
                "document": chunk["document"],
                "chunk_id": chunk_id,
                "text": chunk["text"],
            }
        )

    return citations
