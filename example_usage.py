import os
import warnings
from pathlib import Path
from dotenv import load_dotenv
from rag_chat import RAGChat

warnings.filterwarnings("ignore", message="Pydantic serializer warnings")


def main():
    env_path = Path(__file__).parent / '.env'
    load_dotenv(env_path)

    rag = RAGChat()

    question = "How to call the API?"

    print(f"Question: {question}")
    print("\n" + "=" * 50 + "\n")

    answer = rag.chat(question)

    print(f"Answer: {answer}")


if __name__ == "__main__":
    main()
