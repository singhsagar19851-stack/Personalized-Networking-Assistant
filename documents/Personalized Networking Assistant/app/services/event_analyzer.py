from transformers import pipeline
from app.config import MODEL_NAMES

# Load model once when the application starts
classifier = pipeline(
    "zero-shot-classification",
    model=MODEL_NAMES["event_analysis"]
)


def extract_event_themes(description: str, candidate_labels=None):
    """
    Extract the top 3 event themes using DistilBERT zero-shot classification.
    """

    if candidate_labels is None:
        candidate_labels = [
            "AI",
            "healthcare",
            "blockchain",
            "education",
            "sustainability"
        ]

    result = classifier(description, candidate_labels)

    return result["labels"][:3]


# Test the service independently
if __name__ == "__main__":
    description = (
        "AI Networking Event for Machine Learning Engineers "
        "discussing Generative AI."
    )

    themes = extract_event_themes(description)

    print("Extracted Themes:")
    print(themes)