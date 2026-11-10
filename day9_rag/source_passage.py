def show_source_passage(
    citations: list[dict] | None,
) -> list[dict]:
    """
    Return original source passages from RAG citations.

    Args:
        citations: List of citation dictionaries containing
                   document, chunk_id and text.

    Returns:
        List of source passages containing document,
        chunk_id and passage.

    Raises:
        ValueError: If citations or citation fields are invalid.
    """

    if not isinstance(citations, list):
        raise ValueError("Citations must be a list")

    passages = []

    for citation in citations:
        if not isinstance(citation, dict):
            raise ValueError("Each citation must be a dictionary")

        required_fields = ["document", "chunk_id", "text"]

        for field in required_fields:
            if field not in citation:
                raise ValueError(f"Missing required citation field: {field}")

            if not isinstance(citation[field], str) or not citation[field].strip():
                raise ValueError(f"Invalid citation field: {field}")

        passages.append(
            {
                "document": citation["document"],
                "chunk_id": citation["chunk_id"],
                "passage": citation["text"],
            }
        )

    return passages
