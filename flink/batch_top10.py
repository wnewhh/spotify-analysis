from pyflink.table import EnvironmentSettings, TableEnvironment
import pandas as pd
# 使用相对路径
LOCAL_PATH = "file:///spotify-analysis/data/spotify.csv"

settings = EnvironmentSettings.in_batch_mode()
t_env = TableEnvironment.create(settings)

t_env.execute_sql(f"""
CREATE TABLE spotify (
    `date` STRING,
    `Source.Name` STRING,
    `rank` INT,
    `uri` STRING,
    `artist_names` STRING,
    `track_name` STRING,
    `source` STRING,
    `peak_rank` INT,
    `previous_rank` INT,
    `weeks_on_chart` INT,
    `streams` BIGINT
) WITH (
    'connector' = 'filesystem',
    'path' = '{LOCAL_PATH}',
    'format' = 'csv',
    'csv.ignore-parse-errors' = 'true',
    'csv.first-row-as-header' = 'true'
)
""")

result = t_env.execute_sql("""
SELECT `track_name`, SUM(`streams`) AS total_streams
FROM spotify
GROUP BY `track_name`
ORDER BY total_streams DESC
LIMIT 10
""")

# 收集结果（list of Row）
rows = result.collect()
# 转换为 Pandas DataFrame
df = pd.DataFrame(rows, columns=['track_name', 'total_streams'])
df.to_csv("output/result_top10_flink.csv", index=False)
print("✅ Flink batch Top10 saved.")
