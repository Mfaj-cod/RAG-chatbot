from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL

client = Groq(api_key=GROQ_API_KEY)
model = GROQ_MODEL

def stream_answer(context, question):
    prompt = f"""
Answer ONLY using the context.
If the question asks for a summary or overview,
synthesize across multiple chunks.
If not found say "Not found in document".

Context:
{context}

Question:
{question}
"""

    stream = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content