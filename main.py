import os
import warnings
from pathlib import Path
from dotenv import load_dotenv
from rag_chat import RAGChat

warnings.filterwarnings("ignore", message="Pydantic serializer warnings")


def load_environment():
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print("Environment variables loaded from .env file")
    else:
        print("No .env file found, using system environment variables")


def main():
    load_environment()

    try:
        rag = RAGChat()
        print("RAG Chat initialized successfully!")
        print("=" * 50)
        print("Welcome to RAG Chat with Vectorize and OpenAI")
        print("Type 'quit' or 'exit' to end the session")
        print("=" * 50)

        while True:
            question = input("\nYour question: ").strip()

            if question.lower() in ['quit', 'exit']:
                print("Goodbye!")
                break

            if not question:
                print("Please enter a question.")
                continue

            print("\n" + "-" * 50)
            answer = rag.chat(question)
            print("-" * 50)
            print(f"\nAnswer: {answer}")

    except Exception as e:
        print(f"Error initializing RAG Chat: {e}")
        print(
            "Please make sure all required environment variables are set in your .env file:")
        print("- OPENAI_API_KEY")
        print("- VECTORIZE_PIPELINE_ACCESS_TOKEN")
        print("- VECTORIZE_ORGANIZATION_ID")
        print("- VECTORIZE_PIPELINE_ID")


if __name__ == "__main__":
    main()
