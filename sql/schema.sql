DROP TABLE IF EXISTS investors;
DROP TABLE IF EXISTS nav_positions;
DROP TABLE IF EXISTS facility_assumptions;
DROP TABLE IF EXISTS covenant_tests;
DROP TABLE IF EXISTS monthly_monitoring;

CREATE TABLE investors (
    investor_id TEXT PRIMARY KEY,
    investor_name TEXT NOT NULL,
    investor_type TEXT NOT NULL,
    total_commitment REAL NOT NULL,
    funded_pct REAL NOT NULL,
    internal_rating TEXT,
    eligible_in_borrowing_base TEXT NOT NULL,
    advance_rate REAL NOT NULL,
    funded_commitment REAL NOT NULL,
    unfunded_commitment REAL NOT NULL,
    borrowing_base_contribution REAL NOT NULL,
    commitment_pct REAL NOT NULL
);

CREATE TABLE nav_positions (
    position_id TEXT PRIMARY KEY,
    portfolio_company TEXT NOT NULL,
    industry TEXT NOT NULL,
    asset_type TEXT NOT NULL,
    cost_basis REAL NOT NULL,
    fair_value_marks REAL NOT NULL,
    status TEXT NOT NULL,
    eligible_nav_collateral TEXT NOT NULL,
    nav_advance_rate REAL NOT NULL,
    fair_value REAL NOT NULL,
    nav_collateral_value REAL NOT NULL,
    portfolio_weight REAL NOT NULL
);

CREATE TABLE facility_assumptions (
    metric TEXT PRIMARY KEY,
    value TEXT
);

CREATE TABLE covenant_tests (
    covenant TEXT PRIMARY KEY,
    current_value REAL NOT NULL,
    test TEXT NOT NULL,
    threshold REAL NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE monthly_monitoring (
    reporting_date TEXT PRIMARY KEY,
    eligible_nav REAL NOT NULL,
    facility_size REAL NOT NULL,
    facility_outstanding REAL NOT NULL,
    facility_utilization_pct REAL NOT NULL,
    subscription_borrowing_base REAL NOT NULL,
    max_nav_debt_capacity REAL NOT NULL,
    total_debt_capacity REAL NOT NULL,
    excess_availability REAL NOT NULL,
    ltv REAL NOT NULL,
    max_ltv_covenant REAL NOT NULL,
    nav_floor REAL NOT NULL,
    covenant_status TEXT NOT NULL,
    watchlist_item TEXT
);
