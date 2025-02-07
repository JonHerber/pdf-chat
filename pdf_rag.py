import streamlit as st

from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

template = """
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, tell the user, that you do not know the answer! Answer with five sentences to keep your answer clear and concise.

Question: {question}
Context: {context}
Answer:
"""

# directory for saving the uploaded files by user
pdf_dir = "pdf-files/"

# load embeddings in memory to retrieve later
# set model to "light" model, can also upgrade to bigger version
embeddings = OllamaEmbeddings(model="deepseek-r1:7b")
vector_store = InMemoryVectorStore(embeddings)

# set same model as for embeddings
model = OllamaLLM(model="deepseek-r1:7b")

def upload_pdf(file):
    # debug print:
    print(pdf_dir + file.name)
    with open(pdf_dir + file.name, "wb") as f:
        f.write(file.getbuffer())

def load_pdf(file_path):
    loader = PDFPlumberLoader(file_path)
    documents = loader.load()

    return documents

def split_text(documents):
    # default splitter with default parameters, might need some tuning
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )

    return text_splitter.split_documents(documents)

# load additional information into rag
def index_documents(documents):
    vector_store.add_documents(documents)

# load information from rag
def retrieve_documents(query):
    return vector_store.similarity_search(query)

def answer_question(question, documents):
    context = "\n\n".join([doc.page_content for doc in documents])
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    return chain.invoke({"question": question, "context": context})

# set UI to only accept PDFs and only one file at a time, can also adjust code to accept multiple documents 
uploaded_file = st.file_uploader(
    "Upload your PDF file here:",
    type="pdf",
    accept_multiple_files=False
)

if uploaded_file:
    upload_pdf(uploaded_file)
    documents = load_pdf(pdf_dir + uploaded_file.name)
    document_chunks = split_text(documents)
    index_documents = (document_chunks)

    question = st.chat_input()

    if question:
        st.chat_message("user").write(question)
        related_information = retrieve_documents(question)
        answer = answer_question(question, related_information)
        st.chat_message("assistant").write(answer)
