import os
from typing import List, Dict, Any
from rag_source_base import RAGSourceBase


class PineconeWrapper(RAGSourceBase):
    """Mock implementation of Pinecone vector database wrapper."""

    def __init__(self):
        self.api_key = os.environ.get("PINECONE_API_KEY")
        self.environment = os.environ.get("PINECONE_ENVIRONMENT")
        self.index_name = os.environ.get("PINECONE_INDEX_NAME")

        if not all([self.api_key, self.environment, self.index_name]):
            raise ValueError("Missing required Pinecone environment variables")

        print(f"Mock Pinecone initialized with index: {self.index_name}")

    def retrieve_documents(self, question: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """
        Mock implementation that returns sample documents.
        In a real implementation, this would query the Pinecone vector database.
        """
        mock_documents = []

        for i in range(min(num_results, 3)):
            mock_documents.append({
                'text': f"This is a mock document {i+1} retrieved from Pinecone for query: '{question}'. "
                f"In a real implementation, this would contain actual content from your knowledge base.",
                'source_display_name': f"mock_source_{i+1}.txt",
                'relevancy': 0.95 - (i * 0.1),
                'metadata': {
                    'source': 'pinecone_mock',
                    'index': self.index_name
                }
            })

        return mock_documents

    def get_required_env_vars(self) -> List[str]:
        return [
            "PINECONE_API_KEY",
            "PINECONE_ENVIRONMENT",
            "PINECONE_INDEX_NAME"
        ]
