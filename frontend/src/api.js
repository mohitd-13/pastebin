const VITE_API_URL = import.meta.env.VITE_API_URL

export async function createPaste(content) {
    const res = await fetch(`${VITE_API_URL}/pastes`, {
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
    const res = await fetch(`${VITE_API_URL}/pastes/${id}`);
    if (!res.ok) {
        throw new Error(`Failed to get paste: ${res.statusText}`);
    }
    return res.json();
}

export async function deletePaste(id) {
  const res = await fetch(`${VITE_API_URL}/pastes/${id}`, {
    method: "DELETE",
  });
  if (!res.ok) {
    throw new Error(`Failed to delete paste: ${res.statusText}`);
  }
}
