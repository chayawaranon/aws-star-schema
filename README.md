# aws-star-schema
This project is aimed to implement ETL pipeline to create star schema using Amazon Web Services(AWS) <br />
> All the data is randomly generated and is not based on anything real. The Users data is created using the Python Faker library

## DATA PIPELINE ARCHITECTURE:
![aws-pipeline-arc](https://user-images.githubusercontent.com/48947748/162723454-29684c0f-5423-453d-9841-b40530f1829e.png) <br />
Data sources from the MySQL database on Amazon RDS are ingested to S3 to store raw data and transform data by Amazon Glue, then import transformed data to Amazon Redshift.

## GLUE WORKFLOW:
![glue-workflow](https://user-images.githubusercontent.com/48947748/162723526-d3c2ce1d-efe6-4e7d-8990-be345c49ef7d.png)
This Glue workflow is scheduled manually. Firstly, we have to update metadata from MySQL and Redshift in Glue and when the update succeeded, we store raw data to S3 then transform data to create a star schema and store it back to S3 and also ingest it to Redshift.

## DATA MODEL:
The ERD for Backend look like following image. <br />
Tables: `users` `orders` `symbols` <br />
![old_schema](https://user-images.githubusercontent.com/48947748/162782767-4961ce2f-ced2-4485-9f80-5d8f85f195f9.jpg) <br />

The ERD for star schema look like following image. <br />
Dimensional Tables : `dim_dates` `dim_symbols` `dim_users` `jnk_dim_orders` <br />
Fact Table : `fact_orders`<br />
![star-schema](https://user-images.githubusercontent.com/48947748/162780855-ee75be05-4ab4-4458-95d2-ea3ef9e4c8d4.jpg)

## TABLE STRUCTURE IN REDSHIFT:
![table-structure-redshift](https://user-images.githubusercontent.com/48947748/162724205-09ca5a26-37ac-4ce1-bbde-8fa7e3af8e21.png)

## SAMPLE DATA:
`dim_dates` table <br />
|date      |year|	month	   |month_of_year|day     |day_of_week|is_week_day|day_of_month|day_of_year|week_of_year|quarter_of_year|
|---------------|----|----------|-------------|--------|-----------|-----------|------------|-----------|------------|---------------|
|2019-07-02|2019|	July	   |7            |Tuesday	|2          |Y          |	2          |183        |27          |	3	            |
|2017-05-20|2017|	May	     |5            |Saturday|6          |N          |	20         |140        |20          |	2		          |
|2014-06-05|2014|	June	   |6            |Thursday|4          |Y          |	5          |156        |23          |	2		          |
|2021-11-18|2021|	November |11           |Thursday|4          |Y          |	18         |322        |46          |	4		          |
|2018-09-14|2018|	September|9            |Friday	|5          |Y          |	14         |257        |37          |	3		          |

`dim_symbols` table <br />
|symbol_id|	symbol|	date_added|	listed_at|
|---|---|---|---|
|18	|KG	|2009-01-15|	exchange1	|
|16	|JB	|2017-02-22|	exchange1 |	
|13	|EM	|2005-11-30|	exchange2	|
|6	|JG	|2005-10-14|	exchange1	|
|11	|LJ	|2006-05-21|	exchange2	|

`dim_users` table <br />
|user_id|	first_name|	last_name|	email|	city|	state|	date_joined|
|---|---|---|---|---|---|---|
|24|	Haley|	White|	znash@example.net|	North Joshuamouth|	Delaware|	2019-12-01  |
|93|	Patrick|	Ortiz|	amanda70@example.net|	South Stephanieburgh|	Alabama|	2019-07-14	|
|41|	Jesus|	Hancock|	sandovalaaron@example.org|	Williamview|	Michigan|	2019-01-26	|
|36|	Natalie|	Simpson|	martha73@example.net|	North Matthew	West| Virginia|	2019-12-16	|
|83|	Nichole|	Osborn|	harmonzachary@example.org|	South Deannaville	West| Virginia|	2019-08-08	|

`jnk_dim_orders` table <br />
|jnk_orders_id|	buy_or_sell|	order_status|
|---|---|---|
|d8ee0ecbafa4fa679bf668fe514534f034efce6a95fd0cd1ab2228fde71de523|	buy|	canceled	|
|4bc80e678b4529fe18470b67c258243336aedf73c1f67345eac790fcc782b2f4|	sell|	executed	|
|348a24a442ccfa6c58c69d0f816b28906a1581409df0bd8d412184f0d5c96781|	sell|	canceled	|
|a65c372f0e7fb1ba610afb7dff22fb7df2cb6710f1fd95cf643a1a1b332bafa3|	buy|	executed	|

`fact_orders` table <br />
|order_id|	order_date_id|	user_id	jnk_order_id|	symbol_id|	price|	quantity|
|---|---|---|---|---|---|
|41157|	2020-01-17|	37|	a65c372f0e7fb1ba610afb7dff22fb7df2cb6710f1fd95cf643a1a1b332bafa3	|12	|113|	15|	
|723722|	2020-09-06|	18|	d8ee0ecbafa4fa679bf668fe514534f034efce6a95fd0cd1ab2228fde71de523|	4	|167|	17|
|492734|	2020-07-11|	99|	d8ee0ecbafa4fa679bf668fe514534f034efce6a95fd0cd1ab2228fde71de523|	5	|177|	14|	
|531178|	2020-08-30|	7|	d8ee0ecbafa4fa679bf668fe514534f034efce6a95fd0cd1ab2228fde71de523|	5	|35	| 19|
|996506|	2019-09-22|	9|	a65c372f0e7fb1ba610afb7dff22fb7df2cb6710f1fd95cf643a1a1b332bafa3|	1	|147|	11|	
