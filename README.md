# 💜 Purple AI Chatbot

## Project Description
Purple AI Chatbot is an AI-powered chatbot developed using Python and Streamlit. It allows users to ask questions and receive intelligent responses using the Gemma 3:1B language model through Ollama.

The chatbot provides a modern dark purple theme with an interactive chat interface.

## Features
- Ask any questions and receive AI-generated answers.
- Supports conversational interaction.
- Displays chat history.
- Clear chat option.
- Modern dark purple user interface.
- Runs locally using Ollama.

## Technologies Used
- Python
- Streamlit
- Ollama
- Gemma 3:1B
- Requests

## Project Structure
```text
AI CHATBOT/
│
├── app.py
└── README.md
```

## Installation

**1. Install Python packages**

```bash
pip install streamlit requests
```

**2. Install Ollama**

Download from: https://ollama.com/download

**3. Download AI Model**

```bash
ollama pull gemma3:1b
```

## Run the Application

```bash
streamlit run app.py
```

The chatbot will open in your web browser.

## How It Works

1. User enters a question in the chat interface.
2. Streamlit receives the question.
3. The question is sent to the Ollama API.
4. Gemma 3:1B processes the question.
5. The AI generates a response.
6. The response is displayed in the chatbot.

## Author
AI Chatbot Project

## Conclusion
Purple AI Chatbot provides a simple and interactive way to communicate with an AI model. It demonstrates the use of Python, Streamlit and local Large Language Models to build an AI-powered chatbot.
