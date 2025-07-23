import google.generativeai as genai
from dotenv import load_dotenv
from retriever import get_relevant_context
import os


# Load .env file
load_dotenv()
# Load API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

def simulate_llm_response(query, context_docs):
    context_text = "\n".join(f"- {doc['title']}: {doc['description']}" for doc in context_docs)

    prompt = f"""You are a helpful assistant for product questions.

Context:
{context_text}

User question: {query}

Answer based ONLY on the context above. If context is insufficient, say 'Sorry, I couldn't find enough information.'"""

    response = model.generate_content(prompt)
    return response.text.strip()

def handle_query(user_id, query):
    docs = get_relevant_context(query)
    if not docs:
        return "Sorry, I couldn't find anything relevant."

    return simulate_llm_response(query, docs)
