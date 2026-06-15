from pathlib import Path
import pandas as pd


DATA_DIR = Path("data")
OUTPUT_TABLE_DIR = Path("outputs/tables")
OUTPUT_REPORT_DIR = Path("outputs/reports")

OUTPUT_TABLE_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_REPORT_DIR.mkdir(parents=True, exist_ok=True)


def load_facility_assumptions() -> dict:
    facility = pd.read_csv(DATA_DIR / "facility_assumptions.csv")
    return dict(zip(facility["metric"], facility["value"]))


def dollars(value: float) -> str:
    value = float(value)
    if abs(value) >= 1_000_000_000:
        return f"${value / 1_000_000_000:,.2f}bn"
    return f"${value / 1_000_000:,.1f}mm"


def percent(value: float) -> str:
    return f"{float(value) * 100:.1f}%"


def multiple(value: float) -> str:
    return f"{float(value):.2f}x"


def create_investor_type_summary(investors: pd.DataFrame) -> pd.DataFrame:
    summary = (
        investors
        .groupby("investor_type", as_index=False)
        .agg(
            total_commitment=("total_commitment", "sum"),
            funded_commitment=("funded_commitment", "sum"),
            unfunded_commitment=("unfunded_commitment", "sum"),
            borrowing_base_contribution=("borrowing_base_contribution", "sum"),
            investor_count=("investor_id", "count"),
        )
    )

    summary["commitment_pct"] = summary["total_commitment"] / investors["total_commitment"].sum()
    summary["effective_advance_rate"] = (
        summary["borrowing_base_contribution"] / summary["unfunded_commitment"]
    )

    summary = summary.sort_values("total_commitment", ascending=False)

    return summary


def create_top_investor_summary(investors: pd.DataFrame) -> pd.DataFrame:
    total_commitments = investors["total_commitment"].sum()

    top = investors.copy()
    top["rank"] = top["total_commitment"].rank(method="first", ascending=False).astype(int)
    top["commitment_pct"] = top["total_commitment"] / total_commitments

    top = top.sort_values("rank")

    return top[
        [
            "rank",
            "investor_id",
            "investor_name",
            "investor_type",
            "internal_rating",
            "eligible_in_borrowing_base",
            "total_commitment",
            "unfunded_commitment",
            "advance_rate",
            "borrowing_base_contribution",
            "commitment_pct",
        ]
    ]


def create_availability_summary(values: dict) -> pd.DataFrame:
    facility_size = float(values["Facility Size"])
    facility_outstanding = float(values["Facility Outstanding"])
    subscription_borrowing_base = float(values["Subscription Borrowing Base"])
    eligible_nav = float(values["Eligible NAV"])
    max_ltv = float(values["Maximum LTV Covenant"])
    max_nav_debt_capacity = float(values["Maximum NAV Debt Capacity"])

    total_debt_capacity = min(
        facility_size,
        subscription_borrowing_base,
        max_nav_debt_capacity,
    )

    excess_availability = total_debt_capacity - facility_outstanding

    rows = [
        ("Facility Size", facility_size),
        ("Subscription Borrowing Base", subscription_borrowing_base),
        ("Eligible NAV", eligible_nav),
        ("Maximum NAV Debt Capacity", max_nav_debt_capacity),
        ("Total Debt Capacity", total_debt_capacity),
        ("Facility Outstanding", facility_outstanding),
        ("Excess Availability", excess_availability),
        ("Current LTV", float(values["Current LTV"])),
        ("Maximum LTV Covenant", max_ltv),
        ("Current Unfunded Coverage", float(values["Current Unfunded Coverage"])),
        ("Minimum Unfunded Coverage Covenant", float(values["Minimum Unfunded Coverage Covenant"])),
    ]

    return pd.DataFrame(rows, columns=["metric", "value"])


def create_concentration_tests(investors: pd.DataFrame) -> pd.DataFrame:
    total_commitments = investors["total_commitment"].sum()

    ranked = investors.sort_values("total_commitment", ascending=False).copy()
    top_1_pct = ranked.iloc[0]["total_commitment"] / total_commitments
    top_5_pct = ranked.head(5)["total_commitment"].sum() / total_commitments
    affiliate_pct = (
        investors.loc[investors["investor_type"] == "GP / Affiliate", "total_commitment"].sum()
        / total_commitments
    )

    tests = [
        {
            "test": "Largest Investor Concentration",
            "current_value": top_1_pct,
            "limit": 0.20,
            "status": "Pass" if top_1_pct <= 0.20 else "Fail",
        },
        {
            "test": "Top 5 Investor Concentration",
            "current_value": top_5_pct,
            "limit": 0.65,
            "status": "Pass" if top_5_pct <= 0.65 else "Fail",
        },
        {
            "test": "GP / Affiliate Concentration",
            "current_value": affiliate_pct,
            "limit": 0.05,
            "status": "Pass" if affiliate_pct <= 0.05 else "Fail",
        },
    ]

    return pd.DataFrame(tests)


