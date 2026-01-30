```bash
User Question
      ↓
Retriever (Pinecone)
      ↓
Top-k chunks
      ↓
LangGraph Node
      ↓
LLM (context strictly injected)
      ↓
Answer + Context + Score
```