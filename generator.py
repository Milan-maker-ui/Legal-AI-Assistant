import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_answer(question: str, retrieved_documents):
    context_parts = []
    for document in retrieved_documents:
        context_parts.append(
            f"""
SOURCE:
{document["source"]}
PAGE:
{document["page"]}
CONTENT:
{document["text"]}
"""
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are a Legal AI Assistant.

Your job is to answer questions using ONLY
the provided legal document context.

Rules:

1. Do not invent information.
2. Do not provide information that is not
   present in the context.
3. If the answer cannot be found, say:
   "I could not find this information in
   the provided documents."
4. Clearly explain the answer.

LEGAL DOCUMENT CONTEXT:

{context}

USER QUESTION:

{question}
"""

    response = client.responses.create(model="gpt-4.1-mini", input=prompt)

    return response.output_text
