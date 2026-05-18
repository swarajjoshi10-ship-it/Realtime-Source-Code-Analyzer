from src.helper import repo_ingestion, load_repo, text_splitter, load_embedding
from dotenv import load_dotenv
from langchain.vectorstores import Chroma

load_dotenv()

#url = "https://github.com/swarajjoshi10-ship-it/stateful-agentic"
#repo_ingestion(url)

documents = load_repo("repo/")
text_chunks = text_splitter(documents)

embeddings = load_embedding()

vectordb = Chroma.from_documents(
    text_chunks,
    embeddings,
    persist_directory="./db"
)

vectordb.persist()