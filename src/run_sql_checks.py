from pathlib import Path
import sqlite3
import pandas as pd


DB_PATH = Path("outputs/fund_finance.db")
REPORT_DIR = Path("outputs/reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_PATH = REPORT_DIR / "sql_monitoring_outputs.md"


QUERIES = {
    "Latest Monitoring Snapshot": """
        SELECT
            reporting_date,
            ROUND(facility_outstanding / 1000000.0, 1) AS outstanding_mm,
            ROUND(facility_utilization_pct * 100.0, 1) AS utilization_pct,
            ROUND(eligible_nav / 1000000.0, 1) AS eligible_nav_mm,
            ROUND(ltv * 100.0, 1) AS ltv_pct,
            ROUND(excess_availability / 1000000.0, 1) AS excess_availability_mm,
            covenant_status,
            watchlist_item
        FROM monthly_monitoring
        ORDER BY reporting_date DESC
        LIMIT 1;
    """,
    "Monthly Facility Trend": """
        SELECT
            reporting_date,
            ROUND(facility_outstanding / 1000000.0, 1) AS outstanding_mm,
            ROUND(facility_utilization_pct * 100.0, 1) AS utilization_pct,
            ROUND(ltv * 100.0, 1) AS ltv_pct,
            ROUND(excess_availability / 1000000.0, 1) AS excess_availability_mm,
            covenant_status
        FROM monthly_monitoring
        ORDER BY reporting_date;
    """,
    "Investor Type Summary": """
        SELECT
            investor_type,
            COUNT(*) AS investor_count,
            ROUND(SUM(total_commitment) / 1000000.0, 1) AS total_commitment_mm,
            ROUND(SUM(unfunded_commitment) / 1000000.0, 1) AS unfunded_commitment_mm,
            ROUND(SUM(borrowing_base_contribution) / 1000000.0, 1) AS borrowing_base_contribution_mm,
            ROUND(SUM(total_commitment) / (SELECT SUM(total_commitment) FROM investors) * 100.0, 1) AS commitment_pct
        FROM investors
        GROUP BY investor_type
        ORDER BY SUM(total_commitment) DESC;
    """,
    "Top Investors": """
        SELECT
            investor_id,
            investor_name,
            investor_type,
            internal_rating,
            eligible_in_borrowing_base,
            ROUND(total_commitment / 1000000.0, 1) AS total_commitment_mm,
            ROUND(unfunded_commitment / 1000000.0, 1) AS unfunded_commitment_mm,
            ROUND(advance_rate * 100.0, 1) AS advance_rate_pct,
            ROUND(borrowing_base_contribution / 1000000.0, 1) AS borrowing_base_contribution_mm
        FROM investors
        ORDER BY total_commitment DESC
        LIMIT 10;
    """,
    "Watchlist NAV Positions": """
        SELECT
            position_id,
            portfolio_company,
            industry,
            asset_type,
            status,
            ROUND(cost_basis / 1000000.0, 1) AS cost_basis_mm,
            ROUND(fair_value / 1000000.0, 1) AS fair_value_mm,
            ROUND(fair_value_marks * 100.0, 1) AS fair_value_mark_pct,
            eligible_nav_collateral
        FROM nav_positions
        WHERE status <> 'Performing'
        ORDER BY fair_value ASC;
    """,
    "Early Warning Monitoring Checks": """
        SELECT
            reporting_date,
            ROUND(ltv * 100.0, 1) AS ltv_pct,
            ROUND(excess_availability / 1000000.0, 1) AS excess_availability_mm,
            covenant_status,
            watchlist_item
        FROM monthly_monitoring
        WHERE ltv >= 0.30
           OR excess_availability <= 10000000
           OR covenant_status IN ('Watch', 'Fail')
        ORDER BY reporting_date;
    """,
}


def main() -> None:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}. Run src/build_sqlite_db.py first.")

    sections = [
        "# SQL Monitoring Outputs",
        "",
        "This report contains sample SQL outputs from the simulated fund finance SQLite database.",
        "",
        "> All data is synthetic and prepared for portfolio project purposes only.",
        "",
    ]

    with sqlite3.connect(DB_PATH) as conn:
        for title, query in QUERIES.items():
            df = pd.read_sql_query(query, conn)

            sections.append(f"## {title}")
            sections.append("")

            if df.empty:
                sections.append("No records returned.")
            else:
                sections.append(df.to_markdown(index=False))

            sections.append("")

    OUTPUT_PATH.write_text("\n".join(sections))

    print("SQL monitoring output report created.")
    print(f"- {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
