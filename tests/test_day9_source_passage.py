import pytest

from day9_rag.source_passage import show_source_passage


def test_show_one_source_passage():
    citations = [
        {
            "document": "04_damaged_parcels.txt",
            "chunk_id": "04_damaged_parcels_0",
            "text": "Customers must report damaged parcels within 48 hours.",
        }
    ]

    result = show_source_passage(citations)

    assert len(result) == 1
    assert result[0]["document"] == "04_damaged_parcels.txt"
    assert result[0]["chunk_id"] == "04_damaged_parcels_0"
    assert result[0]["passage"] == ("Customers must report damaged parcels within 48 hours.")


def test_show_multiple_source_passages():
    citations = [
        {
            "document": "04_damaged_parcels.txt",
            "chunk_id": "damage_0",
            "text": "Report damage within 48 hours.",
        },
        {
            "document": "05_lost_parcels.txt",
            "chunk_id": "lost_0",
            "text": "A parcel is considered lost under the policy.",
        },
    ]

    result = show_source_passage(citations)

    assert len(result) == 2
    assert result[1]["document"] == "05_lost_parcels.txt"


def test_empty_citations_return_empty_list():
    assert show_source_passage([]) == []


@pytest.mark.parametrize(
    ("citation", "missing_field"),
    [
        (
            {
                "chunk_id": "damage_0",
                "text": "Report damage within 48 hours.",
            },
            "document",
        ),
        (
            {
                "document": "damage.txt",
                "text": "Report damage within 48 hours.",
            },
            "chunk_id",
        ),
        (
            {
                "document": "damage.txt",
                "chunk_id": "damage_0",
            },
            "text",
        ),
    ],
)
def test_missing_required_fields_raise_error(
    citation,
    missing_field,
):
    with pytest.raises(
        ValueError,
        match=f"Missing required citation field: {missing_field}",
    ):
        show_source_passage([citation])


def test_original_passage_text_is_preserved():
    original_text = (
        "Customers must report damaged parcels within 48 hours "
        "of delivery and provide photographs of the damaged package."
    )

    citations = [
        {
            "document": "04_damaged_parcels.txt",
            "chunk_id": "damage_0",
            "text": original_text,
        }
    ]

    result = show_source_passage(citations)

    assert result[0]["passage"] == original_text


def test_non_list_input_is_rejected():
    with pytest.raises(ValueError, match="Citations must be a list"):
        show_source_passage(None)
