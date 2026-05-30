const API_URL = process.env.NEXT_PUBLIC_API_URL;

type ChatStreamPayload = {
  document_id: string;
  message: string;
  conversation_id?: string | null;
};

type ChatStreamHandlers = {
  onConversation?: (conversationId: string) => void;
  onSources?: (sources: any[]) => void;
  onToken?: (token: string) => void;
  onDone?: () => void;
  onError?: (message: string) => void;
};

export async function streamChat(
  payload: ChatStreamPayload,
  handlers: ChatStreamHandlers
) {
  const response = await fetch(`${API_URL}/chat/stream`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.body) {
    throw new Error("No response body");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  let buffer = "";

  while (true) {
    const { value, done } = await reader.read();

    if (done) break;

    buffer += decoder.decode(value, { stream: true });

    const lines = buffer.split("\n");
    buffer = lines.pop() || "";

    for (const line of lines) {
      if (!line.trim()) continue;

      const event = JSON.parse(line);

      if (event.type === "conversation") {
        handlers.onConversation?.(event.conversation_id);
      }

      if (event.type === "sources") {
        handlers.onSources?.(event.sources);
      }

      if (event.type === "token") {
        handlers.onToken?.(event.content);
      }

      if (event.type === "error") {
        handlers.onError?.(event.message);
      }

      if (event.type === "done") {
        handlers.onDone?.();
      }
    }
  }
}