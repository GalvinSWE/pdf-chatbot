"use client";

import { useState } from "react";
import {
  createEmbeddingJob,
  getJob,
  uploadDocument,
} from "@/src/lib/api";
import { streamChat } from "@/src/lib/chat-stream";

type Source = {
  page_number: number;
  chunk_index: number;
  distance: number;
  strategy?: string;
  content_preview: string;
};

type Message = {
  role: "user" | "assistant";
  content: string;
};

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [documentId, setDocumentId] = useState<string | null>(null);
  const [jobStatus, setJobStatus] = useState<string | null>(null);

  const [conversationId, setConversationId] = useState<string | null>(null);
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [sources, setSources] = useState<Source[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);

  async function handleUpload() {
    if (!file) return;

    const uploadResult = await uploadDocument(file);
    setDocumentId(uploadResult.document_id);

    const job = await createEmbeddingJob(uploadResult.document_id);
    setJobStatus(job.status);

    const interval = setInterval(async () => {
      const latestJob = await getJob(job.job_id);
      setJobStatus(latestJob.status);

      if (
        latestJob.status === "completed" ||
        latestJob.status === "failed"
      ) {
        clearInterval(interval);
      }
    }, 2000);
  }

  async function handleSend() {
    if (!documentId || !message.trim()) return;

    const userMessage = message;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: userMessage,
      },
      {
        role: "assistant",
        content: "",
      },
    ]);

    setMessage("");
    setSources([]);
    setIsStreaming(true);

    await streamChat(
      {
        document_id: documentId,
        conversation_id: conversationId,
        message: userMessage,
      },
      {
        onConversation: (id) => {
          setConversationId(id);
        },
        onSources: (items) => {
          setSources(items);
        },
        onToken: (token) => {
          setMessages((prev) => {
            const copy = [...prev];
            const lastIndex = copy.length - 1;

            copy[lastIndex] = {
              ...copy[lastIndex],
              content: copy[lastIndex].content + token,
            };

            return copy;
          });
        },
        onDone: () => {
          setIsStreaming(false);
        },
        onError: (errorMessage) => {
          setIsStreaming(false);
          setMessages((prev) => [
            ...prev,
            {
              role: "assistant",
              content: errorMessage,
            },
          ]);
        },
      }
    );
  }

  const canChat = documentId && jobStatus === "completed";

  return (
    <main className="min-h-screen bg-gray-50 p-8">
      <div className="mx-auto max-w-5xl space-y-6">
        <section className="rounded-2xl bg-white p-6 shadow">
          <h1 className="text-2xl font-bold">PDF Chatbot</h1>
          <p className="mt-2 text-gray-600">
            Upload a PDF, process embeddings, then ask questions.
          </p>
        </section>

        <section className="rounded-2xl bg-white p-6 shadow">
          <h2 className="mb-4 text-lg font-semibold">1. Upload PDF</h2>

          <div className="flex gap-3">
            <input
              type="file"
              accept="application/pdf"
              onChange={(event) => {
                setFile(event.target.files?.[0] || null);
              }}
            />

            <button
              onClick={handleUpload}
              className="rounded-lg bg-black px-4 py-2 text-white"
            >
              Upload & Process
            </button>
          </div>

          {documentId && (
            <p className="mt-3 text-sm text-gray-600">
              Document ID: {documentId}
            </p>
          )}

          {jobStatus && (
            <p className="mt-1 text-sm text-gray-600">
              Job status: {jobStatus}
            </p>
          )}
        </section>

        <section className="rounded-2xl bg-white p-6 shadow">
          <h2 className="mb-4 text-lg font-semibold">2. Chat</h2>

          <div className="mb-4 h-[420px] overflow-y-auto rounded-xl border p-4">
            {messages.map((item, index) => (
              <div
                key={index}
                className={`mb-4 ${
                  item.role === "user" ? "text-right" : "text-left"
                }`}
              >
                <div
                  className={`inline-block max-w-[80%] rounded-xl px-4 py-2 ${
                    item.role === "user"
                      ? "bg-black text-white"
                      : "bg-gray-100 text-gray-900"
                  }`}
                >
                  {item.content}
                </div>
              </div>
            ))}

            {isStreaming && (
              <p className="text-sm text-gray-400">Streaming...</p>
            )}
          </div>

          <div className="flex gap-3">
            <input
              value={message}
              onChange={(event) => setMessage(event.target.value)}
              disabled={!canChat || isStreaming}
              placeholder={
                canChat
                  ? "Ask about your PDF..."
                  : "Upload and process a PDF first"
              }
              className="flex-1 rounded-lg border px-4 py-2"
            />

            <button
              onClick={handleSend}
              disabled={!canChat || isStreaming}
              className="rounded-lg bg-black px-4 py-2 text-white disabled:bg-gray-300"
            >
              Send
            </button>
          </div>
        </section>

        {sources.length > 0 && (
          <section className="rounded-2xl bg-white p-6 shadow">
            <h2 className="mb-4 text-lg font-semibold">Sources</h2>

            <div className="space-y-3">
              {sources.map((source, index) => (
                <div
                  key={index}
                  className="rounded-xl border p-3 text-sm text-gray-700"
                >
                  <div className="font-medium">
                    Page {source.page_number}, Chunk {source.chunk_index}
                  </div>
                  <div className="text-xs text-gray-400">
                    Distance: {source.distance.toFixed(2)}
                    {source.strategy ? ` · ${source.strategy}` : ""}
                  </div>
                  <p className="mt-2">{source.content_preview}</p>
                </div>
              ))}
            </div>
          </section>
        )}
      </div>
    </main>
  );
}