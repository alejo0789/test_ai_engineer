import os
import json
import faiss
from sentence_transformers import SentenceTransformer # Reverted: Directly import SentenceTransformer
from src.config import settings

class ProductRetriever:
    """
    Handles the retrieval of relevant product documents from the FAISS index.
    """
    def __init__(self):
        # Reverted: Initialize SentenceTransformer directly
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.docs_data_path = settings.DOCS_DATA_PATH
        self.faiss_index_path = settings.FAISS_INDEX_PATH
        self.documents = self._load_documents()
        self.index = self._load_faiss_index()

    def _load_documents(self):
        """Loads processed documents from the JSON file."""
        if not os.path.exists(self.docs_data_path):
            raise FileNotFoundError(f"Processed documents file not found: {self.docs_data_path}. Please ensure indexing has been performed.")
        with open(self.docs_data_path, 'r', encoding='utf-8') as f:
            docs = json.load(f)
        return docs

    def _load_faiss_index(self):
        """Loads the FAISS index from file."""
        if not os.path.exists(self.faiss_index_path):
            raise FileNotFoundError(f"FAISS index file not found: {self.faiss_index_path}. Please ensure indexing has been performed.")
        index = faiss.read_index(self.faiss_index_path)
        return index

    def get_relevant_context(self, query: str, top_k: int = None) -> list[dict]:
        """
        Retrieves the top-k most semantically similar product documents to the given query.

        Args:
            query (str): The user's query.
            top_k (int, optional): The number of top documents to retrieve.
                                   Defaults to settings.TOP_K_DOCS.

        Returns:
            list[dict]: A list of dictionaries, where each dictionary is a relevant product document.
        """
        if top_k is None:
            top_k = settings.TOP_K_DOCS

        # Encode the query using self.model directly
        query_embedding = self.model.encode([query]).reshape(1, -1) # Reshape for FAISS search

        # Perform a similarity search on the FAISS index
        distances, indices = self.index.search(query_embedding, top_k)

        relevant_docs = []
        for i, idx in enumerate(indices[0]):
            if idx != -1: # Ensure the index is valid
                doc = self.documents[idx]
                doc["_score"] = float(distances[0][i]) # Add score for debugging/ranking insight
                relevant_docs.append(doc)

        return relevant_docs

# Instantiate the retriever
product_retriever = ProductRetriever()