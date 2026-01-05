# Intel Unnati 2026 - Enterprise PDFs into Searchable Knowledge

**A powerful Retrieval-Augmented Generation (RAG) tool** that converts thousands of unstructured enterprise PDFs (reports, manuals, policies) into a fully searchable and structured knowledge base.

## Problem Statement
Companies have thousands of PDF documents containing critical information in unstructured format. Searching within these documents is time-consuming and inefficient.

This tool solves the problem by:
- Reading normal and scanned PDFs (with OCR support)
- Preserving document structure using Table of Contents
- Breaking text into meaningful sections (no chapter cuts)
- Enabling semantic search via Vector Database
- Extracting tables for precise queries
- Describing images/charts for searchability

## Key Features
- OCR for Scanned PDFs – Handles image-based PDFs using Tesseract + OpenCV denoising
- Multilingual Support – Works with Hindi, English, and other languages (queries & content)
- Semantic Search – Powered by multilingual embeddings and Groq AI
- Table Extraction – Accurate table parsing stored for direct querying
- Image & Chart Handling – Generates descriptions for visual content search
- User-Friendly Interface – Clean Streamlit web app with upload, indexing, and chat
- Free & Fast – Uses Groq free tier (Llama 3.3 70B) – no cost!

## Tech Stack
- LangChain – RAG pipeline
- Groq AI – Fast LLM inference (free tier)
- Qdrant – Local vector database
- HuggingFace Embeddings – Multilingual semantic search
- PyMuPDF, Camelot, pytesseract – PDF processing & OCR
- Streamlit – Interactive web interface

## How to Run

### 1. Prerequisites
- Python 3.10+
- Install Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki
- Get free Groq API key: https://console.groq.com/keys

### 2. Setup
git clone https://github.com/Tshivansh319/Intel_Unnati_Enterprise_pdfs_into_searchable_knowledge.git
cd Intel_Unnati_Enterprise_pdfs_into_searchable_knowledge

pip install -r requirements.txt

### 3. Add API Key
Create `.env` file:
GROQ_API_KEY=gsk_your_key_here

### 4. Run
streamlit run app.py

Open http://localhost:8501

**Note**: First indexing downloads multilingual model (~400MB) – one-time only.

## Demo Workflow
1. Upload PDF(s)  (provided in sample_pdf folder)
2. Click "Index Uploaded PDFs" (indexing pdf for first time takes longer time because , it will install a large llm file of 1 GB)
3. longer pdf may take time while indexing due to chunking
4. Ask questions in Hindi or English
   - Example: "What is the leave policy?"

## Project Structure
.
+-- app.py              # Streamlit UI
+-- rag_pipeline.py     # Core RAG logic
+-- requirements.txt
+-- .env                # API key (git ignored)
+-- data/               # Uploaded PDFs (git ignored)
+-- qdrant_db/          # Vector database (git ignored)

## Performance
- 80-page PDF indexing: ~1-3 minutes (after first model download)
- Query response: <2 seconds
- Fully local storage – private & secure

## Made for Intel Unnati 2026
**Document Intelligence & Enterprise Search Challenge**

Thank you Intel Unnati team for this amazing opportunity!

**Submitted by:** Shivansh Tiwari , Jay Soni, Shubham Solat 
**GitHub:** @Tshivansh319

---
Made with love and dedication

