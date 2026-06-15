from pathlib import Path
import pandas as pd
import numpy as np


OUTPUT_DIR = Path("data")
OUTPUT_DIR.mkdir(exist_ok=True)


def money(value: float) -> float:
    """Round dollar values to nearest dollar."""
    return round(float(value), 2)


def generate_investors() -> pd.DataFrame:
    investors = [
        ("INV001", "Northstar Public Pension Trust", "Public Pension", 180_000_000, 0.45, "A", "Yes", 0.90),
        ("INV002", "Atlantic Sovereign Investment Authority", "Sovereign Wealth", 155_000_000, 0.45, "A", "Yes", 0.90),
        ("INV003", "Harbor State Retirement System", "Public Pension", 135_000_000, 0.45, "A", "Yes", 0.90),
        ("INV004", "Crescent Life Insurance Company", "Insurance Company", 120_000_000, 0.45, "A-", "Yes", 0.80),
        ("INV005", "Granite University Endowment", "Endowment / Foundation", 95_000_000, 0.45, "A-", "Yes", 0.75),
        ("INV006", "Redwood Foundation", "Endowment / Foundation", 85_000_000, 0.45, "BBB+", "Yes", 0.75),
        ("INV007", "Meridian Fund-of-Funds III", "Fund-of-Funds", 80_000_000, 0.45, "BBB", "Yes", 0.65),
        ("INV008", "Pioneer Private Markets Program", "Fund-of-Funds", 75_000_000, 0.45, "BBB", "Yes", 0.65),
        ("INV009", "Summit Family Capital", "Family Office / HNW", 60_000_000, 0.45, "BB+", "Yes", 0.50),
        ("INV010", "Bluewater Family Office", "Family Office / HNW", 50_000_000, 0.45, "BB+", "Yes", 0.50),
        ("INV011", "Aurora Ridge GP Commitment", "GP / Affiliate", 45_000_000, 0.45, "NR", "No", 0.00),
        ("INV012", "Lakeside Wealth Partners", "Family Office / HNW", 40_000_000, 0.45, "BB", "Yes", 0.50),
        ("INV013", "Cedar Insurance Separate Account", "Insurance Company", 35_000_000, 0.45, "A-", "Yes", 0.80),
        ("INV014", "Westlake Charitable Foundation", "Endowment / Foundation", 30_000_000, 0.45, "BBB+", "Yes", 0.75),
        ("INV015", "Oakmont Private Markets Feeder", "Feeder / Other", 15_000_000, 0.45, "NR", "No", 0.00),
    ]

    df = pd.DataFrame(
        investors,
        columns=[
            "investor_id",
            "investor_name",
            "investor_type",
            "total_commitment",
            "funded_pct",
            "internal_rating",
            "eligible_in_borrowing_base",
            "advance_rate",
        ],
    )

    df["funded_commitment"] = df["total_commitment"] * df["funded_pct"]
    df["unfunded_commitment"] = df["total_commitment"] - df["funded_commitment"]
    df["borrowing_base_contribution"] = np.where(
        df["eligible_in_borrowing_base"] == "Yes",
        df["unfunded_commitment"] * df["advance_rate"],
        0,
    )

    df["commitment_pct"] = df["total_commitment"] / df["total_commitment"].sum()

    numeric_cols = [
        "total_commitment",
        "funded_commitment",
        "unfunded_commitment",
        "advance_rate",
        "borrowing_base_contribution",
        "commitment_pct",
    ]

    for col in numeric_cols:
        df[col] = df[col].round(4)

    return df


