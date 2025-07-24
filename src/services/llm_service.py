import google.generativeai as genai
from src.config import settings

class LLMService:
    """
    Service for interacting with the Google Gemini Large Language Model.
    Handles prompt construction and API calls.
    """
    def __init__(self):
        """
        Initializes the LLMService, configuring the Gemini API with the API key
        from settings.
        """
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL_NAME)
        # print(f"LLMService initialized with model: {settings.GEMINI_MODEL_NAME}") # Removed for cleaner output

    def generate_answer_with_context(self, query: str, context_docs: list[dict]) -> str:
        """
        Generates an answer to a user query, grounded in provided context documents.

        Args:
            query (str): The user's question.
            context_docs (list[dict]): A list of dictionaries, where each dictionary
                                       represents a relevant document (e.g., product
                                       description) to be used as context.
                                       Expected to have 'title' and 'description' keys.

        Returns:
            str: The generated answer from the LLM, or a predefined message if
                 context is insufficient or an error occurs.
        """
        if not context_docs:
            return "Sorry, I couldn't find enough relevant information to answer your question."

        # Construct the context string from the retrieved documents
        context_string = "\n\n".join([
            f"Product Title: {doc.get('title', 'N/A')}\nProduct Description: {doc.get('description', 'N/A')}"
            for doc in context_docs
        ])

        # Define the prompt for the LLM
        # This prompt is crucial for grounding the LLM and preventing hallucination.
        # It instructs the LLM to use ONLY the provided context.
        prompt = f"""
        You are a helpful assistant specialized in providing information about products.
        Answer the following question based ONLY on the provided product context.
        If the context does not contain enough information to answer the question,
        respond with: "Sorry, I couldn't find enough information in our product catalog to answer that."

        Product Context:
        ---
        {context_string}
        ---

        User Question: {query}

        Your Answer:
        """

        try:
            # Make the API call to the Gemini model
            response = self.model.generate_content(prompt)

            # Check if candidates and content exist in the response
            if response.candidates and len(response.candidates) > 0 and \
               response.candidates[0].content and response.candidates[0].content.parts and \
               len(response.candidates[0].content.parts) > 0:
                return response.candidates[0].content.parts[0].text
            else:
                # Handle cases where the response structure is unexpected or content is missing
                print("Warning: LLM response did not contain expected content structure.")
                return "Sorry, I couldn't generate a response at this time."

        except Exception as e:
            print(f"Error calling LLM: {e}")
            return "An error occurred while trying to generate a response. Please try again later."

# Instantiate the service to be easily imported elsewhere
llm_service = LLMService()