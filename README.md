# 🤖 PlainChat: Memory-Enabled Travel Assistant

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**PlainChat** is a lightweight, context-aware chatbot designed for the travel and hospitality industry. It moves beyond simple keyword matching by implementing **Natural Language Processing (NLP)** and a **turn-based memory system**, allowing for more fluid and human-like interactions.

---

## 🌟 Key Features

*   **🧠 Contextual Memory**  
    The bot tracks the conversation state using a `last_intent` buffer. This allows users to ask follow-up questions like *"Tell me more"* or *"How much does it cost?"* without restating the topic.
*   **🔡 Advanced NLP Pipeline**  
    Integrated with `nltk`, the system uses **Porter Stemming** to normalize user input (e.g., converting "booking," "booked," and "books" to the root "book") for higher accuracy.
*   **🗣️ Text-to-Speech (TTS)**  
    Built-in auditory responses using the `pyttsx3` library, providing a hands-free interactive experience.
*   **📊 Dynamic Knowledge Base**  
    All logic is decoupled from the code. The bot’s "brain" is stored in `Keywordsv6.csv`, making it incredibly easy to update responses or add new travel categories.

---

## 🛠️ Technical Architecture

PlainChat is built with a focus on modularity and efficiency:

1.  **`ChatbotV4.py`**: The core engine. It handles the NLP preprocessing, intent scoring, memory management, and the main conversation loop.
2.  **`Keywordsv6.csv`**: The external dataset containing intents, keywords, and randomized response variations.
3.  **Scoring Logic**: Instead of a "yes/no" match, the bot calculates a match score to ensure it provides the most statistically relevant answer.

---

## 🚀 Getting Started

### Prerequisites
Ensure you have Python 3.x installed along with the following libraries:
```bash
pip install nltk pyttsx3
```

## 📖 Usage Example

> **You:** "I need help with my flight status."  
> **Chatbot:** "I can certainly help with flight updates. Please provide your flight number."  
> **You:** "What time does it arrive?" *(Contextual Follow-up)*  
> **Chatbot:** "The current scheduled arrival is at 4:30 PM."

---

## 📁 Project Structure
*   `ChatbotV4.py` — Main Python application.
*   `Keywordsv6.csv` — Knowledge base and intent mapping[cite: 1].
*   `README.md` — Project documentation.

---

## 👨‍💻 Author
**Rishi Gupta**  
*Grade 12 Student | Aspiring AI Developer*

---