def generate_nav_positions() -> pd.DataFrame:
    positions = [
        ("POS001", "Alpha Diagnostics Term Loan", "Healthcare", "Senior Secured Loan", 55_000_000, 0.96, "Performing", "Yes", 0.85),
        ("POS002", "Beacon Software First Lien Loan", "Software", "Senior Secured Loan", 48_000_000, 0.98, "Performing", "Yes", 0.85),
        ("POS003", "Canyon Logistics Unitranche", "Logistics", "Unitranche Loan", 46_000_000, 0.94, "Performing", "Yes", 0.75),
        ("POS004", "Delta Packaging First Lien Loan", "Packaging", "Senior Secured Loan", 44_000_000, 0.97, "Performing", "Yes", 0.85),
        ("POS005", "Evergreen IT Services Loan", "IT Services", "Senior Secured Loan", 43_000_000, 0.99, "Performing", "Yes", 0.85),
        ("POS006", "Frontier Specialty Manufacturing", "Industrials", "Senior Secured Loan", 42_000_000, 0.95, "Performing", "Yes", 0.85),
        ("POS007", "Granite Business Services Debt", "Business Services", "Unitranche Loan", 40_000_000, 0.93, "Performing", "Yes", 0.75),
        ("POS008", "Harbor Consumer Products Loan", "Consumer", "Senior Secured Loan", 39_000_000, 0.91, "Watchlist", "Yes", 0.65),
        ("POS009", "Ivory Medical Devices Loan", "Healthcare", "Senior Secured Loan", 38_000_000, 0.98, "Performing", "Yes", 0.85),
        ("POS010", "Juniper Data Infrastructure Loan", "Technology Infrastructure", "Senior Secured Loan", 37_000_000, 0.99, "Performing", "Yes", 0.85),
        ("POS011", "Keystone Education Services Debt", "Education", "Unitranche Loan", 36_000_000, 0.92, "Performing", "Yes", 0.75),
        ("POS012", "Lighthouse Restaurant Group Loan", "Restaurants", "Second Lien Loan", 34_000_000, 0.82, "Watchlist", "No", 0.00),
        ("POS013", "Monarch Specialty Chemicals Loan", "Chemicals", "Senior Secured Loan", 33_000_000, 0.94, "Performing", "Yes", 0.85),
        ("POS014", "Northwind Distribution Loan", "Distribution", "Senior Secured Loan", 32_000_000, 0.97, "Performing", "Yes", 0.85),
        ("POS015", "Orchard Media Services Loan", "Media", "Second Lien Loan", 30_000_000, 0.80, "Watchlist", "No", 0.00),
        ("POS016", "Pinnacle Environmental Services", "Environmental Services", "Senior Secured Loan", 28_000_000, 0.96, "Performing", "Yes", 0.85),
        ("POS017", "Quartz Security Systems Loan", "Security Services", "Unitranche Loan", 26_000_000, 0.94, "Performing", "Yes", 0.75),
        ("POS018", "Riverview Food Ingredients Loan", "Food Ingredients", "Senior Secured Loan", 24_000_000, 0.95, "Performing", "Yes", 0.85),
    ]

    df = pd.DataFrame(
        positions,
        columns=[
            "position_id",
            "portfolio_company",
            "industry",
            "asset_type",
            "cost_basis",
            "fair_value_marks",
            "status",
            "eligible_nav_collateral",
            "nav_advance_rate",
        ],
    )

    df["fair_value"] = df["cost_basis"] * df["fair_value_marks"]
    df["nav_collateral_value"] = np.where(
        df["eligible_nav_collateral"] == "Yes",
        df["fair_value"] * df["nav_advance_rate"],
        0,
    )
    df["portfolio_weight"] = df["fair_value"] / df["fair_value"].sum()

    numeric_cols = [
        "cost_basis",
        "fair_value_marks",
        "fair_value",
        "nav_advance_rate",
        "nav_collateral_value",
        "portfolio_weight",
    ]

    for col in numeric_cols:
        df[col] = df[col].round(4)

    return df


