from pathlib import Path
import pandas as pd


DATA_DIR = Path("data")
TABLE_DIR = Path("outputs/tables")
REPORT_DIR = Path("outputs/reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def dollars(value: float) -> str:
    value = float(value)
    if abs(value) >= 1_000_000_000:
        return f"${value / 1_000_000_000:,.2f}bn"
    return f"${value / 1_000_000:,.1f}mm"


def percent(value: float) -> str:
    return f"{float(value) * 100:.1f}%"


def multiple(value: float) -> str:
    return f"{float(value):.2f}x"


def load_assumptions() -> dict:
    df = pd.read_csv(DATA_DIR / "facility_assumptions.csv")
    return dict(zip(df["metric"], df["value"]))


def format_investor_type_summary(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in [
        "total_commitment",
        "funded_commitment",
        "unfunded_commitment",
        "borrowing_base_contribution",
    ]:
        out[col] = out[col].apply(dollars)

    out["commitment_pct"] = out["commitment_pct"].apply(percent)
    out["effective_advance_rate"] = out["effective_advance_rate"].apply(percent)

    out = out.rename(
        columns={
            "investor_type": "Investor Type",
            "total_commitment": "Total Commitment",
            "funded_commitment": "Funded Commitment",
            "unfunded_commitment": "Unfunded Commitment",
            "borrowing_base_contribution": "Borrowing Base Contribution",
            "investor_count": "Investor Count",
            "commitment_pct": "% of Commitments",
            "effective_advance_rate": "Effective Advance Rate",
        }
    )

    return out


def format_top_investors(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    for col in [
        "total_commitment",
        "unfunded_commitment",
        "borrowing_base_contribution",
    ]:
        out[col] = out[col].apply(dollars)

    out["advance_rate"] = out["advance_rate"].apply(percent)
    out["commitment_pct"] = out["commitment_pct"].apply(percent)

    out = out.rename(
        columns={
            "rank": "Rank",
            "investor_id": "Investor ID",
            "investor_name": "Investor Name",
            "investor_type": "Investor Type",
            "internal_rating": "Internal Rating",
            "eligible_in_borrowing_base": "Eligible",
            "total_commitment": "Total Commitment",
            "unfunded_commitment": "Unfunded Commitment",
            "advance_rate": "Advance Rate",
            "borrowing_base_contribution": "Borrowing Base Contribution",
            "commitment_pct": "% of Commitments",
        }
    )

    return out


def format_concentration_tests(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["current_value"] = out["current_value"].apply(percent)
    out["limit"] = out["limit"].apply(percent)

    out = out.rename(
        columns={
            "test": "Test",
            "current_value": "Current Value",
            "limit": "Limit",
            "status": "Status",
        }
    )

    return out


def format_availability(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    formatted_values = []

    for _, row in out.iterrows():
        metric = row["metric"]
        value = float(row["value"])

        if "LTV" in metric:
            formatted_values.append(percent(value))
        elif "Coverage" in metric:
            formatted_values.append(multiple(value))
        else:
            formatted_values.append(dollars(value))

    out["value"] = formatted_values

    out = out.rename(
        columns={
            "metric": "Metric",
            "value": "Value",
        }
    )

    return out


def main() -> None:
    values = load_assumptions()

    investor_type_summary = pd.read_csv(TABLE_DIR / "investor_type_summary.csv")
    top_investors = pd.read_csv(TABLE_DIR / "top_investor_summary.csv")
    concentration_tests = pd.read_csv(TABLE_DIR / "concentration_tests.csv")
    availability = pd.read_csv(TABLE_DIR / "availability_summary.csv")

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

{format_investor_type_summary(investor_type_summary).to_markdown(index=False)}

## Top Investor Summary

{format_top_investors(top_investors.head(10)).to_markdown(index=False)}

## Concentration Tests

{format_concentration_tests(concentration_tests).to_markdown(index=False)}

## Availability Summary

{format_availability(availability).to_markdown(index=False)}

## Analyst Conclusion

The proposed facility demonstrates acceptable simulated borrowing base support at closing. The main credit positives are the institutional investor base, significant eligible unfunded commitments, low current LTV, and positive excess availability.

Recommended monitoring items include investor concentration, NAV deterioration, watchlist assets, changes in LP eligibility, facility utilization, and monthly borrowing base compliance.
"""

    output_path = REPORT_DIR / "borrowing_base_summary_formatted.md"
    output_path.write_text(report)

    print("Formatted borrowing base report created.")
    print(f"- {output_path}")


if __name__ == "__main__":
    main()
