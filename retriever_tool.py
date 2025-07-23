from crewai import Tool
from retriever import get_relevant_context

retriever_tool = Tool(
    name="SemanticRetriever",
    description="Retrieves top-k relevant product documents based on a user query.",
    func=get_relevant_context
)
