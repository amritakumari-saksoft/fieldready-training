from day9_rag.context import assemble_context


def test_context_stays_within_budget():
    chunks = [
        {
            "document": "policy1.txt",
            "chunk_id": "chunk_1",
            "text": "Short policy passage.",
        },
        {
            "document": "policy2.txt",
            "chunk_id": "chunk_2",
            "text": "Another short policy passage.",
        },
    ]

    context, selected = assemble_context(
        chunks,
        token_budget=100,
    )

    assert len(selected) == 2
    assert "policy1.txt" in context


def test_context_rejects_chunks_over_budget():
    chunks = [
        {
            "document": "policy1.txt",
            "chunk_id": "chunk_1",
            "text": "A very long policy passage.",
        }
    ]

    context, selected = assemble_context(
        chunks,
        token_budget=1,
    )

    assert selected == []
    assert context == ""
