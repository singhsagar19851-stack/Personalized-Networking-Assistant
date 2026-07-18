from app.services import event_analyzer

VALID_LABELS = [
    "AI",
    "healthcare",
    "blockchain",
    "education",
    "sustainability"
]


def test_event_analysis_returns_labels():
    result = event_analyzer.extract_event_themes(
        "AI in healthcare and diagnostics"
    )

    # Should return a list
    assert isinstance(result, list)

    # Should return at least one label
    assert len(result) > 0

    # Should return at most three labels
    assert len(result) <= 3

    # Every label should be valid
    for label in result:
        assert isinstance(label, str)
        assert label in VALID_LABELS