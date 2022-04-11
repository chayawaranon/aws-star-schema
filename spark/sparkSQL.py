import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job
from pyspark.sql.functions import explode, sequence, to_date, current_date, sha2

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext().getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

symbols = glueContext.create_dynamic_frame.from_catalog(
    database="star_schema_db",
    table_name="raw_data_symbols",
)

orders = glueContext.create_dynamic_frame.from_catalog(
    database="star_schema_db",
    table_name="raw_data_orders",
)

users = glueContext.create_dynamic_frame.from_catalog(
    database="star_schema_db",
    table_name="raw_data_users",
)

symbols.toDF().createOrReplaceTempView("view_symbols")
orders.toDF().createOrReplaceTempView("view_orders")
users.toDF().createOrReplaceTempView("view_users")

symbols.toDF().repartition(1).write.format('parquet').mode("overwrite").save('s3://raw-data-star-schema/symbols')
users.toDF().repartition(1).write.format('parquet').mode("overwrite").save('s3://raw-data-star-schema/users')
orders.toDF().repartition(1).write.format('parquet').mode("overwrite").save('s3://raw-data-star-schema/orders')

beginDate = '2014-01-01'
spark.sql(f"SELECT explode(sequence(to_date('{beginDate}'),  current_date, interval 1 day)) AS date").createOrReplaceTempView('view_dates')
dim_dates = spark.sql("""SELECT
                          date,
                          YEAR(date) AS year,
                          DATE_FORMAT(date, 'MMMM') AS month,
                          MONTH(date) AS month_of_year,
                          DATE_FORMAT(date, 'EEEE') AS day,
                          WEEKDAY(date) + 1 AS day_of_week,
                          CASE
                            WHEN weekday(date) < 5 THEN 'Y'
                            ELSE 'N'
                          END as is_week_day,
                          DAYOFMONTH(date) AS day_of_month,
                          DAYOFYEAR(date) AS day_of_year,
                          WEEKOFYEAR(date) AS week_of_year,
                          QUARTER(date) AS quarter_of_year
                        FROM
                          view_dates
                        ORDER BY
                          date""")

spark.sql("SELECT DISTINCT buy_or_sell, order_status FROM view_orders").createOrReplaceTempView("view_distinct_value")
jnk_dim_order = spark.sql(""  "SELECT
                                SHA2(CONCAT(buy_or_sell, order_status),256) AS jnk_order_id,
                                buy_or_sell,
                                order_status
                              FROM view_distinct_value""")

fact_orders = spark.sql("""SELECT
                              order_id,
                              order_date AS order_date_id,
                              user_id,
                              SHA2(CONCAT(buy_or_sell, order_status),256) AS jnk_order_id,
                              symbol_id,
                              price,
                              quantity
                            FROM view_orders""")

dim_dates.repartition(1).write.format('parquet').mode("overwrite").save('s3://tranformed-data-star-schema/dim_dates')
fact_orders.repartition(1).write.format('parquet').mode("overwrite").save('s3://tranformed-data-star-schema/fact_orders')
jnk_dim_order.repartition(1).write.format('parquet').mode("overwrite").save('s3://tranformed-data-star-schema/jnk_dim_orders')
symbols.toDF().repartition(1).write.format('parquet').mode("overwrite").save('s3://tranformed-data-star-schema/dim_symbols')
users.toDF().repartition(1).write.format('parquet').mode("overwrite").save('s3://tranformed-data-star-schema/dim_users')

job.commit()