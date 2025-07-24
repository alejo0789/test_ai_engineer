import os
import json
import faiss
from sentence_transformers import SentenceTransformer
from src.config import settings

class ProductIndexer:
    """
    Handles the indexing of product descriptions into a FAISS vector store.
    """
    def __init__(self):
        # Initialize the Sentence Transformer model for embeddings.
        # This will be refactored to use src/services/embedding_service.py later.
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.products_data_path = settings.PRODUCTS_DATA_PATH
        self.docs_data_path = settings.DOCS_DATA_PATH
        self.faiss_index_path = settings.FAISS_INDEX_PATH
        self.documents = []
        self.index = None

    def _load_products(self):
        """Loads product data from the JSON file."""
        if not os.path.exists(self.products_data_path):
            raise FileNotFoundError(f"Product data file not found: {self.products_data_path}")
        with open(self.products_data_path, 'r', encoding='utf-8') as f:
            products = json.load(f)
        self.documents = products
        print(f"Loaded {len(self.documents)} products from {self.products_data_path}")

    def _create_embeddings(self):
        """Creates embeddings for all product descriptions."""
        print("Creating embeddings for product descriptions...")
        descriptions = [doc['description'] for doc in self.documents]
        embeddings = self.model.encode(descriptions, show_progress_bar=True)
        print("Embeddings created.")
        return embeddings

    def _build_faiss_index(self, embeddings):
        """Builds and saves the FAISS index."""
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)  # L2 distance for similarity
        self.index.add(embeddings)
        print(f"FAISS index built with {self.index.ntotal} vectors.")

    def _save_index(self):
        """Saves the FAISS index and processed documents."""
        os.makedirs(os.path.dirname(self.faiss_index_path), exist_ok=True)
        faiss.write_index(self.index, self.faiss_index_path)
        with open(self.docs_data_path, 'w', encoding='utf-8') as f:
            json.dump(self.documents, f, indent=4)
        print(f"FAISS index saved to {self.faiss_index_path}")
        print(f"Processed documents saved to {self.docs_data_path}")

    def index_products(self):
        """Main method to load products, create embeddings, and build/save the index."""
        if os.path.exists(self.faiss_index_path) and os.path.exists(self.docs_data_path):
            print("FAISS index and docs.json already exist. Skipping indexing.")
            return

        print("Starting product indexing...")
        self._load_products()
        embeddings = self._create_embeddings()
        self._build_faiss_index(embeddings)
        self._save_index()
        print("Product indexing complete.")

indexer = ProductIndexer()
