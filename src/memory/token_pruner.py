"""Sliding-window conversational token budget and message history pruner."""


class ConversationalTokenPruner:
    """Prunes older messages when cumulative token estimates exceed context limits."""

    AVG_CHARS_PER_TOKEN = 4.0

    @classmethod
    def estimate_tokens(cls, text: str) -> int:
        """Estimates token footprint based on UTF-8 character length."""
        return max(1, int(len(text.strip()) / cls.AVG_CHARS_PER_TOKEN))

    @classmethod
    def prune_history(cls, messages: list[dict], max_token_limit: int = 3000) -> list[dict]:
        """Keeps system prompt intact while sliding user/assistant history within token ceiling."""
        if not messages:
            return []

        system_msg = [m for m in messages if m.get("role") == "system"]
        conversation = [m for m in messages if m.get("role") != "system"]

        system_tokens = sum(cls.estimate_tokens(m.get("content", "")) for m in system_msg)
        budget = max_token_limit - system_tokens

        retained = []
        accumulated = 0
        for msg in reversed(conversation):
            t_count = cls.estimate_tokens(msg.get("content", ""))
            if accumulated + t_count <= budget:
                retained.append(msg)
                accumulated += t_count
            else:
                break

        return system_msg + list(reversed(retained))
