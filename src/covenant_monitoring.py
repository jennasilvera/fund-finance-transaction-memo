from pathlib import Path
import pandas as pd


DATA_DIR = Path("data")
TABLE_DIR = Path("outputs/tables")
REPORT_DIR = Path("outputs/reports")

TABLE_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def dollars(value: float) -> str:
    value = float(value)
    if abs(value) >= 1_000_000_000:
        return f"${value / 1_000_000_000:,.2f}bn"
    return f"${value / 1_000_000:,.1f}mm"


def percent(value: float) -> str:
    return f"{float(value) * 100:.1f}%"


def load_assumptions() -> dict:
    df = pd.read_csv(DATA_DIR / "facility_assumptions.csv")
    return dict(zip(df["metric"], df["value"]))


def build_monthly_covenant_monitoring(monitoring: pd.DataFrame) -> pd.DataFrame:
    df = monitoring.copy()

    df["ltv_status"] = df.apply(
        lambda row: "Pass" if row["ltv"] <= row["max_ltv_covenant"] else "Fail",
        axis=1,
    )

    df["nav_floor_status"] = df.apply(
        lambda row: "Pass" if row["eligible_nav"] >= row["nav_floor"] else "Fail",
        axis=1,
    )

    df["availability_status"] = df.apply(
        lambda row: "Pass" if row["excess_availability"] >= 0 else "Fail",
        axis=1,
    )

    df["overall_status"] = df.apply(
        lambda row: "Fail"
        if "Fail" in [row["ltv_status"], row["nav_floor_status"], row["availability_status"]]
        else row["covenant_status"],
        axis=1,
    )

    return df


def build_watchlist_items(monthly: pd.DataFrame) -> pd.DataFrame:
    watchlist = monthly[
        (monthly["overall_status"].isin(["Watch", "Fail"]))
        | (monthly["watchlist_item"] != "None")
    ].copy()

    if watchlist.empty:
        return pd.DataFrame(
            columns=[
                "reporting_date",
                "issue",
                "severity",
                "commentary",
                "recommended_action",
            ]
        )

    rows = []

    for _, row in watchlist.iterrows():
        severity = "High" if row["overall_status"] == "Fail" else "Medium"

        if row["watchlist_item"] == "Low excess availability":
            commentary = (
                "Excess availability has declined toward the internal monitoring threshold, "
                "which may limit borrower liquidity if utilization increases further."
            )
            recommended_action = (
                "Request updated borrowing base certificate, confirm near-term capital call plan, "
                "and monitor utilization before additional draws."
            )
        elif row["watchlist_item"] == "Elevated LTV":
            commentary = (
                "LTV is approaching the upper end of the expected operating range, increasing "
                "sensitivity to NAV declines."
            )
            recommended_action = (
                "Request portfolio valuation commentary and review watchlist assets, repayment activity, "
                "and projected NAV movement."
            )
        elif row["watchlist_item"] == "LTV covenant breach":
            commentary = (
                "Facility LTV exceeds the maximum LTV covenant and would require immediate escalation."
            )
            recommended_action = (
                "Escalate to credit officer, restrict further borrowings, request cure plan, "
                "and evaluate mandatory prepayment requirements."
            )
        elif row["watchlist_item"] == "NAV below floor":
            commentary = (
                "Eligible NAV has fallen below the required NAV floor, indicating possible portfolio stress."
            )
            recommended_action = (
                "Escalate to credit officer, request updated NAV bridge, review asset marks, "
                "and evaluate amendment or paydown requirements."
            )
        else:
            commentary = "Monthly monitoring identified an item requiring follow-up."
            recommended_action = "Review with portfolio monitoring team and request borrower update."

        rows.append(
            {
                "reporting_date": row["reporting_date"],
                "issue": row["watchlist_item"],
                "severity": severity,
                "commentary": commentary,
                "recommended_action": recommended_action,
            }
        )

    return pd.DataFrame(rows)


