-- ============================================================
-- Sales Performance & Revenue Intelligence
-- SQL Queries for Business Analysis
-- ============================================================
-- Compatible with: MySQL 8+ / PostgreSQL 13+ / SQLite 3.35+
-- ============================================================


-- ── SETUP ────────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS sales (
    row_id        INTEGER PRIMARY KEY,
    order_id      VARCHAR(30),
    order_date    DATE,
    ship_date     DATE,
    ship_mode     VARCHAR(30),
    customer_id   VARCHAR(20),
    customer_name VARCHAR(100),
    segment       VARCHAR(30),
    region        VARCHAR(20),
    state         VARCHAR(50),
    category      VARCHAR(30),
    sub_category  VARCHAR(30),
    product_name  VARCHAR(200),
    sales         DECIMAL(12,2),
    quantity      INT,
    discount      DECIMAL(5,2),
    profit        DECIMAL(12,2)
);

-- Load from CSV:
-- MySQL:      LOAD DATA INFILE 'sample_sales_data.csv' INTO TABLE sales FIELDS TERMINATED BY ',' IGNORE 1 ROWS;
-- PostgreSQL: COPY sales FROM 'sample_sales_data.csv' DELIMITER ',' CSV HEADER;
-- SQLite:     .mode csv  →  .import sample_sales_data.csv sales


-- ── 1. OVERALL KPIs ──────────────────────────────────────────────────────────

SELECT
    ROUND(SUM(sales), 2)                              AS total_revenue,
    ROUND(SUM(profit), 2)                             AS total_profit,
    COUNT(DISTINCT order_id)                          AS total_orders,
    ROUND(AVG(sales), 2)                              AS avg_order_value,
    ROUND(SUM(profit) / NULLIF(SUM(sales), 0) * 100, 1) AS profit_margin_pct
FROM sales;


-- ── 2. MONTHLY REVENUE TREND ─────────────────────────────────────────────────

SELECT
    YEAR(order_date)                   AS yr,      -- MySQL
    -- EXTRACT(YEAR FROM order_date)   AS yr,      -- PostgreSQL / SQLite
    MONTH(order_date)                  AS mo,
    ROUND(SUM(sales),  2)              AS revenue,
    ROUND(SUM(profit), 2)              AS profit,
    COUNT(DISTINCT order_id)           AS orders
FROM sales
GROUP BY yr, mo
ORDER BY yr, mo;


-- ── 3. YEAR-OVER-YEAR GROWTH ─────────────────────────────────────────────────

WITH yearly AS (
    SELECT
        YEAR(order_date) AS yr,
        SUM(sales)       AS revenue
    FROM sales
    GROUP BY yr
)
SELECT
    yr,
    ROUND(revenue, 2) AS revenue,
    ROUND(
        (revenue - LAG(revenue) OVER (ORDER BY yr))
        / NULLIF(LAG(revenue) OVER (ORDER BY yr), 0) * 100, 1
    ) AS yoy_growth_pct
FROM yearly
ORDER BY yr;


-- ── 4. REVENUE BY CATEGORY & SUB-CATEGORY ────────────────────────────────────

SELECT
    category,
    sub_category,
    ROUND(SUM(sales),  2)                                      AS revenue,
    ROUND(SUM(profit), 2)                                      AS profit,
    ROUND(SUM(profit) / NULLIF(SUM(sales),0) * 100, 1)        AS margin_pct,
    COUNT(DISTINCT order_id)                                    AS orders,
    RANK() OVER (PARTITION BY category ORDER BY SUM(sales) DESC) AS rank_in_category
FROM sales
GROUP BY category, sub_category
ORDER BY category, revenue DESC;


-- ── 5. REGIONAL PERFORMANCE ───────────────────────────────────────────────────

SELECT
    region,
    ROUND(SUM(sales),  2)                               AS revenue,
    ROUND(SUM(profit), 2)                               AS profit,
    ROUND(SUM(profit) / NULLIF(SUM(sales),0) * 100, 1) AS margin_pct,
    COUNT(DISTINCT order_id)                             AS total_orders,
    ROUND(AVG(sales), 2)                                AS avg_order_value,
    COUNT(DISTINCT customer_id)                          AS unique_customers
FROM sales
GROUP BY region
ORDER BY revenue DESC;


-- ── 6. TOP 10 STATES BY REVENUE ───────────────────────────────────────────────

