import os
import warnings
from typing import List, Dict, Any
from litellm import completion
from vectorize_wrapper import VectorizeWrapper

warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")


class RAGChat:
    def __init__(self):
        self.vectorize = VectorizeWrapper()
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")

        if not self.openai_api_key:
            raise ValueError("Missing OPENAI_API_KEY environment variable")

    def format_context(self, documents: List[Any]) -> str:
        if not documents:
            return "No relevant documents found."

        context = "Here are the relevant documents:\n\n"
        for i, doc in enumerate(documents, 1):
            context += f"Document {i}:\n"

            if hasattr(doc, 'text'):
                context += f"Content: {doc.text}\n"

            if hasattr(doc, 'source_display_name'):
                context += f"Source: {doc.source_display_name}\n"

            if hasattr(doc, 'relevancy'):
                context += f"Relevance Score: {doc.relevancy}\n"

            context += "\n"

        return context

    def generate_answer(self, question: str, context: str) -> str:
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that answers questions based on the provided context. If the context doesn't contain relevant information, say so."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}\n\nPlease provide a comprehensive answer based on the context above."
            }
        ]

        try:
            response = completion(
                model="openai/gpt-4o-mini",
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {e}"

    def chat(self, question: str, num_results: int = 5) -> str:
        print(f"Retrieving documents for: {question}")
        documents = self.vectorize.retrieve_documents(question, num_results)

        if documents:
            print(f"Found {len(documents)} relevant documents")
        else:
            print("No documents found")

        context = self.format_context(documents)

        print("Generating answer...")
        answer = self.generate_answer(question, context)

        return answer
