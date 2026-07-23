-- Active: 1784670873714@@127.0.0.1@3306
-- Which assets had the highest average daily trading volume?
SELECT 
    ticker,
    AVG(volume) AS avg_volume
FROM stock_prices
GROUP BY ticker
ORDER BY avg_volume DESC;


-- Which assets generated the highest total return?

SELECT
    ticker,
    cumulative_return AS total_return
FROM stock_prices AS sp
WHERE date = (
    SELECT MAX(date)
    FROM stock_prices
    WHERE ticker = sp.ticker
)
ORDER BY total_return DESC;


-- Which assets experienced the deepest drawdowns?

SELECT
    ticker,
    MIN(drawdown) AS max_drawdown,
    AVG(drawdown) AS avg_drawdown
FROM stock_prices
GROUP BY ticker
ORDER BY max_drawdown ASC;


-- Which assets experienced the greatest average intraday price movement?

SELECT
    ticker,
    AVG(high_low_spread_pct) AS avg_high_low_spread_pct
FROM stock_prices
GROUP BY ticker
ORDER BY avg_high_low_spread_pct DESC;

-- Which assets experienced the greatest average volatility over 30 days?

SELECT
    ticker,
    AVG(volatility_30d) AS avg_30d_volatility
FROM stock_prices
GROUP BY ticker
ORDER BY avg_30d_volatility DESC;