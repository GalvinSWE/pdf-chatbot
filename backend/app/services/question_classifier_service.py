def is_overview_question(question: str) -> bool:
    q = question.lower().strip()

    keywords = [
        "sách này dạy về gì",
        "sách này nói về gì",
        "cuốn sách này dạy về gì",
        "cuốn sách này nói về gì",
        "tài liệu này nói về gì",
        "document này nói về gì",
        "pdf này nói về gì",
        "tóm tắt",
        "summary",
        "overview",
        "about",
    ]

    return any(keyword in q for keyword in keywords)