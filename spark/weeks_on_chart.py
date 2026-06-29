from pyspark.sql import SparkSession
from pyspark.sql.functions import col, max as _max, desc

USER = "wne"
HDFS_PATH = f"hdfs://localhost:9000/user/{USER}/input/spotify.csv"

spark = SparkSession.builder.appName("WeeksOnChart").getOrCreate()

df = spark.read.option("header", True).option("inferSchema", True).csv(HDFS_PATH)

# 直接使用已有的 weeks_on_chart 列，取每首歌的最大在榜周数
weeks_count = df.groupBy("track_name").agg(_max("weeks_on_chart").alias("max_weeks_on_chart")) \
                .orderBy(desc("max_weeks_on_chart")).limit(20)

weeks_count.toPandas().to_csv("output/result_weeks_on_chart.csv", index=False)
print("Weeks on chart saved.")
spark.stop()