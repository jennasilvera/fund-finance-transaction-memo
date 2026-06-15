from pathlib import Path
import pandas as pd


DATA_DIR = Path("data")
TABLE_DIR = Path("outputs/tables")
MODEL_DIR = Path("model")
MODEL_DIR.mkdir(exist_ok=True)


def autosize_columns(writer, sheet_name: str, df: pd.DataFrame, startrow: int = 0) -> None:
    worksheet = writer.sheets[sheet_name]

    for idx, col in enumerate(df.columns):
        max_len = max(
            [len(str(col))]
            + [len(str(value)) for value in df[col].head(200).values]
        )
        worksheet.set_column(idx, idx, min(max_len + 2, 34))


def write_title(worksheet, title: str, workbook, start_row: int, start_col: int, end_col: int) -> None:
    title_format = workbook.add_format(
        {
            "bold": True,
            "font_color": "white",
            "bg_color": "#1F4E78",
            "font_size": 12,
            "align": "left",
            "valign": "vcenter",
        }
    )
    worksheet.merge_range(start_row, start_col, start_row, end_col, title, title_format)


def main() -> None:
    investors = pd.read_csv(DATA_DIR / "investors.csv")
    nav = pd.read_csv(DATA_DIR / "nav_positions.csv")
    facility = pd.read_csv(DATA_DIR / "facility_assumptions.csv")
    covenants = pd.read_csv(DATA_DIR / "covenant_tests.csv")
    monitoring = pd.read_csv(DATA_DIR / "monthly_monitoring.csv", keep_default_na=False)

    investor_type_summary = pd.read_csv(TABLE_DIR / "investor_type_summary.csv")
    top_investor_summary = pd.read_csv(TABLE_DIR / "top_investor_summary.csv")
    availability_summary = pd.read_csv(TABLE_DIR / "availability_summary.csv")
    concentration_tests = pd.read_csv(TABLE_DIR / "concentration_tests.csv")
    monthly_covenant_monitoring = pd.read_csv(TABLE_DIR / "monthly_covenant_monitoring.csv", keep_default_na=False)

    output_path = MODEL_DIR / "fund_finance_model.xlsx"

    with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
        workbook = writer.book

        # Formats
        title_fmt = workbook.add_format(
            {
                "bold": True,
                "font_size": 16,
                "font_color": "white",
                "bg_color": "#17365D",
                "align": "left",
                "valign": "vcenter",
            }
        )

        section_fmt = workbook.add_format(
            {
                "bold": True,
                "font_color": "white",
                "bg_color": "#1F4E78",
                "align": "left",
                "valign": "vcenter",
                "border": 1,
            }
        )

        header_fmt = workbook.add_format(
            {
                "bold": True,
                "font_color": "white",
                "bg_color": "#5B9BD5",
                "border": 1,
                "align": "center",
                "valign": "vcenter",
                "text_wrap": True,
            }
        )

        input_fmt = workbook.add_format(
            {
                "font_color": "blue",
                "bg_color": "#FFF2CC",
                "border": 1,
                "num_format": '$#,##0.0,,"mm";[Red]($#,##0.0,,"mm");-',
            }
        )

        formula_fmt = workbook.add_format(
            {
                "font_color": "black",
                "border": 1,
                "num_format": '$#,##0.0,,"mm";[Red]($#,##0.0,,"mm");-',
            }
        )

        percent_fmt = workbook.add_format(
            {
                "font_color": "black",
                "border": 1,
                "num_format": '0.0%;[Red](0.0%);-',
            }
        )

        multiple_fmt = workbook.add_format(
            {
                "font_color": "black",
                "border": 1,
                "num_format": '0.00x;[Red](0.00x);-',
            }
        )

        text_fmt = workbook.add_format({"border": 1, "text_wrap": True})
        date_fmt = workbook.add_format({"border": 1, "num_format": "yyyy-mm-dd"})
        pass_fmt = workbook.add_format({"font_color": "#006100", "bg_color": "#C6EFCE"})
        fail_fmt = workbook.add_format({"font_color": "#9C0006", "bg_color": "#FFC7CE"})
        watch_fmt = workbook.add_format({"font_color": "#9C6500", "bg_color": "#FFEB9C"})

        # ---------------- Cover ----------------
        cover = workbook.add_worksheet("Cover")
        writer.sheets["Cover"] = cover
        cover.hide_gridlines(2)

        cover.merge_range("B2:H2", "Fund Finance Transaction Memo & Credit Request Package", title_fmt)
        cover.write("B4", "Project Type", section_fmt)
        cover.write("C4", "Simulated banker-style fund finance credit package", text_fmt)
        cover.write("B5", "Sponsor", section_fmt)
        cover.write("C5", "Aurora Ridge Capital Partners, L.P.", text_fmt)
        cover.write("B6", "Fund", section_fmt)
        cover.write("C6", "Aurora Ridge Private Credit Fund IV, L.P.", text_fmt)
        cover.write("B7", "Borrower", section_fmt)
        cover.write("C7", "ARPCF IV Financing Vehicle, L.P.", text_fmt)
        cover.write("B8", "Facility", section_fmt)
        cover.write("C8", "Senior secured hybrid subscription / NAV revolving credit facility", text_fmt)
        cover.write("B9", "Purpose", section_fmt)
        cover.write("C9", "Investment funding, follow-on capital, and working capital liquidity", text_fmt)

        cover.write("B11", "Important Disclaimer", section_fmt)
        cover.merge_range(
            "B12:H15",
            "This workbook is a simulated portfolio project for educational and recruiting purposes. "
            "All sponsor names, fund names, investor information, facility terms, portfolio data, and credit metrics are synthetic. "
            "No real client, fund, bank, investor, legal, or proprietary transaction information is used.",
            text_fmt,
        )

        cover.write("B17", "Workbook Sections", section_fmt)
        sections = [
            ["Assumptions", "Core transaction and covenant assumptions"],
            ["Investor Commitments", "Synthetic LP commitments, funded / unfunded amounts, eligibility, and advance rates"],
            ["Borrowing Base", "Subscription borrowing base and concentration tests"],
            ["NAV Collateral", "Synthetic portfolio positions and NAV collateral calculations"],
            ["Facility Summary", "Debt capacity, utilization, LTV, and excess availability"],
            ["Covenant Monitoring", "Monthly covenant status and monitoring controls"],
            ["Output Tables", "Banker-style summary tables for memo and presentation use"],
        ]
        for row_idx, row in enumerate(sections, start=18):
            cover.write(row_idx, 1, row[0], text_fmt)
            cover.write(row_idx, 2, row[1], text_fmt)

        cover.set_column("B:B", 24)
        cover.set_column("C:H", 26)

        # ---------------- Assumptions ----------------
        facility.to_excel(writer, sheet_name="Assumptions", index=False, startrow=2)
        ws = writer.sheets["Assumptions"]
        ws.hide_gridlines(2)
        ws.merge_range("A1:B1", "Core Facility Assumptions", title_fmt)
        ws.set_row(2, 30, header_fmt)
        ws.set_column("A:A", 36)
        ws.set_column("B:B", 28)
        ws.conditional_format("B1:B200", {"type": "no_errors", "format": input_fmt})

        # ---------------- Investor Commitments ----------------
        investors.to_excel(writer, sheet_name="Investor Commitments", index=False, startrow=2)
        ws = writer.sheets["Investor Commitments"]
        ws.hide_gridlines(2)
        ws.freeze_panes(3, 0)
        ws.merge_range(0, 0, 0, len(investors.columns) - 1, "Investor Commitments & Borrowing Base Eligibility", title_fmt)
        ws.set_row(2, 34, header_fmt)
        autosize_columns(writer, "Investor Commitments", investors)

        for col_num, col_name in enumerate(investors.columns):
            if col_name in [
                "total_commitment",
                "funded_commitment",
                "unfunded_commitment",
                "borrowing_base_contribution",
            ]:
                ws.set_column(col_num, col_num, 18, formula_fmt)
            elif col_name in ["funded_pct", "advance_rate", "commitment_pct"]:
                ws.set_column(col_num, col_num, 14, percent_fmt)

        ws.autofilter(2, 0, 2 + len(investors), len(investors.columns) - 1)

        # ---------------- Borrowing Base ----------------
        investor_type_summary.to_excel(writer, sheet_name="Borrowing Base", index=False, startrow=2)
        startrow = len(investor_type_summary) + 6
        concentration_tests.to_excel(writer, sheet_name="Borrowing Base", index=False, startrow=startrow)
        ws = writer.sheets["Borrowing Base"]
        ws.hide_gridlines(2)
        ws.merge_range("A1:H1", "Borrowing Base Summary", title_fmt)
        ws.merge_range(startrow - 1, 0, startrow - 1, 3, "Concentration Tests", section_fmt)
        ws.set_row(2, 30, header_fmt)
        ws.set_row(startrow, 30, header_fmt)
        ws.set_column("A:A", 28)
        ws.set_column("B:E", 18, formula_fmt)
        ws.set_column("F:F", 14)
        ws.set_column("G:H", 16, percent_fmt)

        # ---------------- NAV Collateral ----------------
        nav.to_excel(writer, sheet_name="NAV Collateral", index=False, startrow=2)
        ws = writer.sheets["NAV Collateral"]
        ws.hide_gridlines(2)
        ws.freeze_panes(3, 0)
        ws.merge_range(0, 0, 0, len(nav.columns) - 1, "NAV Collateral & Portfolio Positions", title_fmt)
        ws.set_row(2, 34, header_fmt)
        autosize_columns(writer, "NAV Collateral", nav)

        for col_num, col_name in enumerate(nav.columns):
            if col_name in ["cost_basis", "fair_value", "nav_collateral_value"]:
                ws.set_column(col_num, col_num, 18, formula_fmt)
            elif col_name in ["fair_value_marks", "nav_advance_rate", "portfolio_weight"]:
                ws.set_column(col_num, col_num, 14, percent_fmt)

        ws.autofilter(2, 0, 2 + len(nav), len(nav.columns) - 1)

        # ---------------- Facility Summary ----------------
        availability_summary.to_excel(writer, sheet_name="Facility Summary", index=False, startrow=2)
        ws = writer.sheets["Facility Summary"]
        ws.hide_gridlines(2)
        ws.merge_range("A1:B1", "Facility Capacity, LTV & Excess Availability", title_fmt)
        ws.set_row(2, 30, header_fmt)
        ws.set_column("A:A", 38)
        ws.set_column("B:B", 24)

        # ---------------- Covenant Monitoring ----------------
        monthly_covenant_monitoring.to_excel(writer, sheet_name="Covenant Monitoring", index=False, startrow=2)
        ws = writer.sheets["Covenant Monitoring"]
        ws.hide_gridlines(2)
        ws.freeze_panes(3, 0)
        ws.merge_range(0, 0, 0, len(monthly_covenant_monitoring.columns) - 1, "Monthly Covenant Monitoring", title_fmt)
        ws.set_row(2, 34, header_fmt)
        autosize_columns(writer, "Covenant Monitoring", monthly_covenant_monitoring)
        ws.autofilter(2, 0, 2 + len(monthly_covenant_monitoring), len(monthly_covenant_monitoring.columns) - 1)

        status_cols = []
        for idx, col_name in enumerate(monthly_covenant_monitoring.columns):
            if "status" in col_name.lower():
                status_cols.append(idx)

        for col_idx in status_cols:
            col_letter = chr(ord("A") + col_idx) if col_idx < 26 else None
            if col_letter:
                cell_range = f"{col_letter}4:{col_letter}{4 + len(monthly_covenant_monitoring)}"
                ws.conditional_format(cell_range, {"type": "text", "criteria": "containing", "value": "Pass", "format": pass_fmt})
                ws.conditional_format(cell_range, {"type": "text", "criteria": "containing", "value": "Watch", "format": watch_fmt})
                ws.conditional_format(cell_range, {"type": "text", "criteria": "containing", "value": "Fail", "format": fail_fmt})

        # ---------------- Output Tables ----------------
        ws = workbook.add_worksheet("Output Tables")
        writer.sheets["Output Tables"] = ws
        ws.hide_gridlines(2)

        ws.merge_range("A1:H1", "Memo / Credit Request Output Tables", title_fmt)

        current_row = 3

        tables = [
            ("Key Facility Metrics", availability_summary),
            ("Investor Type Summary", investor_type_summary),
            ("Top Investor Summary", top_investor_summary.head(10)),
            ("Concentration Tests", concentration_tests),
        ]

        for table_name, df in tables:
            ws.merge_range(current_row, 0, current_row, min(len(df.columns) - 1, 8), table_name, section_fmt)
            current_row += 1

            for col_idx, col_name in enumerate(df.columns):
                ws.write(current_row, col_idx, col_name, header_fmt)

            for r_idx, row in enumerate(df.values.tolist(), start=current_row + 1):
                for c_idx, value in enumerate(row):
                    ws.write(r_idx, c_idx, value, text_fmt)

            current_row += len(df) + 4

        ws.set_column("A:A", 32)
        ws.set_column("B:H", 20)

        # ---------------- Charts ----------------
        chart = workbook.add_chart({"type": "line"})
        chart.add_series(
            {
                "name": "Eligible NAV",
                "categories": ["Covenant Monitoring", 3, 0, 14, 0],
                "values": ["Covenant Monitoring", 3, 1, 14, 1],
            }
        )
        chart.set_title({"name": "Eligible NAV Trend"})
        chart.set_y_axis({"num_format": '$#,##0,,"mm"'})
        chart.set_legend({"position": "bottom"})
        ws.insert_chart("J3", chart, {"x_scale": 1.3, "y_scale": 1.1})

        chart2 = workbook.add_chart({"type": "line"})
        chart2.add_series(
            {
                "name": "LTV",
                "categories": ["Covenant Monitoring", 3, 0, 14, 0],
                "values": ["Covenant Monitoring", 3, 9, 14, 9],
            }
        )
        chart2.set_title({"name": "LTV Trend"})
        chart2.set_y_axis({"num_format": "0.0%"})
        chart2.set_legend({"position": "bottom"})
        ws.insert_chart("J22", chart2, {"x_scale": 1.3, "y_scale": 1.1})

    layout = """# Excel Model Layout

## Workbook

`fund_finance_model.xlsx`

## Tabs

1. **Cover**
   - Project overview
   - Simulated transaction summary
   - Disclaimer

2. **Assumptions**
   - Sponsor, fund, borrower, facility size, utilization, pricing, NAV, borrowing base, covenant thresholds

3. **Investor Commitments**
   - Synthetic LP data
   - Funded and unfunded commitments
   - Eligibility
   - Advance rates
   - Borrowing base contribution

4. **Borrowing Base**
   - Investor type aggregation
   - Subscription borrowing base
   - Investor concentration tests

5. **NAV Collateral**
   - Synthetic portfolio positions
   - Fair value marks
   - Eligible NAV collateral
   - NAV advance rates

6. **Facility Summary**
   - Facility size
   - Outstanding balance
   - Borrowing base
   - NAV debt capacity
   - Excess availability
   - LTV
   - Coverage ratios

7. **Covenant Monitoring**
   - Monthly NAV
   - Utilization
   - LTV
   - Excess availability
   - Covenant pass / watch / fail status

8. **Output Tables**
   - Banker-style tables usable in the transaction memo, credit request package, and lender presentation
   - Includes charts for NAV and LTV trends

## Modeling Notes

- All data is synthetic.
- Blue/yellow-style input cells indicate assumptions or hardcoded model inputs.
- Calculated model outputs are based on the synthetic CSV data generated by the Python scripts.
- The workbook is designed to support a fund finance credit memo, not to represent legal or investment advice.
"""

    (MODEL_DIR / "model_layout.md").write_text(layout)

    print("Excel model created successfully.")
    print(f"- {output_path}")
    print(f"- {MODEL_DIR / 'model_layout.md'}")


if __name__ == "__main__":
    main()
