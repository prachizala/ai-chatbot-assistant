"""Core Conversational Engine & Prompt Architecture.

Provides multi-turn memory management, sliding-window token pruning,
custom system persona prompt templates, and dual-mode execution (Live LLM API or Local Mock Engine).
"""

import time
import json
import urllib.request
import urllib.error
from typing import List, Dict, Any, Optional

PERSONAS = {
    "coding_mentor": {
        "name": "Python & Software Engineering Mentor",
        "system_prompt": (
            "You are an encouraging and pragmatic Computer Science Mentor assisting undergraduate students. "
            "Explain concepts clearly, provide idiomatic Python code snippets with comments, "
            "mention Big-O time and space complexity, and share actionable debugging advice."
        ),
        "welcome": "Hello! I am your Python & Software Engineering Mentor. Ask me any coding, data structures, or algorithm question!"
    },
    "academic_tutor": {
        "name": "Academic & Data Science Tutor",
        "system_prompt": (
            "You are an academic university tutor specializing in Python, Statistics, and Applied Machine Learning. "
            "Use first-principles thinking, intuitive analogies, and step-by-step mathematical reasoning."
        ),
        "welcome": "Welcome! I am your Academic Tutor. Ask me about statistics, machine learning, mathematics, or database theory."
    },
    "quick_summarizer": {
        "name": "Concise Technical Summarizer",
        "system_prompt": (
            "You are a concise technical summarizer. Provide high-yield, structured bullet points, "
            "key definitions, and direct executive takeaways without fluff."
        ),
        "welcome": "Ready! Paste notes, concepts, or code to get a concise high-yield summary."
    }
}


def estimate_tokens(text: str) -> int:
    """Rough estimation of token count (~4 characters per token)."""
    if not text:
        return 0
    return max(1, len(text) // 4)


class ConversationManager:
    """Manages chat session state, message pruning, and export formatting."""

    def __init__(self, persona_key: str = "coding_mentor", max_history_tokens: int = 3000):
        self.persona_key = persona_key
        self.max_history_tokens = max_history_tokens
        self.messages: List[Dict[str, str]] = []
        self._initialize_system_prompt()

    def _initialize_system_prompt(self):
        persona = PERSONAS.get(self.persona_key, PERSONAS["coding_mentor"])
        self.messages = [{
            "role": "system",
            "content": persona["system_prompt"]
        }]

    def change_persona(self, new_persona: str):
        if new_persona in PERSONAS and new_persona != self.persona_key:
            self.persona_key = new_persona
            # Preserve user conversation, update system message at index 0
            if self.messages and self.messages[0]["role"] == "system":
                self.messages[0]["content"] = PERSONAS[new_persona]["system_prompt"]
            else:
                self.messages.insert(0, {"role": "system", "content": PERSONAS[new_persona]["system_prompt"]})

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        self.prune_history()

    def get_display_messages(self) -> List[Dict[str, str]]:
        """Returns non-system messages for rendering in UI."""
        return [m for m in self.messages if m["role"] != "system"]

    def total_tokens(self) -> int:
        return sum(estimate_tokens(m["content"]) for m in self.messages)

    def prune_history(self):
        """Maintains the total conversation within token limits using sliding window."""
        while len(self.messages) > 2 and self.total_tokens() > self.max_history_tokens:
            # Remove the oldest non-system message (index 1)
            self.messages.pop(1)

    def clear(self):
        self._initialize_system_prompt()

    def export_as_markdown(self) -> str:
        persona_name = PERSONAS.get(self.persona_key, {}).get("name", "Assistant")
        lines = [f"# Chat Transcript: {persona_name}\n\n"]
        for m in self.get_display_messages():
            prefix = "**User**" if m["role"] == "user" else f"**{persona_name}**"
            lines.append(f"{prefix}:\n{m['content']}\n\n---\n")
        return "".join(lines)


def generate_mock_response(query: str, persona_key: str) -> str:
    """Offline deterministic response generator for offline demos and CI testing."""
    q = query.lower()

    if "binary search" in q:
        return (
            "### Binary Search Algorithm in Python\n\n"
            "Binary Search operates on a sorted array by repeatedly dividing the search space in half.\n\n"
            "```python\n"
            "def binary_search(arr, target):\n"
            "    left, right = 0, len(arr) - 1\n"
            "    while left <= right:\n"
            "        mid = (left + right) // 2\n"
            "        if arr[mid] == target:\n"
            "            return mid\n"
            "        elif arr[mid] < target:\n"
            "            left = mid + 1\n"
            "        else:\n"
            "            right = mid - 1\n"
            "    return -1\n"
            "```\n\n"
            "- **Time Complexity:** $O(\\log n)$ because the problem size is halved each step.\n"
            "- **Space Complexity:** $O(1)$ auxiliary memory."
        )

    if "recursion" in q:
        return (
            "### Understanding Recursion\n\n"
            "Recursion is a programming technique where a function solves a problem by calling itself.\n\n"
            "Every recursive function requires two core components:\n"
            "1. **Base Case:** The condition that terminates recursion and prevents stack overflow.\n"
            "2. **Recursive Step:** Progressing towards the base case with smaller input.\n\n"
            "```python\n"
            "def factorial(n):\n"
            "    if n <= 1:  # Base case\n"
            "        return 1\n"
            "    return n * factorial(n - 1)  # Recursive relation\n"
            "```"
        )

    if "pandas" in q or "dataframe" in q:
        return (
            "### Key Pandas Data Cleaning Operations\n\n"
            "When cleaning tabular data in Pandas, use these essential idioms:\n\n"
            "```python\n"
            "import pandas as pd\n\n"
            "# 1. Drop missing rows or fill with median\n"
            "df['age'] = df['age'].fillna(df['age'].median())\n\n"
            "# 2. Convert date strings to datetime\n"
            "df['timestamp'] = pd.to_datetime(df['timestamp'])\n\n"
            "# 3. Group by and aggregate\n"
            "summary = df.groupby('department')['salary'].mean().reset_index()\n"
            "```"
        )

    # General fallback response
    return (
        f"Thank you for your question: *\"{query}\"*\n\n"
        "Here are 3 fundamental principles to consider:\n"
        "1. **Decomposition:** Break the challenge into smaller, individually testable functions.\n"
        "2. **Edge Cases:** Always check for empty inputs, boundary values, and None/null states.\n"
        "3. **Readability:** Prioritize clean, self-documenting code over clever one-liners.\n\n"
        "*(Running in Offline Mode. Provide an LLM API key in the sidebar for live cloud-hosted answers.)*"
    )


def query_llm(messages: List[Dict[str, str]], api_key: Optional[str] = None) -> str:
    """Dispatches chat request to external LLM endpoint or falls back gracefully to mock engine."""
    user_query = messages[-1]["content"] if messages else ""
    system_persona = "coding_mentor"

    if not api_key:
        return generate_mock_response(user_query, system_persona)

    # Generic HTTP payload dispatch for OpenAI-compatible or generic LLM endpoints
    endpoint = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": m["role"], "content": m["content"]} for m in messages],
        "temperature": 0.7,
        "max_tokens": 800
    }

    try:
        req = urllib.request.Request(endpoint, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        # Fallback to smart offline response if network/key issues occur
        fallback = generate_mock_response(user_query, system_persona)
        return f"{fallback}\n\n*(Note: Live API call returned notice: {str(e)[:60]}... Switched to local offline assistant)*"
