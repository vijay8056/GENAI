import streamlit as st
import os
from logic import process_multiple_pdfs
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

st.set_page_config(page_title="LinuxDocAI", layout="wide")
st.title("📂 LinuxDocAI: Chat with Multiple Docs")

# Initialize Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# File uploader - ENABLED MULTIPLE FILES
uploaded_files = st.file_uploader("Upload PDF documents", type="pdf", accept_multiple_files=True)

if uploaded_files:
    if not os.path.exists("data"): 
        os.makedirs("data")
    
    file_paths = []
    for uploaded_file in uploaded_files:
        file_path = os.path.join("data", uploaded_file.name)
        with open(file_path, "wb") as f: 
            f.write(uploaded_file.getbuffer())
        file_paths.append(file_path)
    
    st.success(f"{len(uploaded_files)} files uploaded!")

    if st.button("Train AI on all Documents"):
        with st.spinner("Analyzing all documents..."):
            st.session_state.db = process_multiple_pdfs(file_paths)
            st.success("AI is ready! Ask anything about your document library.")

# Sidebar to clear memory
if st.sidebar.button("Clear Chat History"):
    st.session_state.chat_history = []
    st.rerun()

# Display Chat History
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Interface
if "db" in st.session_state:
    if user_question := st.chat_input("Ask a question about your documents:"):
        with st.chat_message("user"):
            st.markdown(user_question)
        
        st.session_state.chat_history.append({"role": "user", "content": user_question})

        llm = ChatGoogleGenerativeAI(model="gemini-flash-latest")
        
        system_prompt = (
            "Use the following pieces of retrieved context to answer the question. "
            "If you don't know the answer, say that you don't know."
            "\n\nContext: {context}"
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ])

        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        rag_chain = create_retrieval_chain(st.session_state.db.as_retriever(), question_answer_chain)
        
        response = rag_chain.invoke({
            "input": user_question,
            "chat_history": [] # Memory integration point
        })
        
        with st.chat_message("assistant"):
            st.markdown(response["answer"])
            st.session_state.chat_history.append({"role": "assistant", "content": response["answer"]})
