"""Unit tests for conversation sliding memory window."""
import unittest

class TestMemoryPruning(unittest.TestCase):
    def test_window_retention(self):
        max_turns = 5
        conversation = [{'role': 'user', 'text': f'msg {i}'} for i in range(10)]
        pruned = conversation[-max_turns:]
        self.assertEqual(len(pruned), 5)
        self.assertEqual(pruned[0]['text'], 'msg 5')

if __name__ == '__main__':
    unittest.main()