SELECT
    state,
    region,
    ROUND(SUM(sales),  2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    COUNT(DISTINCT order_id) AS orders
FROM sales
GROUP BY state, region
ORDER BY revenue DESC
LIMIT 10;


-- ── 7. CUSTOMER SEGMENT ANALYSIS ─────────────────────────────────────────────

SELECT
    segment,
    ROUND(SUM(sales),  2)                                    AS revenue,
    ROUND(SUM(profit), 2)                                    AS profit,
    ROUND(SUM(profit) / NULLIF(SUM(sales), 0) * 100, 1)     AS margin_pct,
    COUNT(DISTINCT customer_id)                               AS customers,
    COUNT(DISTINCT order_id)                                  AS orders,
    ROUND(SUM(sales) / NULLIF(COUNT(DISTINCT customer_id),0), 2) AS revenue_per_customer
FROM sales
GROUP BY segment
ORDER BY revenue DESC;


-- ── 8. DISCOUNT IMPACT ON PROFIT ─────────────────────────────────────────────

SELECT
    discount,
    COUNT(*)              AS num_transactions,
    ROUND(AVG(sales),  2) AS avg_sales,
    ROUND(AVG(profit), 2) AS avg_profit,
    ROUND(SUM(profit) / NULLIF(SUM(sales),0) * 100, 1) AS margin_pct
FROM sales
GROUP BY discount
ORDER BY discount;


-- ── 9. SHIPPING MODE PERFORMANCE ─────────────────────────────────────────────

SELECT
    ship_mode,
    COUNT(*)                                 AS orders,
    ROUND(AVG(
        DATEDIFF(ship_date, order_date)      -- MySQL
        -- ship_date - order_date           -- PostgreSQL / SQLite
    ), 1)                                    AS avg_ship_days,
    ROUND(SUM(sales), 2)                     AS revenue,
    ROUND(AVG(profit), 2)                    AS avg_profit_per_order
FROM sales
GROUP BY ship_mode
ORDER BY avg_ship_days;


-- ── 10. RFM SEGMENTATION ─────────────────────────────────────────────────────

WITH rfm_raw AS (
    SELECT
        customer_id,
        customer_name,
        DATEDIFF('2025-01-01', MAX(order_date)) AS recency,   -- MySQL
        COUNT(DISTINCT order_id)                AS frequency,
        ROUND(SUM(sales), 2)                    AS monetary
    FROM sales
    GROUP BY customer_id, customer_name
),
rfm_scored AS (
    SELECT *,
        NTILE(5) OVER (ORDER BY recency   DESC) AS r_score,
        NTILE(5) OVER (ORDER BY frequency ASC)  AS f_score,
        NTILE(5) OVER (ORDER BY monetary  ASC)  AS m_score
    FROM rfm_raw
),
rfm_final AS (
    SELECT *,
        (r_score + f_score + m_score) AS rfm_total,
        CASE
            WHEN (r_score + f_score + m_score) >= 13 THEN 'Champions'
            WHEN (r_score + f_score + m_score) >= 10 THEN 'Loyal Customers'
            WHEN (r_score + f_score + m_score) >= 7  THEN 'Potential Loyalists'
            WHEN (r_score + f_score + m_score) >= 5  THEN 'At Risk'
            ELSE 'Lost'
        END AS rfm_segment
    FROM rfm_scored
)
SELECT
    rfm_segment,
    COUNT(*)                    AS customer_count,
    ROUND(AVG(recency), 0)      AS avg_recency_days,
    ROUND(AVG(frequency), 1)    AS avg_orders,
    ROUND(AVG(monetary), 2)     AS avg_revenue,
    ROUND(SUM(monetary), 2)     AS total_revenue
FROM rfm_final
GROUP BY rfm_segment
ORDER BY total_revenue DESC;


-- ── 11. PRODUCT-LEVEL PROFITABILITY ──────────────────────────────────────────

SELECT
    product_name,
    category,
    sub_category,
    COUNT(*)                                             AS times_ordered,
    ROUND(SUM(sales),  2)                                AS total_revenue,
    ROUND(SUM(profit), 2)                                AS total_profit,
    ROUND(SUM(profit) / NULLIF(SUM(sales),0) * 100, 1)  AS margin_pct
FROM sales
GROUP BY product_name, category, sub_category
ORDER BY total_profit DESC
LIMIT 20;


-- ── 12. LOSS-MAKING PRODUCTS (for action) ────────────────────────────────────

SELECT
    product_name,
    category,
    ROUND(SUM(sales),  2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(AVG(discount) * 100, 1) AS avg_discount_pct,
    COUNT(*) AS num_transactions
FROM sales
GROUP BY product_name, category
HAVING SUM(profit) < 0
ORDER BY profit ASC
LIMIT 15;
