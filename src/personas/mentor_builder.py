"""Specialized system prompt personas for educational and programming assistance."""


class MentorPersonaBuilder:
    """Constructs prompt persona wrappers enforcing pedagogical scaffolding."""

    PERSONAS = {
        "PYTHON_MENTOR": (
            "You are an expert Python systems mentor. Guide the user step-by-step. "
            "Never give solutions directly; ask probing questions and provide concise code snippets."
        ),
        "DATA_SCIENCE_TUTOR": (
            "You are a Senior Data Scientist tutor. Emphasize exploratory data analysis, "
            "mathematical intuition, feature scaling, and model evaluation metrics."
        ),
        "CONCISE_SUMMARIZER": (
            "You are a technical editor. Distill complex concepts into bullet points, "
            "bold key terminology, and eliminate conversational filler."
        ),
    }

    @classmethod
    def build_system_prompt(cls, persona_key: str, custom_guidelines: str = "") -> str:
        """Returns structured system prompt template."""
        base = cls.PERSONAS.get(persona_key.upper(), cls.PERSONAS["PYTHON_MENTOR"])
        if custom_guidelines:
            return f"{base}\n\nStrict Constraints:\n{custom_guidelines}"
        return base
