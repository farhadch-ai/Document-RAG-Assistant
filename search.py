from openai import OpenAI





client = OpenAI()


def answer_question(question,retrieved_chunks, top_k=3):

   

    # Build context
    context = ""

    for chunk in retrieved_chunks:

        context += f"""
SOURCE PAGES: {chunk["pages"]}

{chunk["text"]}

--------------------
"""

    # Build prompt
    prompt = f"""
You are answering questions about a document.

Answer the question ONLY using the provided context.

Rules:
- Do not use outside knowledge.
- If the answer is not present in the context, say "I don't know."
- Cite the page number(s) supporting your answer.
- Do not invent page numbers.
- Give a concise answer.

CONTEXT:
{context}

QUESTION:
{question}
"""

    # Generate answer
    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    # Return everything Streamlit needs
    return {
        "answer": response.output_text,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "total_tokens": response.usage.total_tokens
    }