from crewai import Agent, Task, Crew, LLM, Process
import os
import sys
from src.config import settings
import yaml
import requests

# Add the project root to the Python path to allow imports from 'src'
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, project_root)

# 🔧 FIX: Import the SemanticRetrievalTool
from src.agents.tools.semantic_retrieval_tool import SemanticRetrievalTool
from src.data_pipeline.indexer import indexer  # Needed to ensure index is built

# Define file paths for YAML configurations
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AGENTS_CONFIG_PATH = os.path.join(BASE_DIR, 'configs', 'agents.yaml')
TASKS_CONFIG_PATH = os.path.join(BASE_DIR, 'configs', 'tasks.yaml')

files = {
    'agents': AGENTS_CONFIG_PATH,
    'tasks': TASKS_CONFIG_PATH
}

# Load configurations from YAML files
configs = {}
for config_type, file_path in files.items():
    with open(file_path, 'r') as file:
        configs[config_type] = yaml.safe_load(file)

# Assign loaded configurations to specific variables
agents_config = configs['agents']
tasks_config = configs['tasks']

from typing import List
from pydantic import BaseModel, Field

# 🔧 FIX: Ensure the RAG pipeline's index is built/loaded
print("Ensuring FAISS index is built/loaded...")
try:
    indexer.index_products()
    print("✅ FAISS index ready.")
except FileNotFoundError as e:
    print(f"❌ Error: {e}. Please ensure data/products.json exists.")
    exit(1)
except Exception as e:
    print(f"❌ Unexpected error during indexer initialization: {e}")
    exit(1)

# 🔧 FIX: Verify environment variables
if not settings.GOOGLE_API_KEY:
    print("❌ Error: GOOGLE_API_KEY is not set in your .env file.")
    exit(1)
if not settings.GEMINI_MODEL_NAME:
    print("❌ Error: GEMINI_MODEL_NAME is not set in your .env file.")
    exit(1)

# 🔧 FIX: Usar la misma configuración que el código que funciona
llm = LLM(
    model=settings.GEMINI_MODEL_NAME,  # ← Cambio 1: Usar configuración desde settings
    temperature=0.7,
    api_key=settings.GOOGLE_API_KEY
)

# 🔧 FIX: Instantiate the Semantic Retrieval Tool
semantic_retrieval_tool = SemanticRetrievalTool()

# 🔧 FIX: Verificar que las variables estén configuradas
print(f"Using model: {settings.GEMINI_MODEL_NAME}")
print(f"API key configured: {'Yes' if settings.GOOGLE_API_KEY else 'No'}")
print(f"Semantic retrieval tool initialized: {type(semantic_retrieval_tool).__name__}")

# Creating Agents with SemanticRetrievalTool
retriever_agent_instance = Agent(
    config=agents_config['retriever_agent'],
    tools=[semantic_retrieval_tool], # Corrected: Assign the retrieval tool
    llm=llm
)

responder_agent_instance = Agent(
    config=agents_config['responder_agent'],
    llm=llm
)

# Creating Tasks with explicit tool assignment
retrieve_task = Task(
    description=tasks_config['retrieve_product_context']['description'].format(query="{query}"), # Use {query} placeholder
    expected_output=tasks_config['retrieve_product_context']['expected_output'],
    agent=retriever_agent_instance,
    tools=[semantic_retrieval_tool]
)

generate_response_task = Task(
    description=tasks_config['generate_product_response']['description'].format(query="{query}", context="{context}"), # Use {query} and {context} placeholders
    expected_output=tasks_config['generate_product_response']['expected_output'],
    agent=responder_agent_instance,
    context_for_tool_execution={
        "query": retrieve_task.output, # The actual query from the previous task
        "context_docs": retrieve_task.output # Output of retrieve_task (list[dict])
    }
)

# Creating Crew
crew = Crew(
    agents=[
        retriever_agent_instance,
        responder_agent_instance,
    ],
    tasks=[
        retrieve_task,
        generate_response_task,
    ],
    verbose=True,
    process=Process.sequential # Ensures tasks run in order
)

user = '1234'
query = 'what shampoo can i use for damaged hair'

# The given Python dictionary
inputs = {
    'user_id': user,
    'query': query
}

# 🔧 FIX: Agregar manejo de errores
try:
    result = crew.kickoff(inputs=inputs)
    print("✅ Crew execution successful!")
    print(result)
except Exception as e:
    print(f"❌ Error during crew execution: {e}")
    import traceback
    traceback.print_exc()