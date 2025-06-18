# RAG Python

A Retrieval-Augmented Generation (RAG) chat system that combines Vectorize for document retrieval with OpenAI's GPT-4o-mini for answer generation.

## Features

- Document retrieval using Vectorize API
- Context-aware answer generation using OpenAI's GPT-4o-mini via LiteLLM
- Interactive command-line interface
- Clean wrapper interfaces for both Vectorize and LLM integration

## Setup

1. Install dependencies:

```bash
uv sync
```

2. Set up your environment variables in `.env`:

```
OPENAI_API_KEY="your-openai-api-key"
VECTORIZE_PIPELINE_ACCESS_TOKEN="your-vectorize-token"
VECTORIZE_ORGANIZATION_ID="your-organization-id"
VECTORIZE_PIPELINE_ID="your-pipeline-id"
```

## Usage

### Interactive Chat

Run the main script for an interactive chat session:

```bash
python main.py
```

This will start an interactive session where you can ask questions and get answers based on retrieved documents.

### Programmatic Usage

```python
from rag_chat import RAGChat

rag = RAGChat()
answer = rag.chat("How to call the API?")
print(answer)
```

## Project Structure

- `vectorize_wrapper.py` - Wrapper interface for Vectorize API
- `rag_chat.py` - RAG chat implementation combining retrieval and generation
- `main.py` - Interactive command-line interface
- `example_usage.py` - Example of programmatic usage

## How It Works

1. When you ask a question, the system retrieves relevant documents from Vectorize
2. The retrieved documents are formatted as context
3. The context and question are sent to OpenAI's GPT-4o-mini model
4. The model generates an answer based on the provided context
5. The answer is displayed in the terminal
