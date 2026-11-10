from day9_rag.ask import ask


def sample_chunks():
    return [
        {
            "document": "04_damaged_parcels.txt",
            "chunk_id": "04_damaged_parcels_0",
            "text": ("Customers must report damaged parcels within 48 hours of delivery."),
            "score": 0.90,
        }
    ]


def test_ask_returns_answer_and_citation():
    result = ask(
        "How do I report damaged parcels?",
        retriever=lambda question, top_k: sample_chunks(),
        generator=lambda prompt: "Report damaged parcels within 48 hours.",
    )

    assert "48 hours" in result["answer"]
    assert len(result["citations"]) == 1
    assert result["citations"][0]["document"] == "04_damaged_parcels.txt"


def test_ask_returns_dont_know_when_no_results():
    result = ask(
        "What is the company headquarters?",
        retriever=lambda question, top_k: [],
        generator=lambda prompt: "This should not run",
    )

    assert "I don't know" in result["answer"]
    assert result["citations"] == []


def test_ask_rejects_low_similarity():
    chunks = [
        {
            "document": "04_damaged_parcels.txt",
            "chunk_id": "04_damaged_parcels_0",
            "text": "Damaged parcel policy.",
            "score": 0.10,
        }
    ]

    result = ask(
        "Unrelated question",
        retriever=lambda question, top_k: chunks,
        generator=lambda prompt: "This should not run",
    )

    assert "I don't know" in result["answer"]
    assert result["citations"] == []
