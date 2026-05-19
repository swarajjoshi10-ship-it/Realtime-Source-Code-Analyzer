# Realtime Source Code Analyzer 🚀

A powerful, AI-driven web application that allows you to paste any GitHub repository link and instantly chat with its codebase! Built using Flask, LangChain, ChromaDB, and modern web technologies, this tool clones the repository, indexes its files, and uses an advanced LLM to answer your questions about the source code.

## 🌟 Features

* **Instant Repository Ingestion:** Simply paste a GitHub URL, and the app will clone it and extract all Python files for analysis.
* **Vector-based Search:** Uses ChromaDB and HuggingFace's `all-MiniLM-L6-v2` embedding model to split, embed, and store code chunks for lightning-fast semantic retrieval.
* **Intelligent Q&A:** Powered by OpenRouter and Langchain's `ConversationalRetrievalChain`, allowing you to ask complex questions about the architecture, logic, and functions within the codebase.
* **Interactive UI:** A modern, clean chat interface built with jQuery and CSS, featuring:
  * Dynamic Markdown rendering using `marked.js` so code blocks and lists look perfect.
  * Real-time loading indicators.
  * Persistent repository URLs.
* **In-Process Indexing:** Architected to prevent SQLite lock errors by handling database operations securely on a single thread.

## 🛠️ Technology Stack

* **Backend:** Python, Flask
* **AI/LLM:** LangChain, OpenRouter API (`ChatOpenAI`)
* **Vector Database:** ChromaDB
* **Embeddings:** HuggingFace `sentence-transformers`
* **Frontend:** HTML5, Vanilla CSS, JavaScript (jQuery, marked.js)

## ⚙️ Installation & Setup

1. **Clone this repository:**
   ```bash
   git clone <your-repo-url>
   cd Realtime-Source-Code-Analyzer
   ```

2. **Set up a Virtual Environment:**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory and add your OpenRouter/OpenAI API key:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

## 🚀 Usage

1. Start the Flask application:
   ```bash
   python app.py
   ```
2. Open your web browser and navigate to `http://localhost:8000`.
3. Paste a GitHub repository URL into the input field and click **Load Repository**.
4. Wait a few seconds for the green ✅ success message.
5. Start asking the AI questions about the code! (e.g., "What does the `repo_ingestion` function do?", or "Explain the graph builder workflow.")

## 📝 Important Notes
- The app is currently configured to parse `.py` files automatically. 
- Ensure your repository URL is public (so it doesn't prompt for git credentials in the background).
- The vector database is stored locally in the `db/` folder. If you ever switch embedding models, make sure to delete this folder to avoid dimensionality errors!

