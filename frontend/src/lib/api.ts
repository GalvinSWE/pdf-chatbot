const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function uploadDocument(file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_URL}/documents/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Failed to upload document");
  }

  return response.json();
}

export async function createEmbeddingJob(documentId: string) {
  const response = await fetch(
    `${API_URL}/documents/${documentId}/embed-jobs`,
    {
      method: "POST",
    }
  );

  if (!response.ok) {
    throw new Error("Failed to create embedding job");
  }

  return response.json();
}

export async function getJob(jobId: string) {
  const response = await fetch(`${API_URL}/jobs/${jobId}`);

  if (!response.ok) {
    throw new Error("Failed to get job");
  }

  return response.json();
}

export async function getConversations() {
  const response = await fetch(`${API_URL}/conversations`);

  if (!response.ok) {
    throw new Error("Failed to get conversations");
  }

  return response.json();
}

export async function getConversationMessages(conversationId: string) {
  const response = await fetch(
    `${API_URL}/conversations/${conversationId}/messages`
  );

  if (!response.ok) {
    throw new Error("Failed to get messages");
  }

  return response.json();
}