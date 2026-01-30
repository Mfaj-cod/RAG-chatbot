import os
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

PINECONE_INDEX = "agentic-ai-index"
GROQ_MODEL = "llama-3.1-8b-instant"