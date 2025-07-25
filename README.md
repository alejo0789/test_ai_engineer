# Product Query Bot - RAG Pipeline with Multi-Agent System

A microservice that simulates WhatsApp product queries using a RAG (Retrieval-Augmented Generation) pipeline with multi-agent architecture built with CrewAI and Google Gemini.

## 🎯 Project Overview

This project implements a product query bot that:
- Receives user questions via REST API
- Uses semantic search to find relevant product information
- Employs a multi-agent system (Retriever + Responder agents)
- Returns contextually grounded answers using Google Gemini LLM

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Flask API     │───▶│  Multi-Agent     │───▶│   RAG Pipeline  │
│   /query        │    │  CrewAI System   │    │   FAISS + LLM   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  Retriever Agent │
                    │  (Semantic       │
                    │   Search)        │
                    └──────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  Responder Agent │
                    │  (Answer         │
                    │   Generation)    │
                    └──────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Desktop (for containerized deployment)
- Google API Key for Gemini

### Option 1: Docker Deployment (Recommended)

1. **Clone and setup environment:**
```bash
git clone <your-repo-url>
cd ai_engineer_microservice
```

2. **Create `.env` file:**
```bash
# Copy and edit the environment file
cp .env.example .env
```

Add your Google API key to `.env`:
```
GOOGLE_API_KEY="your_google_api_key_here"
TOP_K_DOCS=5
GEMINI_MODEL_NAME="gemini/gemini-2.0-flash-exp"
```

3. **Start Docker Desktop** (Windows/Mac):
   - Open Docker Desktop from Start Menu
   - Wait for Docker to fully start (whale icon in system tray)

4. **Build and run with Docker Compose:**
```bash
# Build and start the service
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

5. **Verify the service is running:**
```bash
curl http://localhost:5000/health
```

### Option 2: Local Development

1. **Setup virtual environment:**
```bash
python -m venv ai_engineer_microservice
# Windows
ai_engineer_microservice\Scripts\activate
# Mac/Linux  
source ai_engineer_microservice/bin/activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python src/app.py
```

## 🧪 Testing the Application

### Health Check
```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "Product Query Bot is up and running!"
}
```

### Product Query Examples

**1. Hair care query:**
```bash
curl -X POST http://localhost:5000/query \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123", 
    "query": "what shampoo can I use for damaged hair?"
  }'
```

**2. Styling products query:**
```bash
curl -X POST http://localhost:5000/query \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user456", 
    "query": "I need something to hold my hairstyle all day"
  }'
```

**3. Hair treatment query:**
```bash
curl -X POST http://localhost:5000/query \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user789", 
    "query": "weekly treatment for dry hair"
  }'
