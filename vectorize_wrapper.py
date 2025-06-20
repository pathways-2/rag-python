import vectorize_client as v
import os
import ssl
import urllib3
from typing import List, Dict, Any
from rag_source_base import RAGSourceBase

# Disable SSL warnings if we're bypassing verification
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class VectorizeWrapper(RAGSourceBase):
    def __init__(self):
        self.access_token = os.environ.get("VECTORIZE_PIPELINE_ACCESS_TOKEN")
        self.organization_id = os.environ.get("VECTORIZE_ORGANIZATION_ID")
        self.pipeline_id = os.environ.get("VECTORIZE_PIPELINE_ID")

        if not all([self.access_token, self.organization_id, self.pipeline_id]):
            raise ValueError(
                "Missing required Vectorize environment variables")

        # Create SSL context
        try:
            # Try to create a default SSL context first
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = True
            ssl_context.verify_mode = ssl.CERT_REQUIRED
        except Exception:
            # If that fails, create an unverified context as fallback
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            print("Warning: Using unverified SSL context due to certificate issues")

        api_config = v.Configuration(
            access_token=self.access_token,
            host="https://api.vectorize.io/v1"
        )
        
        # Try to configure SSL context if the client supports it
        try:
            api_config.ssl_context = ssl_context
        except AttributeError:
            # If the client doesn't support ssl_context, we'll rely on system settings
            pass
            
        self.api_client = v.ApiClient(api_config)
        self.pipelines = v.PipelinesApi(self.api_client)

    def retrieve_documents(self, question: str, num_results: int = 5) -> List[Dict[str, Any]]:
        try:
            response = self.pipelines.retrieve_documents(
                self.organization_id,
                self.pipeline_id,
                v.RetrieveDocumentsRequest(
                    question=question,
                    num_results=num_results,
                )
            )
            return response.documents
        except ssl.SSLError as e:
            print(f"SSL Error retrieving documents: {e}")
            print("This is likely due to certificate verification issues on macOS.")
            print("Try running: /Applications/Python\\ 3.*/Install\\ Certificates.command")
            return []
        except Exception as e:
            print(f"Error retrieving documents: {e}")
            return []

    def get_required_env_vars(self) -> List[str]:
        return [
            "VECTORIZE_PIPELINE_ACCESS_TOKEN",
            "VECTORIZE_ORGANIZATION_ID",
            "VECTORIZE_PIPELINE_ID"
        ]
