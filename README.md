# RAG Python

A flexible Retrieval-Augmented Generation (RAG) chat system that supports multiple document retrieval sources (Vectorize, Pinecone, or none) combined with OpenAI's GPT-4o-mini for intelligent answer generation.

## Features

- **Multiple RAG Sources**: Choose between Vectorize, Pinecone, or no external knowledge base
- **Interactive CLI**: Beautiful command-line interface with loading animations and colored output
- **Context-Aware Responses**: Generates answers based on retrieved documents and conversation context
- **Extensible Architecture**: Easy to add new RAG sources by implementing the base interface
- **Environment-Aware**: Automatically checks for required environment variables based on selected source

## Quick Start

1. **Install dependencies**:

```bash
uv sync
```

2. **Set up environment variables** (see Configuration section below)

3. **Run the application**:

```bash
uv run main.py
```

## Configuration

### Choosing a RAG Source

Edit `main.py` and modify the `RAG_SOURCE` variable:

```python
from rag_source_base import RAGSourceType

# Choose one of:
RAG_SOURCE = RAGSourceType.NONE       # No document retrieval (OpenAI only)
RAG_SOURCE = RAGSourceType.VECTORIZE  # Use Vectorize.io for retrieval
RAG_SOURCE = RAGSourceType.PINECONE   # Use Pinecone (mock implementation)
```

### Environment Variables

Create a `.env` file in the project root with the required variables:

#### Core (Always Required)

```env
OPENAI_API_KEY=your-openai-api-key-here
```

#### For Vectorize Source (RAGSourceType.VECTORIZE)

```env
OPENAI_API_KEY=your-openai-api-key-here
VECTORIZE_PIPELINE_ACCESS_TOKEN=your-vectorize-token
VECTORIZE_ORGANIZATION_ID=your-organization-id
VECTORIZE_PIPELINE_ID=your-pipeline-id
```

#### For Pinecone Source (RAGSourceType.PINECONE)

```env
OPENAI_API_KEY=your-openai-api-key-here
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_ENVIRONMENT=your-pinecone-environment
PINECONE_INDEX_NAME=your-pinecone-index-name
```

#### For No External Source (RAGSourceType.NONE)

```env
OPENAI_API_KEY=your-openai-api-key-here
```

## Getting API Keys

### OpenAI API Key

1. Go to [OpenAI API](https://platform.openai.com/api-keys)
2. Create a new API key
3. Add billing information to your OpenAI account

### Vectorize API

1. Sign up at [Vectorize.io](https://vectorize.io/)
2. Create a pipeline for your documents
3. Get your organization ID, pipeline ID, and access token from the dashboard

### Pinecone API

1. Sign up at [Pinecone](https://www.pinecone.io/)
2. Create a new index
3. Get your API key and environment from the dashboard
4. Note: Currently using mock implementation - replace with actual Pinecone client

## Project Structure

```
rag-python/
├── main.py              # Main application entry point
├── rag_chat.py             # Core RAG chat logic
├── rag_source_base.py      # Base interface for RAG sources
├── vectorize_wrapper.py    # Vectorize.io implementation
├── pinecone_wrapper.py     # Pinecone mock implementation
├── cli_interface.py        # Command-line interface and styling
├── example_usage.py        # Programmatic usage examples
├── pyproject.toml          # Project dependencies
├── uv.lock                # Dependency lock file
└── .env                   # Environment variables (create this)
```

## Usage

### Interactive Mode

Run the main application:

```bash
python main.py
```

The application will:

1. Check your environment variables
2. Initialize the selected RAG source
3. Start an interactive chat session
4. Display retrieved documents (if using external source)
5. Generate and show AI responses

### Programmatic Usage

```python
from rag_chat import RAGChat
from cli_interface import CLIInterface
from vectorize_wrapper import VectorizeWrapper

# With Vectorize
cli = CLIInterface("My RAG App")
vectorize_source = VectorizeWrapper()
rag = RAGChat(cli, rag_source=vectorize_source)

answer = rag.chat("What is machine learning?")
print(answer)

# Without external source
rag_no_source = RAGChat(cli, rag_source=None)
answer = rag_no_source.chat("What is machine learning?")
print(answer)
```

## How It Works

### With External RAG Source (Vectorize/Pinecone)

1. User asks a question
2. System queries the RAG source for relevant documents
3. Retrieved documents are formatted as context
4. Context + question sent to OpenAI GPT-4o-mini
5. AI generates answer based on provided context
6. Answer displayed with source information

### Without External Source

1. User asks a question
2. Question sent directly to OpenAI GPT-4o-mini
3. AI generates answer from general knowledge
4. Answer displayed

## Adding New RAG Sources

To add a new RAG source (e.g., Chroma, Weaviate):

1. **Create a wrapper class**:

```python
from rag_source_base import RAGSourceBase

class MyNewWrapper(RAGSourceBase):
    def retrieve_documents(self, question: str, num_results: int = 5):
        # Implement your retrieval logic
        return documents

    def get_required_env_vars(self):
        return ["MY_API_KEY", "MY_INDEX_NAME"]
```

2. **Add to enum** in `rag_source_base.py`:

```python
class RAGSourceType(Enum):
    NONE = "none"
    VECTORIZE = "vectorize"
    PINECONE = "pinecone"
    MY_NEW_SOURCE = "my_new_source"  # Add this
```

3. **Update** `get_rag_source()` in `main.py`:

```python
elif RAG_SOURCE == RAGSourceType.MY_NEW_SOURCE:
    wrapper = MyNewWrapper()
    return wrapper, wrapper.get_required_env_vars()
```

## Troubleshooting

### Common Issues

**Missing environment variables**:

- Check your `.env` file exists and has the correct variables
- Ensure no extra spaces around the `=` in your `.env` file

**API key errors**:

- Verify your OpenAI API key is valid and has billing enabled
- Check Vectorize/Pinecone credentials are correct

**Import errors**:

- Run `uv sync` to install all dependencies
- Ensure you're using Python 3.8+

**No documents found**:

- Verify your Vectorize pipeline has documents indexed
- Check your Pinecone index has embeddings

### Getting Help

1. Check the application logs for specific error messages
2. Verify all environment variables are set correctly
3. Test with `RAG_SOURCE = RAGSourceType.NONE` to isolate issues
4. Ensure your API keys have the necessary permissions

## Dependencies

- `python >= 3.8`
- `litellm` - Multi-provider LLM interface
- `vectorize-client` - Vectorize.io Python client
- `python-dotenv` - Environment variable management

See `pyproject.toml` for complete dependency list.
