from fastapi import FastAPI
from .routers import simple_api

app = FastAPI()
app.include_router(simple_api.router)


@app.get("/")
async def read_root():
    return {"Welcome to the club": "Buddy!"}
