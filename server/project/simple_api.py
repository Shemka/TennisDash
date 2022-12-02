from typing import Union
import psycopg2
import os
from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def read_root():
    return {"Welcome to the club": "Buddy!"}


@app.get("/tables/{table_name}")
def get(table_name: str, q: Union[str, None] = None):
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM player LIMIT 10')
    records = cursor.fetchall()
    conn.close()
    cursor.close()
    return {"table_name": table_name, "q": q, "records": records}
