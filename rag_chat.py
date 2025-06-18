import os
import warnings
from typing import List, Dict, Any, Optional
from litellm import completion
from rag_source_base import RAGSourceBase
from cli_interface import Config

warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")


class RAGChat:
    def __init__(self, cli_interface, rag_source: Optional[RAGSourceBase] = None):
        self.cli = cli_interface
        self.rag_source = rag_source

        self.openai_api_key = os.environ.get("OPENAI_API_KEY")

        if not self.openai_api_key:
            raise ValueError("Missing OPENAI_API_KEY environment variable")

    def format_context(self, documents: List[Any]) -> str:
        if not documents:
            return "No relevant documents found."

        context = "Here are the relevant documents:\n\n"
        for i, doc in enumerate(documents, 1):
            context += f"Document {i}:\n"

            if hasattr(doc, 'text') or isinstance(doc, dict) and 'text' in doc:
                text = doc.text if hasattr(doc, 'text') else doc['text']
                context += f"Content: {text}\n"

            if hasattr(doc, 'source_display_name') or isinstance(doc, dict) and 'source_display_name' in doc:
                source = doc.source_display_name if hasattr(
                    doc, 'source_display_name') else doc['source_display_name']
                context += f"Source: {source}\n"

            if hasattr(doc, 'relevancy') or isinstance(doc, dict) and 'relevancy' in doc:
                score = doc.relevancy if hasattr(
                    doc, 'relevancy') else doc['relevancy']
                context += f"Relevance Score: {score}\n"

            context += "\n"

        return context

    def generate_answer(self, question: str, context: str) -> str:
        messages = [
            {
                "role": "system",
                "content": Config.SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": Config.USER_PROMPT_TEMPLATE.format(
                    context=context,
                    question=question
                )
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

    def chat(self, question: str, num_results: int = Config.DEFAULT_NUM_RESULTS) -> str:
        if self.rag_source:
            self.cli.print_retrieving(question)
            documents = self.rag_source.retrieve_documents(
                question, num_results)

            self.cli.print_documents_with_snippets(documents)

            context = self.format_context(documents)
        else:
            context = "No external knowledge base available. Please answer based on your general knowledge."
            self.cli.print_info("Answering without document retrieval")

        self.cli.print_generating()
        answer = self.generate_answer(question, context)

        return answer
