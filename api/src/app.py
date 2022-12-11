from fastapi import FastAPI
from .routers import full_table_collector, simple_interactions, player_time_stats

app = FastAPI()
app.include_router(full_table_collector.router)
app.include_router(simple_interactions.router)
app.include_router(player_time_stats.router)



@app.get("/")
async def read_root():
    return {"Welcome to the club": "Buddy!"}
