import re

def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def split_into_sentences(text: str) -> list[str]:
    return re.split(r"(?<=[.!?。！？])\s+", text)

def chunk_text(
    text: str,
    chunk_size: int = 1200,
    overlap_sentences: int = 2,
    min_chunk_size: int = 200,
) -> list[str]:
    text = clean_text(text)

    if not text:
        return []

    sentences = split_into_sentences(text)

    chunks = []
    current_sentences = []
    current_length = 0

    for sentence in sentences:
        sentence = sentence.strip()

        if not sentence:
            continue

        if current_length + len(sentence) > chunk_size and current_sentences:
            chunk = " ".join(current_sentences).strip()

            if len(chunk) >= min_chunk_size:
                chunks.append(chunk)

            current_sentences = current_sentences[-overlap_sentences:]
            current_length = sum(len(s) for s in current_sentences)

        current_sentences.append(sentence)
        current_length += len(sentence)

    final_chunk = " ".join(current_sentences).strip()

    if len(final_chunk) >= min_chunk_size:
        chunks.append(final_chunk)

    return chunks
