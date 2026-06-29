from pyspark.sql import SparkSession
from pyspark.sql.functions import col, month, avg

USER = "wne"
HDFS_PATH = f"hdfs://localhost:9000/user/{USER}/input/spotify.csv"

spark = SparkSession.builder.appName("MonthlyTrend").getOrCreate()

df = spark.read.option("header", True).option("inferSchema", True).csv(HDFS_PATH)

# 直接使用 date 列（字符串格式 yyyy-MM-dd）
df_with_month = df.withColumn("month", month("date"))

monthly_avg = df_with_month.groupBy("month").agg(avg("streams").alias("avg_streams")) \
                           .orderBy("month")

monthly_avg.toPandas().to_csv("output/result_monthly_avg.csv", index=False)
print("Monthly trend saved.")
spark.stop()