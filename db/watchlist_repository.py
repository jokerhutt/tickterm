# ∴ Jokerhut / db/watchlist_repository.py

from db.database import get_connection

class WatchlistRepository:

    def get_all(self) -> list[str]:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT symbol FROM watchlist ORDER BY rowid"
            ).fetchall()

        return [row["symbol"] for row in rows]

    def add(self, symbol: str) -> None:
        with get_connection() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO watchlist(symbol) VALUES (?)",
                (symbol,),
            )

    def remove(self, symbol: str) -> None:
        with get_connection() as conn:
            conn.execute(
                "DELETE FROM watchlist WHERE symbol = ?",
                (symbol,),
            )
