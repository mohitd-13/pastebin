from contextlib import asynccontextmanager

import aioboto3
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import initialize_database
from app.routers import pastes


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    # Create database tables in postgres if not present
    await initialize_database()

    # Create asynchronous s3 session
    session = aioboto3.Session(profile_name="pastebin")

    async with session.client("s3") as s3:
        app.state.s3 = s3

    yield
    # Shutdown


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(pastes.router)

@app.get("/", tags=["Root"])
def root():
    return {"message": "Welcome to Pastbin"}


@app.get("/healthz", tags=["Health"])
async def health():
    """
    Provides a quick and simple health status message
    """
    return {"status": "Healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
