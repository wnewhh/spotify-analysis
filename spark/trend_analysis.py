from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum, desc

USER = "wne"
HDFS_PATH = f"hdfs://localhost:9000/user/{USER}/input/spotify.csv"

spark = SparkSession.builder.appName("TrendAnalysis").getOrCreate()

df = spark.read.option("header", True).option("inferSchema", True).csv(HDFS_PATH)

# 找出总播放量最高的歌曲
top_song_row = df.groupBy("track_name").agg(_sum("streams").alias("total")) \
                 .orderBy(desc("total")).first()
top_song = top_song_row[0] if top_song_row else None

if top_song:
    trend = df.filter(col("track_name") == top_song) \
              .select("date", "rank") \
              .orderBy("date")
    trend.toPandas().to_csv("output/result_trend_analysis.csv", index=False)
    print(f"Trend for '{top_song}' saved.")
else:
    print("No song found.")
spark.stop()