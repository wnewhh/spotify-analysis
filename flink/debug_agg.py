from pyflink.table import EnvironmentSettings, TableEnvironment

settings = EnvironmentSettings.in_streaming_mode()
t_env = TableEnvironment.create(settings)

t_env.execute_sql("""
CREATE TABLE spotify_source (
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
    `streams` BIGINT,
    `proc_time` AS PROCTIME()
) WITH (
    'connector' = 'filesystem',
    'path' = 'file:///spotify-analysis/data/spotify.csv',
    'format' = 'csv',
    'csv.ignore-parse-errors' = 'true',
    'csv.first-row-as-header' = 'true'
)
""")

result = t_env.execute_sql("SELECT COUNT(*) FROM spotify_source")
result.print()