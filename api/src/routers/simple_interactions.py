from typing import Union
import psycopg2
import os
from fastapi import APIRouter

router = APIRouter()


@router.get("/getTableSize/{table_name}")
async def get_table_size(table_name: str):
    """
    Возвращает размер таблички.
    """
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

@router.get("/isFieldExists/{table_name}")
async def is_field_exists(table_name: str, column: str, value: str): 
    """
    Имеется ли в табличке `table_name` строка где колонка `column` имеет значение `value`.
    Пример: проверить имеется ли нужный айди игрока в табличке.
    """
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {column} = {value}")
    size = int(cursor.fetchone()[0])
    conn.close()
    cursor.close()
    return {
        "table_name": table_name,
        "column": column,
        "value": value,
        "is_exists": size > 0
    }
