from typing import Union
import psycopg2
import os
from fastapi import APIRouter

router = APIRouter()


@router.get("/getTableSize/{table_name}")
async def get_table_size(table_name: str): 
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    size = int(cursor.fetchone()[0])
    conn.close()
    cursor.close()
    return {
        "table_name": table_name,
        "size": size
    }
