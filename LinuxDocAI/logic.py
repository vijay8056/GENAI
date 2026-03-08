import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

def process_multiple_pdfs(file_paths):
    all_pages = []
    
    # 1. Loop through all PDF files and load their content
    for file_path in file_paths:
        if os.path.exists(file_path):
            loader = PyPDFLoader(file_path)
            pages = loader.load()
            all_pages.extend(pages)

    # 2. Split everything into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(all_pages)

    # 3. Create the Vector DB from ALL documents at once
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    
    vector_db = Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings,
        persist_directory="./db"
    )
    return vector_db
