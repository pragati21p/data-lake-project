# data-lake-project

### Project Overview:
The goal is to create a *Data Lake* that:

1. Stores raw and processed data in *AWS S3*.
2. Uses *AWS Glue* for ETL (data extraction, transformation, and loading).
3. Uses *Amazon Athena* to query data directly from S3 using SQL.

### Step-by-Step Implementation:
##### Step 1: Set Up AWS S3 Bucket for Raw and Processed Data
1. Create an S3 Bucket:
   - Open the S3 Console and create a new bucket (e.g., `my-data-lake-bucket`).
   - This bucket will store all raw data files, processed data, and metadata.
2. Organize S3 Bucket:
   - Create directories for raw and processed data:
       - /raw/: Stores raw data files (e.g., CSV, JSON).
       - /processed/: Stores transformed data files (e.g., Parquet, ORC).
       - /metadata/: Stores Glue metadata (optional).

Example structure:
```
my-data-lake-bucket/
  ├── raw/
  ├── processed/
  └── metadata/
```

##### Step 2: Set Up AWS Glue Data Catalog (Metadata)
The AWS Glue Data Catalog will hold the metadata for raw and processed datasets. This allows you to easily query data in S3 using Athena.

1. Create a Glue Database:
   - Go to the AWS Glue Console and create a new Glue database (e.g., my_data_lake_db).
2. Create a Glue Crawler for Raw Data:
   - In the AWS Glue Console, create a new Crawler.
   - Set the source as S3 bucket’s raw data folder (s3://my-data-lake-bucket/raw/).
   - The crawler will infer the schema of the raw data files.
   - Set the crawler to store the results in the my_data_lake_db database.
   - Schedule the crawler to run periodically if you want to automate schema discovery.
##### Step 3: Data Transformation with AWS Glue
1. Create a Glue ETL Job:
   - In the AWS Glue Console, go to ETL Jobs and create a new job.
   - Choose Python/Scala as the language for transformation (Python is commonly used).
   - Set the source as the Glue Catalog Table created by the crawler for raw data.
   - Set the destination as the processed folder in S3 bucket (s3://my-data-lake-bucket/processed/).
2. Write Glue ETL Script: Use the AWS Glue job script editor to create an ETL script that will:
   - Read raw data from S3.
   - Clean, transform, and format the data (e.g., convert CSV/JSON to Parquet).
   - Write the transformed data to the processed folder in S3.

   Example script ([here](https://github.com/pragati21p/data-lake-project/blob/main/transformation.py))

3. Run the Glue Job:
   - Once the script is ready, run the Glue job to execute the ETL process.
   - The processed data will now be available in the processed/ folder in S3.
##### Step 4: Query Data Using Amazon Athena
Now that raw and processed data is in S3 bucket, Amazon Athena can be used to query this data directly from S3 using SQL.

1. Set Up Athena:
   - Go to the Athena Console and choose the Data Catalog (my_data_lake_db).
   - In the query editor, create an Athena table pointing to the processed data stored in S3 (e.g., s3://my-data-lake-bucket/processed/).
2. Create Athena Tables for Processed Data:
   - You can either use the Glue Crawler to create tables automatically or manually define tables in Athena.
Example Athena query to create a table:
```
CREATE EXTERNAL TABLE IF NOT EXISTS processed_data_table (
  column1 STRING,
  column2 INT
)
PARTITIONED BY (date STRING)
STORED AS PARQUET
LOCATION 's3://my-data-lake-bucket/processed/';
```
3. Run Queries on Processed Data:

   - After creating the tables, you can start querying the data using SQL:
```
SELECT column1, column2
FROM processed_data_table
WHERE column2 > 100
LIMIT 10;
```
4. Query Raw Data (if needed):
   - You can also create Athena tables for the raw data if you need to query it directly.
   - Example query to query raw data:
```
CREATE EXTERNAL TABLE IF NOT EXISTS raw_data_table (
  column1 STRING,
  column2 STRING
)
STORED AS JSON
LOCATION 's3://my-data-lake-bucket/raw/';
```
##### Step 5: Automate Data Pipeline and Monitoring
1. Automate the Data Pipeline with AWS Lambda and EventBridge:
   - Set up AWS Lambda functions to automate the process (e.g., trigger Glue ETL jobs on new data arrival).
   - Use AWS EventBridge to trigger Glue jobs or crawlers when new data is uploaded to S3.
2. Set Up Monitoring and Logging:
   - Use Amazon CloudWatch to monitor the Glue jobs, Lambda functions, and Athena queries.
   - Set up CloudWatch Alarms for job failures or performance issues.

##### Step 6: Secure and Optimize the Data Lake
1. Data Encryption:
   - Ensure that data is encrypted at rest (using S3 encryption) and in transit (using SSL/TLS for Glue and Athena).
2. Access Control:
   - Use AWS IAM roles and policies to control access to the data lake, Glue jobs, and Athena queries.
   - Implement S3 Bucket Policies for access control.
3. Cost Optimization:
   - Use S3 storage classes (e.g., Glacier for archival data) to optimize costs.
   - Set up Glue job bookmarks to process only new data during incremental ETL runs.

### Final Architecture Overview:
- Data Storage: Data is stored in AWS S3, both raw and processed.
- Metadata Management: AWS Glue Data Catalog is used to manage metadata.
- ETL Processing: AWS Glue performs the data transformation tasks.
- Querying: Amazon Athena is used to run SQL queries directly on data stored in S3.
- Automation: AWS Lambda and EventBridge automate data pipeline tasks.

This architecture is highly scalable, flexible, and cost-effective. Once set up, it allows for efficient querying and transformation of large datasets with minimal infrastructure management.
