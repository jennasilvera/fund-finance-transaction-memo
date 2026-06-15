from pathlib import Path
import sqlite3
import pandas as pd


DATA_DIR = Path("data")
SQL_DIR = Path("sql")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

DB_PATH = OUTPUT_DIR / "fund_finance.db"


def load_csv(path: Path, keep_default_na: bool = True) -> pd.DataFrame:
    return pd.read_csv(path, keep_default_na=keep_default_na)


def main() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()

    schema_sql = (SQL_DIR / "schema.sql").read_text()

    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(schema_sql)

        load_csv(DATA_DIR / "investors.csv").to_sql(
            "investors",
            conn,
            if_exists="append",
            index=False,
        )

        load_csv(DATA_DIR / "nav_positions.csv").to_sql(
            "nav_positions",
            conn,
            if_exists="append",
            index=False,
        )

        load_csv(DATA_DIR / "facility_assumptions.csv", keep_default_na=False).to_sql(
            "facility_assumptions",
            conn,
            if_exists="append",
            index=False,
        )

        load_csv(DATA_DIR / "covenant_tests.csv").to_sql(
            "covenant_tests",
            conn,
            if_exists="append",
            index=False,
        )

        monitoring = load_csv(DATA_DIR / "monthly_monitoring.csv", keep_default_na=False)
        monitoring["watchlist_item"] = monitoring["watchlist_item"].fillna("None").replace("", "None")

        monitoring.to_sql(
            "monthly_monitoring",
            conn,
            if_exists="append",
            index=False,
        )

        table_counts = pd.read_sql_query(
            """
            SELECT 'investors' AS table_name, COUNT(*) AS row_count FROM investors
            UNION ALL
            SELECT 'nav_positions', COUNT(*) FROM nav_positions
            UNION ALL
            SELECT 'facility_assumptions', COUNT(*) FROM facility_assumptions
            UNION ALL
            SELECT 'covenant_tests', COUNT(*) FROM covenant_tests
            UNION ALL
            SELECT 'monthly_monitoring', COUNT(*) FROM monthly_monitoring;
            """,
            conn,
        )

    print("SQLite database created successfully.")
    print(f"- {DB_PATH}")
    print()
    print(table_counts.to_string(index=False))


if __name__ == "__main__":
    main()
