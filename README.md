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
![old_schema](https://user-images.githubusercontent.com/48947748/162782767-4961ce2f-ced2-4485-9f80-5d8f85f195f9.jpg) <br />
![star-schema](https://user-images.githubusercontent.com/48947748/162780855-ee75be05-4ab4-4458-95d2-ea3ef9e4c8d4.jpg)

## SAMPLE DATA:
![table-structure-redshift](https://user-images.githubusercontent.com/48947748/162724205-09ca5a26-37ac-4ce1-bbde-8fa7e3af8e21.png)

|date      |year|	month	   |month_of_year|day     |day_of_week|is_week_day|day_of_month|day_of_year|week_of_year|quarter_of_year|
|----------|----|----------|-------------|--------|-----------|-----------|------------|-----------|------------|---------------|
|2019-07-02|2019|	July	   |7            |Tuesday	|2          |Y          |	2          |183        |27          |	3	            |
|2017-05-20|2017|	May	     |5            |Saturday|6          |N          |	20         |140        |20          |	2		          |
|2014-06-05|2014|	June	   |6            |Thursday|4          |Y          |	5          |156        |23          |	2		          |
|2021-11-18|2021|	November |11           |Thursday|4          |Y          |	18         |322        |46          |	4		          |
|2018-09-14|2018|	September|9            |Friday	|5          |Y          |	14         |257        |37          |	3		          |


![dim_dates](https://user-images.githubusercontent.com/48947748/162876481-76b0d830-adca-404e-9388-5ef625145c04.png)
![dim_symbols](https://user-images.githubusercontent.com/48947748/162876525-41fe1d12-1eee-433d-bf82-d69894f0a369.png)
![dim_users](https://user-images.githubusercontent.com/48947748/162876552-f3d01260-c974-4098-914c-bbfedb61500b.png)
![jnk_dim_orders](https://user-images.githubusercontent.com/48947748/162876580-b12295dd-f7d1-4a77-ba31-de049c414db3.png)
![fact_orders](https://user-images.githubusercontent.com/48947748/162876642-44054599-5079-4d39-b36b-80a6c3fd238a.png)



