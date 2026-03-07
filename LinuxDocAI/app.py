import streamlit as st
import os
from logic import process_pdf
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

st.title("📂 LinuxDocAI: Chat with your Docs")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF document", type="pdf")

if uploaded_file:
    if not os.path.exists("data"):
        os.makedirs("data")
        
    file_path = os.path.join("data", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"File '{uploaded_file.name}' uploaded!")

    if st.button("Train AI on this Document"):
        with st.spinner("Analyzing document..."):
            db = process_pdf(file_path)
            st.session_state.db = db
            st.success("AI is ready! Ask anything about the document.")

# Chat Interface
if "db" in st.session_state:
    user_question = st.text_input("Ask a question about your PDF:")
    if user_question:
        # Use the EXACT model name verified by check_models.py
        llm = ChatGoogleGenerativeAI(model="gemini-flash-latest")
        
        system_prompt = (
            "Use the following pieces of retrieved context to answer the question. "
            "If you don't know the answer, say that you don't know. "
            "\n\n"
            "{context}"
        )
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])

        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        rag_chain = create_retrieval_chain(st.session_state.db.as_retriever(), question_answer_chain)
        
        response = rag_chain.invoke({"input": user_question})
        
        st.write("### Answer:")
        st.write(response["answer"])