def generate_facility_assumptions(investors: pd.DataFrame, nav: pd.DataFrame) -> pd.DataFrame:
    total_commitments = investors["total_commitment"].sum()
    funded_commitments = investors["funded_commitment"].sum()
    unfunded_commitments = investors["unfunded_commitment"].sum()
    eligible_unfunded = investors.loc[
        investors["eligible_in_borrowing_base"] == "Yes",
        "unfunded_commitment",
    ].sum()
    borrowing_base = investors["borrowing_base_contribution"].sum()

    gross_nav = nav["fair_value"].sum()
    eligible_nav = nav.loc[nav["eligible_nav_collateral"] == "Yes", "fair_value"].sum()

    facility_size = 150_000_000
    facility_outstanding = 110_000_000
    max_ltv = 0.35
    nav_floor = 450_000_000
    min_unfunded_coverage = 2.0

    max_nav_debt_capacity = eligible_nav * max_ltv
    total_debt_capacity = min(facility_size, borrowing_base, max_nav_debt_capacity)
    excess_availability = total_debt_capacity - facility_outstanding
    current_ltv = facility_outstanding / eligible_nav
    unfunded_coverage = eligible_unfunded / facility_outstanding

    assumptions = [
        ("Sponsor", "Aurora Ridge Capital Partners, L.P."),
        ("Fund", "Aurora Ridge Private Credit Fund IV, L.P."),
        ("Borrower", "ARPCF IV Financing Vehicle, L.P."),
        ("Facility Type", "Senior Secured Hybrid Subscription / NAV Revolving Credit Facility"),
        ("Facility Size", facility_size),
        ("Facility Outstanding", facility_outstanding),
        ("Tenor Months", 24),
        ("Extension Option Months", 12),
        ("SOFR Floor", 0.00),
        ("Credit Spread", 0.0275),
        ("Unused Fee", 0.0050),
        ("Total Commitments", total_commitments),
        ("Funded Commitments", funded_commitments),
        ("Unfunded Commitments", unfunded_commitments),
        ("Eligible Unfunded Commitments", eligible_unfunded),
        ("Subscription Borrowing Base", borrowing_base),
        ("Gross NAV", gross_nav),
        ("Eligible NAV", eligible_nav),
        ("Maximum LTV Covenant", max_ltv),
        ("Current LTV", current_ltv),
        ("NAV Floor", nav_floor),
        ("Maximum NAV Debt Capacity", max_nav_debt_capacity),
        ("Total Debt Capacity", total_debt_capacity),
        ("Excess Availability", excess_availability),
        ("Minimum Unfunded Coverage Covenant", min_unfunded_coverage),
        ("Current Unfunded Coverage", unfunded_coverage),
    ]

    return pd.DataFrame(assumptions, columns=["metric", "value"])


def generate_covenant_tests(facility: pd.DataFrame) -> pd.DataFrame:
    values = dict(zip(facility["metric"], facility["value"]))

    tests = [
        (
            "Maximum LTV",
            float(values["Current LTV"]),
            "<=",
            float(values["Maximum LTV Covenant"]),
            "Pass",
        ),
        (
            "NAV Floor",
            float(values["Eligible NAV"]),
            ">=",
            float(values["NAV Floor"]),
            "Pass",
        ),
        (
            "Minimum Unfunded Coverage",
            float(values["Current Unfunded Coverage"]),
            ">=",
            float(values["Minimum Unfunded Coverage Covenant"]),
            "Pass",
        ),
        (
            "Excess Availability",
            float(values["Excess Availability"]),
            ">=",
            0.0,
            "Pass",
        ),
    ]

    return pd.DataFrame(
        tests,
        columns=[
            "covenant",
            "current_value",
            "test",
            "threshold",
            "status",
        ],
    )


