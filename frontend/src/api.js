const backendHost = import.meta.env.BACKEND_HOST || "localhost";
const backendPort = import.meta.env.BACKEND_PORT || "8000";

export const apiUrl = `http://${backendHost}:${backendPort}`;

export async function createPaste(content) {
    const res = await fetch(`${apiUrl}/pastes`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ content })
    });
    if (!res.ok) throw new Error("Failed to create paste");
    return res.json();
}

export async function getPaste(id) {
    const res = await fetch(`${apiUrl}/pastes/${id}`);
    if (!res.ok) throw new Error("Failed to get paste");
    return res.json();
}