import pandas as pd
import re

xlsx_path = 'data/Spotify Global Chart 2024.xlsx'

# 读取所有 sheet（实际上只有一个）
sheets = pd.read_excel(xlsx_path, sheet_name=None)
all_data = []

for sheet_name, df in sheets.items():
    all_data.append(df)

full_df = pd.concat(all_data, ignore_index=True)

# 从 Source.Name 列提取日期（格式：regional-global-weekly-2024-01-04.csv）
def extract_date(source):
    match = re.search(r'(\d{4}-\d{2}-\d{2})', source)
    return match.group(1) if match else None

full_df['date'] = full_df['Source.Name'].apply(extract_date)

# 调整列顺序
cols_order = ['date', 'Source.Name', 'rank', 'uri', 'artist_names', 'track_name', 
              'source', 'peak_rank', 'previous_rank', 'weeks_on_chart', 'streams']
full_df = full_df[cols_order]

# 使用全部数据
full_df.to_csv('data/spotify.csv', index=False)
print(f"预处理完成，共 {len(full_df)} 条记录，保存至 data/spotify.csv")
print("样例数据：")
print(full_df.head())