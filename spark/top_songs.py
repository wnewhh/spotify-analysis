from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum, desc

USER = "wne"
HDFS_PATH = f"hdfs://localhost:9000/user/{USER}/input/spotify.csv"

spark = SparkSession.builder.appName("TopSongs").getOrCreate()

df = spark.read.option("header", True).option("inferSchema", True).csv(HDFS_PATH)

top_songs = df.groupBy("track_name").agg(_sum("streams").alias("total_streams")) \
              .orderBy(desc("total_streams")).limit(10)

top_songs.toPandas().to_csv("output/result_top10_songs.csv", index=False)
print("Top 10 songs saved.")
spark.stop()