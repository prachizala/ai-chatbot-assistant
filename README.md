# MentorAI: Academic & Software Engineering Chatbot

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Unit Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)](tests/)

An interactive educational and software engineering assistant built with Python, Streamlit, and an LLM API client architecture. It provides multi-turn conversational memory, sliding-window token management, persona prompt engineering, and a dual-mode engine (offline mock mode or live cloud LLM API).

---

## 📌 Features

- **Multi-Turn Context Management**: Maintains continuous multi-turn dialogue while dynamically pruning older turns using a sliding-window token budget ($3,000$ tokens default).
- **Specialized System Personas**:
  - **Coding Mentor**: Formulates idiomatic Python snippets, debugging hints, and Big-O complexity notes.
  - **Academic & Data Science Tutor**: Socratic explanations across statistics, linear algebra, and data science theory.
  - **Concise Summarizer**: Produces high-yield, bulleted study summaries.
- **Dual Execution Modes**:
  - **Offline Local Engine (Default)**: Fully functional without an API key for offline demos, local study, and continuous integration testing.
  - **Live Cloud LLM API**: Pluggable integration with standard LLM chat completion APIs.
- **Transcript Export**: One-click export of complete formatted conversation history as clean Markdown (`chat_transcript.md`).
- **Interactive Streamlit UI**: Chat bubble layout, live token counter with visual context window progress bar (`st.progress`), and session memory controls.

---

## 🏗️ System Architecture

```text
+-----------------------+
|  User Question/Prompt |  --> "Explain Binary Search with Time Complexity"
+-----------+-----------+
            |
            v
+-----------------------+
|  ConversationManager  |  1. Injects System Persona Prompt Template
|  (chatbot_engine.py)  |  2. Appends User Input to History List
+-----------+-----------+  3. Prunes History to Fit Token Budget (Sliding Window)
            |
            v
+-----------------------+
|  Query Dispatcher     |  --> [Live LLM API] (if API Key provided)
|                       |  --> [Offline Local Engine] (fallback / zero-cost mode)
+-----------+-----------+
            |
            v
+-----------------------+
|   Streamlit Web UI    |  --> Renders Assistant Chat Message
|       (app.py)        |  --> Real-time Token Usage Metric
+-----------------------+  --> Download Chat Transcript (.md)
```

---

## 📂 Project Structure

```text
ai-chatbot-assistant/
├── app.py                  # Streamlit chat interface & session state management
├── chatbot_engine.py       # Prompt templates, ConversationManager, & LLM dispatcher
├── tests/
│   └── test_chatbot.py     # Unit tests for token estimation, memory, & personas
├── requirements.txt        # Project dependencies
├── .gitignore
└── README.md
```

---

## 🚀 Quickstart Guide

### 1. Clone the Repository
```bash
git clone https://github.com/prachizala/ai-chatbot-assistant.git
cd ai-chatbot-assistant
```

### 2. Set Up Virtual Environment (Recommended)
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Chatbot
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

*Note: By default, the application runs in local offline mode. To connect to a live cloud model, switch the sidebar mode to "Live Cloud API" and enter your API key.*

---

## 🧪 Running Unit Tests

The test suite validates memory pruning, token approximation, persona switches, and offline mock generation using Python's built-in `unittest` framework:

```bash
python -m unittest discover -s tests
```

Expected output:
```text
.......
----------------------------------------------------------------------
Ran 7 tests in 0.000s

OK
```

---

## 👩‍💻 Author

**Prachi Zala**  
- Bachelor of Computer Applications (BCA) Student, Ahmedabad, Gujarat, India  
- GitHub: [@prachizala](https://github.com/prachizala)  
- Focus: Python, Data Analytics, and Applied Machine Learning
