const VITE_BACKEND_HOST = import.meta.env.VITE_BACKEND_HOST || 'localhost';
const VITE_BACKEND_PORT = import.meta.env.VITE_BACKEND_PORT || '8080';

const apiUrl = `http://${VITE_BACKEND_HOST}:${VITE_BACKEND_PORT}`;

export async function createPaste(content) {
    const res = await fetch(`${apiUrl}/pastes`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ content })
    });
    if (!res.ok) {
        throw new Error(`Failed to create paste: ${res.statusText}`);
    }
    return res.json();
}

export async function getPaste(id) {
    const res = await fetch(`${apiUrl}/pastes/${id}`);
    if (!res.ok) {
        throw new Error(`Failed to get paste: ${res.statusText}`);
    }
    return res.json();
}

export async function deletePaste(id) {
  const res = await fetch(`${apiUrl}/pastes/${id}`, {
    method: "DELETE",
  });
  if (!res.ok) {
    throw new Error(`Failed to delete paste: ${res.statusText}`);
  }
}
