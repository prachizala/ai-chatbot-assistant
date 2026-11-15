import unittest
import sys
import os

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from chatbot_engine import (
    estimate_tokens,
    ConversationManager,
    generate_mock_response,
    query_llm,
    PERSONAS
)


class TestChatbotEngine(unittest.TestCase):
    """Test suite for conversational memory, prompt management, and response dispatch."""

    def test_estimate_tokens(self):
        self.assertEqual(estimate_tokens(""), 0)
        self.assertEqual(estimate_tokens("word"), 1)
        text = "This is a sentence containing roughly ten words."
        tokens = estimate_tokens(text)
        self.assertGreater(tokens, 5)

    def test_conversation_manager_initialization(self):
        cm = ConversationManager(persona_key="coding_mentor")
        self.assertEqual(len(cm.messages), 1)
        self.assertEqual(cm.messages[0]["role"], "system")
        self.assertIn("Computer Science Mentor", cm.messages[0]["content"])
        self.assertEqual(len(cm.get_display_messages()), 0)

    def test_add_message_and_history(self):
        cm = ConversationManager()
        cm.add_message("user", "How do I reverse a list in Python?")
        cm.add_message("assistant", "Use arr[::-1] or arr.reverse().")

        display_msgs = cm.get_display_messages()
        self.assertEqual(len(display_msgs), 2)
        self.assertEqual(display_msgs[0]["role"], "user")
        self.assertEqual(display_msgs[1]["role"], "assistant")

    def test_prune_history_token_limit(self):
        # Configure small token limit
        cm = ConversationManager(max_history_tokens=50)
        long_text = "Python is an interpreted, high-level programming language. " * 10
        cm.add_message("user", "First message " + long_text)
        cm.add_message("assistant", "First response " + long_text)
        cm.add_message("user", "Second message " + long_text)

        # Older non-system messages must be pruned, system prompt retained
        self.assertEqual(cm.messages[0]["role"], "system")
        self.assertLessEqual(cm.total_tokens(), 300)

    def test_change_persona(self):
        cm = ConversationManager(persona_key="coding_mentor")
        cm.change_persona("academic_tutor")
        self.assertEqual(cm.persona_key, "academic_tutor")
        self.assertIn("academic university tutor", cm.messages[0]["content"])

    def test_export_as_markdown(self):
        cm = ConversationManager()
        cm.add_message("user", "What is Big-O notation?")
        cm.add_message("assistant", "Big-O characterizes upper bound execution time.")
        md = cm.export_as_markdown()
        self.assertIn("# Chat Transcript", md)
        self.assertIn("**User**:", md)
        self.assertIn("Big-O notation", md)

    def test_mock_response_offline(self):
        resp_bs = generate_mock_response("How to do binary search?", "coding_mentor")
        self.assertIn("binary_search", resp_bs)
        self.assertIn("Time Complexity", resp_bs)

        resp_rec = generate_mock_response("Explain recursion please", "coding_mentor")
        self.assertIn("factorial", resp_rec)

        # Without API key, query_llm should return mock output without crashing
        res = query_llm([{"role": "user", "content": "How to do binary search?"}], api_key=None)
        self.assertIn("binary_search", res)


if __name__ == "__main__":
    unittest.main()
