CREATE TABLE IF NOT EXISTS dim_dates(
    date DATE,
    year INTEGER,
    month VARCHAR(10),
    month_of_year INTEGER,
    day VARCHAR(10),
    day_of_week INTEGER,
    is_week_day CHAR(1),
    day_of_month INTEGER,
    day_of_year INTEGER,
    week_of_year INTEGER,
    quarter_of_year INTEGER
);

CREATE TABLE IF NOT EXISTS dim_symbols(
    symbol_id INTEGER,
    symbol VARCHAR(155),
    date_added DATE,
    listed_at VARCHAR(155)
);

CREATE TABLE IF NOT EXISTS dim_users(
    user_id INTEGER,
    first_name VARCHAR(155),
    last_name VARCHAR(155),
    email VARCHAR(155),
    city VARCHAR(155),
    state VARCHAR(155),
    date_joined DATE
);

CREATE TABLE IF NOT EXISTS jnk_dim_order(
    jnk_order_id VARCHAR(300),
    buy_or_sell VARCHAR(155),
    order_status VARCHAR(155)
);

CREATE TABLE IF NOT EXISTS fact_orders(
    order_id INTEGER,
    order_date_id DATE,
    user_id INTEGER,
    jnk_order_id VARCHAR(300),
    symbol_id INTEGER,
    price INTEGER,
    quantity INTEGER
);




