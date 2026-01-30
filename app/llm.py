import google.generativeai as genai
from config import GOOGLE_API_KEY, GEMINI_MODEL

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(GEMINI_MODEL)


def stream_answer(context, question):
    prompt = f"""
Answer ONLY using the context.
If not found say "Not found in document".

Context:
{context}

Question:
{question}
"""

    response = model.generate_content(prompt, stream=True)

    for chunk in response:
        if chunk.text:
            yield chunk.text
