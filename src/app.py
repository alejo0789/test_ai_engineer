from flask import Flask, request, jsonify
from src.schema import validate_query_request
from src.agents.crew_test import product_query_crew
from src.data_pipeline.indexer import indexer # Import the product_indexer
import os

app = Flask(__name__)

# --- Application Startup (Corrected Initialization) ---
# Initialize the RAG pipeline by ensuring FAISS index and documents are ready.
# This ensures the knowledge base is built before the server starts.
print("Initializing RAG pipeline: Checking/building FAISS index...")
try:
    indexer.index_products()
    print("RAG pipeline initialized successfully.")
except Exception as e:
    print(f"Error during RAG pipeline initialization: {e}")
    # Consider raising the exception here if the app cannot function without the index
    # raise e # Uncomment to prevent app from starting if indexing fails

# --- Health Check Endpoint (Optional but Recommended) ---
@app.route('/health', methods=['GET'])
def health_check():
    """
    Provides a simple health check endpoint to confirm the application is running.
    """
    return jsonify({"status": "healthy", "message": "Product Query Bot is up and running!"}), 200

# --- Main Query Endpoint ---
@app.route('/query', methods=['POST'])
def handle_query():
    """
    Handles incoming user queries, validates them, and processes them
    through the multi-agent CrewAI pipeline.
    """
    try:
        # 1. Get JSON data from the request
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request must be JSON"}), 400

        # 2. Validate input using schema.py
        validated_data = validate_query_request(data)
        user_id = validated_data["user_id"]
        query = validated_data["query"]

        print(f"Received query from user '{user_id}': '{query}'")

        # 3. Execute the multi-agent CrewAI pipeline
        # The product_query_crew handles both retrieval and response generation.
        final_answer = product_query_crew.run_crew(user_id=user_id, query=query)

        # 4. Return the result
        return jsonify({"user_id": user_id, "query": query, "response": final_answer}), 200

    except ValueError as e:
        # Handle validation errors from schema.py
        print(f"Validation Error: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Catch any other unexpected errors during processing
        print(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An internal server error occurred.", "details": str(e)}), 500

if __name__ == '__main__':
    # Set FLASK_DEBUG to 1 for development, 0 for production.
    # In a Docker setup, this might be handled via environment variables.
    app.run(host='0.0.0.0', port=os.getenv("PORT", 5000), debug=os.getenv("FLASK_DEBUG", "0") == "1")