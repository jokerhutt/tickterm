# ∴ Jokerhut / db/database.py

import sqlite3

DB_PATH = "tickterm.db"

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    with get_connection() as conn:

        # init watchlist
        conn.execute("""
            CREATE TABLE IF NOT EXISTS watchlist (
                symbol TEXT PRIMARY KEY
            )
        """)

        # init asset_metadata
        conn.execute("""
            CREATE TABLE IF NOT EXISTS asset_metadata (
                symbol TEXT PRIMARY KEY,
                long_name TEXT,
                description TEXT,
                sector TEXT,
                industry TEXT,
                exchange TEXT
            )        
        """)