```

### Using PowerShell (Windows):
```powershell
$body = @{
    user_id = "test_user"
    query = "what shampoo can I use for damaged hair?"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/query" -Method Post -Body $body -ContentType "application/json"
```

### Expected Response Format:
```json
{
  "user_id": "user123",
  "query": "what shampoo can I use for damaged hair?",
  "response": "Based on our product catalog, I recommend the Zubale Shampoo for damaged hair. It's a natural shampoo enriched with aloe and vitamin E that refreshes and strengthens hair. For additional treatment, you might also consider the Zubale Hair Mask, which is specifically designed as a deep treatment for dry and damaged hair and should be used weekly for best results."
}
```

## 🔧 Configuration

### Environment Variables
- `GOOGLE_API_KEY`: Your Google Gemini API key (required)
- `TOP_K_DOCS`: Number of documents to retrieve (default: 5)
- `GEMINI_MODEL_NAME`: Gemini model to use (default: "gemini/gemini-2.0-flash-exp")
- `FLASK_DEBUG`: Enable Flask debug mode (0/1)
- `PORT`: Port for the Flask app (default: 5000)

### Product Data
Products are stored in `data/products.json`. The system automatically:
1. Indexes product descriptions into FAISS vector store
2. Creates embeddings using SentenceTransformers
3. Stores processed data in `data/docs.json` and `data/faiss.index`

## 🏛️ Project Structure

```
├── src/
│   ├── agents/
│   │   ├── configs/
│   │   │   ├── agents.yaml      # Agent configurations
│   │   │   └── tasks.yaml       # Task definitions
│   │   ├── tools/
│   │   │   └── semantic_retrieval_tool.py
│   │   ├── crew.py             # Main crew orchestration
│   │   └── crew_test.py        # Production crew class
│   ├── data_pipeline/
│   │   ├── indexer.py          # FAISS indexing logic
│   │   └── retriever.py        # Semantic retrieval
│   ├── services/
│   │   └── llm_service.py      # Gemini LLM integration
│   ├── app.py                  # Flask application
│   ├── config.py               # Configuration management
│   └── schema.py               # Input validation
├── data/
│   ├── products.json           # Source product data
│   ├── docs.json              # Processed documents (auto-generated)
│   └── faiss.index            # Vector index (auto-generated)
├── tests/
│   └── unit/                   # Unit tests
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env                        # Environment variables
```

## 🤖 Multi-Agent System

### Retriever Agent
- **Role**: Product Information Retriever
- **Goal**: Semantically search and retrieve relevant product documents
- **Tools**: SemanticRetrievalTool (FAISS + SentenceTransformers)

### Responder Agent  
- **Role**: Product Information Responder
- **Goal**: Generate accurate answers grounded in retrieved context
- **Tools**: Google Gemini LLM integration

### Agent Communication Flow
1. **Input**: User query received via REST API
2. **Retrieval**: Retriever Agent finds top-k similar products
3. **Generation**: Responder Agent crafts contextual answer
4. **Output**: JSON response with grounded answer

## 🧪 Running Tests

```bash
# Run unit tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## 🐳 Docker Commands

```bash
# Build image
docker build -t product-query-bot .

# Run container
docker run -p 5000:5000 --env-file .env product-query-bot

# Using docker-compose
docker-compose up --build    # Build and run
docker-compose down         # Stop services
docker-compose logs         # View logs
```

## 🚨 Troubleshooting

### Common Issues

**1. Docker daemon not running (Windows):**
```
ERROR: error during connect: this error may indicate that the docker daemon is not running
```
**Solution**: Start Docker Desktop from Start Menu and wait for it to fully load.

**2. Google API Key errors:**
```
❌ Error: GOOGLE_API_KEY is not set in your .env file.
```
**Solution**: Add your Google API key to the `.env` file.

**3. FAISS index not found:**
```
FileNotFoundError: FAISS index file not found
```
**Solution**: The app automatically builds the index on first run. Ensure `data/products.json` exists.

**4. Port already in use:**
```
Error: Port 5000 is already in use
```
**Solution**: 
```bash
# Change port in docker-compose.yml or .env
PORT=5001

# Or stop other services using port 5000
```

### Debug Mode
To enable verbose logging:
```bash
# Set in .env file
FLASK_DEBUG=1

# Or run directly
FLASK_DEBUG=1 python src/app.py
```

## 📊 Performance & Metrics

- **Indexing**: ~5 products indexed in <1 second
- **Query Response**: Average response time <2 seconds
- **Memory Usage**: ~200MB with loaded models
- **Vector Store**: FAISS L2 distance, 384-dimensional embeddings

## 🔮 Future Enhancements

- [ ] Conversation memory/context tracking
- [ ] Multi-language support
- [ ] Real-time product catalog updates
- [ ] Analytics and usage metrics
- [ ] Rate limiting and authentication
- [ ] Advanced prompt engineering
- [ ] Integration with external product APIs

## 📝 Development Notes

**Time Spent**: ~3 hours
- Setup & Architecture: 45 min
- RAG Pipeline Implementation: 60 min  
- Multi-Agent System: 45 min
- Testing & Documentation: 30 min

**Key Design Decisions**:
- Used CrewAI for agent orchestration (simpler than LangGraph for this scope)
- FAISS for vector storage (fast, lightweight)
- SentenceTransformers for embeddings (good quality/speed balance)
- Google Gemini for generation (reliable, cost-effective)

## 📧 Contact

For questions or issues, please contact:
- alejo0789@hotmail.com


---

**Built with ❤️ Alejandro Carvajal for Zubale's AI Engineering Assessment**