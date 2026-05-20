# Realtime Source Code Analyzer

A full-stack Retrieval-Augmented Generation (RAG) system designed to clone, parse, and analyze GitHub repositories in real-time. Built with LangChain, ChromaDB, and Flask, this application allows developers to interactively chat with and query arbitrary codebases using context-aware LLMs.

## Problem Statement

Understanding complex or unfamiliar codebases is a significant bottleneck in software engineering. Traditional search tools (like `grep`) lack semantic understanding and architectural context. This project solves this by transforming raw source code into a queryable, semantic knowledge base, enabling engineers to ask natural language questions about architecture, logic, and dependencies, drastically reducing onboarding and debugging time.

## Features

* **Real-time Repository Ingestion:** Dynamically clones and processes target GitHub repositories on demand.
* **Language-Aware Chunking:** Uses AST-based parsing (`LanguageParser`) and language-specific recursive text splitting to maintain logical code boundaries (e.g., keeping functions and classes intact).
* **Local Vector Embeddings:** Leverages HuggingFace (`all-MiniLM-L6-v2`) for fast, local, and cost-effective embedding generation.
* **Semantic Vector Search:** Implements ChromaDB for efficient storage and MMR (Maximal Marginal Relevance) retrieval of code snippets.
* **Context-Aware Memory:** Utilizes `ConversationSummaryMemory` to maintain chat history and context across multi-turn Q&A sessions.
* **LLM Orchestration:** Integrates `ConversationalRetrievalChain` with OpenRouter (OpenAI-compatible endpoints) for intelligent code analysis and explanation.

## Architecture

The system follows a modular, event-driven architecture designed for scalability and clear separation of concerns:

1. **Frontend UI (`templates/`, `static/`):** A responsive web interface for users to input repository URLs and chat with the AI.
2. **Backend Services (`app.py`):** A Flask application serving as the orchestration layer, handling routing, state management, and API integrations.
3. **Ingestion Pipeline (`src/helper.py`):** 
   - Clones the target repository.
   - Loads `.py` files using LangChain's `GenericLoader`.
   - Chunks the documents semantically.
4. **Vector Database (`db/`):** A persistent Chroma instance that stores the code embeddings.
5. **Retrieval & Generation:** When a query is made, the system embeds the query, searches Chroma for the top `k` most relevant code chunks (using MMR), and passes them along with conversation history to the LLM to generate an accurate response.

## Tech Stack

* **AI/LLM:** LangChain, OpenRouter (ChatOpenAI), HuggingFace Embeddings
* **Backend:** Python, Flask
* **Database/Vector DB:** ChromaDB
* **Frontend:** HTML, CSS, JavaScript (Jinja2 Templates)
* **DevOps/Tools:** GitPython, python-dotenv

## Project Structure

```
Realtime-Source-Code-Analyzer/
├── app.py                  # Main Flask application and orchestration logic
├── store_index.py          # Standalone script for manual embedding and DB initialization
├── src/
│   └── helper.py           # Core ingestion logic: cloning, parsing, chunking, and embedding
├── templates/              # HTML templates for the web interface
├── static/                 # Static assets (CSS/JS)
├── db/                     # Persisted Chroma vector database
├── repo/                   # Ephemeral directory for cloned target repositories
├── requirements.txt        # Python dependencies
└── .env                    # Environment variables (e.g., API keys)
```

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/Realtime-Source-Code-Analyzer.git
   cd Realtime-Source-Code-Analyzer
   ```

2. **Set up a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory and add your API keys:
   ```env
   OPENAI_API_KEY=your_openrouter_api_key_here
   ```

## Usage

Start the Flask development server:

```bash
python app.py
```

Navigate to `http://localhost:8000` in your browser. Enter a GitHub repository URL to ingest the codebase, and begin asking architectural or implementation questions via the chat interface.

## Challenges Faced & Optimizations

* **Context Window Management:** Large code files easily exceed LLM context limits. Implemented `RecursiveCharacterTextSplitter` with Python language awareness to ensure chunks are logically sound and fit within token limits.
* **Retrieval Relevance:** Standard similarity search often returned redundant code snippets. Switched to Maximal Marginal Relevance (MMR) search to optimize for both relevance and diversity in the retrieved context.
* **State Management:** Handled dynamic repository switching by safely clearing the ephemeral `repo/` directory before new ingestions.

## License

This project is licensed under the MIT License.
