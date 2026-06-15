# SQL Monitoring Outputs

This report contains sample SQL outputs from the simulated fund finance SQLite database.

> All data is synthetic and prepared for portfolio project purposes only.

## Latest Monitoring Snapshot

| reporting_date   |   outstanding_mm |   utilization_pct |   eligible_nav_mm |   ltv_pct |   excess_availability_mm | covenant_status   | watchlist_item   |
|:-----------------|-----------------:|------------------:|------------------:|----------:|-------------------------:|:------------------|:-----------------|
| 2026-12-31       |              120 |                80 |             582.7 |      20.6 |                       30 | Pass              | None             |

## Monthly Facility Trend

| reporting_date   |   outstanding_mm |   utilization_pct |   ltv_pct |   excess_availability_mm | covenant_status   |
|:-----------------|-----------------:|------------------:|----------:|-------------------------:|:------------------|
| 2026-01-31       |              110 |              73.3 |      18.8 |                       40 | Pass              |
| 2026-02-28       |              115 |              76.7 |      19.6 |                       35 | Pass              |
| 2026-03-31       |              123 |              82   |      20.8 |                       27 | Pass              |
| 2026-04-30       |              113 |              75.3 |      19.4 |                       37 | Pass              |
| 2026-05-31       |              125 |              83.3 |      21.3 |                       25 | Pass              |
| 2026-06-30       |              119 |              79.3 |      20.2 |                       31 | Pass              |
| 2026-07-31       |              128 |              85.3 |      22.1 |                       22 | Pass              |
| 2026-08-31       |              123 |              82   |      21.2 |                       27 | Pass              |
| 2026-09-30       |              130 |              86.7 |      22.4 |                       20 | Pass              |
| 2026-10-31       |              122 |              81.3 |      21.1 |                       28 | Pass              |
| 2026-11-30       |              126 |              84   |      21.7 |                       24 | Pass              |
| 2026-12-31       |              120 |              80   |      20.6 |                       30 | Pass              |

## Investor Type Summary

| investor_type          |   investor_count |   total_commitment_mm |   unfunded_commitment_mm |   borrowing_base_contribution_mm |   commitment_pct |
|:-----------------------|-----------------:|----------------------:|-------------------------:|---------------------------------:|-----------------:|
| Public Pension         |                2 |                   315 |                    173.3 |                            155.9 |             26.3 |
| Endowment / Foundation |                3 |                   210 |                    115.5 |                             86.6 |             17.5 |
| Sovereign Wealth       |                1 |                   155 |                     85.3 |                             76.7 |             12.9 |
| Insurance Company      |                2 |                   155 |                     85.3 |                             68.2 |             12.9 |
| Fund-of-Funds          |                2 |                   155 |                     85.3 |                             55.4 |             12.9 |
| Family Office / HNW    |                3 |                   150 |                     82.5 |                             41.3 |             12.5 |
| GP / Affiliate         |                1 |                    45 |                     24.8 |                              0   |              3.8 |
| Feeder / Other         |                1 |                    15 |                      8.3 |                              0   |              1.3 |

## Top Investors

| investor_id   | investor_name                           | investor_type          | internal_rating   | eligible_in_borrowing_base   |   total_commitment_mm |   unfunded_commitment_mm |   advance_rate_pct |   borrowing_base_contribution_mm |
|:--------------|:----------------------------------------|:-----------------------|:------------------|:-----------------------------|----------------------:|-------------------------:|-------------------:|---------------------------------:|
| INV001        | Northstar Public Pension Trust          | Public Pension         | A                 | Yes                          |                   180 |                     99   |                 90 |                             89.1 |
| INV002        | Atlantic Sovereign Investment Authority | Sovereign Wealth       | A                 | Yes                          |                   155 |                     85.3 |                 90 |                             76.7 |
| INV003        | Harbor State Retirement System          | Public Pension         | A                 | Yes                          |                   135 |                     74.3 |                 90 |                             66.8 |
| INV004        | Crescent Life Insurance Company         | Insurance Company      | A-                | Yes                          |                   120 |                     66   |                 80 |                             52.8 |
| INV005        | Granite University Endowment            | Endowment / Foundation | A-                | Yes                          |                    95 |                     52.3 |                 75 |                             39.2 |
| INV006        | Redwood Foundation                      | Endowment / Foundation | BBB+              | Yes                          |                    85 |                     46.8 |                 75 |                             35.1 |
| INV007        | Meridian Fund-of-Funds III              | Fund-of-Funds          | BBB               | Yes                          |                    80 |                     44   |                 65 |                             28.6 |
| INV008        | Pioneer Private Markets Program         | Fund-of-Funds          | BBB               | Yes                          |                    75 |                     41.3 |                 65 |                             26.8 |
| INV009        | Summit Family Capital                   | Family Office / HNW    | BB+               | Yes                          |                    60 |                     33   |                 50 |                             16.5 |
| INV010        | Bluewater Family Office                 | Family Office / HNW    | BB+               | Yes                          |                    50 |                     27.5 |                 50 |                             13.8 |

## Watchlist NAV Positions

| position_id   | portfolio_company                | industry    | asset_type          | status    |   cost_basis_mm |   fair_value_mm |   fair_value_mark_pct | eligible_nav_collateral   |
|:--------------|:---------------------------------|:------------|:--------------------|:----------|----------------:|----------------:|----------------------:|:--------------------------|
| POS015        | Orchard Media Services Loan      | Media       | Second Lien Loan    | Watchlist |              30 |            24   |                    80 | No                        |
| POS012        | Lighthouse Restaurant Group Loan | Restaurants | Second Lien Loan    | Watchlist |              34 |            27.9 |                    82 | No                        |
| POS008        | Harbor Consumer Products Loan    | Consumer    | Senior Secured Loan | Watchlist |              39 |            35.5 |                    91 | Yes                       |

## Early Warning Monitoring Checks

No records returned.
