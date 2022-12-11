from typing import Union
import psycopg2
import os
from fastapi import APIRouter

router = APIRouter()


@router.get("/getPlayerTimeStats")
async def get_player_time_stats(player_id: Union[str, None] = None, limit: Union[str, None] = None): 
    """
    Возвращает изменение рейтинга игроков
    """
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()
    cursor.execute("".join([
        f"SELECT * FROM player_ranking",
        f" WHERE player_id = {player_id}" if player_id else "",
        f" LIMIT {limit}" if limit else "",
    ]))
    columns = [desc[0] for desc in cursor.description]
    records = cursor.fetchall()
    conn.close()
    cursor.close()
    return {
        "player_id": player_id,
        "count": len(records),
        "data": [dict(zip(columns, record)) for record in records]
    }


@router.get("/getDetailedPlayerTimeStats")
async def get_det_player_time_stats(player_id: Union[str, None] = None, limit: Union[str, None] = None): 
    """
    Возвращает изменение подробного рейтинга игроков
    """
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()
    cursor.execute("".join([
        f"SELECT * FROM player_elo_ranking",
        f" WHERE player_id = {player_id}" if player_id else ""
        f" LIMIT {limit}" if limit else "",
    ]))
    columns = [desc[0] for desc in cursor.description]
    records = cursor.fetchall()
    conn.close()
    cursor.close()
    return {
        "player_id": player_id,
        "count": len(records),
        "data": [dict(zip(columns, record)) for record in records]
    }
