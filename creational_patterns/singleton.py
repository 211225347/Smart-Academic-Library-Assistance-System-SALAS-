"""
creational_patterns/singleton.py
Pattern: Singleton
Use Case: DatabaseConnection — ensures only one database connection pool
          exists across the entire SALAS application.

Justification: The SALAS system uses a single PostgreSQL database. If
every request created a new connection, the database would be overwhelmed
during peak semester periods. The Singleton ensures the connection pool
is created once and reused across all services. Thread-safety is
implemented using a lock to handle concurrent request initialisation.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import threading
from typing import Optional


class DatabaseConnection:
    """
    Thread-safe Singleton managing the PostgreSQL connection pool.
    Maps to NFR-07 (1,000 concurrent users) and NFR-09 (data security).
    """

    _instance: Optional["DatabaseConnection"] = None
    _lock: threading.Lock = threading.Lock()

    def __init__(self):
        # Guard: prevent direct instantiation after singleton exists
        raise RuntimeError(
            "DatabaseConnection is a Singleton. "
            "Use DatabaseConnection.get_instance() instead."
        )

    def _init(self, host: str, port: int, database: str, pool_size: int):
        """Private initialiser called only by get_instance."""
        self._host = host
        self._port = port
        self._database = database
        self._pool_size = pool_size
        self._is_connected = False
        self._query_count = 0
        self._connection_id = id(self)
        self._connect()

    def _connect(self) -> None:
        self._is_connected = True

    @classmethod
    def get_instance(cls, host: str = "localhost", port: int = 5432,
                     database: str = "salas_db",
                     pool_size: int = 20) -> "DatabaseConnection":
        """
        Thread-safe factory method using double-checked locking.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    instance = object.__new__(cls)
                    instance._init(host, port, database, pool_size)
                    cls._instance = instance
        return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        """Resets singleton — ONLY for use in unit tests."""
        with cls._lock:
            cls._instance = None

    def execute_query(self, sql: str, params: tuple = ()) -> dict:
        if not self._is_connected:
            raise ConnectionError("Database not connected.")
        self._query_count += 1
        return {
            "sql": sql,
            "params": params,
            "rows_affected": 1,
            "query_number": self._query_count
        }

    @property
    def is_connected(self) -> bool:
        return self._is_connected

    @property
    def query_count(self) -> int:
        return self._query_count

    @property
    def connection_id(self) -> int:
        return self._connection_id

    def disconnect(self) -> None:
        self._is_connected = False

    def __repr__(self) -> str:
        return (f"DatabaseConnection(host={self._host}, "
                f"db={self._database}, connected={self._is_connected})")


class CatalogueService:
    """Example service using the DatabaseConnection Singleton."""

    def __init__(self):
        self._db = DatabaseConnection.get_instance()

    def find_resource(self, resource_id: str) -> dict:
        return self._db.execute_query(
            "SELECT * FROM resources WHERE resource_id = %s",
            (resource_id,)
        )

    def get_available_resources(self) -> dict:
        return self._db.execute_query(
            "SELECT * FROM resources WHERE available_copies > 0"
        )


if __name__ == "__main__":
    DatabaseConnection.reset_instance()
    db1 = DatabaseConnection.get_instance()
    db2 = DatabaseConnection.get_instance()
    print(f"Same instance: {db1 is db2}")
    print(f"Connected: {db1.is_connected}")

    results = []
    def get_db():
        db = DatabaseConnection.get_instance()
        results.append(db.connection_id)

    threads = [threading.Thread(target=get_db) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"All thread IDs identical: {len(set(results)) == 1}")
