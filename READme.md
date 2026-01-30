# Agentic AI RAG Assistant

A Retrieval-Augmented Generation (RAG) chatbot that answers questions **strictly grounded in an Agentic AI eBook (PDF)** using:

- Groq - llama-3.1-8b-instant (LLM)
- LangGraph (pipeline orchestration)
- Pinecone (vector database)
- SentenceTransformers (embeddings)
- Flask + Bootstrap (UI)

The assistant retrieves relevant document chunks, reasons over them, and streams answers live with source citations and confidence.

---

## Features

- PDF ingestion → chunk → embed → Pinecone  
- LangGraph RAG pipeline
- Streaming token responses (typewriter effect)  
- Sources + confidence score  
- Conversation memory
- Dark UI
- Fully Python (no low-code / no vibe tools)

---

# Architecture Overview
```bash
User Question
↓
Flask API (/chat)
↓
LangGraph Pipeline
↓
Retriever (Pinecone similarity search)
↓
Top-k context chunks
↓
Groq (grounded generation)
↓
Streaming answer → UI
↓
Sources + confidence
```
---

### Flow

1. PDF → chunked
2. Chunks → embeddings
3. Stored in Pinecone
4. Query → similar chunks retrieved
5. LLM answers using ONLY retrieved context
6. Response streamed to UI

---

# Project Structure

```bash
app/
│
├── main.py → Flask server & API routes
├── graph.py → LangGraph RAG pipeline
├── retriever.py → Pinecone search
├── embeddings.py → SentenceTransformer embeddings
├── llm.py → Groq wrapper
├── ingest.py → PDF ingestion script
│
├── templates/
│ └── index.html → Chat UI
│
├── static/
│ └── script.js → Frontend logic
│
data/
└── Ebook-Agentic-AI.pdf
|
requirements.txt
|
READme.md
```

---

# Setup Instructions

## Clone

```bash
git clone https://github.com/Mfaj-cod/RAG-chatbot
cd RAG-chatbot
```
## Create environment
```bash
python -m venv venv
venv\Scripts\activate
```
## Install dependencies
```bash
pip install -r requirements.txt
```
## Add environment variables
```bash
PINECONE_API_KEY=xxxx
GROQ_API_KEY=xxxx
```
## Ingest the PDF (one time only)
```bash
python app/ingest.py
```
This will:
- read PDF
- split into chunks
- create embeddings
- upload to Pinecone

## Run server
```bash
python app/main.py
```
## Open
```bash
http://127.0.0.1:5000
```
## Sample Queries

Try:
1. What is Agentic AI?
2. What are the components of an agentic system?
3. How does planning work in agent architectures?
4. Explain perception and execution in agents
5. What are challenges in building autonomous agents?
6. Summarize the key ideas of the book

## API (POST /chat)
Request:
```bash
{
  "question": "What is agentic AI?"
}
```
Streaming response:
- tokens
- confidence score
- retrieved contexts

---
## Tech Stack
```bash
| Layer      | Tool             |
| ---------- | ---------------- |
| Frontend   | Bootstrap + JS   |
| Backend    | Flask            |
| Pipeline   | LangGraph        |
| LLM        | Groq(llama-3.1-8b-instant) |
| Embeddings | all-MiniLM-L6-v2 |
| Vector DB  | Pinecone         |
```
---
#### Author
- RAG + Agents + LangGraph implementation in pure Python.