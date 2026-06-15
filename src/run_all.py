import subprocess
import sys
from pathlib import Path


SCRIPTS = [
    "src/generate_synthetic_data.py",
    "src/borrowing_base.py",
    "src/export_formatted_borrowing_base_report.py",
    "src/covenant_monitoring.py",
    "src/build_excel_model.py",
    "src/build_sqlite_db.py",
    "src/run_sql_checks.py",
]


def run(script: str) -> None:
    print(f"\nRunning {script}...")
    result = subprocess.run([sys.executable, script], check=False)

    if result.returncode != 0:
        raise SystemExit(f"Pipeline failed at {script}")


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    print(f"Project root: {repo_root}")

    for script in SCRIPTS:
        run(script)

    print("\nPipeline completed successfully.")
    print("Generated outputs:")
    print("- data/*.csv")
    print("- model/fund_finance_model.xlsx")
    print("- outputs/fund_finance.db")
    print("- outputs/tables/*.csv")
    print("- outputs/reports/*.md")


if __name__ == "__main__":
    main()
