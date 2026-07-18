import requests
from urllib.parse import quote
from app.config import FACT_CHECK_API

import wikipedia


def fact_check(query: str) -> str:
    try:
        return wikipedia.summary(query, sentences=3)

    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results found. Try one of: {', '.join(e.options[:5])}"

    except wikipedia.exceptions.PageError:
        return "No information found."

    except Exception as e:
        return f"Fact-checking failed: {e}"