def generate_monthly_monitoring(facility: pd.DataFrame) -> pd.DataFrame:
    values = dict(zip(facility["metric"], facility["value"]))

    months = pd.date_range("2026-01-31", periods=12, freq="ME")

    base_nav = float(values["Eligible NAV"])
    facility_size = float(values["Facility Size"])
    outstanding = float(values["Facility Outstanding"])
    borrowing_base = float(values["Subscription Borrowing Base"])
    max_ltv = float(values["Maximum LTV Covenant"])
    nav_floor = float(values["NAV Floor"])

    nav_changes = [0.000, 0.006, 0.004, -0.010, 0.003, 0.005, -0.018, 0.002, 0.004, -0.006, 0.003, 0.005]
    utilization_changes = [0, 5_000_000, 8_000_000, -10_000_000, 12_000_000, -6_000_000, 9_000_000, -5_000_000, 7_000_000, -8_000_000, 4_000_000, -6_000_000]
    borrowing_base_changes = [0, 2_000_000, 1_500_000, -4_000_000, 2_500_000, 2_000_000, -5_000_000, 1_000_000, 1_500_000, -2_000_000, 1_000_000, 1_000_000]

    rows = []
    current_nav = base_nav
    current_outstanding = outstanding
    current_bb = borrowing_base

    for i, month in enumerate(months):
        current_nav = current_nav * (1 + nav_changes[i])
        current_outstanding = max(0, min(facility_size, current_outstanding + utilization_changes[i]))
        current_bb = current_bb + borrowing_base_changes[i]

        max_nav_debt_capacity = current_nav * max_ltv
        total_debt_capacity = min(facility_size, current_bb, max_nav_debt_capacity)
        excess_availability = total_debt_capacity - current_outstanding
        ltv = current_outstanding / current_nav
        utilization_pct = current_outstanding / facility_size

        covenant_status = "Pass"
        watchlist_item = "None"

        if ltv > max_ltv:
            covenant_status = "Fail"
            watchlist_item = "LTV covenant breach"
        elif current_nav < nav_floor:
            covenant_status = "Fail"
            watchlist_item = "NAV below floor"
        elif excess_availability < 10_000_000:
            covenant_status = "Watch"
            watchlist_item = "Low excess availability"
        elif ltv > 0.30:
            covenant_status = "Watch"
            watchlist_item = "Elevated LTV"

        rows.append(
            {
                "reporting_date": month.date().isoformat(),
                "eligible_nav": round(current_nav, 2),
                "facility_size": round(facility_size, 2),
                "facility_outstanding": round(current_outstanding, 2),
                "facility_utilization_pct": round(utilization_pct, 4),
                "subscription_borrowing_base": round(current_bb, 2),
                "max_nav_debt_capacity": round(max_nav_debt_capacity, 2),
                "total_debt_capacity": round(total_debt_capacity, 2),
                "excess_availability": round(excess_availability, 2),
                "ltv": round(ltv, 4),
                "max_ltv_covenant": round(max_ltv, 4),
                "nav_floor": round(nav_floor, 2),
                "covenant_status": covenant_status,
                "watchlist_item": watchlist_item,
            }
        )

    return pd.DataFrame(rows)


def main() -> None:
    investors = generate_investors()
    nav = generate_nav_positions()
    facility = generate_facility_assumptions(investors, nav)
    covenants = generate_covenant_tests(facility)
    monitoring = generate_monthly_monitoring(facility)

    investors.to_csv(OUTPUT_DIR / "investors.csv", index=False)
    nav.to_csv(OUTPUT_DIR / "nav_positions.csv", index=False)
    facility.to_csv(OUTPUT_DIR / "facility_assumptions.csv", index=False)
    covenants.to_csv(OUTPUT_DIR / "covenant_tests.csv", index=False)
    monitoring.to_csv(OUTPUT_DIR / "monthly_monitoring.csv", index=False)

    print("Synthetic fund finance datasets created successfully.")
    print(f"- {OUTPUT_DIR / 'investors.csv'}")
    print(f"- {OUTPUT_DIR / 'nav_positions.csv'}")
    print(f"- {OUTPUT_DIR / 'facility_assumptions.csv'}")
    print(f"- {OUTPUT_DIR / 'covenant_tests.csv'}")
    print(f"- {OUTPUT_DIR / 'monthly_monitoring.csv'}")


if __name__ == "__main__":
    main()
