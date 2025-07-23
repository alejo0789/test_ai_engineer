from crewai import Agent
from responder import generate_answer_with_context

def ResponderAgent():
    return Agent(
        name="Responder Agent",
        role="Responsible for responding to user questions using Gemini",
        goal="Craft accurate and helpful answers grounded in retrieved context",
        backstory="LLM-powered agent focused on factual, context-based answers only",
        tools=[generate_answer_with_context]
    )
