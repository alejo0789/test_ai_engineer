from crewai.tools import BaseTool
from src.data_pipeline.retriever import product_retriever # Import the instantiated retriever
from src.config import settings # Import settings for top_k

class SemanticRetrievalTool(BaseTool):
    name: str = "Semantic Product Retriever"
    description: str = (
        "Useful for semantically searching and retrieving the most relevant product documents "
        "from the knowledge base based on a user's query. "
        f"Returns the top {settings.TOP_K_DOCS} most relevant documents by default."
    )
   

    def _run(self, query: str) -> list[dict]: 
        """
        Executes the semantic retrieval based on the provided query.

        Args:
            query (str): The user's question or search query.

        Returns:
            list[dict]: A list of dictionaries, where each dictionary is a relevant product document.
                        Returns an empty list if no results are found.
        """
        relevant_docs = product_retriever.get_relevant_context(query, top_k=settings.TOP_K_DOCS)
        return relevant_docs