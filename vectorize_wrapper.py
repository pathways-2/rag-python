import vectorize_client as v
import os
from typing import List, Dict, Any


class VectorizeWrapper:
    def __init__(self):
        self.access_token = os.environ.get("VECTORIZE_PIPELINE_ACCESS_TOKEN")
        self.organization_id = os.environ.get("VECTORIZE_ORGANIZATION_ID")
        self.pipeline_id = os.environ.get("VECTORIZE_PIPELINE_ID")

        if not all([self.access_token, self.organization_id, self.pipeline_id]):
            raise ValueError(
                "Missing required Vectorize environment variables")

        api_config = v.Configuration(
            access_token=self.access_token,
            host="https://api.vectorize.io/v1"
        )
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
        except Exception as e:
            print(f"Error retrieving documents: {e}")
            return []
