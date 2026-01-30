import os
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

PINECONE_INDEX = "agentic-ai-index"
GEMINI_MODEL = "gemini-2.5-flash"