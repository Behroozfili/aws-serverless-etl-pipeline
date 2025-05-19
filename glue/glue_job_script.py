from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, trim, length, year, month, dayofweek, when
from pyspark.sql import Window
import pyspark.sql.functions as F

def main():
    # Initialize Spark session
    spark = SparkSession.builder.appName("Clean Online Retail Data").getOrCreate()

    # Define input and output file paths
    input_path = "ml-model/data/online_retail.csv"
    output_path = "ml-model/data/output/cleaned_data"

    # Read CSV data with header and infer schema
    df = spark.read.option("header", True).option("inferSchema", True).csv(input_path)

    # Filter out rows with null values in important columns
    df_cleaned = df.filter(
        (col("CustomerID").isNotNull()) &
        (col("InvoiceNo").isNotNull()) &
        (col("Quantity").isNotNull()) &
        (col("UnitPrice").isNotNull())
    )

    # Remove duplicate records based on key columns
    df_cleaned = df_cleaned.dropDuplicates(["InvoiceNo", "CustomerID", "InvoiceDate", "StockCode"])

    # Filter out rows with non-positive Quantity and UnitPrice
    df_cleaned = df_cleaned.filter(
        (col("Quantity") > 0) &
        (col("UnitPrice") > 0)
    )

    # Convert InvoiceDate to timestamp format
    df_cleaned = df_cleaned.withColumn("InvoiceDate", to_timestamp(col("InvoiceDate"), "MM/dd/yyyy HH:mm"))

    # Filter out rows with invalid InvoiceDate
    df_cleaned = df_cleaned.filter(col("InvoiceDate").isNotNull())

    # Trim whitespace from Description and filter out empty descriptions
    df_cleaned = df_cleaned.withColumn("Description", trim(col("Description")))
    df_cleaned = df_cleaned.filter((col("Description").isNotNull()) & (length(col("Description")) > 1))

    # Create a new column for total price (Quantity * UnitPrice)
    df_cleaned = df_cleaned.withColumn("TotalPrice", col("Quantity") * col("UnitPrice"))

    # Remove outliers in Quantity based on 1st and 99th percentiles
    quantiles_quantity = df_cleaned.approxQuantile("Quantity", [0.01, 0.99], 0.0)
    q1_qty, q99_qty = quantiles_quantity[0], quantiles_quantity[1]
    df_cleaned = df_cleaned.filter((col("Quantity") >= q1_qty) & (col("Quantity") <= q99_qty))

    # Remove outliers in TotalPrice based on 1st and 99th percentiles
    quantiles_price = df_cleaned.approxQuantile("TotalPrice", [0.01, 0.99], 0.0)
    q1_price, q99_price = quantiles_price[0], quantiles_price[1]
    df_cleaned = df_cleaned.filter((col("TotalPrice") >= q1_price) & (col("TotalPrice") <= q99_price))

    # Feature engineering: extract Year, Month, and Day of Week from InvoiceDate
    df_cleaned = df_cleaned.withColumn("Year", year(col("InvoiceDate"))) \
                           .withColumn("Month", month(col("InvoiceDate"))) \
                           .withColumn("DayOfWeek", dayofweek(col("InvoiceDate")))

    # Add a column to mark returned orders (InvoiceNo starts with 'C')
    df_cleaned = df_cleaned.withColumn(
        "IsReturn",
        when(col("InvoiceNo").startswith("C"), 1).otherwise(0)
    )

    # Rename InvoiceNo column to InvoiceNumber for clarity
    df_cleaned = df_cleaned.withColumnRenamed("InvoiceNo", "InvoiceNumber")

    # Write cleaned data to CSV with header, overwrite if exists
    df_cleaned.write.mode("overwrite").option("header", True).csv(output_path)

    # Stop the Spark session
    spark.stop()

if __name__ == "__main__":
    main()
