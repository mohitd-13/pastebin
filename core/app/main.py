import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database import initialize_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables on startup
    await initialize_database()
    yield
    
app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "Welcome to Pastbin"}

@app.get("/healthz", tags=["Health"])
async def health():
    """
    Provides a quick and simple health status message
    """
    return {"status": "Healthy"}


@app.get("/{id}")
def get_text(id: int):
    return {"message": f"Read text data {id}"}

@app.post("/paste")
def create_link(text: str | None = None):
    return {"message": "Get unique id"}

@app.delete("/{id}")
def delete_text(id: int):
    return {"message": "Delete text data"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)