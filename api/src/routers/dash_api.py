from typing import Union
import psycopg2
import os
from fastapi import APIRouter

router = APIRouter()


@router.get("/getAge")
async def get_age(limit: Union[str, None] = None):
    """
    Возвращает фамилию и возраст из БД.

    Дополнительные параметры:
    limit: int
        количество записей которые нужно вернуть.
    """
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()
    cursor.execute("".join(
        ["SELECT last_name, age FROM player_v WHERE age IS NOT NULL AND active='True'",
         f" LIMIT {limit}" if limit else ""]))

    columns = [desc[0] for desc in cursor.description]
    records = cursor.fetchall()
    conn.close()
    cursor.close()
    return {
        "data": [dict(zip(columns, record)) for record in records]
    }


@router.get("/getTitles")
async def get_titles(limit: Union[str, None] = None):
    """
    Возвращает фамилию и количество титулов>0 из БД.

    Дополнительные параметры:
    limit: int
        количество записей которые нужно вернуть.
    """
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()
    cursor.execute("".join(
        ["SELECT last_name, titles FROM player_v WHERE titles>0",
         f" LIMIT {limit}" if limit else ""]))

    columns = [desc[0] for desc in cursor.description]
    records = cursor.fetchall()
    conn.close()
    cursor.close()
    return {
        "data": [dict(zip(columns, record)) for record in records]
    }


@router.get("/getHand")
async def get_hand(limit: Union[str, None] = None):
    """
    Возвращает фамилию и рабочую руку из БД.
    R - правая
    L - левая
    Дополнительные параметры:
    limit: int
        количество записей которые нужно вернуть.
    """
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()
    cursor.execute("".join(
        ["SELECT last_name, hand FROM player WHERE hand IS NOT NULL",
         f" LIMIT {limit}" if limit else ""]))

    columns = [desc[0] for desc in cursor.description]
    records = cursor.fetchall()
    conn.close()
    cursor.close()
    return {
        "data": [dict(zip(columns, record)) for record in records]
    }


@router.get("/getQuantityByCountry")
async def get_quantity(limit: Union[str, None] = None):
    """
    Возвращает фамилию и рабочую руку из БД.
    R - правая
    L - левая
    Дополнительные параметры:
    limit: int
        количество записей которые нужно вернуть.
    """
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()
    cursor.execute("".join(
        ["SELECT last_name, hand FROM player WHERE hand IS NOT NULL",
         f" LIMIT {limit}" if limit else ""]))

    columns = [desc[0] for desc in cursor.description]
    records = cursor.fetchall()
    conn.close()
    cursor.close()
    return {
        "data": [dict(zip(columns, record)) for record in records]
    }


@router.get("/getAgeWinners")
async def get_age_winners(limit: Union[str, None] = None):
    """
    Возвращает возраст победителей матчей из БД.
    R - правая
    L - левая
    Дополнительные параметры:
    limit: int
        количество записей которые нужно вернуть.
    """
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()
    cursor.execute("".join(
        ["SELECT ROUND(winner_age) FROM match",
         f" LIMIT {limit}" if limit else ""]))

    columns = [desc[0] for desc in cursor.description]
    records = cursor.fetchall()
    conn.close()
    cursor.close()
    return {
        "data": [dict(zip(columns, record)) for record in records]
    }


@router.get("/getMinutesMatch")
async def get_minutes(limit: Union[str, None] = None):
    """
    Возвращает количество минут матчей из БД.
    R - правая
    L - левая
    Дополнительные параметры:
    limit: int
        количество записей которые нужно вернуть.
    """
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()
    cursor.execute("".join(
        ["SELECT minutes FROM match_stats",
         f" LIMIT {limit}" if limit else ""]))

    columns = [desc[0] for desc in cursor.description]
    records = cursor.fetchall()
    conn.close()
    cursor.close()
    return {
        "data": [dict(zip(columns, record)) for record in records]
    }


@router.get("/getLevel")
async def get_level():
    """
    Возвращает уровень и количество игроков на данном уровне из БД.
    Их всего 9, обозначаются латинскими буквами
    """
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()
    cursor.execute("".join(
        "SELECT level, COUNT(level) FROM player_match_stats_v GROUP BY 1;"))
    columns = [desc[0] for desc in cursor.description]
    records = cursor.fetchall()
    conn.close()
    cursor.close()
    return {
        "data": [dict(zip(columns, record)) for record in records]
    }
