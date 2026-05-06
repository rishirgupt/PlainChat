PlainChat: Memory-Enabled Travel Assistant
PlainChat is a Python-based conversational AI designed to streamline travel and hospitality inquiries. Unlike basic keyword-matching bots, PlainChat utilizes Natural Language Processing (NLP) and a contextual memory system to engage in meaningful, multi-turn dialogues.

It is designed to be lightweight, efficient, and easily customizable via an external knowledge base.

Core Features
Contextual Memory: The chatbot remembers the "last intent" discussed, allowing users to ask follow-up questions (e.g., "Tell me more" or "What time?") without repeating the subject.

Advanced NLP Pipeline: Uses the nltk library for tokenization and Porter Stemming. This ensures the bot understands word variations like "arriving," "arrival," and "arrive."

Text-to-Speech (TTS): Integrated with pyttsx3 to provide auditory feedback, making the interaction more accessible and immersive.

Dynamic Knowledge Base: Powered by Keywordsv6.csv, allowing you to update the bot’s logic and responses without touching a single line of code.

Scoring-Based Intent Recognition: Implements a weighted scoring system to determine the most relevant response based on user input.

Technical Architecture
PlainChat follows a modular class-based structure:

Preprocessing: Cleans input, removes noise, and reduces words to their root stems.

Intent Matching: Compares processed tokens against the Keywordsv6.csv database.

State Management: Tracks conversation turns and clears memory after a set threshold (5 turns) to ensure context remains fresh and relevant.

Getting Started
Prerequisites

Python 3.x

NLTK

pyttsx3

Installation

Bash
pip install nltk pyttsx3
Running the Bot
Ensure Keywordsv6.csv is in the root directory and run:

Bash
python PlainChat.py
Quick Tips for your GitHub Repo:
The CSV File: Make sure you upload Keywordsv6.csv to the repo so others can run the code immediately.

Requirements.txt: Create a file named requirements.txt and put nltk and pyttsx3 inside it. It makes your project look much more professional.
