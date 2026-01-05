import streamlit as st
import os
import shutil
from rag_pipeline import index_pdfs, query_knowledge

st.set_page_config(
    page_title="PDF Knowledge Base - Intel Unnati",
    page_icon="??",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main {background-color: #f8f9fa;}
    .stButton>button {width: 100%; border-radius: 8px; height: 3em;}
    .success-box {padding: 1rem; border-radius: 10px; background-color: #e8f5e8; border-left: 5px solid #4caf50;}
    .chat-user {background-color: #e3f2fd; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid #2196f3;}
    .chat-assistant {background-color: #f0f4f8; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid #8bc34a;}
    .footer {text-align: center; color: #666; margin-top: 3rem;}
</style>
""", unsafe_allow_html=True)

st.title("PDF Knowledge Base")
st.markdown("### Upload Reports, Manuals & Policies -> Index -> Ask Questions in Hindi/English")
st.markdown("_Powered by Groq AI | Multilingual Support | Free & Fast_")

with st.sidebar:
    st.header("PDF Management")
    
    uploaded_files = st.file_uploader(
        "Upload one or more PDFs",
        type="pdf",
        accept_multiple_files=True,
        help="Supports text and scanned PDFs"
    )
    
    if uploaded_files:
        saved_paths = []
        for file in uploaded_files:
            path = os.path.join("data", file.name)
            with open(path, "wb") as f:
                f.write(file.getbuffer())
            saved_paths.append(path)
            st.caption(f"Uploaded: {file.name} ({file.size // 1024} KB)")
        
        if st.button("Index Uploaded PDFs", type="primary"):
            with st.spinner("Indexing PDFs... (First time downloads model ~1GB, takes 2-4 mins)"):
                index_pdfs(saved_paths)
            st.success("PDFs indexed successfully!")
            st.balloons()

    if st.button("Clear Database"):
        if os.path.exists("qdrant_db"):
            shutil.rmtree("qdrant_db")
        if os.path.exists("data"):
            shutil.rmtree("data")
            os.mkdir("data")
        st.success("Database and files cleared!")
        st.rerun()

st.markdown("### Ask Questions")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(f"<div class='chat-user'><strong>You:</strong> {msg['content']}</div>", unsafe_allow_html=True)
    else:
        with st.chat_message("assistant"):
            st.markdown(f"<div class='chat-assistant'><strong>Answer:</strong> {msg['content']}</div>", unsafe_allow_html=True)
            if "sources" in msg:
                with st.expander("View Sources"):
                    for i, src in enumerate(msg["sources"], 1):
                        st.caption(f"Source {i}: {src[:600]}...")

if prompt := st.chat_input("Ask in Hindi or English (e.g., ?? ????? ??? ????? ???????? ????)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"<div class='chat-user'><strong>You:</strong> {prompt}</div>", unsafe_allow_html=True)
    
    with st.chat_message("assistant"):
        with st.spinner("Searching your PDFs..."):
            answer, sources = query_knowledge(prompt)
        st.markdown(f"<div class='chat-assistant'><strong>Answer:</strong> {answer}</div>", unsafe_allow_html=True)
        
        if sources:
            with st.expander("View Sources"):
                for i, src in enumerate(sources, 1):
                    st.caption(f"Source {i}: {src[:600]}...")
            st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})
        else:
            st.session_state.messages.append({"role": "assistant", "content": answer})

st.markdown("<div class='footer'>Made for Intel Unnati 2026 | Multilingual PDF Search Tool</div>", unsafe_allow_html=True)
