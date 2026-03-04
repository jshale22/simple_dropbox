from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
import uvicorn

from routers.directory import router as directory_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.running = True
    try:
        yield
    finally:
        app.state.running = False

app = FastAPI(lifespan=lifespan)
app.include_router(directory_router)
app.state.running = False

@app.get("/health")
def health_check():
    if not app.state.running:
        raise HTTPException(status_code=503, detail="Service Unavailable")
    return {"running": app.state.running}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
