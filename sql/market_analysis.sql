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