def create_markdown_report(
    investor_type_summary: pd.DataFrame,
    top_investors: pd.DataFrame,
    availability: pd.DataFrame,
    concentration_tests: pd.DataFrame,
    values: dict,
) -> str:
    facility_size = float(values["Facility Size"])
    facility_outstanding = float(values["Facility Outstanding"])
    borrowing_base = float(values["Subscription Borrowing Base"])
    eligible_unfunded = float(values["Eligible Unfunded Commitments"])
    eligible_nav = float(values["Eligible NAV"])
    current_ltv = float(values["Current LTV"])
    excess_availability = float(values["Excess Availability"])
    unfunded_coverage = float(values["Current Unfunded Coverage"])

    report = f"""# Borrowing Base & Availability Summary

## Executive Summary

The simulated fund has {dollars(eligible_unfunded)} of eligible unfunded investor commitments and a subscription borrowing base of {dollars(borrowing_base)}. The requested facility size is {dollars(facility_size)}, with {dollars(facility_outstanding)} currently outstanding.

The facility is constrained by the committed facility size rather than the calculated borrowing base or NAV debt capacity. Based on the current outstanding amount, excess availability is {dollars(excess_availability)}.

## Key Metrics

| Metric | Value |
|---|---:|
| Facility Size | {dollars(facility_size)} |
| Facility Outstanding | {dollars(facility_outstanding)} |
| Subscription Borrowing Base | {dollars(borrowing_base)} |
| Eligible Unfunded Commitments | {dollars(eligible_unfunded)} |
| Eligible NAV | {dollars(eligible_nav)} |
| Current LTV | {percent(current_ltv)} |
| Current Unfunded Coverage | {multiple(unfunded_coverage)} |
| Excess Availability | {dollars(excess_availability)} |

## Credit Interpretation

The subscription borrowing base provides meaningful support relative to the proposed facility size. Eligible unfunded commitments are materially above the current outstanding balance, and the current LTV is below the proposed maximum LTV covenant.

The investor base is diversified across public pensions, sovereign wealth, insurance companies, endowments, fund-of-funds, and family offices. GP / affiliate commitments are excluded from the borrowing base.

## Investor Type Summary

{investor_type_summary.to_markdown(index=False)}

## Top Investor Summary

{top_investors.head(10).to_markdown(index=False)}

## Concentration Tests

{concentration_tests.to_markdown(index=False)}

## Availability Summary

{availability.to_markdown(index=False)}

## Analyst Conclusion

The proposed facility demonstrates acceptable simulated borrowing base support at closing. The main credit positives are the institutional investor base, significant eligible unfunded commitments, low current LTV, and positive excess availability.

Recommended monitoring items include investor concentration, NAV deterioration, watchlist assets, changes in LP eligibility, facility utilization, and monthly borrowing base compliance.
"""
    return report


def main() -> None:
    investors = pd.read_csv(DATA_DIR / "investors.csv")
    values = load_facility_assumptions()

    investor_type_summary = create_investor_type_summary(investors)
    top_investors = create_top_investor_summary(investors)
    availability = create_availability_summary(values)
    concentration_tests = create_concentration_tests(investors)

    investor_type_summary.to_csv(OUTPUT_TABLE_DIR / "investor_type_summary.csv", index=False)
    top_investors.to_csv(OUTPUT_TABLE_DIR / "top_investor_summary.csv", index=False)
    availability.to_csv(OUTPUT_TABLE_DIR / "availability_summary.csv", index=False)
    concentration_tests.to_csv(OUTPUT_TABLE_DIR / "concentration_tests.csv", index=False)

    report = create_markdown_report(
        investor_type_summary,
        top_investors,
        availability,
        concentration_tests,
        values,
    )

    report_path = OUTPUT_REPORT_DIR / "borrowing_base_summary.md"
    report_path.write_text(report)

    print("Borrowing base analysis complete.")
    print(f"- {OUTPUT_TABLE_DIR / 'investor_type_summary.csv'}")
    print(f"- {OUTPUT_TABLE_DIR / 'top_investor_summary.csv'}")
    print(f"- {OUTPUT_TABLE_DIR / 'availability_summary.csv'}")
    print(f"- {OUTPUT_TABLE_DIR / 'concentration_tests.csv'}")
    print(f"- {report_path}")


if __name__ == "__main__":
    main()
