from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app import config
from app.database import lifespan
from app.routers import (
    post_route,
    user_route,
    auth_route,
    vote_route
    )


app = FastAPI(debug= True,lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status":"ok","message":"Health check successful"}

app.include_router(post_route.router)
app.include_router(user_route.router)
app.include_router(auth_route.router)
app.include_router(vote_route.router)

if __name__ == "__main__":
    uvicorn.run("main:app",reload=True)