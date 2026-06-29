from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum, max as _max, corr

USER = "wne"
HDFS_PATH = f"hdfs://localhost:9000/user/{USER}/input/spotify.csv"

spark = SparkSession.builder.appName("CorrelationAnalysis").getOrCreate()

df = spark.read.option("header", True).option("inferSchema", True).csv(HDFS_PATH)

# 每首歌的总播放量和最大在榜周数
agg_df = df.groupBy("track_name").agg(
    _sum("streams").alias("total_streams"),
    _max("weeks_on_chart").alias("max_weeks")
)

# 计算相关系数
corr_value = agg_df.stat.corr("total_streams", "max_weeks")
print(f"Correlation between total streams and max weeks: {corr_value}")

# 保存相关系数到文件
with open("output/correlation_result.txt", "w") as f:
    f.write(f"Pearson correlation: {corr_value}\n")

# 保存聚合数据用于可视化（可选）
agg_df.toPandas().to_csv("output/song_weeks_streams.csv", index=False)

spark.stop()