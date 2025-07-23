import faiss
import json
from sentence_transformers import SentenceTransformer

INDEX_PATH = "data/faiss.index"
DOCS_PATH = "data/docs.json"
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load index and docs once
index = faiss.read_index(INDEX_PATH)
with open(DOCS_PATH, "r") as f:
    documents = json.load(f)

def get_relevant_context(query, top_k=2):
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, top_k)

    results = [documents[i] for i in indices[0]]
    return results
