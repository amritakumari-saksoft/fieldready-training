from day9_rag.citations import build_citations


def test_citations_include_source_and_chunk():
    chunks = [
        {
            "document": "04_damaged_parcels.txt",
            "chunk_id": "04_damaged_parcels_0",
            "text": "Report damage within 48 hours.",
        }
    ]

    citations = build_citations(chunks)

    assert len(citations) == 1
    assert citations[0]["document"] == "04_damaged_parcels.txt"
    assert citations[0]["chunk_id"] == "04_damaged_parcels_0"


def test_duplicate_citations_are_removed():
    chunk = {
        "document": "04_damaged_parcels.txt",
        "chunk_id": "04_damaged_parcels_0",
        "text": "Report damage within 48 hours.",
    }

    citations = build_citations([chunk, chunk])

    assert len(citations) == 1
