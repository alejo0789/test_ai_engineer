import os
import sys

# Determine the project root dynamically
# This script assumes it is placed in the project's root directory,
# or a subdirectory from which it can navigate up to the root.
current_script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = current_script_dir

# Navigate up until a directory containing 'src' is found, indicating the project root.
# This loop handles cases where the script might be in a nested directory
# if not directly at the project root by default when executed.
for _ in range(5):  # Check up to 5 levels up
    if os.path.exists(os.path.join(project_root, 'src')):
        break
    project_root = os.path.abspath(os.path.join(project_root, os.pardir))

if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(f"Added '{project_root}' to sys.path for module discovery.")

try:
    from src.data_pipeline.indexer import indexer
    from src.data_pipeline.retriever import product_retriever
    from src.config import settings # Needed for TOP_K_DOCS and data paths
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please ensure your Python path is correctly configured and the 'src' directory is accessible.")
    print(f"Current sys.path: {sys.path}")
    sys.exit(1)

print("\n--- Running Basic Retriever Logic Test ---")

# Ensure FAISS index is built/loaded
print("\nEnsuring FAISS index is built/loaded...")
try:
    indexer.index_products()
    print("✅ FAISS index ready.")
except FileNotFoundError as e:
    print(f"❌ Error: {e}. Please ensure 'data/products.json' exists in your project's 'data' directory.")
    print("You might need to run the indexing script first: python -m src.data_pipeline.indexer")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error during indexer initialization: {e}")
    sys.exit(1)

# Define a sample query and top_k value
sample_query = "shampoo for dry hair"
top_k_results = settings.TOP_K_DOCS # Using the configured TOP_K_DOCS from settings

print(f"\n--- Retrieving relevant documents for query: '{sample_query}' (Top {top_k_results}) ---")

# Get relevant documents using the retriever
try:
    relevant_documents = product_retriever.get_relevant_context(sample_query, top_k=top_k_results)

    # Print the results
    if relevant_documents:
        print("\nRetrieved Documents:")
        for doc in relevant_documents:
            print(f"  Title: {doc.get('title', 'N/A')}")
            print(f"  Description: {doc.get('description', 'N/A')}")
            print(f"  Score: {doc.get('_score', 'N/A')}")
            print("-" * 20)
    else:
        print("No relevant documents found for the query.")
except Exception as e:
    print(f"❌ An error occurred during document retrieval: {e}")
    import traceback
    traceback.print_exc()

print("\n--- Retriever Test Complete ---")