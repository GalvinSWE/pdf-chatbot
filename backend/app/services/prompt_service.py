def build_rag_prompt(
    question: str,
    chunks,
):
    context_sections = []

    for chunk in chunks:
        context_sections.append(
            f"""
[Page {chunk.page_number}]
{chunk.content}
"""
        )

    context = "\n".join(context_sections)

    prompt = f"""
You are a helpful AI assistant.

Answer ONLY using the provided context.

If the answer is not found in the context,
say:
"I could not find the answer in the document."

Include page citations when possible.

Context:
{context}

Question:
{question}
"""

    return prompt