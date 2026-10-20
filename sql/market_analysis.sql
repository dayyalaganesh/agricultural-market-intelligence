-- Agricultural Market Intelligence Platform
-- SQL Analytics Queries

-- 1. Total records in the dataset
SELECT COUNT(*) AS total_records
FROM mandi_prices;

-- 2. Top 10 commodities by average modal price
SELECT
    commodity,
    ROUND(AVG(modal_price), 2) AS avg_modal_price,
    COUNT(*) AS record_count
FROM mandi_prices
GROUP BY commodity
ORDER BY avg_modal_price DESC
LIMIT 10;

-- 3. Top 10 markets by average modal price
-- Only markets with at least 10 records
SELECT
    state,
    market,
    COUNT(*) AS record_count,
    ROUND(AVG(modal_price), 2) AS avg_modal_price
FROM mandi_prices
GROUP BY state, market
HAVING COUNT(*) >= 10
ORDER BY avg_modal_price DESC
LIMIT 10;

-- 4. Data quality: check price consistency
SELECT
    COUNT(*) FILTER (
        WHERE min_price > max_price
    ) AS min_greater_than_max,
    COUNT(*) FILTER (
        WHERE modal_price < min_price
           OR modal_price > max_price
    ) AS modal_outside_range
FROM mandi_prices;
-- 5. Commodity price spread
-- Describes variation across records, not change over time
SELECT
    commodity,
    COUNT(*) AS record_count,
    ROUND(MIN(modal_price), 2) AS lowest_modal_price,
    ROUND(MAX(modal_price), 2) AS highest_modal_price,
    ROUND(MAX(modal_price) - MIN(modal_price), 2) AS modal_price_spread
FROM mandi_prices
GROUP BY commodity
HAVING COUNT(*) >= 2
ORDER BY modal_price_spread DESC
LIMIT 10;


-- 6. State-level market coverage
SELECT
    state,
    COUNT(DISTINCT market) AS market_count,
    COUNT(DISTINCT commodity) AS commodity_count,
    COUNT(*) AS record_count
FROM mandi_prices
GROUP BY state
ORDER BY record_count DESC;


-- 7. Dataset profile
SELECT
    COUNT(*) AS total_records,
    COUNT(DISTINCT state) AS distinct_states,
    COUNT(DISTINCT market) AS distinct_markets,
    COUNT(DISTINCT commodity) AS distinct_commodities,
    COUNT(DISTINCT arrival_date) AS distinct_arrival_dates
FROM mandi_prices;
