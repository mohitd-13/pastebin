from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to Pastbin"}

@app.post("/paste")
def create_link(text: str | None = None):
    return {"message": "Get unique id"}

@app.get("/{id}")
def get_text(id: int):
    return {"message": "Read text data"}

@app.delete("/{id}")
def delete_text(id: int):
    return {"message": "Delete text data"}