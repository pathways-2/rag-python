from abc import ABC, abstractmethod
from typing import List, Dict, Any
from enum import Enum


class RAGSourceType(Enum):
    NONE = "none"
    VECTORIZE = "vectorize"
    PINECONE = "pinecone"


class RAGSourceBase(ABC):
    """Base class for all RAG document retrieval sources."""

    @abstractmethod
    def retrieve_documents(self, question: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents based on the question.

        Args:
            question: The query string
            num_results: Number of results to return

        Returns:
            List of documents with relevant content
        """
        pass

    @abstractmethod
    def get_required_env_vars(self) -> List[str]:
        """
        Get list of required environment variables for this source.

        Returns:
            List of environment variable names
        """
        pass