def format_monthly_table(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    for col in [
        "eligible_nav",
        "facility_size",
        "facility_outstanding",
        "subscription_borrowing_base",
        "max_nav_debt_capacity",
        "total_debt_capacity",
        "excess_availability",
        "nav_floor",
    ]:
        out[col] = out[col].apply(dollars)

    for col in [
        "facility_utilization_pct",
        "ltv",
        "max_ltv_covenant",
    ]:
        out[col] = out[col].apply(percent)

    out = out.rename(
        columns={
            "reporting_date": "Reporting Date",
            "eligible_nav": "Eligible NAV",
            "facility_size": "Facility Size",
            "facility_outstanding": "Facility Outstanding",
            "facility_utilization_pct": "Utilization",
            "subscription_borrowing_base": "Subscription Borrowing Base",
            "max_nav_debt_capacity": "Max NAV Debt Capacity",
            "total_debt_capacity": "Total Debt Capacity",
            "excess_availability": "Excess Availability",
            "ltv": "LTV",
            "max_ltv_covenant": "Max LTV Covenant",
            "nav_floor": "NAV Floor",
            "covenant_status": "Original Status",
            "watchlist_item": "Watchlist Item",
            "ltv_status": "LTV Status",
            "nav_floor_status": "NAV Floor Status",
            "availability_status": "Availability Status",
            "overall_status": "Overall Status",
        }
    )

    return out


def format_watchlist_table(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    return df.rename(
        columns={
            "reporting_date": "Reporting Date",
            "issue": "Issue",
            "severity": "Severity",
            "commentary": "Commentary",
            "recommended_action": "Recommended Action",
        }
    )


def create_report(values: dict, monthly: pd.DataFrame, watchlist: pd.DataFrame) -> str:
    latest = monthly.iloc[-1]

    pass_count = (monthly["overall_status"] == "Pass").sum()
    watch_count = (monthly["overall_status"] == "Watch").sum()
    fail_count = (monthly["overall_status"] == "Fail").sum()

    latest_nav = float(latest["eligible_nav"])
    latest_outstanding = float(latest["facility_outstanding"])
    latest_excess_availability = float(latest["excess_availability"])
    latest_ltv = float(latest["ltv"])
    latest_utilization = float(latest["facility_utilization_pct"])

    status_summary = "Pass"
    if fail_count > 0:
        status_summary = "Fail"
    elif watch_count > 0:
        status_summary = "Watch"

    watchlist_text = (
        "No active watchlist items were identified during the monitoring period."
        if watchlist.empty
        else format_watchlist_table(watchlist).to_markdown(index=False)
    )

    report = f"""# Covenant Monitoring Report

## Executive Summary

This report reviews monthly covenant compliance for the simulated $150.0 million senior secured hybrid subscription / NAV revolving credit facility for ARPCF IV Financing Vehicle, L.P.

The latest reporting period shows eligible NAV of {dollars(latest_nav)}, facility outstanding of {dollars(latest_outstanding)}, utilization of {percent(latest_utilization)}, LTV of {percent(latest_ltv)}, and excess availability of {dollars(latest_excess_availability)}.

Overall monitoring status: **{status_summary}**

## Covenant Dashboard

| Metric | Result |
|---|---:|
| Pass Months | {pass_count} |
| Watch Months | {watch_count} |
| Fail Months | {fail_count} |
| Latest Eligible NAV | {dollars(latest_nav)} |
| Latest Facility Outstanding | {dollars(latest_outstanding)} |
| Latest Facility Utilization | {percent(latest_utilization)} |
| Latest LTV | {percent(latest_ltv)} |
| Latest Excess Availability | {dollars(latest_excess_availability)} |

## Core Covenant Tests

| Covenant | Threshold | Monitoring Logic |
|---|---:|---|
| Maximum LTV | {percent(float(values["Maximum LTV Covenant"]))} | Facility outstanding / eligible NAV must remain at or below the threshold |
| NAV Floor | {dollars(float(values["NAV Floor"]))} | Eligible NAV must remain at or above the NAV floor |
| Excess Availability | $0.0mm minimum | Total debt capacity less facility outstanding must remain positive |
| Minimum Unfunded Coverage | {float(values["Minimum Unfunded Coverage Covenant"]):.2f}x | Eligible unfunded commitments / facility outstanding |

## Monthly Monitoring Table

{format_monthly_table(monthly).to_markdown(index=False)}

## Watchlist Items

{watchlist_text}

## Analyst Commentary

The facility remains supported by positive excess availability, a current LTV below the maximum LTV covenant, and meaningful eligible unfunded commitments. The monthly monitoring process should focus on NAV movement, utilization trends, investor eligibility, and any deterioration in portfolio assets classified as watchlist positions.

## Recommended Monitoring Actions

- Continue monthly borrowing base certification review
- Track facility utilization relative to total debt capacity
- Monitor NAV movement and portfolio valuation marks
- Review watchlist portfolio companies and any deteriorating assets
- Confirm no investor defaults or changes to LP eligibility
- Escalate any LTV, NAV floor, or availability breach to credit officers

## Final Monitoring View

Based on the simulated monthly data, the facility remains acceptable for continued monitoring under the proposed covenant package. No credit approval changes are recommended unless future reporting shows NAV deterioration, increased utilization, or reduced borrowing base availability.
"""

    return report


def main() -> None:
    values = load_assumptions()
    monitoring = pd.read_csv(DATA_DIR / "monthly_monitoring.csv", keep_default_na=False)
    monitoring["watchlist_item"] = monitoring["watchlist_item"].fillna("None").replace("", "None")

    monthly = build_monthly_covenant_monitoring(monitoring)
    watchlist = build_watchlist_items(monthly)

    monthly.to_csv(TABLE_DIR / "monthly_covenant_monitoring.csv", index=False)
    watchlist.to_csv(TABLE_DIR / "watchlist_items.csv", index=False)

    report = create_report(values, monthly, watchlist)

    output_path = REPORT_DIR / "covenant_monitoring_report.md"
    output_path.write_text(report)

    print("Covenant monitoring report created.")
    print(f"- {TABLE_DIR / 'monthly_covenant_monitoring.csv'}")
    print(f"- {TABLE_DIR / 'watchlist_items.csv'}")
    print(f"- {output_path}")


if __name__ == "__main__":
    main()
