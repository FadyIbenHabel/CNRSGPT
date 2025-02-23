from flask import Flask, request, jsonify , render_template
from llama_index.core import SimpleDirectoryReader, Document, StorageContext
from llama_index.core.indices.vector_store.base import VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.settings import Settings
from llama_index.llms.groq import Groq
from llama_index.readers.file import PDFReader
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
import pymongo
import re

# Initialize Flask App
app = Flask(__name__)

# Secret Key for LLM API 
secretkey="le clé secret de GroqCloudApi"

# Initialize LLM Model (Groq Llama-3.3-70B)
llm = Groq(model="llama-3.3-70b-versatile", api_key=secretkey)

# Configure Embedding Model
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
Settings.chunk_size = 512
Settings.chunk_overlap = 50

# Connect to MongoDB Atlas
mongo_uri = "mongodb+srv://<identifiant>:<mot de passe>@cluster01.c42ne.mongodb.net/?retryWrites=true&w=majority&appName=Cluster01"
mongodb_client = pymongo.MongoClient(mongo_uri)
vector_store = MongoDBAtlasVectorSearch(mongodb_client)
vector_store.create_vector_search_index(dimensions=384, path="embedding", similarity="cosine")
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Function to clean unwanted sections from PDFs
def preprocess_text(text):
    noise_patterns = [
        r"\b(references|bibliography|acknowledgments|appendix)\b.*",
        r"DOI\s?:?\s?\d+\.\d+/[^\s]+",
        r"©\s?\d{4}.*",
        r"Permission to make digital or hard copies.*",
    ]
    for pattern in noise_patterns:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE | re.DOTALL)
    return text.strip()

# Loading documents from local storage
def load_documents():
    documents = []
    reader = SimpleDirectoryReader("./data", file_extractor={".pdf": PDFReader()})
    for doc in reader.load_data():
        cleaned_text = preprocess_text(doc.text)
        new_doc = Document(text=cleaned_text, metadata=doc.metadata)
        documents.append(new_doc)
    return documents

# Initialize Vector Index
def initialize_index():
    global index
# creating the index
    documents = load_documents()
    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context, show_progress=True)
# loading the index from stored vectors (apres la premiere compilation on de-commente ça)
#index = VectorStoreIndex.from_vector_store(
#    vector_store=vector_store, storage_context=storage_context
#)

# Initialize Query Engine
def initialize_chatbot():
    global query_engine
    query_engine = index.as_chat_engine(
        llm=llm,
        chat_mode="context",
        system_prompt=(
            "You are an advanced academic chatbot specializing in University of Lyon 1 research papers."
            "Your primary role is to assist users by providing precise, research-backed responses based on these papers."
            "You must focus only on answering questions related to the research content provided."
            "If a question is related to the research, provide a structured, detailed, and professional response."
            "Ensure your answers are factually accurate, technically correct, and well-structured."
            "If necessary, cite key findings from the papers while avoiding unnecessary speculation."
        ),
    )

# Initialize Index & Chat Engine
initialize_index()
initialize_chatbot()
# API Route : Home Route
@app.route('/')
def home():
    return render_template('chatbot.html')

# API Route: Query Chatbot
@app.route("/query", methods=["GET"])
def query_index():
    query_text = request.args.get("text", None)
    if not query_text:
        return jsonify({"error": "No text provided"}), 400

    response = query_engine.chat(query_text)
    return jsonify({"response": str(response)}), 200

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
