from langchain.vectorstores import Chroma
from src.helper import load_embedding, repo_ingestion
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify, render_template
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryMemory

app = Flask(__name__)
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

embeddings=load_embedding()
persist_directory="db"

#load persisted database from disk and use it as normal
vectordb = Chroma(persist_directory=persist_directory,
                  embedding_function=embeddings)

#llm=ChatOpenAI()
llm = ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=OPENAI_API_KEY,
    model_name="openrouter/free"
)

memory=ConversationSummaryMemory(llm=llm,
                                  memory_key="chat_history",
                                  return_messages=True)
qa = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectordb.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 8}
    ),
    memory=memory
)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/chatbot", methods=["GET", "POST"])
def gitRepo():

    if request.method == "POST":
        user_input = request.form.get("question")
        try:
            repo_ingestion(user_input)
            from src.helper import load_repo, text_splitter
            documents = load_repo("repo/")
            if not documents:
                return jsonify({"error": "No Python files found in this repository."}), 400
                
            text_chunks = text_splitter(documents)
            if not text_chunks:
                return jsonify({"error": "Failed to chunk documents."}), 400
                
            global vectordb
            vectordb.add_documents(text_chunks)
            vectordb.persist()
        except Exception as e:
            print(f"Error loading repo: {e}")
            return jsonify({"error": str(e)}), 400
    
    return jsonify({"response": str(user_input)})

@app.route("/get",methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input=msg
    print(input)

    if input == "clear":
        if os.path.exists("repo"):
            os.system("rmdir /s /q repo")

    result=qa(input)
    print(result['answer'])
    return str(result['answer'])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True, threaded=False)

