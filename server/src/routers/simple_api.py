from typing import Union
import psycopg2
import os
from fastapi import APIRouter

router = APIRouter()


@router.get("/tables/{table_name}")
async def get(table_name: str, q: Union[str, None] = None):
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {table_name} LIMIT 10')
    records = cursor.fetchall()
    conn.close()
    cursor.close()
    return {"table_name": table_name, "q": q, "records": records}
