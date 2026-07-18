from app.services import topic_generator


def test_topic_generation_returns_suggestions():
    themes = ["AI", "healthcare"]
    interests = ["ethics", "automation"]

    suggestions = topic_generator.generate_topics(themes, interests)

    # Should return a list
    assert isinstance(suggestions, list)

    # Should not be empty
    assert len(suggestions) > 0

    # Every suggestion should be a non-empty string
    for suggestion in suggestions:
        assert isinstance(suggestion, str)
        assert suggestion.strip() != ""


def test_generate_strings():
    themes = ["AI"]
    interests = ["machine learning"]

    suggestions = topic_generator.generate_topics(themes, interests)

    for suggestion in suggestions:
        assert isinstance(suggestion, str)


def test_generate_non_empty_strings():
    themes = ["blockchain"]
    interests = ["finance"]

    suggestions = topic_generator.generate_topics(themes, interests)

    for suggestion in suggestions:
        assert len(suggestion.strip()) > 0