from app.services.openrouter_service import create_chat_response

def rewrite_question_with_history(
    question: str,
    recent_messages: list,
) -> str:
    history_text = "\n".join(
        [
            f"{message.role}: {message.content}"
            for message in recent_messages[-6:]
        ]
    )

    prompt = f"""
        You rewrite follow-up questions into standalone questions.

        Rules:
        - Use the chat history only to resolve references like "that", "phần đó", "nó", "ý trên".
        - Do not answer the question.
        - Return only the rewritten standalone question.
        - Keep the user's language.

        Chat history:
        {history_text}

        Follow-up question:
        {question}

        Standalone question:
    """

    return create_chat_response(prompt).strip()


def get_last_assistant_message(recent_messages: list):
    for message in reversed(recent_messages):
        if message.role == "assistant":
            return message.content
    return None