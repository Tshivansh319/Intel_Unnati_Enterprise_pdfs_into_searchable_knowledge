import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
import fitz  # PyMuPDF for ToC

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.2,
    groq_api_key=os.getenv("GROQ_API_KEY")
)

embeddings = HuggingFaceEmbeddings(
    model_name="intfloat/multilingual-e5-large",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True}
)

def get_vectorstore():
    try:
        return Qdrant.from_existing_collection(
            embedding=embeddings,
            path="./qdrant_db",
            collection_name="pdf_knowledge"
        )
    except:
        return None

def extract_toc(pdf_path):
    """PDF ?? Table of Contents ??????? ??"""
    doc = fitz.open(pdf_path)
    toc = doc.get_toc()
    doc.close()
    return toc

def index_pdfs(pdf_paths):
    if not pdf_paths:
        raise ValueError("No PDF files provided.")
    
    all_docs = []
    for pdf_path in pdf_paths:
        try:
            loader = PyPDFLoader(pdf_path)
            docs = loader.load()
            if not docs:
                print(f"Warning: No text extracted from {pdf_path}")
                continue
            all_docs.extend(docs)
        except Exception as e:
            print(f"Error loading {pdf_path}: {e}")
            continue
    
    if not all_docs:
        raise ValueError("No text could be extracted from any PDF.")
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(all_docs)
    
    if not splits:
        raise ValueError("Failed to split documents into chunks.")
    
    Qdrant.from_documents(
        splits,
        embeddings,
        path="./qdrant_db",
        collection_name="pdf_knowledge"
    )

def query_knowledge(query, pdf_paths=None):
    vectorstore = get_vectorstore()
    if vectorstore is None:
        return "No PDFs indexed yet. Please upload and index some PDFs first.", []
    
    # Special handling for "????? ????????" type questions
    if any(word in query.lower() for word in ["?????", "?????", "how many", "total", "???"]):
        if pdf_paths:
            toc_list = []
            for path in pdf_paths:
                toc = extract_toc(path)
                story_chapters = [item for item in toc if "?????" in item[1] or "story" in item[1].lower()]
                toc_list.extend(story_chapters)
            if toc_list:
                count = len(toc_list)
                answer = f"?? ????? ??? ??? {count} ???????? ????"
                sources = [f"Chapter: {item[1]}" for item in toc_list]
                return answer, sources
    
    # Normal semantic search
    retriever = vectorstore.as_retriever(search_kwargs={"k": 8})  # ?????? sources
    
    system_prompt = (
        "You are a helpful assistant. Answer in Hindi if question is in Hindi. "
        "Use ONLY the following context. Be accurate."
        "\n\nContext: {context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    result = rag_chain.invoke({"input": query})
    answer = result["answer"]
    sources = [doc.page_content for doc in result["context"]]
    
    return answer, sources
