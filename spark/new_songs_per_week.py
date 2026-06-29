from pyspark.sql import SparkSession
from pyspark.sql.functions import col, weekofyear, year, count, first, row_number
from pyspark.sql.window import Window

USER = "wne"
HDFS_PATH = f"hdfs://localhost:9000/user/{USER}/input/spotify.csv"

spark = SparkSession.builder.appName("NewSongsPerWeek").getOrCreate()

df = spark.read.option("header", True).option("inferSchema", True).csv(HDFS_PATH)

# 对每首歌，找到它首次出现的周
window_song = Window.partitionBy("track_name").orderBy("date")
df_with_rn = df.withColumn("rn", row_number().over(window_song))
first_appear = df_with_rn.filter(col("rn") == 1)

# 提取周数和年份
first_appear = first_appear.withColumn("week", weekofyear("date")) \
                           .withColumn("year", year("date"))

# 按周统计新歌数
new_songs = first_appear.groupBy("year", "week").agg(count("track_name").alias("new_songs")) \
                        .orderBy("year", "week")

new_songs.toPandas().to_csv("output/new_songs_per_week.csv", index=False)
print("New songs per week saved.")
spark.stop()