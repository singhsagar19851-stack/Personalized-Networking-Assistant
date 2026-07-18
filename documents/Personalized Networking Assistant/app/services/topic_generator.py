from transformers import pipeline, set_seed
from app.config import MODEL_NAMES

generator = pipeline(
    "text-generation",
    model=MODEL_NAMES["text_generator"]
)

set_seed(42)


def generate_topics(event_themes, user_interests):
    prompt = (
        f"I'm attending a networking event focused on {', '.join(event_themes)}. "
        f"I'm personally interested in {', '.join(user_interests)}. "
        f"What are three creative and engaging conversation starters I could use?"
    )

    outputs = generator(
        prompt,
        max_length=80,
        num_return_sequences=1
    )

    suggestions = outputs[0]["generated_text"].split("\n")[:3]

    return [
        s.strip("- ").strip()
        for s in suggestions
        if s.strip()
    ]