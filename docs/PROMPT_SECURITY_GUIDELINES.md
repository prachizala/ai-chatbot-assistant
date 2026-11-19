# Prompt Injection Sanitization & Safety Guidelines

## Guardrail Architecture
- User inputs are filtered against common jailbreak patterns (`ignore previous instructions`, `DAN mode`).
- System prompts use strict role delimiters (`<system_instructions> ... </system_instructions>`).
- Model responses undergo post-generation safety moderation checks.
