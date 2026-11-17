"""Check persistence against an existing, externally provisioned test database."""

from pathlib import Path
import sqlite3
import sys

from order import Order, cancel_order


def main():
    database = Path(__file__).resolve().parent / "environment" / "orders.sqlite"
    try:
        connection = sqlite3.connect(database.as_uri() + "?mode=rw", uri=True)
    except sqlite3.Error as error:
        print(f"ENVIRONMENT UNAVAILABLE: {error}; integration scenarios not run.")
        return 2
    try:
        connection.execute("BEGIN")
        connection.execute("CREATE TEMP TABLE cancellation_check (status TEXT)")
        order = Order("integration-101", "alice", "unshipped")
        assert cancel_order(order, "alice")
        connection.execute("INSERT INTO cancellation_check VALUES (?)", (order.status,))
        assert connection.execute("SELECT status FROM cancellation_check").fetchone() == ("cancelled",)
    finally:
        connection.rollback()
        connection.close()
    print("Integration fixture passed; this is not a production adapter test.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
