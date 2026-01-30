import os
import uuid
from pypdf import PdfReader
from tqdm import tqdm
from pinecone import Pinecone, ServerlessSpec

from embeddings import embed_texts
from config import PINECONE_API_KEY, PINECONE_INDEX

abs_path = os.path.abspath(__file__)
dir_path = os.path.dirname(abs_path)

def chunk_text(text, size=750, overlap=150):
    chunks = []
    for i in range(0, len(text), size - overlap):
        chunks.append(text[i:i+size])
    return chunks


def ingest_pdf(path):
    reader = PdfReader(path)

    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    chunks = chunk_text(text)

    pc = Pinecone(api_key=PINECONE_API_KEY)

    if PINECONE_INDEX not in [i["name"] for i in pc.list_indexes()]:
        pc.create_index(
            name=PINECONE_INDEX,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )

    index = pc.Index(PINECONE_INDEX)

    vectors = []
    embeds = embed_texts(chunks)

    for chunk, emb in zip(chunks, embeds):
        vectors.append({
            "id": str(uuid.uuid4()),
            "values": emb,
            "metadata": {"text": chunk}
        })

    index.upsert(vectors)

    print("Ingestion complete.")


if __name__ == "__main__":
    ingest_pdf(os.path.join(dir_path, "../data/Ebook-Agentic-AI.pdf"))