from typing import Union
import psycopg2
import os
from fastapi import APIRouter

router = APIRouter()


@router.get("/getTable/{table_name}")
async def get_any_table(table_name: str, offset: Union[str, None] = None, limit: Union[str, None] = None): 
    """
    Возвращает всю табличку `table_name` из БД.

    Дополнительные параметры:
    offset: int
        номер строки с которой нужно начать;
    limit: int
        количество записей которые нужно вернуть.
    """
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()
    cursor.execute("".join([
        f"SELECT * FROM {table_name}",
        f" LIMIT {limit}" if limit else "",
        f" OFFSET {offset}" if offset else ""
    ]))
    columns = [desc[0] for desc in cursor.description]
    records = cursor.fetchall()
    conn.close()
    cursor.close()
    return {
        "table_name": table_name,
        "offset": offset,
        "limit": limit,
        "data": [dict(zip(columns, record)) for record in records]
    }
