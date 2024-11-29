import boto3
import awswrangler as wr
import pandas as pd
from awsglue.dynamicframe import DynamicFrame
from awsglue.context import GlueContext
from pyspark.context import SparkContext

# Initialize GlueContext
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Define raw data source (Glue Catalog Table)
raw_data = glueContext.create_dynamic_frame.from_catalog(
    database = "my_data_lake_db",
    table_name = "raw_data_table",
)

# Convert to Spark DataFrame for transformation
df = raw_data.toDF()

# Perform transformations (example: convert to Parquet)
transformed_df = df.select("column1", "column2")  # Simple transformation example
transformed_dynamic_frame = DynamicFrame.fromDF(transformed_df, glueContext, "transformed_data")

# Write the transformed data to S3 in Parquet format
wr.s3.to_parquet(
    df = transformed_df,
    path = "s3://my-data-lake-bucket/processed/",
    dataset = True,
    mode = "overwrite"
)

print("Transformation complete!")