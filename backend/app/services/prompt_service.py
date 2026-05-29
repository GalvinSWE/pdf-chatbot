def build_rag_prompt(
    question: str,
    chunks: list[dict],
):
    context_sections = []

    for chunk in chunks:
        context_sections.append(
            f"""
[Source: page {chunk["page_number"]}, chunk {chunk["chunk_index"]}, strategy {chunk.get("strategy", "unknown")}]
{chunk["content"]}
"""
        )

    context = "\n".join(context_sections)

    prompt = f"""
You are a PDF question-answering assistant.

Your task:
Answer the user's question using ONLY the context below.

Rules:
1. Do not use outside knowledge.
2. If the answer is not clearly found in the context, say:
   "I could not find the answer in the document."
3. Include page citations in this format: (page X).
4. Be concise and factual.
5. If the question asks for an overview or summary, synthesize from the provided sources.
6. Do not invent page numbers or facts.

Context:
{context}

User question:
{question}

Answer:
"""

    return prompt