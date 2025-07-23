import json
import faiss
import os
from sentence_transformers import SentenceTransformer

DATA_PATH = "data/products.json"
INDEX_PATH = "data/faiss.index"
DOCS_PATH = "data/docs.json"

model = SentenceTransformer('all-MiniLM-L6-v2')

def index_documents():
    if os.path.exists(INDEX_PATH):
        print("Index already exists.")
        return

    with open(DATA_PATH, "r") as f:
        products = json.load(f)

    texts = [p["description"] for p in products]
    embeddings = model.encode(texts)

    dim = embeddings[0].shape[0]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    faiss.write_index(index, INDEX_PATH)

    with open(DOCS_PATH, "w") as f:
        json.dump(products, f)

    print("Indexed products into FAISS.")
