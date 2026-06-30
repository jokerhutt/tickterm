

from db.database import get_connection
from models.asset import AssetMetadata

class AssetMetadataRepository:

    def get_all(self) -> dict[str, AssetMetadata]:
        with get_connection() as conn:
            rows = conn.execute("""
                SELECT *
                FROM asset_metadata
                ORDER BY rowid
            """).fetchall()

        return {
            row["symbol"]: AssetMetadata(
                symbol=row["symbol"],
                long_name=row["long_name"],
                description=row["description"],
                sector=row["sector"],
                industry=row["industry"],
                exchange=row["exchange"],
            )
            for row in rows
        }

    def add(self, metadata: AssetMetadata) -> None:
        with get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO asset_metadata (
                    symbol,
                    long_name,
                    description,
                    sector,
                    industry,
                    exchange
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                metadata.symbol,
                metadata.long_name,
                metadata.description,
                metadata.sector,
                metadata.industry,
                metadata.exchange,
            ))

    def remove(self, symbol: str) -> None:
        with get_connection() as conn:
            conn.execute(
                "DELETE FROM asset_metadata WHERE symbol = ?",
                (symbol,),
            )

