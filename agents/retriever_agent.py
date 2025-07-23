from crewai import Agent
from retriever import get_relevant_context

def RetrieverAgent():
    return Agent(
        name="Retriever Agent",
        role="Responsible for retrieving the most relevant product descriptions",
        goal="Given a user query, return the top-k matching documents from the knowledge base",
        backstory="Specialized in vector-based semantic search using FAISS",
        tools=[get_relevant_context]
    )
