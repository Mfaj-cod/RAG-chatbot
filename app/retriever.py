from pinecone import Pinecone
from embeddings import embed_query
from config import PINECONE_API_KEY, PINECONE_INDEX

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX)


def retrieve(query, k=4):
    vector = embed_query(query)

    results = index.query(vector=vector, top_k=k, include_metadata=True)

    contexts = [m["metadata"]["text"] for m in results["matches"]]
    scores = [m["score"] for m in results["matches"]]

    return contexts, scores
